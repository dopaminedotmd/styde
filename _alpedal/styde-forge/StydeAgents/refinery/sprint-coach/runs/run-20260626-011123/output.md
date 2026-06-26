Team status — three sprints examined.
Sprint 23
  planned: 42 points
  delivered: 38 points
  velocity: 0.90
  blockers: 2 (auth service migration, flaky e2e suite)
Sprint 24
  planned: 40 points
  delivered: 40 points
  velocity: 1.00
  blockers: 1 (staging db restore lock)
Sprint 25
  planned: 44 points
  delivered: 32 points
  velocity: 0.73
  blockers: 4 (3 infra, 1 dependency freeze)
Trend: velocity declining. Sprint 25 drop signals systemic issue, not one-off.
Blocker cluster in Sprint 25: all infra-related. Three AWS IAM policy changes, one npm audit forced upgrade that broke the build pipeline.
Kaizen recommendation:
  1.  Add infra-change freeze window — last 48 hours of sprint, no IAM or pipeline changes unless emergency.
  2.  Extract dependency-upgrade ticket type with its own SLA. Treat it as planned work, not a spike.
  3.  Retro action: why did three IAM changes hit same sprint? Team over-delegated infra access without change-review gate.
Standup prompt for next session:
  "What infra or dependency change is coming this week that we have not yet scheduled?"
Daily flow check: WIP = 6, swimlane count = 4. One team member carries 2 items alone. Suggest pair-swarming that column, not splitting into subtasks.
Kanban tweak: add a "blocked (waiting)" lane between Dev and Review. Current board hides waiting time because cards stay in Dev while author waits for external sign-off. Invisible delay is the most dangerous kind.
Retro invite: scheduled. Focus question — "what made Sprint 23 better than Sprint 25, and can we bottle that?"