Bughunter Core — full analysis complete. 15 bugs found across 8 source files.
---
BUG REPORT: Styde Forge v3.0 — Code Audit
---
BUG #1 — CRITICAL
File: Core/forge.py:1090-1120 + Core/state.py:143-144
Race: _activity_seq increment not thread-safe in parallel loop
_activity_seq += 1 at state.py:143-144 is a bare read-modify-write on a module global with no lock. In cmd_loop_parallel (forge.py:974, 1005, 1029, 1036, 1052), multiple threads call log_activity() concurrently. Two threads can read the same sequence number, producing duplicate activity IDs (id: 379 appears twice in state.yaml — see lines 23 and 58). This corrupts the activity log and makes update_activity() target the wrong entry.
Fix: Wrap _activity_seq in a threading.Lock or use itertools.count with a lock.
BUG #2 — CRITICAL
File: Core/state.py:154-165 + forge.py:1090-1120
Race: log_activity() TOCTOU on state.yaml across parallel threads
Each log_activity() call does load_state() (read) then save_state() (write) as separate non-atomic operations. In cmd_loop_parallel, multiple threads call log_activity simultaneously from _run_one_parallel (forge.py:974, 1005, 1029, 1036). Thread A reads state (gets activity=[...]), Thread B reads state (gets same activity=[...]), Thread A saves (appends its entry), Thread B saves (appends only its entry, overwriting Thread A's write). Activity entries are silently lost. The filesystem lock in save_state() protects only the write, not the read-modify-write cycle.
Fix: Use batch_writes() within each parallel thread, or add a lock around the entire read-modify-write cycle.
BUG #3 — HIGH
File: scripts/parallel_spawn.py:34, 141
Wrong blueprint directory: references non-existent /blueprints/ instead of /StydeAgents/blueprints/
Line 34: FORGE_ROOT / "blueprints" — the blueprints directory is at FORGE_ROOT / "StydeAgents" / "blueprints" (defined in Core/blueprint.py:12 as BLUEPRINTS_DIR). Directory layout confirms: root-level has no /blueprints/ dir, only /StydeAgents/blueprints/. Both find_failed_blueprints() (line 34) and the default fallback (line 141) always return empty lists because the glob target doesn't exist. All parallel spawn operations silently skip every blueprint.
Impact: --all-failed and default-batch spawn modes are completely broken.
Fix: Change to FORGE_ROOT / "StydeAgents" / "blueprints".
BUG #4 — HIGH
File: Core/state.py:154 + forge.py:974, 1005, 1029, 1036
log_activity() bypasses batch_writes in parallel context
In cmd_loop_parallel, each recursive call to _run_one_parallel calls log_activity() directly, which triggers load_state() + save_state() per call (3 RTTs per iteration). The parallel loop never uses batch_writes, so each thread issues separate atomic writes. Combined with Bug #2, this amplifies the race window: every log_activity/update_activity pair in the parallel loop (forge.py:974-991, 1005-1029, 1036-1054) incurs 2-3 separate state.yaml writes per thread per iteration. For N=46 blueprints at 5 iterations, that is ~700 state.yaml writes in uncontrolled parallel, with most overwriting each other.
Fix: Batch state mutations per thread and flush once at thread completion.
BUG #5 — HIGH
File: scripts/parallel_improve.py:62-103
Never updates state.yaml improvement/agent entries inline
improve_one() runs teacher analysis, saves teacher_review.yaml, applies version bump (writes to config.yaml), and calls rebuild_state.py at the end. But during execution it never appends to state.yaml's "improvements" list, never updates agent "status" to "improved", never records "version" or "diagnosis" in the agent entry. The rebuild_state.py script (analyzed below) resets improvements=[], evaluations=[], and total_evaluations=0. So every parallel_improve run wipes the evaluation history.
Impact: All evaluation and improvement history is reset to zero on every run.
Fix: Mutate state.yaml inline in improve_one(), or fix rebuild_state.py to preserve evals/improvements.
BUG #6 — HIGH
File: scripts/rebuild_state.py:48-61
Destructive state reset: zeroes evaluations, improvements, total_evaluations
Line 55: total_evaluations: 0
Line 58: evaluations: []
Line 59: improvements: []
The rebuild script constructs a brand-new state dict discarding all existing evaluation records, improvement history, and counters. Both parallel_spawn.py (line 181) and parallel_improve.py (line 158) and promote_production.py (line 148) call this at the end, which means every batch operation wipes the accumulated evaluation/improvement history.
Fix: Scan filesystem for eval.yaml files to reconstruct evaluations list instead of zeroing.
BUG #7 — HIGH
File: Core/forge.py:1138-1141
FEEDBACK.md truncation logic produces double separators and garbled formatting
The _save_blueprint_feedback function splits existing content on "\n---\n" (line 1139). Each new entry starts with "\n---\n" (line 1131). When re-joining with "\n---\n".join(kept + [entry]) at line 1141, the result has:
 - First entry empty string after split (content starts with \n---\n, so split yields ['', 'first entry', ...])
 - Double "\n---\n" between last kept entry and the new entry (because new entry also starts with \n---\n)
 - Inconsistent encoding: after several iterations the file alternates between having and not having the leading \n---\n on entries
Impact: FEEDBACK.md becomes progressively malformed. Starts with empty title, then duplicated separators.
Fix: Normalize entries to NOT include the separator, then join with "\n---\n" at write time.
BUG #8 — MEDIUM
File: Core/persistence.py:67-81
atomic_append() not actually atomic — two write() calls
Opens file with 'a' mode, then calls f.write(line) followed by (if needed) f.write('\n'). These are two separate write syscalls. Between them, a crash leaves the file with a line that has no trailing newline. Additionally, on Windows, Python's write() in text mode may convert \n to \r\n which is not atomic even with O_APPEND semantics.
Impact: Rare partial-line corruption in appended log files.
Fix: Append '\n' directly to the line string before the single write() call.
BUG #9 — MEDIUM
File: Core/blueprint.py:231
Dead import: yaml imported redundantly inside _load_historical_context()
yaml is already imported at the top of blueprint.py (line 7: import yaml). The redundant import yaml inside _load_historical_context at line 231 shadows the top-level import. No functional effect but dead code.
Fix: Remove the inner import.
BUG #10 — MEDIUM
File: Core/forge.py:837-859
_count_consecutive_passes() returns 0 when current score < 85 even if there are previous passes
Logic: count = 1 if current_score >= 85 else 0, then iterates previous agents. But if current_score < 85, the function returns 0 regardless of previous passes. Works with current callers (they use the result to determine archive/retry) but the return value is misleading — it conflates "no chain" with "score too low". Caller at line 1072 in parallel loop uses it to determine stage: a blueprint with 2 previous ≥85 but current 84 gets stage "refinery" instead of getting another shot. The should_retry at line 1085 then gets consecutive=0 and may archive prematurely.
Fix: Move the "current score threshold" logic to the caller, let _count_consecutive_passes count actual history.
BUG #11 — MEDIUM
File: Core/state.py:92-127
batch_writes() is not reentrant-safe for error recovery
If an exception occurs inside a batch_writes() context, the finally block flushes _batch_state if _batch_dirty is True. But if the exception happened DURING a save_state() call inside the batch, _batch_state and _batch_dirty may be in an inconsistent state. The was_batching guard handles nesting but not error recovery: after an exception in the outer batch, _batch_state is set to None but the caller's local state variable is stale. Another caller that enters batch_writes() later would start fresh.
Impact: Low under normal operation, but can cause state loss if save_state() raises inside batch_writes().
Fix: Add try/except around the flush in the finally block.
BUG #12 — LOW
File: Core/persistence.py:49-50
Fallback shutil.move after PermissionError in atomic_write
When os.replace fails with PermissionError after 5 retries, the fallback uses shutil.move (line 50). But shutil.move on Windows is not atomic — it copies then deletes. A crash between copy and delete leaves both files, and the target file may be the old version (if the copy overwrites it atomically is OS-dependent). The function returns True even if shutil.move fails partially.
Impact: Rarely, atomic_write silently produces a non-atomic result on Windows under file lock contention.
Fix: Raise after 5 retries instead of falling back to non-atomic move.
BUG #13 — LOW
File: Core/hermes_bridge.py:96-97
Prompt truncation comment says "before cache lookup" but code does it after cache check
Comment at line 95: "Do this BEFORE cache lookup so cache key uses truncated prompt". But the truncation at line 96-97 happens AFTER the cache check at line 83-92. The cache key is computed from the full untruncated prompt. A future request with a truncated prompt would miss cache because the key differs.
Impact: Cache miss for truncated prompts, but functionality is correct — just suboptimal caching for long prompts.
Fix: Move truncation before cache lookup.
BUG #14 — LOW
File: Core/smart_cache.py:37-54
Pragma settings applied on every _get_db() call but only the first connection matters
Each call to _get_db() opens a new SQLite connection and sets PRAGMA journal_mode=WAL and synchronous=NORMAL. WAL mode is a persistent database property, not a connection property — once set, it persists across connections. The PRAGMA calls on subsequent connections do nothing but waste cycles. Similarly, the CREATE TABLE IF NOT EXISTS calls run on every connection open.
Impact: Negligible performance cost (~1ms per call).
Fix: Cache the connection at module level.
BUG #15 — LOW
File: Core/forge.py:1420-1425
cmd_storage() fallthrough line prints help after error
When an unknown subcommand is given, print(error) and print(help) both execute (lines 1424-1425). After both prints, the function returns normally. There's no sys.exit(1). Compare with other command fallthroughs (cmd_storage_upload line 1245, cmd_storage_list line 1266) which call sys.exit(1). Inconsistent error handling.
Impact: A failed storage subcommand returns exit code 0, which could mask failures in scripts.
Fix: Add sys.exit(1) after the help print, consistent with other handlers.
---
SUMMARY
CRITICAL: 2 (race on _activity_seq, race on state.yaml in parallel loop)
HIGH: 4 (wrong blueprint dir, state wipes, broken FEEDBACK.md, parallel_improve no state update)
MEDIUM: 5 (TOCTOU chain, non-atomic append, dead import, _count_ logic, batch_writes recovery)
LOW: 4 (permissions fallback, cache order, sqlite pragmas, exit codes)
Total: 15 unique bugs. Most critical is the combination of BUG #1 and BUG #2: the parallel loop is fundamentally thread-unsafe with shared state.yaml mutations, causing data loss on every multi-blueprint run.