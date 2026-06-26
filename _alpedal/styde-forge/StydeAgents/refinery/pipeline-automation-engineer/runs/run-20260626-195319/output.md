Pipeline Automation Engine — deployment blueprint and implementation guide
name: pipeline-automation-engineer
domain: devops
version: 1
status: draft
target: styde-forge refinery-to-production pipeline
core components:
1. pipeline orchestrator
   file: forge/core/pipeline_orchestrator.py
   class: PipelineOrchestrator
   manages: spawn phase, eval phase, improve phase, promote phase
   state machine: idle -> spawning -> evaluating -> improving -> promoting -> idle
   persistence: state.yaml with phase, scores, timestamps, error log
2. spawn phase
   triggers: cron schedule, manual trigger, eval-score-below-threshold
   action: delegates to forge.spawn_agent() with blueprint + config
   output: agent_id, agent_dir, timestamp
   recorded: state.yaml agent:agent_id, phase:spawning
3. eval phase
   runs: forge.evaluate_agent(agent_id) via delegate_task sub (max 20 parallel)
   scoring: 0-100 scale per tier (general, fas_05, tier1, tier2, tier3)
   trigger limit: eval runs when previous eval exists AND score < 85
   early exit: if 2 consecutive scores < 40, flag as failing and notify
4. promote gate
   condition: score >= 85 for 3 consecutive eval runs
   gate: manual approval required (state.yaml promote:promoting_gate:true)
   promotion action: copy agent from refinery/ to production/, tag as promoted
   rollback: previous production agent archived as promoted/rollback-{timestamp}
   rejection: keep in refinery, log reason, notify
5. scheduler
   engine: threading.Timer with configurable intervals from pipeline_config.yaml
   default schedule:
     code review: every 4 hours
     security scan: every 12 hours
     health check: every 1 hour
     batch audit: every 24 hours
   config override: pipeline_config.yaml schedule section
6. notification hooks
   channels: file log, webhook POST, command center dashboard
   critical events: state corruption, agent crash, 3+ consecutive eval failures
   webhook url: configurable in pipeline_config.yaml hooks.webhook_url
   payload: {event, agent_id, score, phase, timestamp, details}
7. safety system
   lock file: pipeline.lock prevents concurrent pipeline runs
   max retries: 3 per phase before escalation
   verify promotion: re-eval promoted agent within 10 minutes of promotion
   manual override: promote:false in config halts all auto-promotion
   rollback: restore production agent from archives/promoted/rollback-*
8. logging system
   per-stage logs: logs/pipeline/{spawn,eval,improve,promote}/{timestamp}.log
   aggregated: logs/pipeline/pipeline.log with timestamps and phases
   failure notifications: log + webhook + command center update
   log retention: 30 days, auto-cleanup in health check
config file: pipeline_config.yaml
schedule:
  code_review_interval_hours: 4
  security_scan_interval_hours: 12
  health_check_interval_hours: 1
  batch_audit_interval_hours: 24
hooks:
  webhook_url: http://localhost:8766/api/pipeline-event
  notify_on_failure: true
  notify_on_promotion: true
promotion:
  min_score: 85
  consecutive_passes_required: 3
  auto_promote: false
  verify_promotion: true
  rollback_enabled: true
safety:
  max_retries_per_phase: 3
  lock_timeout_seconds: 300
  manual_override: false
  verify_interval_minutes: 10
state.yaml structure:
agent:
  current_agent_id: null
  phase: idle
  scores: []
  consecutive_passes: 0
  last_eval_score: 0
  previous_eval_scores: []
  status: inactive
promote:
  promoting_gate: false
  promoted_at: null
  current_production: null
  archived: []
  rollback_available: false
schedule:
  code_review_next: null
  security_scan_next: null
  health_check_next: null
  batch_audit_next: null
errors:
  - timestamp: null
    phase: null
    message: null
    severity: null
implementation priority:
1. pipeline_orchestrator.py — state machine and phase orchestration
2. pipeline_config.yaml — configuration loader with defaults
3. notification.py — webhook POST and file log dispatcher
4. scheduler.py — cron-like threading timer
5. safety.py — lock file, retry logic, verification
6. integrate with existing forge spawn/eval/promote functions
7. command-center dashboard events for pipeline state
8. deploy as managed background process under forge supervisor
Ready to implement on your signal. One file at a time, terminal execution after each.