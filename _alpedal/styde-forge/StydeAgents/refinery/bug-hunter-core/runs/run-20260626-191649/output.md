Systematic code audit complete. Applying triage gate per feedback — each finding classified as BUG (causes runtime misbehavior) or REFACTOR (code quality) before reporting.
---
BUG HUNTER REPORT — Styde Forge v3.0 Core
Triage gate active: BUG entries only, verified for observable runtime misbehavior.
---
BUG #1 — blueprint definition permanently removed on production promotion, breaking all future spawns
File: Core/forge.py, lines 880-886
Severity: HIGH
The function _promote_agent calls shutil.move() to relocate the entire blueprint directory from StydeAgents/blueprints/{name} to StydeAgents/blueprints-archive/{name}. After this, the blueprint directory no longer exists at the expected path. Any subsequent spawn, loop, or eval operation that calls validate_blueprint() or load_blueprint_context() will fail with FileNotFoundError because these functions look exclusively in StydeAgents/blueprints/.
This is called from BOTH the sequential loop (line 810) and the parallel loop (line 1079). In the sequential loop, it triggers a break, so the user would need to spawn again manually. In the parallel loop, other blueprints continue running, but if the same blueprint name is submitted again, it silently fails.
Impact: After an agent reaches production, the blueprint is permanently destroyed. You cannot re-spawn or further iterate that blueprint. The forge loop design intends iteration until >=85 for 3 consecutive runs, but the archive action is irreversible and premature — it fires on the FIRST promotion rather than after the final loop iteration.
Reproduction:
1. forge.py loop some-blueprint --max 10
2. Agent reaches >=85 score on iteration N
3. _promote_agent moves the blueprint definition to archive
4. Loop breaks cleanly at line 813
5. User runs forge.py loop some-blueprint again
6. validate_blueprint fails: blueprint not found
Fix: Use shutil.copytree() instead of shutil.move(). The blueprint definition should be COPIED to archive, not moved, so the source remains available for subsequent iterations.
---
BUG #2 — thread-unsafe module-level globals in state.py cause duplicate activity IDs and state corruption in parallel execution
File: Core/state.py, lines 131, 143-144, 22-23, 76
Severity: HIGH
The module-level variables _activity_seq (line 131), _batch_state (line 22), and _batch_dirty (line 23) are mutated without any synchronization. In cmd_loop_parallel, each worker thread calls log_activity() (line 974, 1005, 1036 of forge.py) and update_activity() (line 991, 1029, 1052) directly from concurrent threads. The line `_activity_seq += 1` at line 143 is a read-modify-write that is NOT atomic in Python — two threads can read the same value and write the same value back, producing duplicate activity IDs.
Each worker thread also calls load_state() independently (line 1071), which reads the same state.yaml from disk. Multiple threads reading and writing activity entries to the same state file without coordination produces interleaved or overwritten data.
Impact: Activity log entries get duplicate IDs, causing update_activity() calls to match the wrong entry. State files written by concurrent save_state() calls race and one thread's activity entries can be silently dropped. The CommandCenter dashboard displays corrupted activity history. Under load, state.yaml can enter an inconsistent state.
Reproduction:
1. forge.py loop-parallel bp1,bp2 --w 2
2. Both threads call log_activity() simultaneously for spawn, eval, improve steps
3. _activity_seq yields same ID to both threads
4. update_activity() updates only one entry, leaving the other with stale status
Fix: Wrap _activity_seq with threading.Lock, or use itertools.count(start=1). Increment under lock. For batch_state, use thread-local storage (threading.local()) instead of module globals, or hold a lock for the duration of batch operations.
---
BUG #3 — _count_consecutive_passes undercounts by 1 in parallel execution, blocking legitimate production promotion
File: Core/forge.py, lines 837-859, called from line 1072
Severity: MEDIUM
In the parallel loop path, _run_one_parallel calls _count_consecutive_passes() with state loaded fresh from disk (line 1071). This state does not yet contain the current agent entry — the entry is accumulated in the local ch["agents"] list and merged only at line 1110 after all threads finish.
The function then computes:
  count = 1 if current_score >= 85 else 0
  for a in reversed(bp_agents[:-1]):  # skip last element of bp_agents
When the current agent is NOT in bp_agents (because state hasn't been updated yet), bp_agents[:-1] skips the most recent PREVIOUS agent entry, not the current one. This loses one entry from the consecutive chain.
Example: state has [run-1(85), run-2(86), run-3(88)]. Current run scores 90.
- count = 1 (current)
- bp_agents = [run-1, run-2, run-3]
- bp_agents[:-1] = [run-1, run-2]
- reversed: run-2 (88) >= 85 → count=2, run-1 (85) >= 85 → count=3
- Result: 3. Actual consecutive: current(90) + run-3(88) + run-2(86) + run-1(85) = 4.
If the actual chain is exactly 3 (e.g. [run-1(85), run-2(86)] in state, current=90):
- count = 1
- bp_agents[:-1] = [run-1]
- reversed: run-1(85) >= 85 → count=2
- Result: 2. Actual: current(90) + run-2(86) + run-1(85) = 3.
- Production gate (>= 3 consecutive) fails even though it should pass.
Impact: Intermittent false negatives in parallel production promotion. The rare case where a blueprint reaches exactly 3 consecutive passes is silently rejected, forcing unnecessary extra iterations.
Reproduction:
1. Run a blueprint through 2 iterations that both score >=85
2. Run forge.py loop-parallel some-blueprint (single BP in parallel mode)
3. Third iteration scores >=85
4. _count_consecutive_passes reports 2 instead of 3
5. Agent stays in refinery instead of being promoted
Fix: In the parallel loop path, do not use bp_agents[:-1]. Use all previous agents since the current one is not in state yet. Or, add the current agent to a temporary list before calling the function.
---
BUG #4 — promonote_agent called from TWO concurrent threads can race on blueprints-archive directory
File: Core/forge.py, lines 880-886
Severity: LOW (corner case)
In cmd_loop_parallel, two different blueprints could both reach production stage at nearly the same time. _promote_agent uses these lines:
  bp_dst = FORGE_ROOT / "StydeAgents" / "blueprints-archive" / blueprint_name
  if bp_src.exists() and not bp_dst.exists():
    bp_dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(bp_src), str(bp_dst))
Since each blueprint has its own directory name, the race is only possible if two threads both try to mkdir the parent directory simultaneously. On Windows, os.makedirs (via Path.mkdir(parents=True)) is not atomic and can raise FileExistsError in this scenario. The exception at line 129 (checkpoint creation catch-all) would handle it, but the promoted agent's blueprint might not be archived.
Impact: Rare — only with near-simultaneous promotion of two different blueprints in parallel mode. One blueprint fails to archive its definition (which is actually a GOOD thing given BUG #1, but inconsistent).
Fix: Accept the race or wrap the move in a try-except. Low priority.
---
REFACTOR APPENDIX — code quality concerns demoted from bug report per triage gate
REFACTOR #1: smart_cache.py line 31 — PRAGMA journal_mode=WAL set on EVERY connection open. Each call to _get_db() sets PRAGMAs, which is redundant after the first call. SQLite pragmas persist per connection, not per database. For caching operations called hundreds of times, the repeated set-and-commit per get/set is measurable overhead. Consider a connection pool or keeping a persistent connection.
REFACTOR #2: forge.py line 1140 — _save_blueprint_feedback() logic for trimming FEEDBACK.md entries is confusing: `entries[-9:] if len(entries) > 9 else entries[-5:] if len(entries) > 5 else entries`. This keeps at most 9 entries but the threshold logic jumps from 5 to 9 with no middle ground. Works correctly but hard to reason about.
REFACTOR #3: hermes_bridge.py line 97 — Truncation comment says "Do this BEFORE cache lookup" but code places cache lookup before truncation. The cache key uses the full untruncated prompt, which means the same full prompt always maps to the same cache key, but the stored response was generated from the truncated version. Functionally correct (same input = same output), but the comment is misleading.
REFACTOR #4: forge.py lines 727-755 — Redundant eval fallback code. The combined eval fallback and separate eval retry blocks are nearly identical (~25 lines duplicated). Works correctly but violates DRY.
REFACTOR #5: persistence.py atomic_write uses a for-else pattern on retry loop (lines 41-52) where the else branch calls shutil.move() as a last resort. If shutil.move() also fails with PermissionError, the exception is caught by the outer handler which cleans up the temp file. This silently suppresses the second failure. Works but the error vanishes instead of being logged.
REFACTOR #6: checkpoint.py _copy_dir (line 219) — The exclusion pattern matching `rel.startswith(p.rstrip("/"))` is fragile. Pattern "blueprints/" matches "blueprints" (no trailing slash) correctly, but "blueprints-archive/" also matches "blueprints". Since "blueprints-archive/" is not in EXCLUDE_PATTERNS, this doesn't cause exclusion errors, but it could cause false positives if similar names are added to the exclusion list.
---
SUMMARY
3 confirmed bugs found in Core forge code. Bug #1 (blueprint destruction on promotion) is the highest priority — it permanently breaks the forge workflow after an agent reaches production. Bug #2 (thread-unsafe globals) is a correctness issue in parallel execution mode, and Bug #3 (consecutive count undercount) causes sporadic promotion failures in the same mode.
6 refactor items demoted to appendix per triage gate — none cause observable runtime misbehavior.