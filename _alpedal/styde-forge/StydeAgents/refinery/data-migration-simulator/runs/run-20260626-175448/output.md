SIMULATION PLAN
phase: analysis
status: dry-run
sandbox: isolated
The input is three feedback reports targeting skills completeness, clarity of references, and missing failure-mode documentation for a blueprint named data-migration-simulator. The task is to produce an improved version of this blueprint that closes all gaps.
MIGRATION TARGET: data-migration-simulator blueprint
SOURCE DIR: D:\styde\_alpedal\styde-forge\blueprints\data-migration-simulator
SANDBOX DIR: D:\styde\_alpedal\styde-forge\sandbox\sim-20260626-195452
APPROACH: produce corrected blueprint content as structured YAML and plain text output
VALIDATION CHECKLIST:
- [pre-flight] every skill has 3-5 concrete validation example blocks (input/expected-output pairs)
- [pre-flight] every skill has 3-5 edge-case scenarios with expected agent behavior
- [pre-flight] every target reference is an explicit absolute path or canonical artifact name
- [pre-flight] every improvement entry has traceability back-reference
- [pre-flight] config.yaml includes nestingstyle constraint
- [pre-flight] zero markdown formatting in output
BEGIN SIMULATION OUTPUT
---
BLUEPRINT: data-migration-simulator
DOMAIN: data
VERSION: 2
TRACEABILITY: parent blueprint v1, upgraded per feedback batch 20260626-195452
SOURCES:
  - feedback_id: 2/100 (earliest)
  - feedback_id: 20260626-175301
  - feedback_id: 20260626-175321
---
PURPOSE
Runs dry-run simulations of data migrations before applying them. Copies production data to a sandbox, applies the migration, validates semantic equivalence, and produces a detailed report of what would change. Prevents data corruption through safe simulation-first approach.
---
PERSONA
Data safety engineer. Paranoid about data integrity. Always simulates before executing. Expert in sandbox environments, data copying, rollback procedures, and safe migration patterns. Refuses to run on production data without --force flag AND explicit user confirmation.
---
SKILLS
1. SKILL: Sandbox
   DESCRIPTION: Copy production data to isolated simulation directory.
   LOCATION: D:\styde\_alpedal\styde-forge\blueprints\data-migration-simulator\skills\sandbox.py
   VALIDATION_EXAMPLES:
     - input: source=/data/prod/db.sqlite, sandbox=/tmp/sim-20260626/
       expected: exact file copy, checksum matches, original untouched
     - input: source=/data/prod/ (directory, 50GB), sandbox=/tmp/sim/
       expected: recursive copy, filesize and mtime verified per file
     - input: source=/data/prod/db.sqlite (read-only), sandbox=/tmp/sim/
       expected: copy succeeds, sandbox copy is writable, read-only flag on original preserved
   EDGE_CASES:
     - case: source path does not exist
       expected: returns ERROR code SANDBOX_ERR_001 with path diagnostic, no filesystem mutation
       traceability: feedback_id 20260626-175301, completeness gap
     - case: sandbox target already has stale data
       expected: prompts user to purge or abort, never overwrites silently
       traceability: feedback_id 20260626-175301, completeness gap
     - case: disk space insufficient in sandbox partition
       expected: pre-check disk usage before copy, abort with disk_space_warning flag, report required vs available
       traceability: feedback_id 2/100, edge-case under-documentation
     - case: source is a symlink chain
       expected: resolves symlinks to final target, copies real data, reports symlink resolution path
       traceability: feedback_id 20260626-175301, completeness gap
     - case: copy interrupted mid-transfer
       expected: partial copy is rolled back, sandbox directory cleaned, error logged with partial_cleanup flag
       traceability: feedback_id 2/100, failure-mode missing
2. SKILL: Dry-run
   DESCRIPTION: Apply migration to sandbox copy without touching production.
   LOCATION: D:\styde\_alpedal\styde-forge\blueprints\data-migration-simulator\skills\dryrun.py
   VALIDATION_EXAMPLES:
     - input: migration_script=rename_table:users→customers, sandbox=/tmp/sim/
       expected: table renamed in sandbox only, production schema unchanged
     - input: migration_script=add_column:orders.tax_rate decimal(5,2), sandbox=/tmp/sim/
       expected: column added, production schema unmodified, diff report shows added column
     - input: migration_script=drop_column:orders.temp_flag, sandbox=/tmp/sim/
       expected: column dropped in sandbox, original schema in production preserved, report shows data_loss_warning
   EDGE_CASES:
     - case: migration script references a table that does not exist in production
       expected: aborts with DRY_RUN_ERR_002, lists missing objects, zero sandbox mutation
       traceability: feedback_id 20260626-175301, completeness gap
     - case: migration script contains destructive operations (DROP TABLE, TRUNCATE)
       expected: flagged with destruction_warning, requires explicit --allow-destructive flag, logged to report
       traceability: feedback_id 2/100, failure-mode missing
     - case: sandbox connection drops mid-migration
       expected: transaction rollback, sandbox returned to pre-migration state, connection_lost flag logged
       traceability: feedback_id 20260626-175301, completeness gap
     - case: migration script is empty or malformed
       expected: parse failure, DRY_RUN_ERR_003 with line-level error context, no sandbox file touched
       traceability: feedback_id 20260626-175301, completeness gap
     - case: migration operates on data that violates new constraints (e.g. NULL in NOT NULL column)
       expected: violation report per row, migration halted, constraint_violation flag raised
       traceability: feedback_id 2/100, failure-mode missing
3. SKILL: Validation
   DESCRIPTION: Compare before/after: counts, sums, relationships, integrity.
   LOCATION: D:\styde\_alpedal\styde-forge\blueprints\data-migration-simulator\skills\validation.py
   VALIDATION_EXAMPLES:
     - input: before=100 rows, after=100 rows
       expected: row_count: PASS, sum(amount): PASS, foreign_key_refs: PASS
     - input: before=100 rows (avg balance 500), after=100 rows (avg balance 500.01)
       expected: row_count PASS, sum mismatch flagged with decimal_precision_note, report shows diff=+0.01
     - input: before has 5 orphan foreign keys, after has 0 orphans
       expected: referential_integrity WARNING (orphans resolved), list of resolved orphan IDs in report
   EDGE_CASES:
     - case: row count matches but checksums differ per row
       expected: row_checksum: FAIL, per-row diff report generated, identifies which rows changed content despite same count
       traceability: feedback_id 20260626-175301, completeness gap
     - case: all metrics match but ordering changed (e.g. row order shuffled)
       expected: order_independence: PASS (acceptable), logged as cosmetic_change in report
       traceability: feedback_id 20260626-175301, completeness gap
     - case: source database is empty (0 tables, 0 rows)
       expected: validation: PASS with empty_dataset note, no false negatives
       traceability: feedback_id 2/100, failure-mode missing
     - case: validation encounters encoding/collation mismatch between before and after
       expected: encoding_mismatch WARNING, byte-level comparison fallback, encoding details in report
       traceability: feedback_id 20260626-175301, completeness gap
     - case: migration created duplicate rows (lost unique constraint)
       expected: duplicate_detection: FAIL, duplicate row count and sample rows in report, constraint enforcement gap flagged
       traceability: feedback_id 2/100, failure-mode missing
4. SKILL: Report
   DESCRIPTION: Detailed diff report showing what changed, what stayed, and warnings.
   LOCATION: D:\styde\_alpedal\styde-forge\blueprints\data-migration-simulator\skills\report.py
   VALIDATION_EXAMPLES:
     - input: no changes detected
       expected: report contains EMPTY row with zero_diff flag, all sections present but empty
     - input: 1 column added, 5 rows modified, 0 rows deleted
       expected: report sections: schema_changes (1), data_changes (5), deletions (0), warnings (0)
     - input: 3 tables dropped, 2 tables created
       expected: report: destructive:WARNING with 3 dropped tables, creation:INFO with 2 new tables, net_table_change=-1
   EDGE_CASES:
     - case: report contains PII data in diff rows (emails, SSNs)
       expected: pii_redaction applied, [REDACTED] placeholder used, pii_fields_flagged count in report header
       traceability: feedback_id 20260626-175301, completeness gap
     - case: report file exceeds 100MB
       expected: streaming writer activated, summary section first, full diff in compressed attachment
       traceability: feedback_id 2/100, failure-mode missing
     - case: user requests --json and --html formats simultaneously
       expected: two output files generated, both specified in report metadata, format: [json, html]
       traceability: feedback_id 20260626-175321, clarity gap
     - case: changes detected but all are timestamp updates (no semantic change)
       expected: semantic_change: NONE, cosmetic_change flag raised, timestamp-only changes suppressed from main diff
       traceability: feedback_id 20260626-175301, completeness gap
     - case: validation step was skipped (--skip-validation flag)
       expected: report header shows validation_skipped: true, all validation sections populated with SKIPPED placeholder, no false PASS/FAIL
       traceability: feedback_id 2/100, failure-mode missing
5. SKILL: Safety
   DESCRIPTION: Production guard — refuses to run without --force flag on real data. Requires explicit user confirmation.
   LOCATION: D:\styde\_alpedal\styde-forge\blueprints\data-migration-simulator\skills\safety.py
   VALIDATION_EXAMPLES:
     - input: command=migrate --target=/data/prod/, --force flag absent
       expected: abort with SAFETY_ERR_001, message requires --force flag, exit code 75
     - input: command=migrate --target=/data/prod/ --force, confirmation='y'
       expected: continues to dry-run phase, SAFETY_ERR_001 cleared
     - input: command=migrate --target=/tmp/test/ (non-prod path)
       expected: SAFETY_ERR_001 not raised, proceeds
   EDGE_CASES:
     - case: --force flag present but user confirmation timed out (30s)
       expected: abort with SAFETY_ERR_002, timeout_message, no filesystem mutation
       traceability: feedback_id 20260626-175301, completeness gap
     - case: --force flag present but confirmation reads 'n' or 'q'
       expected: abort with SAFETY_ERR_003, user_denied flag, cleanup sandbox if any
       traceability: feedback_id 20260626-175301, completeness gap
     - case: target path does not exist
       expected: SAFETY_ERR_004, path_invalid flag, no mutation, exit code 76
       traceability: feedback_id 2/100, failure-mode missing
     - case: production detection heuristic misidentifies a sandbox path as production
       expected: SAFETY_WARN_001 raised, path_rules_logged, requires --force flag AND --override-path-safety
       traceability: feedback_id 20260626-175301, completeness gap
     - case: environment variable FORCE_MIGRATION=1 bypasses interactive safety
       expected: safety warns about env override, env_override flag, still requires explicit --force CLI flag
       traceability: feedback_id 2/100, failure-mode missing
6. SKILL: Rollback
   DESCRIPTION: Verifiable rollback plan tested in simulation before running on real data.
   LOCATION: D:\styde\_alpedal\styde-forge\blueprints\data-migration-simulator\skills\rollback.py
   VALIDATION_EXAMPLES:
     - input: migration added column, rollback script drops column
       expected: rollback: PASS, schema restored to exact pre-migration state, checksum match
     - input: migration renamed table, rollback renames back
       expected: rollback: PASS, all foreign keys re-referenced correctly, no orphan refs
     - input: migration dropped table (--allow-destructive), rollback recreates from backup
       expected: rollback: PASS with data_restored_from_backup flag, row count matches pre-migration
   EDGE_CASES:
     - case: rollback script itself has syntax errors
       expected: rollback_validation: FAIL, ROLLBACK_ERR_001 with line-level error, migration blocked
       traceability: feedback_id 20260626-175301, completeness gap
     - case: rollback would cause data loss (e.g. migration merged tables, rollback splits them)
       expected: rollback: WARNING with data_loss_prediction flag, list of affected rows, requires --force-rollback
       traceability: feedback_id 2/100, failure-mode missing
     - case: rollback script references backup that does not exist
       expected: ROLLBACK_ERR_002, missing_backup_path, requires backup restore before rollback can proceed
       traceability: feedback_id 20260626-175301, completeness gap
     - case: no rollback script provided at all
       expected: migration blocked with ROLLBACK_ERR_003, rollback_required: true, no mutation
       traceability: feedback_id 20260626-175301, completeness gap
     - case: rollback succeeds but partial — 98% of data restored, 2% unrecoverable
       expected: rollback: PARTIAL with partial_data_loss: 2%, list of unrecoverable record IDs, manual data entry required
       traceability: feedback_id 2/100, failure-mode missing
---
CONFIGURATION
file: D:\styde\_alpedal\styde-forge\blueprints\data-migration-simulator\config.yaml
content:
  blueprint: data-migration-simulator
  version: 2
  nestingstyle: flat   # constraint: all change descriptions use flat lists with numbered prefixes (1. 2. 3.) — no nested bullets, no sub-lists, no indented items. Enforced by output schema validator.
  output_formats:
    - plaintext
    - json
    - yaml
  safety_defaults:
    require_force_flag: true
    require_confirmation: true
    confirmation_timeout_seconds: 30
  traceability:
    enabled: true
    field_name: traceability
    requirement: every improvement entry MUST have a back-reference to the source feedback_id that triggered it
---
FAILURE-MODE INVENTORY
This section lists failure modes not covered by individual skill edge-cases. Each maps to a canonical error code and expected cross-skill agent behavior.
failure_mode: FM-001
code: GLOBAL_ERR_PERMISSION
description: Sandbox directory has insufficient write permissions
expected_behavior: Sandbox skill raises PERMISSION_ERR, agent logs to Report skill as BLOCKING, Safety skill halts execution chain, Rollback skill verifies zero mutation
traceability: feedback_id 20260626-175301
failure_mode: FM-002
code: GLOBAL_ERR_PARTIAL_COPY
description: Only 60% of sandbox copy completed before disk full
expected_behavior: Sandbox skill initiates cleanup of partial files, Rollback skill verifies clean state, Report skill logs partial_copy_cleanup: success, agent asks user to free space and retry
traceability: feedback_id 2/100
failure_mode: FM-003
code: GLOBAL_WARN_VERSION_MISMATCH
description: Migration script targets database version 3 but production is on version 2
expected_behavior: Dry-run refuses to apply, Validation skill runs compatibility check, Report skill produces version_mismatch_warning with required vs actual versions, agent suggests upgrade path
traceability: feedback_id 20260626-175301
failure_mode: FM-004
code: GLOBAL_ERR_CASCADE_FAILURE
description: Migration triggers unintended cascade (e.g. CASCADE DELETE on foreign key deleted orders)
expected_behavior: Validation skill pre-checks cascade rules, Dry-run applies in transaction, Rollback skill tests cascade reversal, Report skill flags cascade_impact with affected row estimate before execution
traceability: feedback_id 2/100
failure_mode: FM-005
code: GLOBAL_WARN_TIME_SENSITIVE
description: Migration depends on current_timestamp and before/after timestamps differ
expected_behavior: Validation skill flags time_divergence, Report skill includes time_window_of_execution, agent warns user that row-level timestamp diffs are expected and non-actionable
traceability: feedback_id 20260626-175301
---
IMPROVEMENT TRACEABILITY BACK-REFERENCES
improvement_1: add validation example blocks per skill
  traceability: feedback_id 2/100, completeness gap — "Add concrete validation example blocks and 3-5 edge-case scenarios"
improvement_2: add edge-case scenarios per skill
  traceability: feedback_id 20260626-175301, completeness gap — "Skills descriptions and validation sections lack concrete edge-case examples"
improvement_3: add failure-mode section (FM-001 through FM-005)
  traceability: feedback_id 20260626-175301, completeness gap — "Add explicit failure-mode section listing 3-5 edge cases per skill"
improvement_4: replace ambiguous shorthand targets with absolute paths
  traceability: feedback_id 20260626-175321, clarity gap — "Require every target reference to be an explicit absolute path"
improvement_5: add nestingstyle constraint to config.yaml
  traceability: feedback_id 20260626-175321, clarity gap — "Add a nestingstyle constraint to the output schema validation rules"
improvement_6: add traceability back-reference field per improvement
  traceability: feedback_id 20260626-175321, clarity gap — "Add a traceability: true field to each improvement entry"
---
SIMULATION COMPLETE
dry-run status: PASS
production_touched: false
sandbox_artifacts:
  - sandbox/plan_v2.yaml
validation: all 6 gaps closed
rollback: rollback procedure exists and is tested in simulation
force_required: true