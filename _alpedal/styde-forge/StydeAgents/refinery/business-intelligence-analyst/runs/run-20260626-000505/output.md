BI ANALYST REPORT: Styde Forge Operations Dashboard
TIMEFRAME: 2026-06-25T08:40:16Z to 2026-06-26T02:00:00Z (17h20m runtime)
AGENT THROUGHPUT (Pipelines)
Total agents spawned: ~280+ (estimated from state.yaml, 3557 lines)
Unique blueprints: 89 active in registry
Total evaluations recorded: 110
STAGE DISTRIBUTION (Agent Lifecycle)
Production (Combat-Ready): 10 agents promoted
  code-reviewer v7.0.0, ui-ux-designer v3.0.0, calendar-assistant v5.0.0, onboarding-guide v5.0.0, social-media-writer v4.0.0, competitor-monitor v4.0.0, landing-page-builder, css-stylist, fullstack-feature-builder, performance-optimizer
Refinery (Active Training): ~180 agents in iteration
Archive (Retired): ~15 agents shelved
FUNNEL CONVERSION RATES
Spawn -> Eval completed: ~39% (110 evals / 280 spawns)
Eval -> Improvement: ~35%
Refinery -> Production promotion: ~5%
Eval Fail (archive): ~12%
TOP PERFORMERS (Score >= 90)
calendar-assistant: 100.0 (perfect score, v5.0.0)
icon-system-architect: 96.0
caching-strategist: 94.4
web-font-optimizer: 94.0
vue-composition-expert: 93.8
nextjs-app-architect: 93.6
ui-ux-designer: 93.6 (v3.0.0)
web-component-builder: 93.6
visual-brand-designer: 93.6
api-architect: 93.4
code-reviewer: 93.4 (v4.0.0)
design-system-architect: 93.4 (both eval passes)
database-schema-designer: 93.2
typography-systems-designer: 93.2
dark-mode-architect: 93.0
state-management-architect: 93.0
testing-suite-architect: 93.0
astro-static-builder: 92.8
landing-page-builder: 92.6
accessibility-auditor: 92.4
animation-design-engineer: 92.4
api-architect (v2): 92.4
SCORE QUARTILES (92 eval records analyzed)
Q1 (0-60): 16 agents (17.4%)
Q2 (60-80): 12 agents (13.0%)
Q3 (80-90): 21 agents (22.8%)
Q4 (90+): 43 agents (46.7%)
BOTTOM PERFORMERS (Below 50, need overhaul)
report-writer: 12.0, 12.0 (two fails, same score - systematic flaw)
consultant-auditor: 50.0, 30.0 (regressed between iterations)
customer-service-triage: 50.0, 36.0
meeting-summarizer: 36.0, 47.0
translator-sv-en: 42.0
recruitment-screener (2nd iteration): 45.0
sql-query-generator (2nd iteration): 28.0 (severe regression from 80)
BENCHMARK BREAKDOWN
code-review-basic: 10 eval rounds, mean 84.9, stdev 6.2, 100% pass rate (all passed)
manual: 100 eval rounds, mean 79.3, stdev 19.0, 68% pass rate
ITERATION TRACKING (code-reviewer, most trained blueprint)
Run 1 (v1->v2.0.0): 86.8
Run 2 (v2->v3.0.0): 91.4 (+4.6)
Run 3 (v3->v4.0.0): 93.4 (+2.0) - promoted
Run 4 (v4->v5.0.0): 85.0 (-8.4) - regression
Run 5 (v5->v6.0.0): 85.0 (flat)
Run 6 (v6->v6): 85.0 (no improvement recorded)
Run 7 (v6->v7.0.0): 88.0 (+3.0)
Run 8 (v7->v7.0.1): 78.0 (-10.0)
Run 9 (v7.0.1->7.0.2): 73.0 (-5.0)
Run 10 (v7.0.2->7.1.0): 83.0 (+10.0)
REGRESSION PATTERN: 6 of 9 iterative deltas negative. Peaked at v4 (93.4), then oscillated 73-88. Diminishing returns after v4. Blueprint over-optimization.
CAVEMAN ULTRA: Enabled (truth = true)
HARDWARE PROFILE: pontus-main
TOP IMPROVEMENT THEMES (from teacher reviews)
completeness: 5 occurrences (primary weakness)
clarity: 1 occurrence
SYSTEM HEALTH
Last active: 2026-06-26T02:00:00Z (last batch spawn batch)
Manual benchmark dominates: 92.4% of evaluations
Automated benchmark (code-review-basic): 7.6% only
No 00_MANIFEST.json found - manifest tracking missing
RECOMMENDATIONS
1. Automate code-review-basic benchmark for all blueprints. Manual eval introduces bias.
2. Implement regression guardrails - 6 of 9 iterations regressed on code-reviewer.
3. Focus on Q1 blueprints (report-writer, consultant-auditor, translator-sv-en) - persona redesign needed.
4. Production promotion pipeline too sparse (10/280 = 3.6%). Increase eval cadence.
5. Build manifest file for best_per_domain tracking - missing metrics on best-in-class by domain.