ZERO JOBS CURRENTLY SCHEDULED. FULL CRON SYSTEM DESIGN FOLLOWS.
---
STYDE FORGE CRON SCHEDULE v1
Domain: hermes-opt
Target: E:\Stryde\_alpedal\styde-forge
TZ: Europe/Stockholm (UTC+1/+2 DST)
---
JOB 1: forge-daily-health
Schedule: 0 7 * * * (07:00 CET daily)
Mode: agent + script
Script: forge-daily-status.sh (pre-run data collector)
Skill: none
Deliver: origin (console output)
Purpose: Collect forge state, agent counts, disk usage, last eval scores. Inject into agent prompt. Agent writes a concise daily status report.
Pre-run script (forge-daily-status.sh):
```
#!/bin/bash
FORGE=E:\Stryde\_alpedal\styde-forge
echo "=== FORGE DAILY HEALTH ==="
date -u +"UTC: %Y-%m-%d %H:%M:%S"
echo "TZ: Europe/Stockholm"
if [ -f $FORGE/state.yaml ]; then
  echo "--- STATE ---"
  grep -E "total_agents_spawned|total_evaluations|loop_iterations|last_checkpoint" $FORGE/state.yaml
fi
echo "--- AGENTS IN REFINERY ---"
ls $FORGE/StydeAgents/refinery/ 2>/dev/null | wc -l
echo "--- AGENTS IN PRODUCTION ---"
ls $FORGE/StydeAgents/production/ 2>/dev/null | wc -l
echo "--- STORAGE USAGE ---"
du -sh $FORGE/StydeAgents/ 2>/dev/null
du -sh $FORGE/logs/ 2>/dev/null
echo "--- RESOURCES ---"
free -h 2>/dev/null | head -2
df -h $FORGE 2>/dev/null | tail -1
```
Agent prompt on each run: "Read the injected pre-run status data. Produce a 3-line daily forge health summary: total agents spawned, storage used, any failures since last report. Deliver to console."
Workdir: E:\Stryde\_alpedal\styde-forge
---
JOB 2: blueprint-audit-weekly
Schedule: 0 9 * * 1 (09:00 CET every Monday)
Mode: agent
Skill: none
Script: none
Deliver: origin
Purpose: Validate all 149 blueprints. Report broken ones.
Agent prompt: "List all blueprints under E:\Stryde\_alpedal\styde-forge\blueprints\. For each, verify: persona.md exists and >= 50 chars, BLUEPRINT.md exists and has ## Purpose section, config.yaml exists and is valid YAML with agent: section. Report count_valid / count_total. List any broken blueprints with their specific errors."
Workdir: E:\Stryde\_alpedal\styde-forge
---
JOB 3: system-resource-monitor
Schedule: every 30m
Mode: no-agent (pure script)
Script: forge-resource-check.sh
Deliver: origin (only when output is non-empty = threshold exceeded)
Purpose: Watchdog. Silent when healthy. Alerts when resource thresholds breached.
Pre-run script (forge-resource-check.sh):
```
#!/bin/bash
FORGE=E:\Stryde\_alpedal\styde-forge
ALERT=""
# Check disk usage
DISK_PCT=$(df $FORGE 2>/dev/null | tail -1 | awk '{print $5}' | tr -d '%')
if [ "$DISK_PCT" -gt 85 ]; then
  ALERT="$ALERT DISK=${DISK_PCT}% (threshold 85%)"
fi
# Check state file integrity
if [ ! -f $FORGE/state.yaml ]; then
  ALERT="$ALERT STATE_MISSING"
fi
# Check circuit breaker health
BREAKER_COUNT=$(ls $FORGE/99_INDEXES/circuit_breakers_*.json 2>/dev/null | wc -l)
if [ "$BREAKER_COUNT" -gt 5 ]; then
  ALERT="$ALERT OPEN_CIRCUITS=${BREAKER_COUNT}"
fi
# Check stale lock files
STALE_LOCKS=$(find $FORGE -name "*.lock" -mmin +60 2>/dev/null | wc -l)
if [ "$STALE_LOCKS" -gt 0 ]; then
  ALERT="$ALERT STALE_LOCKS=${STALE_LOCKS}"
fi
if [ -n "$ALERT" ]; then
  echo "FORGE ALERT: $(date -u +%Y-%m-%dT%H:%M:%SZ)$ALERT"
fi
```
No agent = script output delivered directly. Empty output = silent = healthy.
Workdir: E:\Stryde\_alpedal\styde-forge
---
JOB 4: forge-loop-tick
Schedule: every 2h
Mode: agent
Skill: none
Script: none
Deliver: origin
Purpose: Advance forge pipeline. Pick best candidate blueprint from refinery, spawn next agent, evaluate, improve. Core training loop.
Agent prompt: "Styde Forge loop tick. 1) Read state.yaml from E:\Stryde\_alpedal\styde-forge\. 2) Count queued vs completed agents per blueprint. 3) If any blueprint has completed agents without eval, run: python Core/forge.py eval <blueprint> <run_id>. 4) If eval passed (composite >= 80), run: python Core/forge.py improve <blueprint> <run_id>. 5) If gaps exist (blueprint spawned < 2 agents), spawn another: python Core/forge.py spawn <blueprint>. 6) Report what you did: queued, spawned, evaluated, improved counts."
Workdir: E:\Stryde\_albedal\styde-forge
---
JOB 5: stale-run-cleanup
Schedule: 0 3 * * * (03:00 CET daily)
Mode: no-agent
Script: forge-cleanup.sh
Deliver: origin (only when runs are cleaned)
Purpose: Remove stale artifacts. Runs in dead hours.
Pre-run script (forge-cleanup.sh):
```
#!/bin/bash
FORGE=E:\Stryde\_alpedal\styde-forge
CLEANED=0
# Remove runs older than 7 days in refinery that have eval.yaml and passed production
find $FORGE/StydeAgents/refinery -name "eval.yaml" -mtime +7 2>/dev/null | while read EVAL; do
  RUN_DIR=$(dirname "$EVAL")
  COMPOSITE=$(grep -A5 "composite:" "$EVAL" 2>/dev/null | grep "composite_score" | awk '{print $2}' | tr -d ' ')
  if [ -n "$COMPOSITE" ] && [ "$COMPOSITE" -ge 85 ]; then
    rm -rf "$RUN_DIR/spawn_context.yaml" "$RUN_DIR/self_eval_prompt.txt" "$RUN_DIR/judge_eval_prompt.txt" "$RUN_DIR/self_eval_response.txt" "$RUN_DIR/judge_eval_response.txt" 2>/dev/null
    CLEANED=$((CLEANED + 1))
  fi
done
# Remove orphaned lock files
find $FORGE -name "*.lock" -mmin +120 -delete 2>/dev/null
# Truncate logs older than 30 days
find $FORGE/logs -name "*.log" -mtime +30 -delete 2>/dev/null
echo "CLEANUP: removed ${CLEANED} stale eval artifacts, $(find $FORGE -name '*.lock' 2>/dev/null | wc -l) locks remaining"
```
---
JOB DEPENDENCY CHAIN: forge-loop-tick -> run forge-daily-health at 07:00 AFTER loop-tick
Constraint: weekly-audit only runs Monday 09:00, skipped if forge-loop-tick is unhealthy.
Recovery: if forge-loop-tick fails 3 consecutive times, pause it and escalate via system-resource-monitor alert.
---
ERROR RECOVERY STRATEGY:
1. Every job retries 2x on failure (hermes cron auto-retry via config retry_on_failure: true)
2. After 3 consecutive failures -> job auto-paused. system-resource-monitor detects pause and alerts.
3. Locks: forge-loop-tick acquires lock. If lock exists > 60 min, cleanup job removes it.
4. Circuit breaker pattern: if loop-tick fails 5x within 1 hour, skip loop-tick until next scheduled run.
---
IMPLEMENTATION (one-liners):
hermes cron create --name forge-daily-health --deliver origin --repeat 0 --workdir "E:\Stryde\_alpedal\styde-forge" --script forge-daily-status.sh "Read the injected pre-run status data. Produce a 3-line daily forge health summary" "0 7 * * *"
hermes cron create --name blueprint-audit-weekly --deliver origin --repeat 0 --workdir "E:\Stryde\_alpedal\styde-forge" "List all blueprints...verify each..." "0 9 * * 1"
hermes cron create --name system-resource-monitor --deliver origin --repeat 0 --workdir "E:\Stryde\_alpedal\styde-forge" --script forge-resource-check.sh --no-agent "every 30m"
hermes cron create --name forge-loop-tick --deliver origin --repeat 0 --workdir "E:\Stryde\_alpedal\styde-forge" "Advance forge pipeline..." "every 2h"
hermes cron create --name stale-run-cleanup --deliver origin --repeat 0 --workdir "E:\Stryde\_alpedal\styde-forge" --script forge-cleanup.sh --no-agent "0 3 * * *"
---
5 JOBS TOTAL. 2 agent-mode (daily-health, loop-tick, weekly-audit). 2 no-agent watchdog/cleanup (system-monitor, stale-cleanup). 1 mixed-mode weekly audit. All workdir pointed at forge root. Scripts under ~/.hermes/scripts/.