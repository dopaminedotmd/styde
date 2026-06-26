state migration report for D:\styde\_alpedal\styde-forge\state.yaml
source file
  path: state.yaml
  size: 294,920 bytes
  lines: 9,884
  sha256: a2cdb9203eb3f8e182365704b08f20b1ed226a145c88ce33971f797b176fa8c4
backup status
  backup/state.yaml.bak exists: yes
  backup/state.yaml.bak sha256: cc3fdf817800eef8110f32b072fed1bf64569552489987eb875566a6ed6d7bfd
  backup/state.yaml.bak matches source: NO (STALE)
  backup differs from source: source modified AFTER last migration
source content breakdown
  activity:         200 items  (105 eval, 47 improve, 48 spawn)
  agents:           892 items
  archive_entries:   64 items
  blueprints:       190 items (unique blueprint names)
  evaluations:        0 items (EMPTY LIST)
  improvements:     274 items
  total_agents:     378 (DECLARED - does not match actual list count)
  total_evaluations: 287 (DECLARED - but evaluations list is empty)
DATA INTEGRITY ISSUES IN SOURCE
  total_agents count mismatch: declared 378, actual list 892 items (514 gap)
  total_evaluations declared 287 but evaluations list contains 0 items (all 287 missing from state)
  evaluations appear to have been tracked in activity log only (106 eval actions exist)
  all 287 evaluations referenced by metadata were never persisted to the evaluations array
PREVIOUS MIGRATION STATE (from earlier run)
  output/agents/ - 1,975 total files
    191 blueprint-grouped files (one per unique blueprint)
    1,784 individual agent files (run_id named)
  output/evaluations/ - 14 files
    1 README.yaml stub (count: 0)
    12 per-blueprint evaluation files (total 110 evaluations)
    1 aggregate evaluations.yaml (declares 109, actually contains 109)
  output/activity/ - 238 files
  output/improvements/ - 274 files
  output/archive/ - 64 files (matching archive_entries count)
  output/index.yaml - migration index (see verification below)
PREVIOUS INDEX VERIFICATION
  index source_sha256: cc3fdf817800eef8110f32b072fed1bf64569552489987eb875566a6ed6d7bfd
  current source sha256: a2cdb9203eb3f8e182365704b08f20b1ed226a145c88ce33971f797b176fa8c4
  MISMATCH - index references old state, not current file
  index agent_file_count: 892 (CLAIMED)
  actual individual agent files on disk: 1,784
  DISCREPANCY: index undercounts by 892 files
  index evaluation_file_count: 1 (CLAIMED - counting README.yaml only)
  actual evaluation files on disk: 14
  DISCREPANCY: index undercounts evaluations by 13 files
  index runid entries: 652 (of 892 agents indexed, 240 missing)
SEMANTIC CHECKSUM COMPARISON
metric                   source state.yaml    previous output    match
agent count              892 (list actual)    index claims 892   yes (by claim)
                         378 (metadata)                          no (metadata wrong)
total_evaluations        287 (metadata)      109 in evalua-     no - 178 missing
                         0 (in list)         tions.yaml
mean composite score     0 (no evals)        ~83.2 (109 evals)  n/a (no source evals)
activity items           200                 238 files on disk  no (38 extra files)
improvements             274                 274 files on disk  yes
archive entries          64                  64 files on disk   yes
backup integrity         source changed      bak is stale       FAIL
CHANGES REQUIRED FOR CORRECT MIGRATION
1. BACKUP: create fresh backup matching current source sha256
2. AGENTS: write 892 individual agent files, not 1,975 (previous run wrote extra copies)
3. EVALUATIONS: cannot migrate from evaluations list (empty). Must extract from activity log's 106 eval actions as source of truth. Acknowledge 287-106=181 evaluations are unrecoverable metadata inflation.
4. ACTIVITY: write exactly 200 activity files matching source activity count
5. INDEX: rebuild with correct sha256 and accurate file counts
6. MISSING DATA: 240 run_ids not indexed - must add complete index
DIFFS (source to corrected migration)
agents/
  before: 1,975 files (191 grouped + 1,784 individual)
  after:  892 files (individual only, one per agents[] entry)
  change: -1,083 files (remove duplicates)
evaluations/
  before: 14 files (109-110 eval entries extracted from activity log)
  after:  13 files (106 eval entries extracted from activity log)
  change: update evaluations.yaml: total_evaluations from 109 to 106, remove stale README.yaml
  note: 287 - 106 = 181 evaluations referenced in metadata but unrecoverable
activity/
  before: 238 files
  after:  200 files
  change: -38 files (remove entries that don't exist in source)
improvements/
  before: 274 files
  after:  274 files
  change: none (match)
archive/
  before: 64 files
  after:  64 files
  change: none (match)
index.yaml
  before: source_sha256=cc3fdf81... agent_count=892 evals_count=1 runids=652
  after:  source_sha256=a2cdb920... agent_count=892 evals_count=106 runids=892
  change: update all counts and sha256, add 240 missing run_id entries
DATA LOSS SUMMARY
  evaluations: 181 of 287 declared evaluations irrecoverable
    (only 106 existed as activity entries with action=eval)
  agent metadata: total_agents 378 vs actual 892 is a metadata bug in source
    (no data loss - all 892 agents present in the agents list)
  backup: stale - current source state unrecoverable from backup
VERIFICATION COMMANDS (run after migration)
  ls output/agents/*.yaml | wc -l   -> 892
  ls output/evaluations/*.yaml | grep -cv README | wc -l -> 13
  ls output/activity/*.yaml | wc -l  -> 200
  ls output/improvements/*.yaml | wc -l -> 274
  sha256sum state.yaml -> match index source_sha256
  python3 -c "import yaml; d=yaml.safe_load(open('output/evaluations/evaluations.yaml')); print(len(d['evaluations']))" -> 106
ROLLBACK PROCEDURE (if migration fails verification)
  1. cp backup/state.yaml.bak state.yaml
  2. rm -rf output/agents/* output/evaluations/* output/activity/*
  3. python3 forge.py reload --from-backup
  4. verify: sha256sum state.yaml matches old sha256 cc3fdf817800eef8110f32b072fed1bf64569552489987eb875566a6ed6d7bfd
STATUS: MIGRATION NOT COMPLETE
  Stopping condition NOT met: backup is stale, index is inaccurate,
  and 181 evaluations are irrecoverable. Previous migration produced
  1,975 agent files instead of 892 and 238 activity files instead of 200.
  Correct migration requires purging the inflated output and rewriting
  from the current state.yaml with filesystem verification at every step.