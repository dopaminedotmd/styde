=== MESSAGE QUEUE TOPOLOGY ===
system: event-driven ecommerce backend
pattern: competing consumers + event sourcing + transactional outbox
queues:
  orders:
    type: rabbitmq
    exchange: orders.topic
    exchange_type: topic
    bindings:
      - routing_key: order.created
        queue: order_created_queue
      - routing_key: order.paid
        queue: order_paid_queue
      - routing_key: order.shipped
        queue: order_shipped_queue
      - routing_key: order.cancelled
        queue: order_cancelled_queue
    dlq:
      exchange: orders.dlx
      queue: orders_dead_letter_queue
      ttl: 300000
      max_retries: 3
      retry_delay: 10000
  payments:
    type: kafka
    topic: payment.events
    partitions: 12
    replication_factor: 3
    consumer_groups:
      - name: payment-processor
        offset: earliest
        max_retries: 5
      - name: fraud-detection
        offset: latest
        max_retries: 2
    dlq: payment.events.dlq
  notifications:
    type: sqs
    fifo: true
    content_based_deduplication: true
    dlq: notifications_dlq.fifo
    max_receive_count: 3
    delay_seconds: 0
=== EVENT-DRIVEN MICROSERVICE ===
service: order-service
handler: order_created_handler
idempotency:
  strategy: idempotency_key + database
  lookup: SELECT processed_at FROM idempotency_keys WHERE key = $1
  ttl: 7 days
  dedup_window: 60 seconds
processing:
  ack_mode: manual
  prefetch: 10
  concurrency: 5
  poison_pill:
    max_attempts: 3
    action: move_to_dlq
    circuit_breaker:
      threshold: 10
      cooldown: 60000
error_handling:
  transient: retry with exponential backoff  (2^n * 1000ms  capped 30000ms)
  persistent: move to DLQ  alert ops
  schema_mismatch: reject immediately  log schema registry id  alert dev
=== DEAD LETTER CONFIGURATION ===
dlq_policy:
  primary_queue: orders_created
  dlx: orders.dlx
  dlq: orders_dead_letter
  retry_logic:
    type: exponential_backoff
    initial_delay: 1000
    multiplier: 2
    max_delay: 60000
    jitter: true
  redrive:
    manual_redrive: true
    auto_redrive: false
    redrive_threshold: time_since_death < 86400000  only last 24h
  alert_on:
    - dlq_depth > 100
    - redrive_failure_rate > 0.05
    - message_age > 3600000
=== KAFKA TOPIC CONFIGURATION ===
topic: order.events
partitions: 24
replication_factor: 3
retention: 7 days
cleanup_policy: compact,delete
compression: zstd
segment_size: 536870912
configs:
  min.insync.replicas: 2
  unclean.leader.election.enable: false
  message.timestamp.type: LogAppendTime
  max.message.bytes: 1048576
consumer_groups:
  order-processor:
    protocol: CooperativeStickyAssignor
    max.poll.records: 500
    session.timeout.ms: 45000
    heartbeat.interval.ms: 15000
    auto.offset.reset: earliest
  analytics:
    protocol: RangeAssignor
    max.poll.records: 1000
    auto.offset.reset: latest
=== IDEMPOTENT HANDLER PATTERN ===
def handle_order_created(message, db, producer):
    key = message.headers['idempotency-key']
    result = db.query_one('SELECT processed FROM idempotency_keys WHERE key = %s', [key])
    if result and result[0]:
        return  duplicate silently acknowledged
    txn = db.begin()
    try:
        order = message.body
        db.execute('INSERT INTO orders VALUES (%s, %s, ...)', [order.id, order.status], connection=txn)
        db.execute('INSERT INTO idempotency_keys (key, processed) VALUES (%s, TRUE)', [key], connection=txn)
        txn.commit()
        producer.publish('order.confirmed', {'order_id': order.id}, headers={'idempotency-key': str(uuid4())})
    except Exception as e:
        txn.rollback()
        raise RetryableError(str(e))  goes back to queue via DLQ retry
=== TRANSACTIONAL OUTBOX ===
outbox:
  table: outbox_events
  columns:
    - id UUID PRIMARY KEY
    - aggregate_type VARCHAR
    - aggregate_id UUID
    - event_type VARCHAR
    - payload JSONB
    - created_at TIMESTAMP
    - published_at TIMESTAMP NULL
  poller:
    interval: 100ms
    batch_size: 100
    lock_timeout: 5000
  publisher:
    type: rabbitmq
    exchange: outbox.exchange
    confirm_mode: publisher_confirm
    on_failure: log and retry  do not mark published_at