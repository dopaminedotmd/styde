Orchestration Workflow Design for Styde Forge v3.0
PHASE 1: BATCH PLANNER
Input: list of blueprints + tasks for this cycle
Output: ordered batch plan with collision-free assignments
Algorithm:
1. Parse all tasks. Each task has:
   task_id: str
   blueprint: str
   action: spawn|eval|improve|promote
   files_written: [list of relative paths]
   files_read: [list of relative paths]
   depends_on: [list of task_ids]
2. Build dependency graph DAG:
   Blueprint A:
     spawn-A → eval-A → improve-A → promote-A
   Blueprint B:
     spawn-B → eval-B → improve-B → promote-B
   Cross-blueprint deps (optional, from config.yaml):
     depends_on config in blueprint's config.yaml
3. File collision detection:
   For each pair of tasks (Ti, Tj) in same candidate batch:
     if Ti.files_written intersects Tj.files_written → COLLISION
     if Ti.files_written intersects Tj.files_read (and Ti is not Tj) → potential read-write collision
   Collision map:
     state.yaml: ALL write tasks collide, serialized to batch of 1
     output.md: only same-blueprint spawn tasks collide (one run dir per spawn)
     eval.yaml: only same-blueprint eval tasks collide
     teacher_review.yaml: only same-blueprint improve tasks collide
4. Batch construction:
   Level 0: all tasks with empty depends_on
     Sort by collision groups
     Split into batches of max_batch_size (default 5)
     Within each batch: verify NO file collisions
   Level 1: tasks whose deps are all in Level 0 or Level 1
     Same process
   Continue until all tasks assigned.
PHASE 2: TOKEN BUCKET RATE LIMITER
Class TokenBucket:
   capacity: int (default 5)
   refill_rate: float (tokens per second, default 0.5)
   tokens: float = capacity
   last_refill: timestamp
   Method consume(tokens=1) -> bool:
     refill()
     if tokens >= 1:
       tokens -= 1
       return True
     return False
   Method wait_for_tokens(tokens=1, timeout=300):
     while not consume(tokens):
       sleep(1)
       if timeout exceeded: raise
PHASE 3: PER-BATCH CHECKPOINT
Format: checkpoints/batch-{batch_id}-{timestamp}/
  metadata.yaml:
  {
    batch_id: 2,
    phase: "orchestrator",
    batch_index: 0,
    total_batches: 4,
    tasks: [
      {
        task_id: "spawn-orchestration-workflow-builder",
        status: "completed",
        output_path: "StydeAgents/refinery/orchestration-workflow-builder/runs/run-20260626-194800/output.md"
      },
      {
        task_id: "spawn-caveman-mode-enforcer",
        status: "failed",
        error: "timeout",
        retry_count: 1
      },
      {
        task_id: "spawn-mockup-to-code-converter",
        status: "pending"
      }
    ],
    global_state_snapshot: "hash_of_state_yaml"
  }
  state.yaml  (copy of current state)
  filestore/  (per-task output snapshots, keyed by task_id)
PHASE 4: RESUME LOGIC
On start:
  1. Scan checkpoints/ for latest {batch_id, timestamp}
  2. Load latest batch checkpoint metadata
  3. For each task in that batch:
     if status == "completed": skip (output already exists)
     if status == "failed" and retry_count < max_retries: retry
     if status == "failed" and retry_count >= max_retries: mark as dead, continue
     if status == "pending" or "running": process
  4. When current batch fully processed, proceed to next batch
PHASE 5: ORCHESTRATOR MAIN LOOP
function run_orchestrator(blueprints, task_spec=null, max_workers=5):
  1. Load state, acquire lock
  2. Check for crash -> recover if needed
  3. Phase 1: PLAN
     tasks = build_task_list(blueprints, task_spec)
     batches = plan_batches(tasks)
     save_batch_plan(batches)
  4. Phase 2: DISPATCH
     token_bucket = TokenBucket(capacity=max_workers, refill_rate=1)
     for batch in batches:
       batch_id = batch.index
       checkpoint_before_batch(batch_id)
       results = {}
       with ThreadPoolExecutor(max_workers=max_workers) as pool:
         futures = {}
         for task in batch.tasks:
           token_bucket.wait_for_tokens()
           if circuit_breaker_for(task.blueprint).can_proceed():
             futures[pool.submit(dispatch_task, task)] = task.task_id
         for future in as_completed(futures):
           task_id = futures[future]
           results[task_id] = future.result()
           token_bucket = TokenBucket(...)  # token returns on completion
       checkpoint_after_batch(batch_id, results)
       # Handle failures: retry failed tasks, update circuit breakers
     # All batches complete
  5. Phase 3: FINALIZE
     update_global_state()
     create_full_forge_checkpoint("orchestrator-cycle")
     release_lock()
PHASE 6: INTEGRATION WITH EXISTING FORGE.PY
New CLI commands in forge.py:
  orchestrate --blueprints bp1,bp2,bp3 --max-workers 5
  orchestrator-status
  orchestrator-resume
The orchestrator reuses:
  - Core.spawn.build_spawn_prompt (for spawn tasks)
  - Core.hermes_bridge.spawn_agent / run_eval / run_teacher (for execution)
  - Core.evaluate.* (for eval tasks)
  - Core.teacher.* (for improve tasks)
  - Core.checkpoint.create_checkpoint (for final checkpoint)
  - Core.recovery.acquire_lock / release_lock
  - Core.circuit_breaker.*
  - Core.state.batch_writes (for batched state updates)
FILE COLLISION MATRIX:
                  spawn-A  spawn-B  eval-A  eval-B  improve-A  improve-B
spawn-A           COLLIDE  OK       RW      OK      RW         OK
spawn-B           OK       COLLIDE  OK      RW      OK         RW
eval-A            RW       OK       COLLIDE OK      RW         OK
eval-B            OK       RW       OK      COLLIDE OK          RW
improve-A         RW       OK       RW      OK      COLLIDE    OK
improve-B         OK       RW       OK      RW      OK         COLLIDE
state.yaml write  COLLIDE COLLIDE  COLLIDE COLLIDE COLLIDE    COLLIDE
RW = read-write collision (eval-A reads spawn-A's output.md)
COLLIDE = write-write collision (same file type, same blueprint)
OK = no collision, can run in parallel
BATCH CONSTRUCTION EXAMPLE (3 blueprints):
Blueprint A (orchestration-workflow-builder)
Blueprint B (caveman-mode-enforcer)
Blueprint C (mockup-to-code-converter)
Batch 0: spawn-A, spawn-B, spawn-C
  Files: each writes to different run dir -> no collision
  Note: state.yaml writes serialized after batch
Batch 1: eval-A, eval-B, eval-C
  Each reads its own output.md, writes its own eval.yaml -> OK
  No cross-blueprint file access
Batch 2: improve-A, improve-B, improve-C
  Each reads its own eval.yaml, writes its own teacher_review.yaml -> OK
Batch 3: promote-A, promote-B, promote-C
  Files: each moves its own run dir -> directories = files, collision?
FULL PIPELINE AS BATCHED ORCHESTRATOR:
batch_plan:
  - batch_id: 0
    tasks: [spawn-A, spawn-B, spawn-C]
    parallel: true
    collision_ok: true
    checkpoint_before: checkpoints/batch-0-before/
  - batch_id: 1
    tasks: [eval-A, eval-B, eval-C]
    parallel: true
    depends_on_batch: 0
    collision_ok: true
    checkpoint_before: checkpoints/batch-1-before/
  - batch_id: 2
    tasks: [improve-A, improve-B, improve-C]
    parallel: true
    depends_on_batch: 1
    collision_ok: true
    checkpoint_before: checkpoints/batch-2-before/
  - batch_id: 3
    tasks: [promote-A, promote-B]  # only if scores >= 85
    parallel: true
    depends_on_batch: 2
    checkpoint_before: checkpoints/batch-3-before/
  - batch_id: 4
    tasks: [state_sync, global_checkpoint]
    parallel: false
    depends_on_batch: 3
    serial: true  # state.yaml write
IMPLEMENTATION FILES TO CREATE:
D:\styde\_alpedal\styde-forge\Core\orchestrator.py
  - BatchPlanner class (phase 1)
  - TokenBucket class (phase 2)
  - Orchestrator class (phase 5)
  - checkpoint/resume methods (phase 3-4)
  - file collision detection
D:\styde\_alpedal\styde-forge\Core\batch_checkpoint.py
  - BatchCheckpoint class
  - per-batch save/load/resume
  - integrates with Core.checkpoint
D:\styde\_alpedal\styde-forge\scripts\forge_orchestrator.py
  - CLI entry point for orchestrate command
  - calls Orchestrator.run()
  - handles graceful shutdown
D:\styde\_alpedal\styde-forge\Core\tests\test_orchestrator.py
  - test batch planning
  - test file collision detection
  - test token bucket rate limiting
  - test checkpoint/resume recovery