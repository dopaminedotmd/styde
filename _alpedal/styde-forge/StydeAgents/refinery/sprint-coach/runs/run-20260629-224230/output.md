Raw sprint data missing. No input provided — no sprint rows, no delivered columns, no velocity values.
Unblocking actions available:
Action 1: Paste raw sprint data in this format:
sprint: 1
committed: 20
delivered: 18
scope_change: 0
blockers: "Auth dependency"
---
sprint: 2
committed: 22
delivered: 20
scope_change: 2
blockers: "none"
Paste raw block, one sprint per --- separator. Include at minimum committed and delivered per sprint.
Action 2: Provide file path to CSV or markdown table. Acceptable formats:
  E:/Stryde/_alpedal/styde-forge/sprints/sprint_data.csv
  C:/Users/jonat/sprints/sprint_review.md
Action 3: Use sample dataset with dummy values. Template output below will use placeholder data showing what a real analysis looks like.
Action 4: Describe the team context verbally — team size, current sprint number, known impediments — and I will suggest a starting format for data collection.
Template output (with placeholder values filled as YAML):
velocity_cross_check:
  sprints_analyzed: 3
  warnings: []
average_velocity:
  sp_delivered_sum: 58
  sprint_count: 3
  average: 19.33
  formula: "58 / 3"
blockers_and_next_steps:
  - blocker: "Sprint 1 — 2 SP unfinished, root cause: unplanned production incident"
    owner: "Scrum Master"
    next_action: "Add incident-response buffer (3 SP) to next sprint plan"
    timeframe: "before next sprint planning"
  - blocker: "Sprint 2 — scope change of 2 SP mid-sprint degrades predictability"
    owner: "Product Owner"
    next_action: "Freeze scope after sprint day 3 or formalize change-control process"
    timeframe: "next retrospective"
data_gap: true
data_gap_note: "All values above are placeholders. Provide real data for accurate analysis."
Paste raw sprint data or file path and I will run the full blueprint-mandated cross-check, recompute averages from source rows, enumerate assigned blockers with owners, actions, and timeframes.