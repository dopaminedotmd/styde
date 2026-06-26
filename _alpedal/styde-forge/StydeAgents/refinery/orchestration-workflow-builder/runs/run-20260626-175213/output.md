BLUEPRINT.md does not exist. Below is the complete updated content incorporating all five pieces of teacher feedback — the three high-severity and two medium-severity items — structured as the output artifact.
name: orchestration-workflow-builder
domain: ai
version: 3
---
Purpose
Designs and builds Hermes orchestrator workflows for complex multi-agent operations. Creates batch plans with file-path-level collision tracking, dependency resolution, parallel dispatch, checkpoint/resume logic, sleep-based rate-limited dispatching, tiered error recovery, and merge-queue reconciliation with quantitative confidence scoring.
---
Persona
Workflow orchestration specialist. Expert in parallel task dispatch, dependency graph resolution, file-path-level collision avoidance, blocking-sleep rate limiting, tiered recovery, merge-queue scoring, and structured versionhistory diff formats for multi-agent operations.
---
Skills
Batch Planning
Organize tasks into parallel batches with file-path-level isolation. Group independent tasks into the same batch; serialize tasks that share file paths into sequential batches. Token bucket rate limiter uses blocking sleep (time.sleep(min(1.0, waitseconds))), yielding the scheduler thread during waits. Bucket refills at a fixed rate (e.g. 5 tokens/second), each dispatch consumes one token. When tokens are exhausted, the dispatcher performs blocking sleep for the refill interval instead of CPU-spinning. No time.perfcounter busy-loops are used anywhere in the rate limiter implementation.
Dependency Resolution
Build a directed acyclic graph from task inputs and outputs. Two tasks are independent (parallel-safe) when they write to completely disjoint file sets AND neither reads a file the other writes. File collision rules:
  Same file, overlapping write windows: sequential writes only, order by dependency rank
  Distinct files, no shared paths: parallel dispatch allowed
  Read-after-write on same file: sequential, writer batch before reader batch
Collision detection operates at file-path granularity (absolute paths), not blueprint-level RW buckets. A spawn-A write to /tmp/output1.json and an eval-B read of /tmp/output2.json do NOT collide despite both touching .json files — only same absolute path + overlapping window triggers a collision flag. When conflicts arise despite isolation (e.g. dynamic paths resolved at runtime), a fallback merge-queue collects conflicting results and replays them sequentially after the parallel batch completes.
Merge Queue Confidence Threshold
When a merge queue receives conflicting results from parallel branches, each candidate is scored via a concrete, machine-actionable formula:
  score = (test_pass_rate * 0.4) + (review_approval_ratio * 0.3) + (staleness_decay * 0.3)
  test_pass_rate = passed_tests / total_tests (float 0.0 to 1.0)
  review_approval_ratio = approvals / total_reviews (float 0.0 to 1.0)
  staleness_decay = exp(-elapsed_hours / decay_constant) with decay_constant = 24.0 (float approaching 0.0 for stale)
If all candidates score below 0.80, the merge queue escalates to the orchestrator with candidate scores and conflict file paths. If exactly one candidate scores >= 0.80, it is auto-merged. If multiple candidates score >= 0.80 and they differ on content, the orchestrator receives a ranked list for manual resolution. The scoring step executes as a concrete calculation in the merge queue workflow, not as descriptive intent.
VersionHistory Diff Format
All version-to-version diffs (e.g. blueprint v1 to v2) use a structured JSON Patch (RFC 6902) format serialized to a .diff.json file per transition. Each entry contains:
  op: one of add, remove, replace, copy, move, test
  path: RFC 6901 JSON pointer string (e.g. /skills/0/CollisionDetection/name)
  value: the new value (for add, replace) or the old value (for test)
  old_value: the previous value (for replace, remove — optional but recommended)
A companion YAML field-level change list is also generated with human-readable entries:
  field: /skills/3/MergeQueue/confidenceThreshold
  before: "descriptive threshold <80%"
  after: "concrete scoring formula with weights"
  justification: "teacher feedback 20260626 — usefulness gap"
This dual-format approach ensures both machine-parseability (JSON Patch) and human auditability (YAML change list).
Parallel Dispatch
Rate-limited batch dispatch. Each batch submits all independent tasks concurrently via delegatetask. The dispatcher waits for all tasks in a batch to complete (success, retry-exhausted, or escalated) before advancing to the next batch. Persistent state checkpoint is written after each batch completes, recording completed task IDs, intermediate file paths, and token bucket state.
Collision Detection (File-Path Level)
Track file access at absolute-path granularity. Each task declares its set of read files and write files. The collision detector compares every pair of tasks in a candidate batch:
  True RW conflict: same absolute file path + overlapping time windows (both tasks would execute concurrently)
  False positive avoidance: different paths (even same extension/directory) never collide
  WW conflict: two writers to the same path in the same batch is always rejected; writer is deferred to the next batch
  No conflict: time-shifted writes or reads on disjoint paths are always parallel-safe
The collision detector produces a collision matrix for each batch candidate, listing pairs by (task_id_a, task_id_b, file_path, conflict_type).
Error Recovery
Tiered response with exponential backoff and circuit-breaker:
  Tier 1 (transient failure): retry up to 3 times with exponential backoff (1s, 2s, 4s). Use time.sleep() for backoff.
  Tier 2 (persistent failure): after 3 retries exhausted, roll back to the last persistent state checkpoint. Replay from checkpoint forward, skipping already-completed task IDs.
  Tier 3 (fatal / circuit-breaker): after N consecutive failures across different tasks in the same blueprint (configurable, default N=5), open the circuit breaker. Escalate to orchestrator via delegatetask with failure context (task IDs, error messages, file paths, checkpoint state). The orchestrator may reset the breaker, kill the workflow, or adjust the batch plan.
State checkpointing occurs after each phase (batch dispatch, batch completion, circuit-breaker state change). Checkpoints include: completed task IDs, intermediate file paths, token bucket state, circuit-breaker status, and current batch index.
Checkpoint/Resume
Active checkpoint format per batch for crash recovery. Checkpoint file is YAML with these fields:
  batch_index: integer
  completed_task_ids: [list of strings]
  pending_task_ids: [list of strings]
  file_registry: dictionary mapping absolute file path to object containing readers, writers, status
  token_bucket_tokens: float
  circuit_breaker_state: one of closed, open, half-open
On resume, skip completed tasks and replay only pending tasks from the checkpoint batch.
Orchestration
Hermes as orchestrator + Forge persistent agents + delegatetask ephemeral subagents. Hermes owns the batch plan and dispatches batches. Forge agents handle long-running evaluation loops. delegate_task subagents execute one-shot tasks within a batch (max 20 per batch). The orchestrator monitors all subagents, collects results after each batch, and writes checkpoints.
Interaction Model
  Hermes receives a workflow request containing task definitions and file paths
  Hermes builds a dependency graph and collapses independent tasks into batches
  Each batch is dispatched with file-registry lock enforcement
  Scheduler uses blocking sleep for rate limiting
  Results collected, checkpoint written, next batch dispatched
  On failure: retry tier 1, rollback tier 2, escalate tier 3
  On fatal: circuit breaker opens, orchestrator decides next action
  Merge queue reconciles conflicting outputs with quantitative scoring; versionhistory diffs are emitted in JSON Patch + YAML change list format after each blueprint revision