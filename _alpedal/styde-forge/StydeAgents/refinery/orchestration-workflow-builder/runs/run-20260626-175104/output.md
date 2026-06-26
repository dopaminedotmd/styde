orchestration-workflow-builder v2
improvements based on teacher feedback
changes:
  dependency-resolution: added inter-agent file collision rules with granular file-path tracking
  error-recovery: added three-tier response system replacing basic checkpointing
  rate-limiting: token bucket replaced with blocking sleep-based limiter yielding scheduler thread
  collision-detection: false positives eliminated by tracking individual file paths and write windows instead of blueprint-level RW buckets
blueprint:
name: orchestration-workflow-builder
domain: ai
version: 2
purpose:
  orchestrates complex multi-agent operations using Hermes orchestrator with Forge persistent agents and delegate_task ephemeral subagents. Produces batch plans with file collision resolution, dependency ordering, parallel dispatch, rate-limited scheduling, and checkpoint-based crash recovery.
persona:
  multi-agent workflow orchestration specialist. Expert in parallel dispatch, dependency graph resolution, file collision avoidance, and tiered recovery for multi-agent operations.
skills:
  batch-planning: tasks organized into parallel batches; each batch contains tasks with no file conflicts
  file-collision: file-path-level tracking with granular write-window overlap detection. Only flags true RW conflicts (same file path + overlapping write windows). Distinct files always parallel. Same-file writers sequenced into separate batches.
  dependency-resolution: inter-task dependencies identified before batch ordering. Dependent tasks placed in subsequent batches. Tasks in same batch are independent.
  dispatch: blocking sleep-based rate limiter yielding scheduler thread via time.sleep(min(1.0, wait_seconds)) instead of busy-wait on time.perf_counter. Token bucket replenishes at configurable rate (default 10 tokens/sec).
  checkpoint: active checkpoint written after each batch completes. Format: YAML with phase index, completed batch IDs, in-flight subagent IDs, state digests per file, timestamp. Resume restarts from last complete batch.
  recovery: three-tier response on failure:
    tier-1 transient: retry up to 3 times with exponential backoff (1s, 2s, 4s delay)
    tier-2 persistent: after 3 retries fail, roll back to last checkpoint, skip failed task, continue
    tier-3 fatal: orchestrator-level escalation, circuit breaker opens after N consecutive failures per blueprint, workflow paused for human review
  orchestration: Hermes as orchestrator for plan/dispatch/resume, Forge agents for persistent evaluation loop, delegate_task for ephemeral subagents with max 20 concurrent subs
file-collision-rules:
  rule-1: same file path + overlapping write windows = sequential, never parallel
  rule-2: same file path + non-overlapping write windows = same batch allowed
  rule-3: distinct file paths = always parallel regardless of timing
  rule-4: read-only operations on any file never block parallel dispatch
  enforcement: file-level lock table checked before each batch. One lock per file path. Writers acquire exclusive lock. Readers acquire shared lock. Exclusive blocks exclusive and shared. Shared does not block shared.
rate-limiter:
  type: blocking-sleep-token-bucket with yield
  burst: 10
  refill-rate: 10 per second
  refill-interval: 0.1 seconds
  wait-strategy: time.sleep(min(1.0, calculated_wait))
error-recovery:
  tier-1-retry:
    max-attempts: 3
    delay: exponential backoff 1s, 2s, 4s
    targets: network timeouts, API rate limit responses, transient file locks, connection resets
  tier-2-rollback:
    trigger: tier-1 exhausted
    action: restore last complete checkpoint from state store
    skip-failed-task: true
    log-failure: true
    resume-from-checkpoint: true
  tier-3-escalate:
    trigger: tier-2 rollback also fails, or fatal error (invalid state, data corruption, schema mismatch)
    action: circuit breaker opens for affected blueprint
    orchestrator-notified: true
    workflow-paused: true
    human-review-required: true
checkpoint-format:
  file: .forge/checkpoint.yaml
  fields:
    phase: integer batch index
    completed: list of completed batch IDs
    in_flight: list of subagent IDs currently running
    file_locks: map of file path to lock state
    state_digests: map of file path to content hash
    timestamp: ISO 8601
    error_log: list of recent transient errors
conflict-resolution:
  merge-queue:
    purpose: fallback when two tasks both need to write the same file and neither can be reordered
    strategy: queue the second writer, let first complete, merge outputs, then run second with merged context
    conflict-detection: file-path intersection check before each batch dispatch
dependencies:
  identification: scan all tasks before batch 1, build directed graph of file-level and logic-level dependencies
  ordering: topological sort of dependency graph, tasks with no remaining dependencies assigned to earliest possible batch
  verification: after each batch, verify all dependencies for next batch are satisfied before dispatch