Full code review follows. Findings grouped CRITICAL, MAJOR, MINOR.
CRITICAL
1. dashboard.py:34 — broadcast() always removes SSE clients after first message
   Problem: Queue.put_nowait() returns None on success, not True. `not None` evaluates to True, so `dead = [q for q in sse_clients if not q.put_nowait(data)]` removes EVERY client from the list after delivering their first event. SSE clients are instantly disconnected after receiving one message.
   Fix: `dead = []` and wrap put_nowait in try/except. Remove clients only on queue.Full or BrokenPipeError.
2. dashboard.py:837-853 — SSE handler blocks the HTTP server thread
   Problem: _serve_sse() runs a `while True` loop with `q.get(timeout=30)` directly in the HTTP handler thread. The HTTPServer uses a single thread by default, so one SSE client blocks ALL other HTTP requests (API calls, other SSE clients) for up to 30 seconds at a time.
   Fix: Use ThreadingHTTPServer or spawn a dedicated thread per SSE client.
3. smart_cache.py:82-119 — SQLite connection open/close per cache lookup
   Problem: Each get() call opens a new SQLite connection, runs queries, then closes it. Same for set() and invalidate_*(). With 10+ cache hits per spawn cycle, this creates 10+ connections with WAL checkpoint overhead each time.
   Fix: Use a module-level connection pool or keep a single persistent connection with thread-safe locking.
4. smart_cache.py:74-82 — Cache key includes full prompt text as hash input
   Problem: _make_key() hashes the ENTIRE prompt string. For eval prompts (often 2000+ tokens), this forces allocation and hashing of multi-kilobyte strings on every lookup. With up to 50+ lookups per loop iteration this adds measurable latency.
   Fix: Hash only a deterministic subset (prompt length + first 100 chars + last 100 chars) or use a content-addressed approach.
5. forge.py:289 vs forge.py:789 — State save race in loop
   Problem: cmd_spawn saves state at line 290 in the spawn handler, but cmd_loop defers state save until the end of iteration (line 789). Inside the loop, eval (line 423) and improve (line 557) handlers also call save_state() which writes state.yaml independently. The deferred save at line 789 can overwrite concurrent state changes from nested eval/improve calls, losing evaluation records.
   Fix: Pass state as a mutable parameter through the whole loop and save once at the end, or use a state mutator pattern instead of load->modify->save cycles.
MAJOR
6. recovery.py:163-171 — _process_alive unhandled PermissionError on Windows
   Problem: os.kill(pid, 0) on Windows raises PermissionError (not OSError) when the target process runs under a different user account. The except clauses catch OSError and ProcessLookupError but NOT PermissionError. This propagates as an unhandled exception in is_locked(), detect_crash(), and acquire_lock().
   Fix: Add `except PermissionError: return True` (the process is alive, we just can't signal it).
7. hermes_bridge.py:105-121 — shell=True with string interpolation in tempfile path
   Problem: Line 106 builds a shell command string: `f'cat "{tmp_path}" | {cmd_str}'` and runs it with shell=True. While tmp_path originates from tempfile.NamedTemporaryFile (safe), the cmd_str includes model name from user config (line 97: `-m model`). If a blueprint config specifies an adversarial model name with shell metacharacters, this enables command injection.
   Fix: Use subprocess.PIPE and feed stdin directly instead of shell piping. Or use `subprocess.run(cmd, input=prompt, text=True)` with the temp file content.
8. hermes_bridge.py:127-169 — Direct-arg path has exception handling; tempfile path does not
   Problem: The direct-arg path (line 156) catches subprocess.TimeoutExpired and FileNotFoundError. The tempfile path (line 112) does NOT catch these — if hermes binary is missing or the call times out, the exception propagates unhandled through the shell=True call.
   Fix: Add identical try/except blocks to the tempfile path, or merge both paths into one that always pipes stdin.
9. state.py:18-42 — _acquire_lock uses blocking retry loop without yield
   Problem: The busy-wait loop (line 34) calls `time.sleep(0.05)` inside a while loop that can run up to 30 seconds (600 iterations). During this time, any concurrent forge process holding the lock is competing for filesystem I/O. With 5+ concurrent agent spawns, lock contention degrades throughput.
   Fix: Use exponential backoff (0.05, 0.1, 0.2, ... up to 1s max) and add a jitter component.
10. teacher.py:99-145 — parse_teacher_response silently swallows all parse errors
    Problem: The function tries three parse strategies (direct, fence-strip, line-scan) but on all failures returns None with zero diagnostic info. The caller in forge.py (line 768) checks `if review:` and prints "Teacher parse failed." but the actual parse error is lost.
    Fix: Return the raw text alongside None so the caller can log/debug. Add logging of the specific YAML error.
11. dashboard.py:232-233 — sse_broadcaster bare except silences all errors
    Problem: `try: broadcast(...) except: pass` on a 2-second timer loop. If broadcast raises any exception (e.g. queue.Full, memory error), it's silently swallowed and the broadcaster thread continues. The pass means ALL errors are invisible.
    Fix: Log the exception or at minimum print to stderr.
12. dashboard.py:98 — tasklist | find python.exe is fragile
    Problem: `subprocess.run(["tasklist","/FI","IMAGENAME eq python.exe","/FO","CSV"], ...)` — tasklist output format varies by Windows locale. On non-English Windows the column headers differ and CSV parsing breaks. Also counts ALL python.exe processes system-wide, not just forge.
    Fix: Count managed engines from the engine registry instead of tasklist. Use WMI or psutil for cross-locale support.
13. dashboard.py:194-197 — psutil import at function scope causes import to fail silently
    Problem: `import psutil` inside get_system_health() means if psutil is not installed, the import fails at call time (when dashboard serves /api/state). The exception is caught by the caller? No — build_state_json() calls get_system_health() without a try/except, so a missing psutil crashes the entire SSE stream.
    Fix: Import at module level with a try/except fallback, or wrap get_system_health() in build_state_json().
14. forge.py:662-666 — Caveman logic inverted in loop
    Problem: Line 661-666: `caveman_on = spawn.get("caveman", True)` then `if not caveman_on and is_markdown(output_text): strip`. This means when caveman IS on, markdown is NOT stripped. But cavman rules in spawn.py already strip markdown from the prompt. The inconsistency means: prompt is stripped, but agent output can contain markdown if the agent ignores caveman rules.
    Fix: Always strip markdown when caveman is ON regardless of what the agent was told. Invert: `if caveman_on and is_markdown(...): strip`.
15. caveman.py:112-122 — inject_eval and inject_teacher prepend rules to prompts that already contain YAML format instructions
    Problem: Both evaluate.py and teacher.py already include YAML output format instructions in their base prompts. inject_eval prepends CAVEMAN_EVAL_RULES before that. If caveman is ON, the eval agent sees TWO sets of YAML formatting instructions, which can cause conflicting output formats.
    Fix: Make inject_eval/inject_teacher replace the existing format instructions rather than prepend.
MINOR
16. forge.py:251 — _state_file() returns Path but is never called in cmd_spawn which uses load_state/save_state directly
    Some functions use _state_file() for path, others hardcode. Inconsistent.
17. forge.py:1107 — IndexError on forge.py eval with only 2 args (no run_id)
    `bm = sys.argv[4] if ...` will never be reached because line 1111 accesses sys.argv[3] first and throws IndexError on insufficient args. The error message on line 1108 is dead code.
18. circuit_breaker.py:196-212 — Breaker state is in-memory only, lost on restart
    A restart after 3 failures clears all breaker state. Each blueprint starts fresh with zero failures.
19. smart_cache.py:248-256 — _get_blueprint_version reads config.yaml from disk on every cache operation
    With 50 cache lookups per loop, this means 50+ YAML parses of the same config.yaml. Cache the version in memory.
20. evaluate.py:71-98 — parse_eval_yaml regex fallback ignores score context
    The regex `r'score:\\s*(\\d+)'` on line 89 matches any number after "score:" in ANY context, including instruction text. If the prompt says "score between 0-100", the regex captures "0" from the instruction, not from the response YAML.
    Fix: Only regex-search the response portion after removing instruction text.
21. forge.py:85 — HardwareAdapter.detect() is called but may fail silently
    If detect() raises an exception (line 96), `hw_profile_name = "pontus-main"` is used but the exception is just printed. The profile is set to None. This means cmd_status() at line 165 accesses `state['hardware_profile']` which is the string "pontus-main" — not the detected profile. The error is swallowed.
22. dashboard.py:85 — `dead = [q for q in sse_clients if not q.put_nowait(data)]` modifies list while iterating
    Even if the logic were correct, iterating over sse_clients while removing items from it within the same comprehension is undefined behavior across threads.
23. persistence.py:63-68 — atomic_append opens file in append mode but does not fsync the directory
    For USB/sync safety, fsync should also be called on the parent directory handle after first write. Without directory fsync, a crash after the first append can lose the directory entry.
24. spawn.py:40-41 — run_id uses second-level precision
    `datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")` — multiple spawns within the same second produce identical run_ids. The run_dir.mkdir on line 42 uses exist_ok=True so later spawns silently overwrite earlier output.
    Fix: Add microseconds: `strftime("%Y%m%d-%H%M%S-%f")`.
25. blueprint.py:109-128 — _load_historical_context imports Core.state at function scope
    Inline import works but bypasses any top-level import guards. If load_state() raises after a partial init, the traceback is confusing.
26. hermes_bridge.py:328-341 — Combined eval split is fragile
    `output.split("---")` assumes exactly one "---" delimiter. If the model's output contains "---" inside a YAML value (possible in notes), the split produces wrong parts.
    Fix: Use a unique delimiter or match YAML blocks with regex capture groups.
27. dashboard.py:681-683 — Production promotion toast fires on every SSE tick
    `if d.production > prevProduction and prevProduction > 0: addToast(...)` — when production count changes, this fires EVERY 2-second SSE tick until prevProduction catches up. With no dedup, the toast appears repeatedly.
    Fix: Add a "promoted_agents" set to track which agents already triggered the toast.
SUMMARY: 3 critical bugs (SSE clients immediately disconnecting, HTTP server blocked by SSE, SQLite connection thrash), 12 major issues (error handling holes, race conditions, inverted caveman logic, fragile Windows process checks), 12 minor issues. Most critical: the broadcast() bug renders SSE non-functional beyond one event per client. The inverted caveman logic in cmd_loop means caveman mode incorrectly allows markdown through.