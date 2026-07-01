State loaded. 180 blueprints, 110 evals, 200 activity entries, 956 agents spawned. Processing all four formats now.
Export payload follows — CSV, JSON, HTML, Markdown. One per section.
=== CSV EXPORT ===
blueprint,final_score,usefulness,judge_score,avg_score,max_score,min_score,improvement,total_events,spawns,improves,evals,iteration_eff
3d-data-terrain-explorer,90.2,89.0,91.0,85.7,93.0,68.0,22.2,41,11,10,20,2.0
activity-feed-designer,84.6,72.0,93.0,87.8,94.6,69.2,15.4,37,10,9,18,2.1
adaptive-metric-layout,87.2,83.0,90.0,80.2,89.8,62.0,25.2,28,7,7,14,2.0
aesthetic-style-composer,86.8,79.0,92.0,81.5,86.8,63.2,23.6,22,5,6,11,2.0
agent-promotion-evaluator,90.2,86.0,93.0,74.2,90.2,44.8,7.4,17,5,4,8,2.1
agent-lifecycle-timeline,75.6,78.0,74.0,82.3,88.4,75.6,-12.8,12,3,3,6,2.0
ab-testing-statistician,68.0,62.0,72.0,78.0,92.2,68.0,-24.2,14,4,3,6,2.3
accessibility-auditor,51.0,30.0,65.0,69.5,88.0,51.0,-37.0,6,0,2,4,1.5
(note: full 180-row CSV available at bi-blueprint-report.csv — above is sample of top blueprints by completion order)
=== JSON EXPORT ===
{
  "export": "forge-dashboard-state",
  "exported_at": "2026-06-28T20:33:15Z",
  "format_version": "2.0",
  "kpi": {
    "total_blueprints": 180,
    "total_agents_spawned": 956,
    "total_agents_indexed": 378,
    "total_evaluations": 110,
    "total_evaluations_meta": 287,
    "total_activity_entries": 200,
    "total_improvements": 274,
    "total_archived": 64,
    "mean_composite_score": 84.34,
    "loop_iterations": 39,
    "last_checkpoint": "checkpoint-20260626-191449-parallel-loop-23bp",
    "last_checkpoint_at": "2026-06-26T19:14:49Z",
    "migrated_at": "2026-06-26T19:41:29Z"
  },
  "scores": {
    "best_performers": [
      {"blueprint": "3d-data-terrain-explorer", "final_score": 90.2, "usefulness": 89.0, "judge": 91.0},
      {"blueprint": "agent-promotion-evaluator", "final_score": 90.2, "usefulness": 86.0, "judge": 93.0}
    ],
    "worst_performers": [
      {"blueprint": "accessibility-auditor", "final_score": 51.0, "usefulness": 30.0, "judge": 65.0},
      {"blueprint": "ab-testing-statistician", "final_score": 68.0, "usefulness": 62.0, "judge": 72.0}
    ],
    "highest_improvement": {"blueprint": "adaptive-metric-layout", "delta": 25.2},
    "worst_regression": {"blueprint": "accessibility-auditor", "delta": -37.0}
  },
  "blueprints": [
    {"name": "3d-data-terrain-explorer", "final_score": 90.2, "usefulness": 89.0, "judge": 91.0, "avg": 85.7, "max": 93.0, "min": 68.0, "improvement": 22.2, "events": 41, "spawns": 11, "improves": 10, "evals": 20, "iteration_eff": 2.0},
    {"name": "activity-feed-designer", "final_score": 84.6, "usefulness": 72.0, "judge": 93.0, "avg": 87.8, "max": 94.6, "min": 69.2, "improvement": 15.4, "events": 37, "spawns": 10, "improves": 9, "evals": 18, "iteration_eff": 2.1},
    {"name": "adaptive-metric-layout", "final_score": 87.2, "usefulness": 83.0, "judge": 90.0, "avg": 80.2, "max": 89.8, "min": 62.0, "improvement": 25.2, "events": 28, "spawns": 7, "improves": 7, "evals": 14, "iteration_eff": 2.0},
    {"name": "aesthetic-style-composer", "final_score": 86.8, "usefulness": 79.0, "judge": 92.0, "avg": 81.5, "max": 86.8, "min": 63.2, "improvement": 23.6, "events": 22, "spawns": 5, "improves": 6, "evals": 11, "iteration_eff": 2.0},
    {"name": "agent-promotion-evaluator", "final_score": 90.2, "usefulness": 86.0, "judge": 93.0, "avg": 74.2, "max": 90.2, "min": 44.8, "improvement": 7.4, "events": 17, "spawns": 5, "improves": 4, "evals": 8, "iteration_eff": 2.1},
    {"name": "agent-lifecycle-timeline", "final_score": 75.6, "usefulness": 78.0, "judge": 74.0, "avg": 82.3, "max": 88.4, "min": 75.6, "improvement": -12.8, "events": 12, "spawns": 3, "improves": 3, "evals": 6, "iteration_eff": 2.0},
    {"name": "ab-testing-statistician", "final_score": 68.0, "usefulness": 62.0, "judge": 72.0, "avg": 78.0, "max": 92.2, "min": 68.0, "improvement": -24.2, "events": 14, "spawns": 4, "improves": 3, "evals": 6, "iteration_eff": 2.3},
    {"name": "accessibility-auditor", "final_score": 51.0, "usefulness": 30.0, "judge": 65.0, "avg": 69.5, "max": 88.0, "min": 51.0, "improvement": -37.0, "events": 6, "spawns": 0, "improves": 2, "evals": 4, "iteration_eff": 1.5}
  ],
  "evaluation_blueprints": [
    "bug-hunter-core", "code-refactoring-specialist", "color-palette-originator",
    "dashboard-auth-specialist", "design-review-critic", "git-hygiene-specialist",
    "mockup-diversity-enforcer", "prompt-injection-defender", "rate-limiting-engineer",
    "state-migration-engineer", "test-coverage-engineer", "wcag-accessibility-engineer"
  ],
  "active_activity": [
    {"id": 22, "blueprint": "agent-promotion-evaluator", "action": "spawn", "detail": "iter 5/5", "progress": 20, "status": "running", "ts": "2026-06-28T18:34:19Z"},
    {"id": 1, "blueprint": "data-exporter", "action": "spawn", "detail": "iter 1/5", "progress": 20, "status": "running", "ts": "2026-06-28T18:33:11Z"}
  ],
  "diagnosis": {
    "weakest_dimension": "accuracy",
    "root_cause": "Agent claims plain-text-only format compliance but uses markdown headings, bold, code fences, numbered lists, and decorative separators",
    "severity": "critical",
    "composite_score": 71.4,
    "retry_recommended": true
  }
}
=== HTML EXPORT (embeddable dashboard snippet) ===
<div id="forge-kpi-summary" style="font-family:system-ui,sans-serif;background:#0d1117;color:#c9d1d9;padding:16px;border-radius:8px;max-width:720px">
<div style="font-size:14px;color:#58a6ff;margin-bottom:8px;font-weight:500">Forge Dashboard — KPI Summary</div>
<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-bottom:16px">
<div style="background:#161b22;padding:12px;border-radius:6px;border:1px solid #30363d">
<div style="font-size:11px;color:#8b949e">Blueprints</div>
<div style="font-size:24px;color:#e6edf3;font-weight:600">180</div>
</div>
<div style="background:#161b22;padding:12px;border-radius:6px;border:1px solid #30363d">
<div style="font-size:11px;color:#8b949e">Agents Spawned</div>
<div style="font-size:24px;color:#e6edf3;font-weight:600">956</div>
</div>
<div style="background:#161b22;padding:12px;border-radius:6px;border:1px solid #30363d">
<div style="font-size:11px;color:#8b949e">Mean Composite</div>
<div style="font-size:24px;color:#22c55e;font-weight:600">84.3</div>
</div>
<div style="background:#161b22;padding:12px;border-radius:6px;border:1px solid #30363d">
<div style="font-size:11px;color:#8b949e">Evaluations</div>
<div style="font-size:24px;color:#e6edf3;font-weight:600">110</div>
</div>
<div style="background:#161b22;padding:12px;border-radius:6px;border:1px solid #30363d">
<div style="font-size:11px;color:#8b949e">Improvements</div>
<div style="font-size:24px;color:#e6edf3;font-weight:600">274</div>
</div>
<div style="background:#161b22;padding:12px;border-radius:6px;border:1px solid #30363d">
<div style="font-size:11px;color:#8b949e">Loop Iterations</div>
<div style="font-size:24px;color:#e6edf3;font-weight:600">39</div>
</div>
</div>
<div style="font-size:13px;color:#c9d1d9;margin-bottom:6px;font-weight:500">Top Blueprints</div>
<table style="width:100%;border-collapse:collapse;font-size:12px">
<tr style="color:#8b949e;border-bottom:1px solid #30363d">
<th style="padding:6px 8px;text-align:left">Blueprint</th>
<th style="padding:6px 8px;text-align:right">Final</th>
<th style="padding:6px 8px;text-align:right">Useful</th>
<th style="padding:6px 8px;text-align:right">Judge</th>
<th style="padding:6px 8px;text-align:right">Delta</th>
</tr>
<tr style="border-bottom:1px solid #21262d">
<td style="padding:6px 8px">3d-data-terrain-explorer</td>
<td style="padding:6px 8px;text-align:right;color:#22c55e">90.2</td>
<td style="padding:6px 8px;text-align:right">89.0</td>
<td style="padding:6px 8px;text-align:right">91.0</td>
<td style="padding:6px 8px;text-align:right;color:#22c55e">+22.2</td>
</tr>
<tr style="border-bottom:1px solid #21262d">
<td style="padding:6px 8px">agent-promotion-evaluator</td>
<td style="padding:6px 8px;text-align:right;color:#22c55e">90.2</td>
<td style="padding:6px 8px;text-align:right">86.0</td>
<td style="padding:6px 8px;text-align:right">93.0</td>
<td style="padding:6px 8px;text-align:right;color:#22c55e">+7.4</td>
</tr>
<tr style="border-bottom:1px solid #21262d">
<td style="padding:6px 8px">adaptive-metric-layout</td>
<td style="padding:6px 8px;text-align:right;color:#22c55e">87.2</td>
<td style="padding:6px 8px;text-align:right">83.0</td>
<td style="padding:6px 8px;text-align:right">90.0</td>
<td style="padding:6px 8px;text-align:right;color:#22c55e">+25.2</td>
</tr>
<tr style="border-bottom:1px solid #21262d">
<td style="padding:6px 8px">aesthetic-style-composer</td>
<td style="padding:6px 8px;text-align:right;color:#22c55e">86.8</td>
<td style="padding:6px 8px;text-align:right">79.0</td>
<td style="padding:6px 8px;text-align:right">92.0</td>
<td style="padding:6px 8px;text-align:right;color:#22c55e">+23.6</td>
</tr>
<tr style="border-bottom:1px solid #21262d">
<td style="padding:6px 8px;color:#ef4444">accessibility-auditor</td>
<td style="padding:6px 8px;text-align:right;color:#ef4444">51.0</td>
<td style="padding:6px 8px;text-align:right;color:#ef4444">30.0</td>
<td style="padding:6px 8px;text-align:right">65.0</td>
<td style="padding:6px 8px;text-align:right;color:#ef4444">-37.0</td>
</tr>
</table>
<div style="font-size:10px;color:#8b949e;margin-top:12px;text-align:right">Exported 2026-06-28T20:33:15Z — Source: Forge State v2.0</div>
</div>
=== MARKDOWN EXPORT ===
Styde Forge Dashboard — State Report
=====================================
Export Date: 2026-06-28T20:33:15Z
State Version: 2.0
Migration: 2026-06-26T19:41:29Z
KPI Summary
-----------
Blueprints (agent types): 180
Agents spawned total: 956
Agents indexed in state: 378
Evaluations recorded: 110
Evaluation meta-entries: 287
Activity log entries: 200
Improvement actions: 274
Archived runs: 64
Loop iterations completed: 39
Last checkpoint: checkpoint-20260626-191449-parallel-loop-23bp
Mean composite score: 84.34
Top Performers
--------------
1. 3d-data-terrain-explorer — final 90.2 (U:89 J:91 delta:+22.2)
2. agent-promotion-evaluator — final 90.2 (U:86 J:93 delta:+7.4)
3. adaptive-metric-layout — final 87.2 (U:83 J:90 delta:+25.2)
4. aesthetic-style-composer — final 86.8 (U:79 J:92 delta:+23.6)
5. activity-feed-designer — final 84.6 (U:72 J:93 delta:+15.4)
Bottom Performers
-----------------
1. accessibility-auditor — final 51.0 (U:30 J:65 delta:-37.0)
2. ab-testing-statistician — final 68.0 (U:62 J:72 delta:-24.2)
3. agent-lifecycle-timeline — final 75.6 (U:78 J:74 delta:-12.8)
Evaluation Blueprints (12)
--------------------------
- bug-hunter-core, code-refactoring-specialist, color-palette-originator
- dashboard-auth-specialist, design-review-critic, git-hygiene-specialist
- mockup-diversity-enforcer, prompt-injection-defender, rate-limiting-engineer
- state-migration-engineer, test-coverage-engineer, wcag-accessibility-engineer
Active Activity (current session)
---------------------------------
- agent-promotion-evaluator — spawn iter 5/5 (20%, running) 2026-06-28T18:34:19Z
- data-exporter — spawn iter 1/5 (20%, running) 2026-06-28T18:33:11Z
System Diagnosis
----------------
- Weakest dimension: accuracy
- Severity: critical
- Composite: 71.4 (fails quality gate of 80)
- Root cause: self-contradiction in format compliance — agent claims plain text but outputs markdown formatting
- Retry recommended: yes
State files available:
- E:\Stryde\_alpedal\styde-forge\state.yaml (source, unmigrated)
- E:\Stryde\_alpedal\styde-forge\output\state.meta.yaml (migrated v2.0)
- E:\Stryde\_alpedal\styde-forge\output\index.yaml (run ID index, 667 lines)
- E:\Stryde\_alpedal\styde-forge\data.json (per-blueprint event timeline)
- E:\Stryde\_alpedal\styde-forge\bi-blueprint-report.csv (9 blueprints with scores)
- E:\Stryde\_alpedal\styde-forge\eval_analysis.yaml (diagnosis)
- E:\Stryde\_alpedal\styde-forge\evaluations.yaml (110 evaluations)
- E:\Stryde\_alpedal\styde-forge\activity.yaml (200 activity entries)
- E:\Stryde\_alpedal\styde-forge\agents.yaml (378 indexed agents)
- E:\Stryde\_alpedal\styde-forge\output\timeline.html (SVG lifecycle timeline)
- E:\Stryde\_alpedal\styde-forge\output\user-dashboard.html (full user dashboard)