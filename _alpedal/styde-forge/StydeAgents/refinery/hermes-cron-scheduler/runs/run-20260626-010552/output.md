Blueprint hermes-cron-scheduler version 2.0 output.
Based on the actual hermes-agent cronjob tool API documented at https://hermes-agent.nousresearch.com/docs/user-guide/features/cron.
Three design decisions driven by the Styde Forge repo context:
1. All jobs use action="create" with named parameters matching the real cronjob tool
2. No invented --no-agent flag — the real API uses no_agent=True on the tool
3. No fake pre-run script concept — the real API uses script= parameter with wakeAgent gates
4. Workdir paths use absolute paths: /e/Stryde/_alpedal/styde-forge (MSYS-compatible for Windows)
=== JOB 1: Blueprint Health Check ===
cronjob(
    action="create",
    name="blueprint-health-check",
    schedule="0 6 * * *",
    workdir="/e/Stryde/_alpedal/styde-forge",
    prompt="Read all blueprints under blueprints/ and check config.yaml for version, domain, min_pass_score. Report any blueprint missing config.yaml or with min_pass_score below 70. Save findings to ~/.hermes/data/health/blueprint-health.md.",
    deliver="local",
)
=== JOB 2: Forge Core Pulse ===
cronjob(
    action="create",
    name="forge-core-pulse",
    schedule="every 4h",
    workdir="/e/Stryde/_alpedal/styde-forge",
    prompt="Check the forge core process. Run uv run python -c 'from forge import ForgeCore; f=ForgeCore(); print(f.status())' or equivalent. Report agent count, iteration stats, memory usage. Deliver a one-line health summary.",
    deliver="local",
)
=== JOB 3: Agent Eval Digest (chained from Job 1) ===
cronjob(
    action="create",
    name="agent-eval-digest",
    schedule="30 6 * * *",
    context_from="<job1_id>",
    workdir="/e/Stryde/_alpedal/styde-forge",
    prompt="Scan checkpoints/ for the latest eval.yaml files. List each blueprint, its composite score, and whether production_ready is true. Identify the bottom 3 blueprints by score. Append recommendations to ~/.hermes/data/health/eval-digest.md.",
    deliver="local",
)
=== JOB 4: Memory Pressure Watchdog (no-agent mode) ===
cronjob(
    action="create",
    name="memory-pressure-watchdog",
    schedule="every 5m",
    no_agent=True,
    script="memory-watchdog.sh",
    deliver="local",
)
Script that this job references, written to ~/.hermes/scripts/memory-watchdog.sh:
#!/bin/bash
# ~/.hermes/scripts/memory-watchdog.sh
MEM_PCT=$(free | awk '/^Mem:/ {printf "%.0f", $3/$2 * 100}')
if [ "$MEM_PCT" -gt 85 ]; then
  echo "WARNING: RAM at ${MEM_PCT}%"
  echo "{\"wakeAgent\": false}"
else
  # silent tick — no delivery
  echo "{\"wakeAgent\": false}"
fi
=== JOB 5: Stale Blueprint Gate ===
cronjob(
    action="create",
    name="stale-blueprint-gate",
    schedule="0 8 * * 1",
    script="stale-check.sh",
    workdir="/e/Stryde/_alpedal/styde-forge",
    prompt="Find all blueprints where config.yaml shows last_reviewed older than 30 days. List them along with their version and score. Suggest which ones to retrain.",
    deliver="local",
)
Pre-check script that avoids waking the agent if nothing is stale:
#!/bin/bash
# ~/.hermes/scripts/stale-check.sh
CUTOFF=$(date -d '30 days ago' +%s)
STALE=0
for f in /e/Stryde/_alpedal/styde-forge/blueprints/*/config.yaml; do
  REVIEWED=$(grep 'last_reviewed:' "$f" 2>/dev/null | cut -d"'" -f2)
  [ -z "$REVIEWED" ] && continue
  REVIEW_TS=$(date -d "$REVIEWED" +%s 2>/dev/null)
  [ "$REVIEW_TS" -le "$CUTOFF" ] && STALE=$((STALE + 1))
done
if [ "$STALE" -eq 0 ]; then
  echo '{"wakeAgent": false}'
else
  echo "Found $STALE stale blueprints"
  echo '{"wakeAgent": true}'
fi
=== JOB 6: Daily Session Cleanup ===
cronjob(
    action="create",
    name="daily-session-cleanup",
    schedule="0 3 * * *",
    workdir="/e/Stryde/_alpedal/styde-forge",
    prompt="Run hermes sessions prune --keep 50 to trim session history. Check disk usage of state.db. Report size before and after. If state.db exceeds 100MB, flag for review.",
    deliver="local",
)
=== JOB 7: Skill Sync (weekly, chained from Job 3) ===
cronjob(
    action="create",
    name="weekly-skill-sync",
    schedule="0 9 * * 1",
    context_from="<job3_id>",
    workdir="/e/Stryde/_alpedal/styde-forge",
    prompt="Check blueprints/ for any newly added blueprints since last week. For each new blueprint, verify it has a properly configured eval block (min_pass_score, judge_model). If any are missing, write a repair plan to ~/.hermes/data/sync/new-blueprints.md.",
    deliver="local",
)
=== SCHEDULE OVERVIEW ===
timezone: Etc/UTC (all schedules)
scheduler tick: 60s (gateway default)
time      job                       repeat
06:00     blueprint-health-check    daily
06:30     agent-eval-digest         daily (chained from job 1)
03:00     daily-session-cleanup     daily
every 4h  forge-core-pulse          6x/day
every 5m  memory-pressure-watchdog  288x/day (no-agent, script-only)
08:00 Mon stale-blueprint-gate     weekly (script-gated)
09:00 Mon weekly-skill-sync        weekly (chained from job 3)
=== ERROR RECOVERY CHAIN ===
provider fallback: jobs inherit configured fallback_providers from config.yaml. If primary model (deepseek-v4-flash) is rate-limited, fallback to next provider in pool.
credential rotation: credential pool handles API key exhaustion on high-frequency jobs (memory-pressure-watchdog is no-agent, so unaffected).
workdir serialization: all workdir jobs (1,2,3,5,6,7) run sequentially on scheduler tick to prevent cwd corruption. Workdir-less jobs (4) run in parallel pool.
job isolation: failed job does not block other jobs on same tick. Scheduler processes all due jobs independently.
alert on failure: cron sends delivery with error context when a job fails. [SILENT] suppression only applies to successful runs.