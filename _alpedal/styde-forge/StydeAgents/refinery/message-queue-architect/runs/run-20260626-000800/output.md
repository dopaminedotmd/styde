# Message Queue Architecture: RabbitMQ for Event-Driven Microservices

**Document Version:** 1.0
**Date:** 2026-06-26
**Author:** Message Queue Architect (Styde Forge)
**Target Stack:** RabbitMQ 3.13+ · Node.js (amqplib) · Python (pika)

---

## Table of Contents

1. [Overview & Design Principles](#1-overview--design-principles)
2. [Exchange & Topology Patterns](#2-exchange--topology-patterns)
3. [Dead Letter Queues & Retry Policies](#3-dead-letter-queues--retry-policies)
4. [Event-Driven Microservice Communication](#4-event-driven-microservice-communication)
5. [Idempotency Keys](#5-idempotency-keys)
6. [Message Ordering Guarantees](#6-message-ordering-guarantees)
7. [Full Reference Implementation](#7-full-reference-implementation)

---

## 1. Overview & Design Principles

### Architectural Goals

| Principle | Description |
|---|---|
| **Durability** | Messages and queues survive broker restarts |
| **At-Least-Once Delivery** | Publisher confirms + consumer acknowledgements |
| **Idempotency** | Duplicate-safe processing via idempotency keys |
| **Observability** | Dead letter queues, metrics, structured logging |
| **Ordering** | Partitioned ordering where required by business rules |
| **Backpressure** | Per-queue prefetch limits, flow control |

### RabbitMQ Topology (High Level)

```
┌─────────────────────────────────────────────────────────────────┐
│                        RABBITMQ BROKER                          │
│                                                                 │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐        │
│  │  topic:      │   │  fanout:     │   │  direct:     │        │
│  │  events      │   │  broadcasts  │   │  commands    │        │
│  └──────┬───────┘   └──────┬───────┘   └──────┬───────┘        │
│         │                  │                  │                 │
│    ┌────▼────┐        ┌────▼────┐        ┌────▼────┐           │
│    │ Queues  │        │ Queues  │        │ Queues  │           │
│    │ + DLX   │        │ + DLX   │        │ + DLX   │           │
│    └─────────┘        └─────────┘        └─────────┘           │
│         │                  │                  │                 │
│    ┌────▼────┐        ┌────▼────┐        ┌────▼────┐           │
│    │ DLQ     │        │ DLQ     │        │ DLQ     │           │
│    │ (retry) │        │ (retry) │        │ (retry) │           │
│    └─────────┘        └─────────┘        └─────────┘           │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Exchange & Topology Patterns

### 2.1 Topic Exchange — Event Routing by Type & Domain

**Use case:** Route events by `domain.entity.action` so consumers subscribe to granular event streams.

```
Exchange: events.topic (type: topic)

Routing Keys:
  order.created          → order-service, notification-service, analytics
  order.paid             → order-service, invoice-service
  order.*                → order-audit-logger (wildcard consumer)
  payment.#              → payment-service (catch-all)
  *.created              → entity-creation-logger
```

**Topology Declaration (Node.js — amqplib):**

```javascript
const amqp = require('amqplib');

async function declareTopology(channel) {
  // 1. Declare the topic exchange
  await channel.assertExchange('events.topic', 'topic', {
    durable: true,
    autoDelete: false,
  });

  // 2. Declare queues with dead-letter exchange
  const queues = [
    { name: 'order-service.q', routingKeys: ['order.created', 'order.paid'] },
    { name: 'notification-service.q', routingKeys: ['order.created', 'user.registered'] },
    { name: 'analytics.q', routingKeys: ['order.created', 'payment.*'] },
    { name: 'audit-log.q', routingKeys: ['#'] }, // catch-all
  ];

  for (const q of queues) {
    await channel.assertQueue(q.name, {
      durable: true,
      arguments: {
        'x-dead-letter-exchange': 'dlx.topic',
        'x-dead-letter-routing-key': `dead.${q.name}`,
      },
    });

    for (const rk of q.routingKeys) {
      await channel.bindQueue(q.name, 'events.topic', rk);
    }
  }
}
```

**Topology Declaration (Python — pika):**

```python
import pika
from pika.exchange_type import ExchangeType

def declare_topology(channel: pika.channel.Channel):
    # 1. Declare the topic exchange
    channel.exchange_declare(
        exchange='events.topic',
        exchange_type=ExchangeType.topic,
        durable=True,
        auto_delete=False,
    )

    # 2. Declare queues with dead-letter exchange
    queues = [
        {'name': 'order-service.q', 'keys': ['order.created', 'order.paid']},
        {'name': 'notification-service.q', 'keys': ['order.created', 'user.registered']},
        {'name': 'analytics.q', 'keys': ['order.created', 'payment.*']},
        {'name': 'audit-log.q', 'keys': ['#']},
    ]

    arguments = {
        'x-dead-letter-exchange': 'dlx.topic',
        'x-dead-letter-routing-key': '',  # set per-queue below
    }

    for q in queues:
        dlx_args = {**arguments, 'x-dead-letter-routing-key': f'dead.{q["name"]}'}
        channel.queue_declare(
            queue=q['name'],
            durable=True,
            arguments=dlx_args,
        )
        for rk in q['keys']:
            channel.queue_bind(
                queue=q['name'],
                exchange='events.topic',
                routing_key=rk,
            )
```

### 2.2 Fanout Exchange — Broadcast Events

**Use case:** Configuration changes, cache invalidations, or any event where every bound queue must receive a copy.

```
Exchange: cache.invalidation (type: fanout)

Bound Queues (all receive every message):
  service-a.cache-invalidation.q
  service-b.cache-invalidation.q
  service-c.cache-invalidation.q
```

**Declaration (Node.js):**

```javascript
await channel.assertExchange('cache.invalidation', 'fanout', {
  durable: true,
  autoDelete: false,
});

// Services bind their own queues
const services = ['service-a', 'service-b', 'service-c'];
for (const svc of services) {
  const qName = `${svc}.cache-invalidation.q`;
  await channel.assertQueue(qName, { durable: true });
  await channel.bindQueue(qName, 'cache.invalidation', '');
}
```

**Declaration (Python):**

```python
channel.exchange_declare(
    exchange='cache.invalidation',
    exchange_type=ExchangeType.fanout,
    durable=True,
    auto_delete=False,
)

for svc in ['service-a', 'service-b', 'service-c']:
    q_name = f'{svc}.cache-invalidation.q'
    channel.queue_declare(queue=q_name, durable=True)
    channel.queue_bind(queue=q_name, exchange='cache.invalidation')
```

### 2.3 Direct Exchange — Command Dispatching / RPC

**Use case:** Point-to-point command delivery, request-reply patterns.

```
Exchange: commands.direct (type: direct)

Routing Keys (1:1 with queue names):
  order.create       → order.command.q
  payment.capture    → payment.command.q
  user.register      → user.command.q
```

**Declaration (Node.js):**

```javascript
await channel.assertExchange('commands.direct', 'direct', {
  durable: true,
  autoDelete: false,
});

const commands = [
  { routingKey: 'order.create', queue: 'order.command.q' },
  { routingKey: 'payment.capture', queue: 'payment.command.q' },
  { routingKey: 'user.register', queue: 'user.command.q' },
];

for (const cmd of commands) {
  await channel.assertQueue(cmd.queue, {
    durable: true,
    arguments: {
      'x-dead-letter-exchange': 'dlx.direct',
      'x-dead-letter-routing-key': `dead.${cmd.queue}`,
    },
  });
  await channel.bindQueue(cmd.queue, 'commands.direct', cmd.routingKey);
}
```

### 2.4 Headers Exchange — Content-Based Routing

**Use case:** Route messages based on header attributes rather than routing key strings. Useful when routing depends on multiple dimensions.

```
Exchange: events.headers (type: headers)

Binding Arguments (x-match: all = AND, any = OR):
  { x-match: all, region: 'eu', priority: 'high' }  → eu-high-priority.q
  { x-match: any, region: 'us', region: 'apac' }    → non-eu-processing.q
```

**Declaration (Python):**

```python
channel.exchange_declare(
    exchange='events.headers',
    exchange_type=ExchangeType.headers,
    durable=True,
    auto_delete=False,
)

channel.queue_declare(queue='eu-high-priority.q', durable=True)
channel.queue_bind(
    queue='eu-high-priority.q',
    exchange='events.headers',
    routing_key='',
    arguments={'x-match': 'all', 'region': 'eu', 'priority': 'high'},
)
```

---

## 3. Dead Letter Queues & Retry Policies

### 3.1 Architecture Overview

```
                      ┌────────────────────┐
                      │   Primary Queue    │
                      │  (x-dead-letter-   │
                      │   exchange = DLX)  │
                      └────────┬───────────┘
                               │ reject/nack (requeue=false) or TTL expiry
                               ▼
                      ┌────────────────────┐
                      │  Dead Letter       │
                      │  Exchange (DLX)    │
                      └────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                 ▼
     ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
     │  Retry Queue │  │   Park Queue  │  │  Final DLQ   │
     │  (TTL delay) │  │ (manual insp) │  │  (alerting)  │
     └──────┬───────┘  └──────────────┘  └──────────────┘
            │ x-dead-letter-exchange → primary queue
            │ (after TTL expires)
            ▼
     ┌──────────────┐
     │ Back to      │
     │ Primary Queue│
     └──────────────┘
```

### 3.2 Retry Policy Design

**Exponential Backoff with Max Retries:**

| Retry # | Delay | Cumulative |
|---------|-------|------------|
| 1 | 5 seconds | 5s |
| 2 | 25 seconds | 30s |
| 3 | 125 seconds | 2m 35s |
| 4 | 625 seconds | ~13m |
| 5 | 3125 seconds | ~1h 5m |

After 5 retries → Park Queue (manual inspection) → Final DLQ after 7 days.

### 3.3 Topology Setup with Retry Infrastructure

**Node.js Implementation:**

```javascript
const RETRY_DELAYS = [5000, 25000, 125000, 625000, 3125000]; // ms
const MAX_RETRIES = RETRY_DELAYS.length;

async function declareDLXTopology(channel) {
  // --- Dead Letter Exchange ---
  await channel.assertExchange('dlx.topic', 'topic', {
    durable: true,
    autoDelete: false,
  });

  // --- Retry Queues (one per delay level) ---
  for (let level = 0; level < MAX_RETRIES; level++) {
    const retryQueueName = `retry.level-${level}.q`;
    await channel.assertQueue(retryQueueName, {
      durable: true,
      arguments: {
        'x-dead-letter-exchange': 'events.topic',       // back to primary exchange
        'x-dead-letter-routing-key': 'order.created',    // original routing key
        'x-message-ttl': RETRY_DELAYS[level],
      },
    });
    await channel.bindQueue(retryQueueName, 'dlx.topic', `retry.level-${level}`);
  }

  // --- Park Queue (manual intervention) ---
  await channel.assertQueue('park.q', {
    durable: true,
    arguments: {
      'x-dead-letter-exchange': 'dlx.topic',
      'x-dead-letter-routing-key': 'park',
    },
  });
  await channel.bindQueue('park.q', 'dlx.topic', 'park');

  // --- Final DLQ (alert on messages here) ---
  await channel.assertQueue('final.dlq', {
    durable: true,
  });
  await channel.bindQueue('final.dlq', 'dlx.topic', 'final');
}
```

### 3.4 Consumer with Retry Logic

**Node.js — Consumer with Nack + Retry Header:**

```javascript
async function consumeWithRetry(channel, queueName) {
  await channel.prefetch(10); // fair dispatch, backpressure

  await channel.consume(queueName, async (msg) => {
    if (!msg) return;

    const retryCount = (msg.properties.headers?.['x-retry-count'] || 0);
    const messageId = msg.properties.messageId;

    try {
      await processMessage(msg); // your business logic

      // Success — acknowledge
      channel.ack(msg);
      console.log(`[OK] ${messageId} processed`);

    } catch (error) {
      console.error(`[FAIL] ${messageId} attempt ${retryCount + 1}: ${error.message}`);

      if (retryCount < MAX_RETRIES) {
        // Route to next retry level
        const nextLevel = retryCount;
        const retryRoutingKey = `retry.level-${nextLevel}`;

        channel.publish('dlx.topic', retryRoutingKey, msg.content, {
          persistent: true,
          messageId: messageId,
          headers: {
            ...msg.properties.headers,
            'x-retry-count': retryCount + 1,
            'x-original-routing-key': msg.fields.routingKey,
            'x-error': error.message,
            'x-last-attempt-at': new Date().toISOString(),
          },
        });

        channel.ack(msg); // acknowledge original (handed off to retry)
      } else {
        // Max retries exceeded → park for manual inspection
        channel.publish('dlx.topic', 'park', msg.content, {
          persistent: true,
          messageId: messageId,
          headers: {
            ...msg.properties.headers,
            'x-retry-count': retryCount + 1,
            'x-final-failure': true,
            'x-error': error.message,
            'x-original-routing-key': msg.fields.routingKey,
            'x-last-attempt-at': new Date().toISOString(),
          },
        });

        channel.ack(msg); // acknowledge original (handed off to park)
      }
    }
  }, { noAck: false }); // manual acknowledgements
}
```

**Python — Consumer with Retry Logic:**

```python
import json
import time
from pika import BasicProperties, spec

RETRY_DELAYS = [5_000, 25_000, 125_000, 625_000, 3_125_000]  # ms
MAX_RETRIES = len(RETRY_DELAYS)


def consume_with_retry(channel: pika.channel.Channel, queue_name: str):
    channel.basic_qos(prefetch_count=10)

    def on_message(
        ch: pika.channel.Channel,
        method: spec.Basic.Deliver,
        properties: pika.BasicProperties,
        body: bytes,
    ):
        headers = properties.headers or {}
        retry_count = headers.get('x-retry-count', 0)
        message_id = properties.message_id

        try:
            process_message(body, headers)

            # Success
            ch.basic_ack(delivery_tag=method.delivery_tag)
            print(f"[OK] {message_id} processed")

        except Exception as exc:
            print(f"[FAIL] {message_id} attempt {retry_count + 1}: {exc}")

            if retry_count < MAX_RETRIES:
                # Route to retry queue
                next_level = retry_count
                retry_rk = f'retry.level-{next_level}'

                new_headers = {
                    **headers,
                    'x-retry-count': retry_count + 1,
                    'x-original-routing-key': method.routing_key,
                    'x-error': str(exc),
                    'x-last-attempt-at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                }

                ch.basic_publish(
                    exchange='dlx.topic',
                    routing_key=retry_rk,
                    body=body,
                    properties=BasicProperties(
                        persistent=True,
                        message_id=message_id,
                        headers=new_headers,
                    ),
                )
            else:
                # Max retries → park
                new_headers = {
                    **headers,
                    'x-retry-count': retry_count + 1,
                    'x-final-failure': True,
                    'x-error': str(exc),
                    'x-last-attempt-at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                }

                ch.basic_publish(
                    exchange='dlx.topic',
                    routing_key='park',
                    body=body,
                    properties=BasicProperties(
                        persistent=True,
                        message_id=message_id,
                        headers=new_headers,
                    ),
                )

            # Ack original — we've handed it off
            ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue=queue_name, on_message_callback=on_message)
    print(f"[*] Consuming from {queue_name}. Ctrl+C to stop.")
    channel.start_consuming()
```

### 3.5 Park Queue → Final DLQ Flow

Messages in the park queue get a TTL of 7 days. If not manually resolved, they move to the final DLQ which triggers alerts.

```javascript
// Park queue with 7-day TTL → final DLQ
await channel.assertQueue('park.q', {
  durable: true,
  arguments: {
    'x-dead-letter-exchange': 'dlx.topic',
    'x-dead-letter-routing-key': 'final',
    'x-message-ttl': 7 * 24 * 60 * 60 * 1000, // 7 days
  },
});
```

---

## 4. Event-Driven Microservice Communication

### 4.1 Event Schema Standard

Every event MUST conform to this envelope:

```json
{
  "eventId": "evt_01J4XK8N3P2M1Q5R",
  "eventType": "order.created",
  "eventVersion": "1.0",
  "timestamp": "2026-06-26T00:08:00.000Z",
  "correlationId": "corr_01J4XK8N3P2M1Q5R",
  "causationId": "cmd_01J4XK8N2P1M0Q4R",
  "source": {
    "service": "order-service",
    "instance": "order-service-7d8f9-abc12"
  },
  "payload": {
    "orderId": "ord_12345",
    "customerId": "cust_67890",
    "total": { "amount": 9999, "currency": "USD" },
    "items": [
      { "sku": "WIDGET-A", "quantity": 2, "unitPrice": 4999 }
    ]
  }
}
```

### 4.2 Publisher (Outbox Pattern)

The **Outbox Pattern** ensures exactly-one-publish: write the event to an outbox table in the same database transaction as the business data, then a separate process publishes to RabbitMQ.

**Node.js — Outbox Publisher (with PostgreSQL):**

```javascript
const { v4: uuidv4 } = require('uuid');

async function publishEvent(pool, channel, event) {
  const eventId = uuidv4();
  const correlationId = event.correlationId || uuidv4();

  const envelope = {
    eventId,
    eventType: event.type,
    eventVersion: '1.0',
    timestamp: new Date().toISOString(),
    correlationId,
    causationId: event.causationId || null,
    source: {
      service: 'order-service',
      instance: process.env.HOSTNAME || 'unknown',
    },
    payload: event.payload,
  };

  const body = Buffer.from(JSON.stringify(envelope));

  // 1. Write to outbox in DB transaction
  await pool.query(
    `INSERT INTO outbox (event_id, event_type, routing_key, payload, created_at, status)
     VALUES ($1, $2, $3, $4, NOW(), 'pending')`,
    [eventId, event.type, event.routingKey, body]
  );

  // 2. Publish to RabbitMQ (outside the critical DB transaction)
  //    In production, run this via a separate outbox-poller process
  channel.publish('events.topic', event.routingKey, body, {
    persistent: true,
    messageId: eventId,
    contentType: 'application/json',
    headers: {
      'x-correlation-id': correlationId,
      'x-causation-id': envelope.causationId,
      'x-event-type': event.type,
    },
  }, (err) => {
    if (err) {
      console.error(`Publish failed for ${eventId}: ${err.message}`);
      // Outbox poller will retry
    }
  });
}
```

**Python — Outbox Publisher:**

```python
import json
import uuid
from datetime import datetime, timezone
from psycopg2.extras import RealDictCursor
import pika


def publish_event(conn, cursor, channel, event: dict):
    event_id = str(uuid.uuid4())
    correlation_id = event.get('correlation_id') or str(uuid.uuid4())

    envelope = {
        'eventId': event_id,
        'eventType': event['type'],
        'eventVersion': '1.0',
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'correlationId': correlation_id,
        'causationId': event.get('causation_id'),
        'source': {
            'service': 'order-service',
            'instance': 'order-service-1',
        },
        'payload': event['payload'],
    }

    body = json.dumps(envelope).encode('utf-8')

    # 1. Write to outbox (in DB transaction)
    cursor.execute(
        """INSERT INTO outbox (event_id, event_type, routing_key, payload, created_at, status)
           VALUES (%s, %s, %s, %s, NOW(), 'pending')""",
        (event_id, event['type'], event['routing_key'], body),
    )

    # 2. Publish to RabbitMQ
    channel.basic_publish(
        exchange='events.topic',
        routing_key=event['routing_key'],
        body=body,
        properties=pika.BasicProperties(
            persistent=True,
            message_id=event_id,
            content_type='application/json',
            headers={
                'x-correlation-id': correlation_id,
                'x-causation-id': envelope['causationId'],
                'x-event-type': event['type'],
            },
        ),
        mandatory=True,  # Return undeliverable messages
    )
```

### 4.3 Consumer Patterns

#### Pattern A: Competing Consumers (Horizontal Scaling)

Multiple instances of the same service consume from one queue. RabbitMQ round-robins messages.

```
Queue: order-service.q
  Consumer 1 (instance-a) ────┐
  Consumer 2 (instance-b) ────┤  competing consumers
  Consumer 3 (instance-c) ────┘
```

**Key settings:**
- `prefetch = 1` for strict fair dispatch
- `prefetch = 10` for balanced throughput
- Manual acks only

#### Pattern B: Event Choreography (Saga)

Services react to events from other services without a central orchestrator.

```
order.created
  ├──► payment-service: reserves funds → emits payment.reserved
  │       ├──► inventory-service: reserves stock → emits inventory.reserved
  │       │       └──► shipping-service: creates label → emits shipment.created
  │       └──► (on failure) emits payment.failed
  │               └──► order-service: cancels order → emits order.cancelled
  └──► notification-service: sends confirmation email
```

**Node.js — Saga Participant:**

```javascript
// Each service listens and reacts independently
async function paymentService(channel) {
  await channel.consume('payment-service.q', async (msg) => {
    const event = JSON.parse(msg.content.toString());

    try {
      if (event.eventType === 'order.created') {
        const reservation = await reserveFunds(event.payload);

        // Emit success event
        await publishEvent(channel, {
          type: 'payment.reserved',
          routingKey: 'payment.reserved',
          correlationId: event.correlationId,
          causationId: event.eventId,
          payload: { reservationId: reservation.id, orderId: event.payload.orderId },
        });
      }

      if (event.eventType === 'order.cancelled') {
        await releaseFunds(event.payload.orderId);
      }

      channel.ack(msg);
    } catch (error) {
      // Emit compensating event
      await publishEvent(channel, {
        type: 'payment.failed',
        routingKey: 'payment.failed',
        correlationId: event.correlationId,
        causationId: event.eventId,
        payload: { orderId: event.payload.orderId, reason: error.message },
      });
      channel.ack(msg); // don't retry — we've already compensated
    }
  });
}
```

### 4.4 Publisher Confirms (Reliable Publishing)

**Node.js:**

```javascript
async function publishWithConfirm(channel, exchange, routingKey, content) {
  return new Promise((resolve, reject) => {
    channel.publish(exchange, routingKey, content, {
      persistent: true,
      mandatory: true, // return if unroutable
    }, (err) => {
      if (err) return reject(err);
      resolve();
    });
  });
}

// Enable publisher confirms
await channel.confirmSelect();

// Publish and wait for confirm
await publishWithConfirm(channel, 'events.topic', 'order.created', body);
console.log('Message confirmed by broker');
```

**Python:**

```python
def publish_with_confirm(channel, exchange, routing_key, body):
    channel.confirm_delivery()  # enable publisher confirms

    try:
        channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=body,
            properties=pika.BasicProperties(persistent=True),
            mandatory=True,
        )
        print('Message confirmed by broker')
    except pika.exceptions.UnroutableError:
        print('Message was unroutable — no queue bound')
    except pika.exceptions.NackError:
        print('Message was nacked by broker')
```

---

## 5. Idempotency Keys

### 5.1 Design

Idempotency prevents duplicate processing of the same logical event. Every message carries a unique `messageId` (or `eventId`). Consumers use a **processed-keys store** (Redis, database, or in-memory for single-instance) to track what they've already handled.

```
Message arrives
      │
      ▼
┌─────────────────┐
│ Check idempotency│
│ store for key    │
└──────┬──────────┘
       │
  ┌────┴────┐
  │ Found?  │
  └────┬────┘
   YES │     NO
       ▼      ▼
  ┌──────┐  ┌──────────┐
  │ ACK  │  │ Process  │
  │ skip │  │ message  │
  └──────┘  └────┬─────┘
                 │
          ┌──────▼──────┐
          │ Store key   │
          │ (with TTL)  │
          └──────┬──────┘
                 │
                 ▼
              ┌──────┐
              │ ACK  │
              └──────┘
```

### 5.2 Redis-Based Idempotency Store

**Node.js:**

```javascript
const Redis = require('ioredis');
const redis = new Redis();

const IDEMPOTENCY_TTL = 7 * 24 * 60 * 60; // 7 days

class IdempotencyGuard {
  /**
   * Check if a message has already been processed.
   * Returns true if this is a new message (proceed).
   * Returns false if duplicate (skip).
   */
  static async checkAndSet(messageId) {
    // SET NX: only set if the key does not exist
    const result = await redis.set(
      `idempotency:${messageId}`,
      JSON.stringify({
        processedAt: new Date().toISOString(),
        status: 'processing',
      }),
      'EX', IDEMPOTENCY_TTL,
      'NX',   // SET if Not eXists
    );

    return result === 'OK'; // true = new, false = duplicate
  }

  /**
   * Mark processing as complete.
   */
  static async markComplete(messageId) {
    await redis.set(
      `idempotency:${messageId}`,
      JSON.stringify({
        processedAt: new Date().toISOString(),
        status: 'completed',
      }),
      'EX', IDEMPOTENCY_TTL,
      'XX',  // SET if eXists (overwrite only)
    );
  }

  /**
   * Remove key on processing failure (allows retry).
   */
  static async markFailed(messageId) {
    await redis.del(`idempotency:${messageId}`);
  }
}

// Usage in consumer
async function consumerWithIdempotency(channel, queueName) {
  await channel.consume(queueName, async (msg) => {
    const messageId = msg.properties.messageId;
    const eventType = msg.properties.headers?.['x-event-type'];
    const body = JSON.parse(msg.content.toString());

    try {
      // 1. Idempotency check
      const isNew = await IdempotencyGuard.checkAndSet(messageId);
      if (!isNew) {
        console.log(`[DUPLICATE] ${messageId} — skipping`);
        channel.ack(msg);
        return;
      }

      // 2. Process
      await handleEvent(eventType, body);

      // 3. Mark complete
      await IdempotencyGuard.markComplete(messageId);
      channel.ack(msg);

    } catch (error) {
      // 4. Remove idempotency key so retry can re-process
      await IdempotencyGuard.markFailed(messageId);
      // Nack and let retry infrastructure handle it
      channel.nack(msg, false, false); // don't requeue (goes to DLX)
    }
  });
}
```

**Python:**

```python
import json
import redis.asyncio as aioredis
from datetime import datetime, timezone

IDEMPOTENCY_TTL = 7 * 24 * 60 * 60  # 7 days


class IdempotencyGuard:
    def __init__(self, redis_client: aioredis.Redis):
        self.redis = redis_client

    async def check_and_set(self, message_id: str) -> bool:
        """Returns True if this is a new message."""
        key = f'idempotency:{message_id}'
        value = json.dumps({
            'processedAt': datetime.now(timezone.utc).isoformat(),
            'status': 'processing',
        })
        # SET NX EX: only set if not exists, with TTL
        result = await self.redis.set(key, value, ex=IDEMPOTENCY_TTL, nx=True)
        return result is True

    async def mark_complete(self, message_id: str):
        key = f'idempotency:{message_id}'
        value = json.dumps({
            'processedAt': datetime.now(timezone.utc).isoformat(),
            'status': 'completed',
        })
        await self.redis.set(key, value, ex=IDEMPOTENCY_TTL, xx=True)

    async def mark_failed(self, message_id: str):
        key = f'idempotency:{message_id}'
        await self.redis.delete(key)


# Usage in consumer callback (async)
async def on_message(
    ch, method, properties, body,
    idem_guard: IdempotencyGuard,
):
    message_id = properties.message_id
    event_type = properties.headers.get('x-event-type') if properties.headers else None

    try:
        is_new = await idem_guard.check_and_set(message_id)
        if not is_new:
            print(f'[DUPLICATE] {message_id} — skipping')
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        await handle_event(event_type, json.loads(body))

        await idem_guard.mark_complete(message_id)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception:
        await idem_guard.mark_failed(message_id)
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
```

### 5.3 Database-Based Idempotency (for DB-centric services)

For services already using PostgreSQL, idempotency can live alongside business data:

```sql
CREATE TABLE idempotency_keys (
    message_id      VARCHAR(255) PRIMARY KEY,
    status          VARCHAR(50) NOT NULL DEFAULT 'processing',
    processed_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    expires_at      TIMESTAMPTZ NOT NULL DEFAULT NOW() + INTERVAL '7 days'
);

CREATE INDEX idx_idempotency_expires ON idempotency_keys (expires_at)
    WHERE status = 'completed';
```

**Node.js (PostgreSQL):**

```javascript
async function checkAndInsertIdempotencyKey(pool, messageId) {
  try {
    await pool.query(
      `INSERT INTO idempotency_keys (message_id, status)
       VALUES ($1, 'processing')
       ON CONFLICT (message_id) DO NOTHING`,
      [messageId]
    );
    return pool.query(
      `SELECT status FROM idempotency_keys WHERE message_id = $1`,
      [messageId]
    ).then(r => r.rows[0]?.status === 'processing');
  } catch {
    return false;
  }
}
```

---

## 6. Message Ordering Guarantees

### 6.1 Ordering Model

RabbitMQ guarantees ordering **within a single queue** when:
- Single consumer (no competing consumers)
- No requeues (nack with requeue=true breaks ordering)
- Single channel publishes in order

For multi-consumer scenarios, use **partitioned ordering**.

### 6.2 Partitioned Ordering (Consistent Hashing Exchange)

Use the `x-consistent-hash` exchange to route messages for the same entity (e.g., `orderId`) to the same queue partition, preserving order per entity.

```
Exchange: events.hash (type: x-consistent-hash)

Property to hash on: message_id or custom header
  hash-header: x-partition-key

Queues (partitioned):
  partition-0.q   ← messages where hash(orderId) % 3 == 0
  partition-1.q   ← messages where hash(orderId) % 3 == 1
  partition-2.q   ← messages where hash(orderId) % 3 == 2
```

**Enable consistent hash exchange plugin first:**

```bash
rabbitmq-plugins enable rabbitmq_consistent_hash_exchange
```

**Topology Declaration (Node.js):**

```javascript
const PARTITION_COUNT = 3;

async function declarePartitionedTopology(channel) {
  // Consistent hash exchange
  await channel.assertExchange('events.hash', 'x-consistent-hash', {
    durable: true,
    autoDelete: false,
    arguments: { 'hash-header': 'x-partition-key' },
  });

  for (let i = 0; i < PARTITION_COUNT; i++) {
    const qName = `partition-${i}.q`;
    await channel.assertQueue(qName, { durable: true });
    await channel.bindQueue(qName, 'events.hash', '1'); // weight=1
  }
}

// Publishing with partition key
function publishPartitioned(channel, event, partitionKey) {
  const body = Buffer.from(JSON.stringify(event));
  channel.publish('events.hash', '', body, {
    persistent: true,
    messageId: event.eventId,
    headers: {
      'x-partition-key': partitionKey, // e.g., orderId
    },
  });
}
```

**Topology Declaration (Python):**

```python
PARTITION_COUNT = 3

def declare_partitioned_topology(channel):
    channel.exchange_declare(
        exchange='events.hash',
        exchange_type='x-consistent-hash',
        durable=True,
        auto_delete=False,
        arguments={'hash-header': 'x-partition-key'},
    )

    for i in range(PARTITION_COUNT):
        q_name = f'partition-{i}.q'
        channel.queue_declare(queue=q_name, durable=True)
        channel.queue_bind(
            queue=q_name,
            exchange='events.hash',
            routing_key='1',  # weight
        )


def publish_partitioned(channel, event: dict, partition_key: str):
    body = json.dumps(event).encode('utf-8')
    channel.basic_publish(
        exchange='events.hash',
        routing_key='',
        body=body,
        properties=pika.BasicProperties(
            persistent=True,
            message_id=event['eventId'],
            headers={'x-partition-key': partition_key},
        ),
    )
```

### 6.3 Ordering Guarantees Summary

| Scenario | Guarantee | Mechanism |
|---|---|---|
| Single queue, single consumer | Strict FIFO | Default RabbitMQ behavior |
| Single queue, competing consumers | No ordering | N/A — messages distributed round-robin |
| Partitioned (hash exchange) | Per-partition ordering | Consistent hash routing |
| Single queue with requeue | Ordering broken | Use DLX retry instead of requeue |
| Across multiple exchanges | No ordering | Use timestamps + sequence numbers in app logic |

### 6.4 Application-Level Sequence Numbers

For cases where order matters across partitions, embed a monotonic sequence number per entity:

```json
{
  "eventId": "evt_abc123",
  "eventType": "order.status-changed",
  "payload": {
    "orderId": "ord_12345",
    "status": "shipped",
    "sequenceNumber": 5
  }
}
```

**Consumer reorder buffer (Node.js):**

```javascript
class ReorderBuffer {
  constructor() {
    this.buffers = new Map(); // orderId → Map<seqNum, message>
    this.nextExpected = new Map(); // orderId → nextSeqNum
    this.timeout = 30_000; // 30s max wait for missing sequence
  }

  ingest(orderId, seqNum, message, callback) {
    // Initialize tracking if first message
    if (!this.nextExpected.has(orderId)) {
      this.nextExpected.set(orderId, seqNum);
    }
    if (!this.buffers.has(orderId)) {
      this.buffers.set(orderId, new Map());
    }

    const buffer = this.buffers.get(orderId);
    buffer.set(seqNum, { message, receivedAt: Date.now() });

    // Try to drain in-order
    this.drain(orderId, callback);
  }

  drain(orderId, callback) {
    const buffer = this.buffers.get(orderId);
    let next = this.nextExpected.get(orderId);

    while (buffer.has(next)) {
      const entry = buffer.get(next);
      callback(entry.message);
      buffer.delete(next);
      next++;
      this.nextExpected.set(orderId, next);
    }

    // Clean up stale gaps
    const now = Date.now();
    for (const [seq, entry] of buffer) {
      if (now - entry.receivedAt > this.timeout) {
        // Force deliver to avoid blocking forever
        callback(entry.message);
        buffer.delete(seq);
        this.nextExpected.set(orderId, seq + 1);
      }
    }
  }
}
```

---

## 7. Full Reference Implementation

### 7.1 Complete Connection Manager

**Node.js — `MessageBroker.js`:**

```javascript
const amqp = require('amqplib');
const { v4: uuidv4 } = require('uuid');

class MessageBroker {
  constructor(url = 'amqp://localhost') {
    this.url = url;
    this.connection = null;
    this.channel = null;
    this.reconnectDelay = 1000;
    this.maxReconnectDelay = 30000;
    this.isShuttingDown = false;
  }

  async connect() {
    while (!this.isShuttingDown) {
      try {
        this.connection = await amqp.connect(this.url);
        this.channel = await this.connection.createConfirmChannel();
        this.reconnectDelay = 1000; // reset

        this.connection.on('close', (err) => {
          console.error(`Connection closed: ${err?.message}`);
          if (!this.isShuttingDown) this.reconnect();
        });

        this.connection.on('error', (err) => {
          console.error(`Connection error: ${err.message}`);
        });

        console.log('[Broker] Connected to RabbitMQ');
        return;
      } catch (err) {
        console.error(`Connect failed: ${err.message}. Retrying in ${this.reconnectDelay}ms...`);
        await this.sleep(this.reconnectDelay);
        this.reconnectDelay = Math.min(this.reconnectDelay * 2, this.maxReconnectDelay);
      }
    }
  }

  reconnect() {
    setTimeout(() => this.connect(), this.reconnectDelay);
  }

  async publish(exchange, routingKey, event, options = {}) {
    const messageId = options.messageId || uuidv4();
    const body = Buffer.from(JSON.stringify(event));

    return new Promise((resolve, reject) => {
      this.channel.publish(exchange, routingKey, body, {
        persistent: true,
        messageId,
        contentType: 'application/json',
        headers: options.headers || {},
        mandatory: options.mandatory || false,
        ...options,
      }, (err) => {
        if (err) return reject(err);
        resolve(messageId);
      });
    });
  }

  async consume(queueName, handler, { prefetch = 10 } = {}) {
    await this.channel.prefetch(prefetch);

    await this.channel.consume(queueName, async (msg) => {
      if (!msg) return;
      try {
        await handler(msg);
      } catch (err) {
        console.error(`Unhandled consumer error: ${err.message}`);
        this.channel.nack(msg, false, false);
      }
    }, { noAck: false });
  }

  async shutdown() {
    this.isShuttingDown = true;
    if (this.channel) await this.channel.close();
    if (this.connection) await this.connection.close();
  }

  sleep(ms) {
    return new Promise((res) => setTimeout(res, ms));
  }
}

module.exports = { MessageBroker };
```

**Python — `message_broker.py`:**

```python
import json
import uuid
import time
import pika
from pika.exchange_type import ExchangeType
from typing import Callable, Optional


class MessageBroker:
    def __init__(self, url: str = 'amqp://localhost'):
        self.url = url
        self.connection: Optional[pika.BlockingConnection] = None
        self.channel: Optional[pika.channel.Channel] = None
        self._reconnect_delay = 1.0
        self._max_reconnect_delay = 30.0
        self._shutting_down = False

    def connect(self):
        while not self._shutting_down:
            try:
                self.connection = pika.BlockingConnection(
                    pika.URLParameters(self.url)
                )
                self.channel = self.connection.channel()
                self.channel.confirm_delivery()
                self._reconnect_delay = 1.0
                print('[Broker] Connected to RabbitMQ')
                return
            except pika.exceptions.AMQPConnectionError as exc:
                print(f'Connect failed: {exc}. Retrying in {self._reconnect_delay}s...')
                time.sleep(self._reconnect_delay)
                self._reconnect_delay = min(
                    self._reconnect_delay * 2, self._max_reconnect_delay
                )

    def publish(
        self,
        exchange: str,
        routing_key: str,
        event: dict,
        headers: Optional[dict] = None,
        message_id: Optional[str] = None,
    ) -> str:
        message_id = message_id or str(uuid.uuid4())
        body = json.dumps(event).encode('utf-8')

        self.channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=body,
            properties=pika.BasicProperties(
                persistent=True,
                message_id=message_id,
                content_type='application/json',
                headers=headers or {},
            ),
            mandatory=True,
        )
        return message_id

    def consume(
        self,
        queue_name: str,
        callback: Callable,
        prefetch: int = 10,
    ):
        self.channel.basic_qos(prefetch_count=prefetch)

        def _on_message(ch, method, properties, body):
            try:
                callback(ch, method, properties, body)
            except Exception as exc:
                print(f'Unhandled consumer error: {exc}')
                ch.basic_nack(
                    delivery_tag=method.delivery_tag,
                    requeue=False,
                )

        self.channel.basic_consume(
            queue=queue_name,
            on_message_callback=_on_message,
        )
        print(f'[*] Consuming from {queue_name}. Ctrl+C to stop.')
        self.channel.start_consuming()

    def shutdown(self):
        self._shutting_down = True
        if self.connection and self.connection.is_open:
            self.connection.close()
```

### 7.2 `docker-compose.yml` — Local Development Stack

```yaml
version: '3.9'

services:
  rabbitmq:
    image: rabbitmq:3.13-management-alpine
    container_name: rabbitmq
    ports:
      - '5672:5672'    # AMQP
      - '15672:15672'  # Management UI
    environment:
      RABBITMQ_DEFAULT_USER: admin
      RABBITMQ_DEFAULT_PASS: admin
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq
      - ./rabbitmq/enabled_plugins:/etc/rabbitmq/enabled_plugins
    healthcheck:
      test: ['CMD', 'rabbitmq-diagnostics', '-q', 'ping']
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: redis
    ports:
      - '6379:6379'
    healthcheck:
      test: ['CMD', 'redis-cli', 'ping']
      interval: 5s
      timeout: 3s
      retries: 5

volumes:
  rabbitmq_data:
```

**`rabbitmq/enabled_plugins`:**

```
[rabbitmq_management,rabbitmq_consistent_hash_exchange,rabbitmq_shovel,rabbitmq_shovel_management].
```

### 7.3 Monitoring & Operations

#### Critical Metrics to Monitor

| Metric | RabbitMQ Source | Alert Threshold |
|---|---|---|
| Queue depth | `queue_totals.messages` | > 10,000 (per queue) |
| Message age | `queue_totals.message_bytes` / rate | > 5 minutes oldest |
| Consumer count | `consumers` | == 0 for critical queues |
| Unacknowledged messages | `messages_unacknowledged` | > prefetch * 2 |
| DLQ depth | `final.dlq` messages | > 0 |
| Connection churn | connections opened/min | > 10/min |
| Memory/disk alarm | node health | any alarm triggered |

#### Alerting on Final DLQ

```javascript
// Simple health check endpoint that monitors DLQ depth
async function getFinalDLQDepth(channel) {
  const q = await channel.checkQueue('final.dlq');
  return q.messageCount;
}

// Expose via /health endpoint
app.get('/health/dlq', async (req, res) => {
  const dlqDepth = await getFinalDLQDepth(channel);
  res.json({
    status: dlqDepth === 0 ? 'healthy' : 'degraded',
    finalDlqDepth: dlqDepth,
  });
});
```

### 7.4 Idempotent Event Handler (Complete Example)

**Node.js — Full consumer with all patterns combined:**

```javascript
const { MessageBroker } = require('./MessageBroker');
const IdempotencyGuard = require('./IdempotencyGuard');

async function startOrderService() {
  const broker = new MessageBroker('amqp://admin:admin@localhost');
  await broker.connect();
  await declareTopology(broker.channel);

  await broker.consume('order-service.q', async (msg) => {
    const messageId = msg.properties.messageId;
    const event = JSON.parse(msg.content.toString());
    const retryCount = msg.properties.headers?.['x-retry-count'] || 0;

    try {
      // 1. Idempotency check
      const isNew = await IdempotencyGuard.checkAndSet(messageId);
      if (!isNew) {
        broker.channel.ack(msg);
        return;
      }

      // 2. Process based on event type
      switch (event.eventType) {
        case 'order.created':
          await handleOrderCreated(event.payload);
          break;
        case 'payment.reserved':
          await handlePaymentReserved(event.payload);
          break;
        default:
          console.log(`Unhandled event type: ${event.eventType}`);
      }

      // 3. Success
      await IdempotencyGuard.markComplete(messageId);
      broker.channel.ack(msg);

    } catch (error) {
      // 4. Failure → retry or park
      await IdempotencyGuard.markFailed(messageId);

      if (retryCount < MAX_RETRIES) {
        const nextLevel = retryCount;
        broker.channel.publish('dlx.topic', `retry.level-${nextLevel}`, msg.content, {
          persistent: true,
          messageId,
          headers: {
            ...msg.properties.headers,
            'x-retry-count': retryCount + 1,
            'x-error': error.message,
          },
        });
      } else {
        broker.channel.publish('dlx.topic', 'park', msg.content, {
          persistent: true,
          messageId,
          headers: {
            ...msg.properties.headers,
            'x-retry-count': retryCount + 1,
            'x-final-failure': true,
            'x-error': error.message,
          },
        });
      }

      broker.channel.ack(msg);
    }
  });
}
```

### 7.5 Testing: Simulating Message Flows

**Integration test (Node.js + mocha):**

```javascript
const { expect } = require('chai');
const amqp = require('amqplib');

describe('Message Queue Integration', () => {
  let connection, channel;

  before(async () => {
    connection = await amqp.connect('amqp://localhost');
    channel = await connection.createChannel();
  });

  after(async () => {
    await channel.close();
    await connection.close();
  });

  it('should route order.created to order-service queue', async () => {
    const testBody = { eventId: 'test-1', eventType: 'order.created', payload: {} };

    await channel.publish(
      'events.topic',
      'order.created',
      Buffer.from(JSON.stringify(testBody)),
      { persistent: true, messageId: 'test-1' }
    );

    // Give it a moment to route
    await new Promise(r => setTimeout(r, 500));

    const q = await channel.checkQueue('order-service.q');
    expect(q.messageCount).to.be.at.least(1);

    // Cleanup: purge the queue
    await channel.purgeQueue('order-service.q');
  });

  it('should move failed messages to retry queue', async () => {
    // Publish a message that will fail, verify it lands in retry.level-0.q
    // ...
  });
});
```

---

## Appendix A: Quick Reference — Exchange Types

| Exchange Type | Routing Logic | Use Case |
|---|---|---|
| **direct** | Exact match on routing key | Point-to-point commands, RPC |
| **topic** | Pattern match (`*` = one word, `#` = zero+ words) | Event routing by type |
| **fanout** | Broadcast to all bound queues | Cache invalidation, config changes |
| **headers** | Match on message headers (`x-match: all`/`any`) | Multi-attribute routing |
| **x-consistent-hash** | Hash on header/routing key | Partitioned ordering |
| **x-delayed-message** | Delayed delivery by header `x-delay` | Scheduled/delayed processing |
| **default** (nameless) | Queue name = routing key | Legacy / simple queueing |

## Appendix B: Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|---|---|---|
| `requeue=true` on nack | Breaks ordering, infinite loops | Use DLX + retry queues |
| `noAck: true` everywhere | Lost messages on crash | Use manual acks |
| Single queue for all events | Coupling, scaling issues | Topic exchange + dedicated queues |
| No message TTL on retry queues | Infinite retry loops | Always set `x-message-ttl` |
| Ignoring publisher confirms | Lost messages | Always use confirm channel |
| Large prefetch with slow consumer | Starves other consumers | `prefetch=1` for fair, `prefetch=10-50` for balanced |
| DB + queue without outbox pattern | Dual-write inconsistency | Outbox table or transactional outbox |
| No idempotency | Duplicate processing | Idempotency keys with Redis/DB |
| Hardcoding queue names | Inflexibility | Configuration-driven topology |

---

*End of Architecture Document*
