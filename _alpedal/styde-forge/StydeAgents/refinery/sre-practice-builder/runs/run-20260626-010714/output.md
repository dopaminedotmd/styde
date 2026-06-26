SRE Assessment: Styde Forge System
=====================================
USER JOURNEYS IDENTIFIED
------------------------
1. Blueprint authoring -> agent spawn -> task execution -> result delivery
2. Model invocation (deepseek-v4-flash via hermes_bridge)
3. Agent delegation (delegate_task -> child agents)
4. Teacher evaluation (completeness + usefulness scoring)
5. Dashboard rendering (Tauri v2 frontend)
SLI CANDIDATES PER JOURNEY
---------------------------
journey: blueprint-to-result
  sli: spawn_success_rate
  measure: successful spawns / total spawn attempts
  target: 0.99
journey: blueprint-to-result
  sli: end_to_end_latency_p95
  measure: time from spawn to result delivery
  target: < 30s
journey: model-invocation
  sli: model_availability
  measure: successful model responses / total requests
  target: 0.98
journey: model-invocation
  sli: model_latency_p99
  measure: time from request to first token
  target: < 5s
journey: delegation
  sli: child_completion_rate
  measure: children that produce output / total spawned
  target: 0.95
journey: teacher-evaluation
  sli: evaluation_turnaround
  measure: time from submission to score
  target: < 10s
SLO DEFINITIONS
----------------
class: availability
  slo_name: forge_available
  target: 99.5% over 30 days
  measurement_window: 30d sliding
  burn_rate_alerts:
    - warning: burn > 2x for 1h
    - critical: burn > 10x for 10m
class: latency
  slo_name: spawn_latency
  target: 95% of spawns complete under 30s
  measurement_window: 7d sliding
  burn_rate_alerts:
    - warning: burn > 3x for 30m
    - critical: burn > 12x for 5m
class: quality
  slo_name: agent_completeness
  target: < 5% of spawned agents produce errors not results
  measurement_window: 14d sliding
  burn_rate_alerts:
    - warning: burn > 1.5x for 2h
    - critical: burn > 6x for 15m
ERROR BUDGETS
--------------
service: forge
  slo: forge_available (99.5%)
  budget_per_month: 216 minutes downtime
  current_budget_remaining: unknown (no monitoring found)
  action: install uptime tracker before next deploy
service: agent-completeness
  slo: agent_completeness (95% success)
  budget_per_1000_spawns: 50 allowed failures
  last_known: teacher scores completeness as weakest dimension
  action: this is the highest-priority reliability gap
TOIL IDENTIFIED
----------------
id: T001
  task: manually patching model name across 4+ files when changing default model
  frequency: each model switch
  automation: single config var in forge.py loaded by hermes_bridge.py
  effort_saved: 4 file edits per change
id: T002
  task: verifying spawned agent output for completeness before teacher evaluation
  frequency: every spawn
  automation: add pre-check step in agent_runner before forwarding to teacher
  effort_saved: eliminates human review of every failed agent
id: T003
  task: restarting after stuck child agents hit max_concurrent_children=5
  frequency: when children stall without timeout
  automation: add child timeout (default 120s) with automatic reap
  effort_saved: manual kill + restart cycles
RELIABILITY ROADMAP
--------------------
phase: 0 (immediate)
  items:
    - add child agent timeout (120s default) in agent_runner
    - instrument spawn_success_rate and model_availability as counters
    - create error budget dashboard tile
phase: 1 (this sprint)
  items:
    - implement completeness pre-check before teacher submission
    - add burn rate alerts for spawn_latency
    - centralize model config to single source of truth
    - document SLOs in repo root as RELIABILITY.md
phase: 2 (next sprint)
  items:
    - automate toil T001 (single config var)
    - automate toil T002 (pre-check step)
    - automate toil T003 (child timeout with reap)
    - set up error budget tracking with alerting
phase: 3 (backlog)
  items:
    - blameless postmortem process for SLO violations
    - load test at 2x and 5x current agent spawn rate
    - capacity planning for model API quota usage
    - chaos engineering: inject latency to validate burn rate alerts
CULTURE RECOMMENDATIONS
------------------------
blameless: true
  practice: after every SLO burn alert, write a 5-why analysis
  output: stored in docs/postmortems/YYYY-MM-DD-event.md
  rule: never attribute to individual fault
  review: share at weekly reliability sync
error_budget_policy:
  - if budget > 80% remaining: full deploy velocity
  - if budget 50-80%: code freeze on non-reliability features
  - if budget < 50%: all hands on reliability improvements
  - if budget exhausted: mandatory freeze + postmortem
reward: credit team members who find toil and automate it