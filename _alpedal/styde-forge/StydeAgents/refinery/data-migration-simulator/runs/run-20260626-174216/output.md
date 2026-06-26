NO ACTIVE MIGRATION TASK DETECTED
No production data path specified.
No migration script provided.
No target schema defined.
What I need from you to execute:
phase: SIMULATE
state: AWAITING_INPUT
inputs_required:
  - production_data_path: /path/to/real/data
  - migration_script: /path/to/migration.py or inline SQL
  - target_schema: postgresql://localhost:5432/sandbox
  - validation_rules:
      - row_count_check: true/false
      - null_ratio_check: true/false
      - referential_integrity: true/false
      - custom_checks: [list of SQL assertions]
Execution model:
STEP 1 - sandbox_ready
  Guard checks:   production path exists? T
  Action:         rsync --archive --link-dest=../prod data/ sandbox/
  Result:         isolated filesystem snapshot taken, copy verified by checksum
STEP 2 - dry_run
  Guard checks:   sandbox != production (inode comparison) T
  Action:         apply migration_script against sandbox. rollback plan recorded.
  Result:         migration applied to copy. pre/post state stored in /tmp/delta/
STEP 3 - validation
  Action:         run validation_rules against pre/post snapshots
  Result:         structured diff report with warnings if any ratio exceeds threshold
STEP 4 - report
  Output:         YAML report, stdout only
STEP 5 - rollback_test
  Guard checks:   sandbox was modified T
  Action:         apply reverse migration from rollback plan
  Result:         sandbox restored to pre-migration state, verified by checksum
STEP 6 - production_exec
  Guard:          --force flag present
  Guard:          user confirmation (type "YES I WANT TO MODIFY PRODUCTION DATA")
  Action:         apply migration_script to production_path
  Result:         production data migrated
Give me the data and I execute. No speculative output.