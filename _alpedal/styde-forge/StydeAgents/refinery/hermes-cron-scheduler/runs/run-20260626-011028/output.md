cron_schedule:
  forge_auto:
    - name: validate_blueprints
      schedule: "0 */2 * * *"
      tz: Europe/Stockholm
      command: python -m forge.cron.validate
      retry: 2
      notify_on_fail: true
      depends_on: []
    - name: process_pending_agents
      schedule: "0 */3 * * *"
      tz: Europe/Stockholm
      command: python -m forge.cron.process --batch=25
      retry: 2
      notify_on_fail: true
      depends_on:
        - validate_blueprints
    - name: promote_graduated
      schedule: "0 6,18 * * *"
      tz: Europe/Stockholm
      command: python -m forge.cron.promote
      retry: 3
      notify_on_fail: true
      depends_on:
        - process_pending_agents
    - name: health_check
      schedule: "*/15 * * * *"
      tz: Europe/Stockholm
      command: python -m forge.cron.health
      retry: 1
      notify_on_fail: true
      depends_on: []
  maintenance:
    - name: compact_memory
      schedule: "0 3 * * 0"
      tz: Europe/Stockholm
      command: python -m forge.cron.compact
      retry: 0
      notify_on_fail: true
      depends_on: []
    - name: backup_agents
      schedule: "0 4 * * 0"
      tz: Europe/Stockholm
      command: python -m forge.cron.backup --target=/mnt/backup/agents
      retry: 3
      notify_on_fail: true
      depends_on:
        - compact_memory
  error_recovery:
    max_attempts: 3
    backoff: exponential
    backoff_base_seconds: 60
    handler: python -m forge.cron.recover
    alert_command: hermes chat -p admin -q "CRON FAIL: {job_name} failed after {attempts} attempts"
task_chains:
  - id: daily_pipeline
    steps: [validate_blueprints, process_pending_agents, promote_graduated]
    max_concurrent: 1
    stop_on_fail: true
  - id: weekly_maintenance
    steps: [compact_memory, backup_agents]
    max_concurrent: 1
    stop_on_fail: false
pre_run_scripts:
  validate_blueprints:
    - command: python -m forge.cron.collect_metrics --type=blueprint_count
      timeout: 30
      inject: [blueprint_count, stale_count]
  process_pending_agents:
    - command: python -m forge.cron.count_queue
      timeout: 10
      inject: [queue_depth]
  health_check:
    - command: python -m forge.cron.system_load
      timeout: 15
      inject: [cpu_pct, mem_gb, disk_pct]
    - command: python -m forge.cron.gpu_status
      timeout: 10
      inject: [gpu_util, vram_free]