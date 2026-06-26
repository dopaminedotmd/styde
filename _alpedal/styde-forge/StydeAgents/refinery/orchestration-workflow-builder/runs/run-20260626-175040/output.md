name: orchestration-workflow-builder
domain: ai
version: 2
purpose:
  Designs and builds Hermes orchestrator workflows for complex multi-agent operations.
  Creates batch plans with file collision rules, dependency ordering, parallel dispatch,
  checkpoint/resume logic, and rate-limited dispatching with proper error recovery.
persona:
  Workflow orchestration specialist.
  Expert in parallel task dispatch, dependency graph resolution, file collision
  avoidance, rate-limited dispatch, and checkpoint-based recovery for multi-agent
  operations.
skills:
  batch_planning:
    description: Organize tasks into parallel batches with file isolation.
    rules:
      - One file per subagent per batch.
      - Never two writers on same file in same batch.
      - Distinct files => parallel dispatch allowed.
      - Same file in same batch => sequential writes, first writer completes before
        second writer starts.
      - Cross-batch writes to same file allowed if batches are sequential.
    merge_queue:
      enabled: true
      when: Two subagents complete with pending writes to same file.
      action: Collate outputs and run merge-resolve step before final write.
      fallback: Escalate to orchestrator for manual merge if automatic merge
        exceeds confidence threshold (<80%).
  dependency_resolution:
    description: Resolve inter-task dependencies, order batches correctly.
    method: Static DAG analysis of task inputs and outputs.
    rules:
      - If task-B reads a file written by task-A, task-B belongs in a later batch.
      - If tasks share no files, they are independent and can be parallelized.
      - Detection granularity: file-path-level, not blueprint-level.
        Example: spawn-A writes to /tmp/subtask_A_*.json, eval-B reads
        /tmp/eval_results/*.csv => no collision despite both being blueprints.
      - RW conflict flagged only when: same file path AND overlapping write windows.
      - False positive guard: time-shifted writes to disjoint file sets are never
        flagged as conflicts.
    cross_batch:
      - Track write-sets per batch.
      - Subsequent batch reads: allow if writer batch completed.
      - Subsequent batch writes: allow if no reader in flight on same path.
  collision_detection:
    description: Ensure one file per subagent per batch, never two writers on same file.
    method: File-path-level tracking with fine-grained RW buckets.
    granularity: per-file-path, not per-blueprint.
    false_positive_prevention:
      - spawn-A writes to set S1, eval-B reads from set S2, S1 ∩ S2 = {} => no conflict.
      - Time-shifted writes: if spawn-A writes at t0 and eval-B reads at t1 where
        t1 > t0 + batch_duration, no overlap => no conflict.
    conflict_types:
      write_write:
        severity: fatal
        action: Reject batch, force sequential ordering.
      read_write_overlap:
        severity: warning
        action: Delay reader until writer batch completes, or reorder.
      read_write_disjoint:
        severity: none
        action: Allow parallel dispatch.
  dispatch:
    description: Rate-limited batch dispatch respecting API limits.
    rate_limiter:
      type: blocking_sleep
      algorithm: |
        Calculate wait = max(0.0, next_available - current_time)
        time.sleep(min(1.0, wait))
      justification: |
        Replaces token-bucket busy-wait (time.perf_counter spinning) with
        blocking sleep that yields the scheduler thread. Prevents CPU burn
        during backpressure. Minimum sleep granularity 0.01s, cap at 1.0s
        to avoid excessive wait on transient rate limits.
      tokens_per_second: 10
      burst_size: 20
      max_pending: 5
    batch_order:
      - Compute dependency graph.
      - Topological sort into sequential layers.
      - Within each layer, dispatch all independent tasks in parallel.
      - Between layers, await entire layer completion before next dispatch.
  checkpoint:
    description: Active checkpoint/resume format for crash recovery.
    format:
      type: json
      schema:
        version: 2
        session_id: string
        blueprints: list
        completed_batches: list[int]
        failed_batches: list[int]
        in_flight_tasks: list
        state_per_blueprint:
          phase: string
          last_committed_id: string
          checkpoint_data: object
    frequency: after each batch completes.
    restore: On restart, load latest checkpoint, skip completed batches,
             retry failed batches, resume in-flight tasks.
    persistent_state:
      - Save to .forge/checkpoints/{session_id}/batch_{n}.json
      - Keep last 3 checkpoints for rollback safety.
  error_handling:
    description: Tiered error recovery with circuit breaker and escalation.
    tiers:
      transient:
        description: Network timeouts, API 429/503, temporary I/O errors.
        action: Retry with exponential backoff.
        retry_count: 3
        backoff_base: 1.0
        backoff_factor: 2.0
        max_backoff: 30.0
        jitter: 0.1
      persistent:
        description: Same failure after 3 retries, non-transient errors.
        action: Rollback to last checkpoint.
        rollback:
          - Load last successful batch checkpoint.
          - Restore file state from checkpoint snapshot.
          - Mark affected tasks as pending for reprocessing.
        circuit_breaker:
          enabled: true
          threshold: 3  # consecutive failures on same blueprint
          cooldown: 60  # seconds before allowing retry
          state_file: .forge/circuit_breakers/{blueprint_id}.json
      fatal:
        description: Orchestrator crash, irrecoverable state corruption,
                     resource exhaustion.
        action: Escalate to orchestrator.
        escalation:
          - Halt all in-flight tasks.
          - Persist crash dump to .forge/crashes/{session_id}/.
          - Notify orchestrator via Hermes alert channel.
          - Do NOT auto-retry; await human or orchestrator decision.
    recovery_procedures:
      - After rollback, run integrity check on checkpoint state.
      - If checkpoint corrupted, fall back to previous checkpoint.
      - If all checkpoints corrupted, signal fatal and abort.
      - Partial batch recovery: only re-run failed tasks, not whole batch.
  circuit_breaker:
    description: Prevent repeated failure loops on persistently failing blueprints.
    states:
      closed:
        description: Normal operation, failures are counted.
        transition: On threshold reached => open.
      open:
        description: Requests rejected immediately, no execution.
        transition: After cooldown elapsed => half-open.
      half_open:
        description: One probe request allowed.
        transition: On success => closed. On failure => open with full cooldown.
    persistence: State saved to disk so breaker survives agent restart.
data_flow:
  - Receive task specification (list of blueprints, file paths, config).
  - Build dependency DAG.
  - Validate: check for circular dependencies, missing inputs.
  - Partition into batches: each batch = tasks with no inter-dependency.
  - For each batch:
    a. Validate file collision rules.
    b. Apply rate limiter (blocking sleep, not busy-wait).
    c. Dispatch tasks in parallel via delegate_task.
    d. Monitor task completion.
    e. On success: persist checkpoint.
    f. On transient failure: retry with exponential backoff (max 3).
    g. On persistent failure: rollback to previous checkpoint, update
       circuit breaker state.
    h. On fatal failure: escalate to orchestrator, halt.
  - After all batches complete: run post-processing (merge, validation).
  - Return final state.
error_scenarios:
  - Network partition during dispatch: tier 1 retry.
  - File lock contention: tier 1 retry with jittered backoff.
  - Corrupt checkpoint on load: fall back to previous, if all corrupt -> fatal.
  - Circuit breaker open: reject task, log, skip until cooldown elapses.
  - Orchestrator disconnect: save final checkpoint, await reconnection.
version_history:
  v1: Initial design, token-bucket busy-wait rate limiter, blueprint-level
      collision detection.
  v2: Replaced busy-wait with blocking sleep rate limiter. Sharpened collision
      detection to file-path-level granularity with false positive prevention.
      Added dependency resolution section with merge queue. Added tiered error
      recovery with exponential backoff, circuit breaker, and escalation protocol.