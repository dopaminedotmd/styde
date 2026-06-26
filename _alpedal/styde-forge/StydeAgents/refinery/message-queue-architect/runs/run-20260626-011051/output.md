queue_topology:
  type: rabbitmq
  exchange: topic
  name: stryde.events
  queues:
    - name: stryde.blueprint.process
      routing_key: blueprint.*.process
      durable: true
    - name: stryde.agent.run
      routing_key: agent.*.run
      durable: true
    - name: stryde.refinery.evaluate
      routing_key: refinery.#.evaluate
      durable: true
    - name: stryde.dead.letters
      routing_key: dlq.#
      durable: true
bindings:
  - exchange: stryde.events
    queue: stryde.blueprint.process
    pattern: blueprint.*.process
  - exchange: stryde.events
    queue: stryde.agent.run
    pattern: agent.*.run
  - exchange: stryde.events
    queue: stryde.refinery.evaluate
    pattern: refinery.#.evaluate
  - exchange: stryde.events
    queue: stryde.dead.letters
    pattern: dlq.#
dead_letter_config:
  queue: stryde.dead.letters
  exchange: stryde.dlx
  routing_key: dlq.original.{routing_key}
  policies:
    max_retries: 3
    retry_interval_ms: 5000
    retry_backoff: exponential
    retry_queue: stryde.retry
    retry_ttl_ms: 30000
kafka_topics:
  - name: stryde-blueprint-events
    partitions: 6
    replication_factor: 3
    retention_ms: 604800000
    cleanup_policy: compact
  - name: stryde-agent-logs
    partitions: 3
    replication_factor: 3
    retention_ms: 2592000000
    cleanup_policy: delete
  - name: stryde-dlq
    partitions: 3
    replication_factor: 3
    retention_ms: 2592000000
    cleanup_policy: delete
consumer_groups:
  - group: blueprint-processors
    topics:
      - stryde-blueprint-events
    max_poll_records: 10
    auto_offset_reset: earliest
    enable_auto_commit: false
  - group: agent-runners
    topics:
      - stryde-blueprint-events
    max_poll_records: 5
    auto_offset_reset: latest
    enable_auto_commit: false
idempotent_handler:
  pattern: outbox-table
  implementation:
    - producer writes to outbox table in same transaction as business operation
    - relay process reads outbox and publishes to queue
    - consumer checks idempotency key in dedup store before processing
    - dedup store: redis with TTL = message_retention_period + 1h
    - on duplicate: ack immediately, skip handler
  idempotency_key_source:
    - message_id for point-to-point
    - correlation_id for saga/choreography
    - content_hash for at-least-once delivery
event_driven_flow:
  step_1_blueprint_submitted:
    event: blueprint.submitted
    publisher: forge-api
    handler: blueprint-validator
    output: blueprint.validated or blueprint.rejected
  step_2_blueprint_validated:
    event: blueprint.validated
    publisher: blueprint-validator
    handler: agent-generator
    output: agent.created
  step_3_agent_created:
    event: agent.created
    publisher: agent-generator
    handler: refinery-scheduler
    output: training.scheduled
  step_4_training_complete:
    event: training.complete
    publisher: refinery-worker
    handler: evaluation-trigger
    output: eval.scheduled
  step_5_eval_complete:
    event: eval.complete
    publisher: eval-runner
    handler: promotion-check
    output: agent.promoted or agent.retrained
  step_6_dead_letter:
    event: dlq.routed
    handler: dlq-analyzer
    action: log, alert, optional-manual-retry
error_handling:
  retry_sequence:
    - attempt 1: immediate retry
    - attempt 2: 5s delay
    - attempt 3: 25s delay (exponential backoff)
    - failure: route to DLQ with original message headers preserved
  unprocessable_message:
    action: publish to dlq.analysis queue for human review
    metadata: original_headers, error_stacktrace, retry_count