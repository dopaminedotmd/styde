# Message Queue Architecture: Kafka Streams & Advanced Messaging (C2)

**Document Version:** 2.0  
**Date:** 2026-06-26  
**Author:** Message Queue Architect (Styde Forge)  
**Target Stack:** Apache Kafka 3.7+ · Kafka Streams 3.7 · Confluent Schema Registry 7.6 · Avro 1.11  
**Focus:** Kafka Streams for real-time processing · Exactly-once semantics · Schema Registry with Avro · Dead letter topic patterns · Message replay strategies

---

## Table of Contents

1. [Architecture Overview & Kafka Fundamentals](#1-architecture-overview--kafka-fundamentals)
2. [Kafka Streams for Real-Time Processing](#2-kafka-streams-for-real-time-processing)
3. [Exactly-Once Semantics](#3-exactly-once-semantics)
4. [Schema Registry & Avro Serialization](#4-schema-registry--avro-serialization)
5. [Dead Letter Topic Patterns](#5-dead-letter-topic-patterns)
6. [Message Replay Strategies](#6-message-replay-strategies)
7. [Full Reference Implementation](#7-full-reference-implementation)
8. [Production Operations & Monitoring](#8-production-operations--monitoring)

---

## 1. Architecture Overview & Kafka Fundamentals

### 1.1 When to Choose Kafka (vs RabbitMQ)

| Concern | Kafka | RabbitMQ |
|---|---|---|
| **Throughput** | Millions of messages/sec per broker | ~50K messages/sec |
| **Persistence** | Immutable append-only log, configurable retention | Message deleted after consumption |
| **Replay** | Native — reset consumer offsets | Requires custom dead-letter/retry infrastructure |
| **Ordering** | Strictly ordered within a partition | Per-queue FIFO (breaks on nack/requeue) |
| **Processing Model** | Stream processing (Kafka Streams, ksqlDB, Flink) | Individual message consumers |
| **Delivery Semantics** | At-most-once, at-least-once, exactly-once | At-most-once, at-least-once |
| **Consumer Scaling** | Partition-level parallelism (1 consumer per partition max) | Competing consumers on single queue |
| **Operational Complexity** | High — ZooKeeper/KRaft, partition management | Moderate — single broker easy, clustering harder |

### 1.2 Core Kafka Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         APACHE KAFKA CLUSTER                             │
│                                                                         │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐      │
│  │   Broker 1       │  │   Broker 2       │  │   Broker 3       │      │
│  │   ┌───────────┐  │  │   ┌───────────┐  │  │   ┌───────────┐  │      │
│  │   │ Topic A   │  │  │   │ Topic A   │  │  │   │ Topic A   │  │      │
│  │   │  P0 (L)   │  │  │   │  P1 (L)   │  │  │   │  P2 (F)   │  │      │
│  │   │  P3 (F)   │  │  │   │  P2 (F)   │  │  │   │  P0 (F)   │  │      │
│  │   └───────────┘  │  │   └───────────┘  │  │   └───────────┘  │      │
│  │   ┌───────────┐  │  │   ┌───────────┐  │  │   ┌───────────┐  │      │
│  │   │ Topic B   │  │  │   │ Topic B   │  │  │   │ Topic B   │  │      │
│  │   │  P0 (L)   │  │  │   │  P1 (F)   │  │  │   │  P0 (F)   │  │      │
│  │   └───────────┘  │  │   └───────────┘  │  │   └───────────┘  │      │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘      │
│       L = Leader          F = Follower (ISR)                             │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────┐       │
│  │                     CONTROLLER (KRaft)                         │       │
│  │  Metadata quorum · Leader election · Partition assignment      │       │
│  └──────────────────────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────────────────────┘
         │                        │                        │
    ┌────▼────┐             ┌────▼────┐             ┌────▼────┐
    │Producer │             │Consumer │             │ Streams │
    │  Apps   │             │ Groups  │             │  Apps   │
    └─────────┘             └─────────┘             └─────────┘
```

### 1.3 Topic & Partition Design

```
Topic: orders
Partitions: 6
Replication Factor: 3

  Partition 0 ─── Broker 1 (Leader), Broker 2, Broker 3
  Partition 1 ─── Broker 2 (Leader), Broker 3, Broker 1
  Partition 2 ─── Broker 3 (Leader), Broker 1, Broker 2
  Partition 3 ─── Broker 1 (Leader), Broker 2, Broker 3
  Partition 4 ─── Broker 2 (Leader), Broker 3, Broker 1
  Partition 5 ─── Broker 3 (Leader), Broker 1, Broker 2

Partitioning Strategy:
  orders with key = customer_id  → hash(customer_id) % 6
  orders with key = null         → round-robin (sticky in 2.4+)

Retention Policy:
  retention.ms = 604800000      (7 days)
  retention.bytes = 107374182400 (100 GB per partition)
  cleanup.policy = delete        (or compact for changelog topics)
```

### 1.4 Producer & Consumer Guarantees

```
Producer Configuration:

  acks=all                       ← All in-sync replicas must acknowledge
  enable.idempotence=true        ← Deduplication within producer session
  max.in.flight.requests.per.connection=5  ← Safe with idempotence
  transactional.id=order-prod-01 ← Exactly-once for multi-partition writes

Consumer Configuration:

  enable.auto.commit=false       ← Manual offset management
  isolation.level=read_committed ← Only read committed (transactional) messages
  group.instance.id=consumer-01  ← Static group membership
  max.poll.records=500           ← Batch size control
  max.poll.interval.ms=300000    ← Heartbeat timeout (5 min)
```

---

## 2. Kafka Streams for Real-Time Processing

### 2.1 Streams Topology Model

Kafka Streams is a **Java/Scala library** (not a separate cluster) for building real-time stream processing applications. It uses a **processor topology** DAG.

```
                  SOURCE                       PROCESSOR                    SINK
              ┌──────────────┐            ┌──────────────┐           ┌──────────────┐
  orders ────►│ Source:      │───┐   ┌───►│ Transform:   │───┐  ┌───►│ Sink:        │
              │ orders-topic │   │   │    │ enrich+filter│   │  │    │ valid-orders │
              └──────────────┘   │   │    └──────────────┘   │  │    └──────────────┘
                                 │   │                       │  │
              ┌──────────────┐   │   │    ┌──────────────┐   │  │    ┌──────────────┐
  customers ─►│ Source:      │───┼───┼───►│ Join:        │───┼──┼───►│ Sink:        │
              │ customers    │   │       │ orders+cust   │   │      │ enriched     │
              │ (GlobalKTable)│  │       └──────────────┘   │      │ -orders      │
              └──────────────┘   │                          │      └──────────────┘
                                 │       ┌──────────────┐   │
                                 └──────►│ Branch:      │───┘
                                         │ high-value   │───► high-value-orders
                                         │ low-value    │───► low-value-orders
                                         └──────────────┘

State Stores (local RocksDB):
  - order-counts-store       (windowed aggregation)
  - customer-last-order      (key-value state)
```

### 2.2 Kafka Streams DSL — Complete Topology

```java
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.*;
import org.apache.kafka.streams.kstream.*;
import org.apache.kafka.streams.state.*;
import java.time.Duration;
import java.util.Properties;

public class OrderProcessingTopology {

    public static Topology build() {
        StreamsBuilder builder = new StreamsBuilder();

        // ── Source Streams ──────────────────────────────────────────
        KStream<String, Order> orders = builder.stream(
            "orders",
            Consumed.with(Serdes.String(), orderSerde)
                .withTimestampExtractor(new OrderTimestampExtractor())
        );

        GlobalKTable<String, Customer> customers = builder.globalTable(
            "customers",
            Consumed.with(Serdes.String(), customerSerde),
            Materialized.<String, Customer, KeyValueStore<Bytes, byte[]>>as("customers-store")
        );

        // ── Filter: Remove invalid/corrupted orders ──────────────────
        KStream<String, Order> validOrders = orders
            .filter((orderId, order) -> order != null && order.isValid())
            .filterNot((orderId, order) -> order.getAmount().signum() <= 0);

        // ── Branch: Split by order value ─────────────────────────────
        BranchedKStream<String, Order> branched = validOrders.split(Named.as("order-"))
            .branch(
                (orderId, order) -> order.getAmount().compareTo(new BigDecimal("1000")) >= 0,
                Branched.as("high-value")
            )
            .branch(
                (orderId, order) -> order.getAmount().compareTo(new BigDecimal("1000")) < 0,
                Branched.as("low-value")
            );

        // High-value → immediate processing
        branched.get("order-high-value").to(
            "high-value-orders",
            Produced.with(Serdes.String(), orderSerde)
        );

        // ── Enrich: Join orders with customer data ──────────────────
        KStream<String, EnrichedOrder> enriched = validOrders.join(
            customers,
            (orderId, order) -> order.getCustomerId(),  // foreign key extractor
            (order, customer) -> EnrichedOrder.from(order, customer)
        );

        // ── Aggregation: 5-minute tumbling window order counts ───────
        TimeWindows windows = TimeWindows
            .ofSizeAndGrace(Duration.ofMinutes(5), Duration.ofSeconds(30));

        KTable<Windowed<String>, Long> orderCounts = enriched
            .groupBy(
                (orderId, enrichedOrder) -> enrichedOrder.getCustomerId(),
                Grouped.with(Serdes.String(), enrichedOrderSerde)
            )
            .windowedBy(windows)
            .count(Materialized.<String, Long, WindowStore<Bytes, byte[]>>as(
                "order-counts-window"
            ).withRetention(Duration.ofHours(6)));

        // ── Suppress: Only emit final window results ────────────────
        orderCounts
            .suppress(Suppressed.untilWindowCloses(
                Suppressed.BufferConfig.unbounded()
            ))
            .toStream()
            .to("order-counts-by-customer",
                Produced.with(
                    WindowedSerdes.timeWindowedSerdeFrom(String.class),
                    Serdes.Long()
                )
            );

        // ── Map + Transform: Derived metrics ──────────────────────
        enriched
            .mapValues(EnrichedOrder::toOrderEvent)
            .transform(OrderFraudDetector::new, "fraud-detector-store")
            .filter((key, event) -> event.isSuspicious())
            .to("fraud-alerts", Produced.with(Serdes.String(), orderEventSerde));

        // ── Dead Letter Branch ─────────────────────────────────────
        orders
            .filter((orderId, order) -> order == null || !order.isValid())
            .mapValues(order -> order == null
                ? DeadLetter.invalid("null order", "orders")
                : DeadLetter.invalid(order.getValidationErrors(), "orders"))
            .to("orders.dlq", Produced.with(Serdes.String(), deadLetterSerde));

        // ── Sink: Enriched orders to target topic ──────────────────
        enriched.to(
            "enriched-orders",
            Produced.with(Serdes.String(), enrichedOrderSerde)
        );

        // ── Low-value orders with windowed deduplication ───────────
        branched.get("order-low-value")
            .transformValues(
                () -> new ValueTransformerWithKey<>() {
                    private KeyValueStore<String, String> store;
                    private ProcessorContext context;

                    @Override
                    public void init(ProcessorContext context) {
                        this.context = context;
                        this.store = context.getStateStore("dedup-store");
                    }

                    @Override
                    public Order transform(String key, Order value) {
                        String seen = store.get(value.getDeduplicationKey());
                        if (seen != null) return null; // duplicate → drop
                        store.put(value.getDeduplicationKey(), key);
                        return value;
                    }

                    @Override
                    public void close() {}
                },
                "dedup-store"
            )
            .filter((key, order) -> order != null)
            .to("low-value-orders", Produced.with(Serdes.String(), orderSerde));

        return builder.build();
    }
}
```

### 2.3 Kafka Streams Configuration

```java
public class StreamsApp {

    public static void main(String[] args) {
        Properties props = new Properties();
        props.put(StreamsConfig.APPLICATION_ID_CONFIG, "order-processing-v2");
        props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "kafka1:9092,kafka2:9092,kafka3:9092");
        props.put(StreamsConfig.NUM_STREAM_THREADS_CONFIG, 4); // matches partition count
        props.put(StreamsConfig.REPLICATION_FACTOR_CONFIG, 3);

        // ── Exactly-Once Configuration ──────────────────────────
        props.put(StreamsConfig.PROCESSING_GUARANTEE_CONFIG,
            StreamsConfig.EXACTLY_ONCE_V2);
        props.put(StreamsConfig.TRANSACTION_TIMEOUT_CONFIG, 300_000); // 5 min

        // ── State Store Configuration ───────────────────────────
        props.put(StreamsConfig.STATE_DIR_CONFIG, "/data/kafka-streams/state");
        props.put(StreamsConfig.COMMIT_INTERVAL_MS_CONFIG, 30_000); // 30s
        props.put(StreamsConfig.CACHE_MAX_BYTES_BUFFERING_CONFIG, 10 * 1024 * 1024);

        // ── Fault Tolerance ─────────────────────────────────────
        props.put(StreamsConfig.NUM_STANDBY_REPLICAS_CONFIG, 1);

        // ── Consumer configs (embedded) ─────────────────────────
        props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
        props.put(ConsumerConfig.MAX_POLL_RECORDS_CONFIG, 1000);
        props.put(ConsumerConfig.ISOLATION_LEVEL_CONFIG, "read_committed");

        // ── Producer configs (embedded) ─────────────────────────
        props.put(ProducerConfig.COMPRESSION_TYPE_CONFIG, "zstd");
        props.put(ProducerConfig.LINGER_MS_CONFIG, 5);
        props.put(ProducerConfig.BATCH_SIZE_CONFIG, 32_768);

        Topology topology = OrderProcessingTopology.build();
        KafkaStreams streams = new KafkaStreams(topology, props);

        // ── Clean shutdown ──────────────────────────────────────
        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            streams.close(Duration.ofSeconds(30));
        }));

        // ── State listener ──────────────────────────────────────
        streams.setStateListener((newState, oldState) ->
            System.out.printf("State: %s → %s%n", oldState, newState)
        );

        // ── Uncaught exception handler ──────────────────────────
        streams.setUncaughtExceptionHandler((thread, exception) -> {
            System.err.printf("Thread %s crashed: %s%n", thread.getName(), exception.getMessage());
            // Replace with production alerting
            System.exit(1);
        });

        streams.start();
    }
}
```

### 2.4 Stateful Operations & Interactive Queries

```java
// ── Exposing state stores via REST (Interactive Queries) ─────
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StoreQueryParameters;
import org.apache.kafka.streams.state.*;

public class QueryService {

    private final KafkaStreams streams;

    public QueryService(KafkaStreams streams) {
        this.streams = streams;
    }

    /** Query the windowed order count for a specific customer */
    public Long getOrderCount(String customerId, Instant windowStart) {
        ReadOnlyWindowStore<String, Long> store = streams.store(
            StoreQueryParameters.fromNameAndType(
                "order-counts-window",
                QueryableStoreTypes.windowStore()
            )
        );

        WindowStoreIterator<Long> iterator = store.fetch(
            customerId,
            windowStart,
            windowStart.plus(Duration.ofMinutes(5))
        );

        try (iterator) {
            if (iterator.hasNext()) {
                return iterator.next().value;
            }
        }
        return 0L;
    }

    /** Query the last known state for a customer (KV store) */
    public String getCustomerLastOrder(String customerId) {
        ReadOnlyKeyValueStore<String, String> store = streams.store(
            StoreQueryParameters.fromNameAndType(
                "customer-last-order",
                QueryableStoreTypes.keyValueStore()
            )
        );
        return store.get(customerId);
    }

    /** Check which host owns a partition for routing */
    public HostInfo getHostForKey(String storeName, String key) {
        return streams.queryMetadataForKey(storeName, key, Serdes.String().serializer())
            .activeHost();
    }
}
```

### 2.5 Custom Processor API (Low-Level)

```java
import org.apache.kafka.streams.processor.api.*;

public class OrderFraudDetector
    implements ProcessorSupplier<String, OrderEvent, String, OrderEvent> {

    @Override
    public Processor<String, OrderEvent, String, OrderEvent> get() {
        return new Processor<>() {
            private KeyValueStore<String, OrderState> stateStore;
            private ProcessorContext<String, OrderEvent> context;

            @Override
            @SuppressWarnings("unchecked")
            public void init(ProcessorContext<String, OrderEvent> context) {
                this.context = context;
                this.stateStore = context.getStateStore("fraud-detector-store");
                // Schedule periodic cleanup of stale entries
                context.schedule(
                    Duration.ofMinutes(10),
                    PunctuationType.WALL_CLOCK_TIME,
                    this::cleanupStaleEntries
                );
            }

            @Override
            public void process(Record<String, OrderEvent> record) {
                OrderState previousState = stateStore.get(record.key());

                if (previousState == null) {
                    // First event for this order
                    stateStore.put(record.key(), OrderState.initial(record.value()));
                    return;
                }

                // Detect velocity anomaly: > 5 orders in 1 minute
                if (previousState.isVelocityAnomaly(record.value())) {
                    record.value().setSuspicious(true);
                    record.value().setFraudReason("velocity_anomaly");
                    context.forward(record);
                }

                // Detect location inconsistency
                if (previousState.isLocationMismatch(record.value())) {
                    record.value().setSuspicious(true);
                    record.value().setFraudReason("location_mismatch");
                    context.forward(record);
                }

                // Update state
                previousState.update(record.value());
                stateStore.put(record.key(), previousState);
            }

            private void cleanupStaleEntries(long timestamp) {
                try (KeyValueIterator<String, OrderState> iter = stateStore.all()) {
                    while (iter.hasNext()) {
                        KeyValue<String, OrderState> entry = iter.next();
                        if (entry.value.isStale(timestamp)) {
                            stateStore.delete(entry.key);
                        }
                    }
                }
            }

            @Override
            public void close() {
                // Cleanup resources
            }
        };
    }

    @Override
    public Set<StoreBuilder<?>> stores() {
        return Set.of(
            Stores.keyValueStoreBuilder(
                Stores.persistentKeyValueStore("fraud-detector-store"),
                Serdes.String(),
                orderStateSerde
            )
        );
    }
}
```

---

## 3. Exactly-Once Semantics

### 3.1 Delivery Semantics Spectrum

```
┌──────────────────────────────────────────────────────────────────────┐
│                      DELIVERY GUARANTEE LEVELS                        │
│                                                                      │
│  AT-MOST-ONCE                   AT-LEAST-ONCE         EXACTLY-ONCE  │
│  ┌──────────┐                  ┌──────────┐          ┌──────────┐   │
│  │ Producer │                  │ Producer │          │ Producer │   │
│  │  sends   │                  │  sends   │          │  sends   │   │
│  └────┬─────┘                  └────┬─────┘          └────┬─────┘   │
│       │ fire-and-forget             │ retry until ack       │ tx     │
│       ▼                             ▼                       ▼        │
│  ┌──────────┐                  ┌──────────┐          ┌──────────┐   │
│  │ Kafka    │                  │ Kafka    │          │ Kafka    │   │
│  │ (may     │                  │ (writes  │          │ (atomic  │   │
│  │  lose)   │                  │  may     │          │  write   │   │
│  └──────────┘                  │  dup)    │          │  once)   │   │
│                                └──────────┘          └──────────┘   │
│                                                                      │
│  Producer config:               Producer config:       Producer:     │
│    acks=0                        acks=1 or all           transactional│
│    retries=0                     retries=MAX             .id + initTx│
│                                                          + begin/     │
│  Consumer:                       Consumer:                commit/abort│
│    auto.commit=true              enable.auto.commit                  │
│    (offset committed             =false                Consumer:      │
│     before processing)           (commit after         isolation.level│
│                                  processing)           =read_committed│
│                                          + idempotent │
│                                          consumer     │
└──────────────────────────────────────────────────────────────────────┘
```

### 3.2 Kafka's Exactly-Once Implementation

Kafka achieves exactly-once through **three pillars**:

1. **Idempotent Producer** — deduplicates retries within a producer session
2. **Transactions** — atomic multi-partition writes and consumer offset commits
3. **Read Committed Isolation** — consumers skip aborted transaction markers

```
TRANSACTION LIFECYCLE (Exactly-Once Producer → Consumer):

  PRODUCER                           BROKER                      CONSUMER
  ────────                           ──────                      ────────
  initTransactions() ──────────►  Register transactional.id
                                  Assign producer epoch

  beginTransaction()

  send(partition-0, msg-A) ───►  Append to partition-0
  send(partition-1, msg-B) ───►  Append to partition-1
  sendOffsetsToTransaction(     Append offset commit to
    consumer-group-1 offsets)   __consumer_offsets

  commitTransaction() ────────►  Write COMMIT marker         ─►  Deliver msgs
                                  to all partitions              (isolation.level
                                                                =read_committed)

  ── OR ──

  abortTransaction() ─────────►  Write ABORT marker          ─►  Skip aborted
                                  to all partitions              messages
```

### 3.3 Transactional Producer Implementation

```java
import org.apache.kafka.clients.producer.*;
import org.apache.kafka.common.serialization.StringSerializer;
import java.time.Duration;
import java.util.Properties;

public class TransactionalOrderProducer {

    private final Producer<String, Order> producer;

    public TransactionalOrderProducer(String bootstrapServers) {
        Properties props = new Properties();
        props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
        props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, KafkaAvroSerializer.class);

        // ── Exactly-Once Configuration ─────────────────────────────
        props.put(ProducerConfig.TRANSACTIONAL_ID_CONFIG, "order-producer-01");
        props.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, true);
        props.put(ProducerConfig.ACKS_CONFIG, "all");
        props.put(ProducerConfig.MAX_IN_FLIGHT_REQUESTS_PER_CONNECTION, 5);
        props.put(ProducerConfig.RETRIES_CONFIG, Integer.MAX_VALUE);
        props.put(ProducerConfig.DELIVERY_TIMEOUT_MS_CONFIG, 120_000);

        // ── Schema Registry ────────────────────────────────────────
        props.put(KafkaAvroSerializerConfig.SCHEMA_REGISTRY_URL_CONFIG,
            "http://schema-registry:8081");
        props.put(KafkaAvroSerializerConfig.AUTO_REGISTER_SCHEMAS, false);

        this.producer = new KafkaProducer<>(props);
        this.producer.initTransactions();
    }

    /**
     * Atomically write to multiple topics + commit consumer offsets.
     * Either ALL succeed or ALL roll back.
     */
    public void processWithExactlyOnce(
            ConsumerGroupMetadata consumerGroup,
            Map<TopicPartition, OffsetAndMetadata> offsets,
            OrderMessage message) {

        producer.beginTransaction();

        try {
            // 1. Write to primary topic
            ProducerRecord<String, Order> primaryRecord = new ProducerRecord<>(
                "orders",
                message.getOrderId(),
                message.getOrder()
            );
            producer.send(primaryRecord);

            // 2. Write to audit topic (same transaction)
            ProducerRecord<String, AuditEvent> auditRecord = new ProducerRecord<>(
                "order-audit",
                message.getOrderId(),
                AuditEvent.from(message)
            );
            producer.send(auditRecord);

            // 3. Atomically commit consumer offsets
            producer.sendOffsetsToTransaction(offsets, consumerGroup);

            // 4. Commit the transaction (all-or-nothing)
            producer.commitTransaction();
            System.out.printf("[OK] TX committed for order %s%n", message.getOrderId());

        } catch (ProducerFencedException e) {
            // Fatal — another producer with same transactional.id started
            producer.close();
            throw new RuntimeException("Producer fenced — restart with new epoch", e);

        } catch (KafkaException e) {
            // Abort — nothing is written
            producer.abortTransaction();
            System.err.printf("[ABORT] TX aborted for order %s: %s%n",
                message.getOrderId(), e.getMessage());

            // Retry logic (with idempotency, retries are safe)
            if (isRetryable(e)) {
                processWithExactlyOnce(consumerGroup, offsets, message);
            } else {
                throw e;
            }
        }
    }

    private boolean isRetryable(KafkaException e) {
        return e instanceof TimeoutException
            || e instanceof RetryableException;
    }

    public void close() {
        producer.close(Duration.ofSeconds(30));
    }
}
```

### 3.4 Exactly-Once Consumer & Offset Management

```java
import org.apache.kafka.clients.consumer.*;
import org.apache.kafka.common.TopicPartition;
import java.time.Duration;
import java.util.*;

public class ExactlyOnceOrderConsumer {

    private final KafkaConsumer<String, Order> consumer;
    private final String consumerGroup;

    public ExactlyOnceOrderConsumer(String bootstrapServers, String groupId) {
        this.consumerGroup = groupId;

        Properties props = new Properties();
        props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
        props.put(ConsumerConfig.GROUP_ID_CONFIG, groupId);
        props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
        props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, KafkaAvroDeserializer.class);

        // ── Exactly-Once Consumer Config ─────────────────────────
        props.put(ConsumerConfig.ISOLATION_LEVEL_CONFIG, "read_committed");
        props.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, false);
        props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
        props.put(ConsumerConfig.MAX_POLL_RECORDS_CONFIG, 500);
        props.put(ConsumerConfig.GROUP_INSTANCE_ID_CONFIG, "consumer-01");

        // ── Schema Registry ──────────────────────────────────────
        props.put(KafkaAvroDeserializerConfig.SCHEMA_REGISTRY_URL_CONFIG,
            "http://schema-registry:8081");
        props.put(KafkaAvroDeserializerConfig.SPECIFIC_AVRO_READER_CONFIG, true);

        this.consumer = new KafkaConsumer<>(props);
    }

    public void startConsuming() {
        consumer.subscribe(List.of("orders"));

        while (true) {
            ConsumerRecords<String, Order> records =
                consumer.poll(Duration.ofMillis(500));

            List<ProcessedRecord> processed = new ArrayList<>();

            for (ConsumerRecord<String, Order> record : records) {
                try {
                    // Process the record (idempotent operation)
                    processOrder(record.key(), record.value());

                    processed.add(new ProcessedRecord(record));

                } catch (NonRetryableException e) {
                    // Route to dead letter topic
                    sendToDeadLetter(record, e);
                    processed.add(new ProcessedRecord(record)); // mark as "done"

                } catch (RetryableException e) {
                    // Stop processing this batch; will retry on next poll
                    System.err.printf("Retryable error: %s%n", e.getMessage());
                    break;
                }
            }

            // Commit offsets ONLY for successfully processed records
            if (!processed.isEmpty()) {
                commitProcessedOffsets(processed);
            }
        }
    }

    private void commitProcessedOffsets(List<ProcessedRecord> processed) {
        Map<TopicPartition, OffsetAndMetadata> offsets = new HashMap<>();
        for (ProcessedRecord pr : processed) {
            TopicPartition tp = new TopicPartition(pr.topic, pr.partition);
            long nextOffset = pr.offset + 1;
            offsets.merge(tp,
                new OffsetAndMetadata(nextOffset),
                (existing, incoming) ->
                    existing.offset() > incoming.offset() ? existing : incoming
            );
        }
        consumer.commitSync(offsets);
    }

    // Inner class to track processed records
    private static class ProcessedRecord {
        final String topic;
        final int partition;
        final long offset;
        ProcessedRecord(ConsumerRecord<?, ?> record) {
            this.topic = record.topic();
            this.partition = record.partition();
            this.offset = record.offset();
        }
    }

    private void processOrder(String orderId, Order order)
            throws NonRetryableException, RetryableException {
        // Business logic — must be idempotent
        // Use orderId as idempotency key
    }

    private void sendToDeadLetter(ConsumerRecord<String, Order> record,
                                   Exception error) {
        // See Section 5 — Dead Letter Topic Patterns
    }
}
```

### 3.5 Kafka Streams Exactly-Once (EOS-v2)

```java
// Kafka Streams exactly-once is simpler — just one config flag:

Properties props = new Properties();
props.put(StreamsConfig.PROCESSING_GUARANTEE_CONFIG,
    StreamsConfig.EXACTLY_ONCE_V2);  // ← This is it

// Under the hood, Kafka Streams EOS-v2:
//
// 1. Uses transactional producers for all writes (output topics + changelogs)
// 2. Atomically commits consumer offsets with state store changelog writes
// 3. Uses "read_committed" isolation on all consumer reads
// 4. Does NOT require consumer.sendOffsetsToTransaction() — it's automatic
// 5. Uses "task-level" transactions rather than thread-level (EOS-v1)
//
// EOS-v2 difference from EOS-v1:
//   - EOS-v1: One transaction per thread (all tasks in thread share a TX)
//   - EOS-v2: One transaction per task (finer-grained, better throughput)
//   - EOS-v2 is the default and recommended in Kafka 3.x+
```

### 3.6 Idempotency at the Application Layer

Even with Kafka's exactly-once, **application-level idempotency** is required for true end-to-end exactly-once when external systems are involved.

```java
/**
 * Two-phase idempotency pattern:
 * Phase 1: Kafka + Database in a single transactional scope
 * Phase 2: Deduplication table for external side-effects
 */
public class IdempotentOrderProcessor {

    private final DataSource db;
    private final Map<String, String> processedCache = new LinkedHashMap<>() {
        @Override
        protected boolean removeEldestEntry(Map.Entry<String, String> eldest) {
            return size() > 100_000; // bounded LRU cache
        }
    };

    public void processOrder(String orderId, Order order) {
        // ── Check 1: In-memory LRU dedup ───────────────────────
        if (processedCache.containsKey(orderId)) {
            return; // already processed
        }

        // ── Check 2: Database dedup (survives restarts) ────────
        try (Connection conn = db.getConnection()) {
            conn.setAutoCommit(false);
            try {
                // INSERT ... ON CONFLICT DO NOTHING for idempotency
                PreparedStatement dedup = conn.prepareStatement(
                    "INSERT INTO processed_messages (message_id, processed_at) " +
                    "VALUES (?, NOW()) ON CONFLICT DO NOTHING"
                );
                dedup.setString(1, orderId);
                int inserted = dedup.executeUpdate();

                if (inserted == 0) {
                    // Already processed — skip
                    conn.rollback();
                    processedCache.put(orderId, "");
                    return;
                }

                // Business logic: insert order
                PreparedStatement insert = conn.prepareStatement(
                    "INSERT INTO orders (order_id, customer_id, amount, status) " +
                    "VALUES (?, ?, ?, 'PROCESSING')"
                );
                insert.setString(1, orderId);
                insert.setString(2, order.getCustomerId());
                insert.setBigDecimal(3, order.getAmount());
                insert.executeUpdate();

                conn.commit();
                processedCache.put(orderId, "");

            } catch (SQLException e) {
                conn.rollback();
                throw new RetryableException("DB error", e);
            }
        }
    }
}
```

---

## 4. Schema Registry & Avro Serialization

### 4.1 Why Schema Registry?

```
WITHOUT Schema Registry                    WITH Schema Registry
─────────────────────────                 ──────────────────────
Producer ─► JSON bytes ─► Kafka           Producer ─► Avro bytes ─► Kafka
                                       │
No schema enforcement at broker        │   Producer registers schema
Consumer must know schema implicitly   │   (or auto-registers)
Schema evolution = breaking changes    │
Schema change = coordinated deploy     │   Consumer fetches schema by ID
Payload size = large (JSON text)       │   Schema Registry validates compatibility
                                       │   Schema ID in message header (5 bytes)
                                       │   Forward/backward/Full compatibility
                                       │   Payload size = small (binary)
```

### 4.2 Avro Schema Definitions

#### Order Schema (order.avsc)

```json
{
  "type": "record",
  "name": "Order",
  "namespace": "com.styde.events",
  "doc": "Order event — created when a customer places an order",
  "fields": [
    {"name": "orderId",       "type": "string", "doc": "UUID v4"},
    {"name": "customerId",    "type": "string"},
    {"name": "amount",        "type": {"type": "bytes", "logicalType": "decimal", "precision": 12, "scale": 2}},
    {"name": "currency",      "type": {"type": "enum", "name": "Currency", "symbols": ["USD","EUR","GBP","JPY"]}, "default": "USD"},
    {"name": "items",         "type": {"type": "array", "items": "OrderItem"}},
    {"name": "status",        "type": {"type": "enum", "name": "OrderStatus", "symbols": ["CREATED","CONFIRMED","PAID","SHIPPED","CANCELLED"]}},
    {"name": "shippingAddress","type": ["null", "Address"], "default": null},
    {"name": "createdAt",     "type": {"type": "long", "logicalType": "timestamp-millis"}},
    {"name": "metadata",      "type": {"type": "map", "values": "string"}, "default": {}}
  ]
}
```

#### OrderItem Schema

```json
{
  "type": "record",
  "name": "OrderItem",
  "namespace": "com.styde.events",
  "fields": [
    {"name": "productId",  "type": "string"},
    {"name": "quantity",   "type": "int"},
    {"name": "unitPrice",  "type": {"type": "bytes", "logicalType": "decimal", "precision": 10, "scale": 2}},
    {"name": "discount",   "type": "float", "default": 0.0}
  ]
}
```

#### DeadLetter Schema

```json
{
  "type": "record",
  "name": "DeadLetter",
  "namespace": "com.styde.errors",
  "doc": "Dead letter record for messages that fail processing",
  "fields": [
    {"name": "originalTopic",    "type": "string"},
    {"name": "originalPartition","type": "int"},
    {"name": "originalOffset",   "type": "long"},
    {"name": "originalKey",      "type": ["null", "string"], "default": null},
    {"name": "originalPayload",  "type": "bytes", "doc": "Raw Avro bytes of the failed message"},
    {"name": "errorType",        "type": "string"},
    {"name": "errorMessage",     "type": "string"},
    {"name": "stackTrace",       "type": ["null", "string"], "default": null},
    {"name": "failedAt",         "type": {"type": "long", "logicalType": "timestamp-millis"}},
    {"name": "retryCount",       "type": "int", "default": 0},
    {"name": "headers",          "type": {"type": "map", "values": "string"}, "default": {}}
  ]
}
```

### 4.3 Schema Compatibility Modes

```
Compatibility Modes (set globally or per-subject):

  BACKWARD (default):          New schema can read data written by old schema
                               → Consumers can upgrade first
                               ↓ DELETE fields allowed
                               ↑ ADD optional fields (with default) allowed

  FORWARD:                     Old schema can read data written by new schema
                               → Producers can upgrade first
                               ↓ ADD fields allowed
                               ↑ DELETE optional fields allowed

  FULL:                        Both forward AND backward compatible
                               → Safest — any order upgrade works
                               ↓ Only ADD optional fields with defaults
                               ↓ Only DELETE optional fields with defaults

  BACKWARD_TRANSITIVE:         New schema compatible with ALL previous versions
  FORWARD_TRANSITIVE:          All previous schemas can read new schema
  FULL_TRANSITIVE:             Both transitive — strictest

  NONE:                        No compatibility checks — dangerous!

Recommended for production: FULL or FULL_TRANSITIVE
```

### 4.4 Schema Evolution Examples (Safe Changes)

```json
// V1 Schema
{"name": "OrderCreated", "fields": [
  {"name": "orderId",    "type": "string"},
  {"name": "customerId", "type": "string"},
  {"name": "amount",     "type": "double"}
]}

// V2 — ADD optional field with default (FULL compatible ✅)
{"name": "OrderCreated", "fields": [
  {"name": "orderId",    "type": "string"},
  {"name": "customerId", "type": "string"},
  {"name": "amount",     "type": "double"},
  {"name": "currency",   "type": "string", "default": "USD"}  // ← ADDED
]}

// V3 — ADD optional field to a UNION with null (FULL compatible ✅)
{"name": "OrderCreated", "fields": [
  {"name": "orderId",       "type": "string"},
  {"name": "customerId",    "type": "string"},
  {"name": "amount",        "type": "double"},
  {"name": "currency",      "type": "string", "default": "USD"},
  {"name": "voucherCode",   "type": ["null", "string"], "default": null}  // ← ADDED
]}

// V4 — RENAME a field using ALIASES (FULL compatible ✅)
{"name": "OrderCreated", "fields": [
  {"name": "orderId",    "type": "string"},
  {"name": "userId",     "type": "string", "aliases": ["customerId"]},  // ← RENAMED
  {"name": "amount",     "type": "double"},
  {"name": "currency",   "type": "string", "default": "USD"},
  {"name": "voucherCode","type": ["null", "string"], "default": null}
]}
```

### 4.5 Producer with Schema Registry (Java)

```java
import io.confluent.kafka.serializers.KafkaAvroSerializer;
import io.confluent.kafka.serializers.KafkaAvroSerializerConfig;
import io.confluent.kafka.serializers.subject.TopicRecordNameStrategy;
import org.apache.kafka.clients.producer.*;
import com.styde.events.Order;

public class AvroOrderProducer {

    private final Producer<String, Order> producer;

    public AvroOrderProducer() {
        Properties props = new Properties();
        props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "kafka:9092");
        props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, KafkaAvroSerializer.class);

        // ── Schema Registry Configuration ───────────────────────
        props.put(KafkaAvroSerializerConfig.SCHEMA_REGISTRY_URL_CONFIG,
            "http://schema-registry:8081");
        props.put(KafkaAvroSerializerConfig.AUTO_REGISTER_SCHEMAS, false);
        /*
         * Subject naming strategy options:
         *   TopicNameStrategy      — {topic}-value   (default, per-topic)
         *   RecordNameStrategy     — {record-name}   (per-record-type, shared across topics)
         *   TopicRecordNameStrategy— {topic}-{record-name} (per-topic-per-record-type)
         *
         * Recommended: TopicRecordNameStrategy for multi-type topics
         */
        props.put(KafkaAvroSerializerConfig.VALUE_SUBJECT_NAME_STRATEGY,
            TopicRecordNameStrategy.class.getName());

        this.producer = new KafkaProducer<>(props);
    }

    public void sendOrder(Order order) {
        ProducerRecord<String, Order> record = new ProducerRecord<>(
            "orders",
            order.getOrderId(),
            order
        );

        // Add custom headers
        record.headers()
            .add("event-type", "OrderCreated".getBytes())
            .add("source", "order-service".getBytes())
            .add("correlation-id", UUID.randomUUID().toString().getBytes());

        producer.send(record, (metadata, exception) -> {
            if (exception != null) {
                System.err.printf("Failed to send: %s%n", exception.getMessage());
            } else {
                System.out.printf("Sent to %s-%d @ offset %d%n",
                    metadata.topic(), metadata.partition(), metadata.offset());
            }
        });
    }
}
```

### 4.6 Consumer with Schema Registry (Java)

```java
import io.confluent.kafka.serializers.KafkaAvroDeserializer;
import io.confluent.kafka.serializers.KafkaAvroDeserializerConfig;
import org.apache.kafka.clients.consumer.*;
import com.styde.events.Order;
import com.styde.events.EnrichedOrder;

public class AvroOrderConsumer {

    private final KafkaConsumer<String, Order> consumer;

    public AvroOrderConsumer() {
        Properties props = new Properties();
        props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "kafka:9092");
        props.put(ConsumerConfig.GROUP_ID_CONFIG, "order-processor");
        props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
        props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, KafkaAvroDeserializer.class);

        // ── Schema Registry Configuration ───────────────────────
        props.put(KafkaAvroDeserializerConfig.SCHEMA_REGISTRY_URL_CONFIG,
            "http://schema-registry:8081");
        props.put(KafkaAvroDeserializerConfig.SPECIFIC_AVRO_READER_CONFIG, true);
        /*
         * specific.avro.reader=true means the consumer will use the generated
         * Java class (Order) rather than GenericRecord. This is strongly
         * recommended for type safety.
         *
         * When reading a message written with V1 using V2's Order class,
         * any new field not in V1 gets its default value — that's forward
         * compatibility in action.
         */

        this.consumer = new KafkaConsumer<>(props);
    }
}
```

### 4.7 Schema Registry REST API (Operational Usage)

```bash
# ── Register a new schema ─────────────────────────────────────
curl -X POST http://schema-registry:8081/subjects/orders-value/versions \
  -H "Content-Type: application/vnd.schemaregistry.v1+json" \
  -d '{"schema": "{...avro schema...}", "schemaType": "AVRO"}'

# ── Check compatibility before registering ─────────────────────
curl -X POST http://schema-registry:8081/compatibility/subjects/orders-value/versions/latest \
  -H "Content-Type: application/vnd.schemaregistry.v1+json" \
  -d '{"schema": "{...new schema...}"}'

# Response: {"is_compatible": true}

# ── Get schema by ID ───────────────────────────────────────────
curl http://schema-registry:8081/schemas/ids/42

# ── List all versions of a subject ─────────────────────────────
curl http://schema-registry:8081/subjects/orders-value/versions

# ── Set compatibility mode for a subject ───────────────────────
curl -X PUT http://schema-registry:8081/config/orders-value \
  -H "Content-Type: application/json" \
  -d '{"compatibility": "FULL_TRANSITIVE"}'

# ── Get global compatibility ───────────────────────────────────
curl http://schema-registry:8081/config

# ── Delete a schema version (soft delete) ──────────────────────
curl -X DELETE http://schema-registry:8081/subjects/orders-value/versions/3
```

### 4.8 Schema Evolution CI/CD Pipeline

```yaml
# .github/workflows/schema-ci.yml
name: Schema Compatibility Check

on:
  pull_request:
    paths:
      - 'schemas/**/*.avsc'

jobs:
  schema-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Start Schema Registry
        run: |
          docker compose -f ci/docker-compose.yml up -d schema-registry
          sleep 15  # wait for readiness

      - name: Check Compatibility
        run: |
          for schema in schemas/*.avsc; do
            subject=$(basename "$schema" .avsc)
            echo "Checking $subject..."

            # Get latest registered schema
            latest=$(curl -s "http://localhost:8081/subjects/$subject/versions/latest" | jq -r '.schema')

            # Check compatibility
            compatibility=$(curl -s -X POST \
              "http://localhost:8081/compatibility/subjects/$subject/versions/latest" \
              -H "Content-Type: application/vnd.schemaregistry.v1+json" \
              -d "{\"schema\": $(jq -Rs . < "$schema")}" \
              | jq -r '.is_compatible')

            if [ "$compatibility" != "true" ]; then
              echo "❌ $subject is NOT compatible!"
              exit 1
            fi
            echo "✅ $subject is compatible"
          done

      - name: Generate Java Classes (Maven)
        run: mvn avro:schema
```

---

## 5. Dead Letter Topic Patterns

### 5.1 Dead Letter Architecture

```
┌───────────────────────────────────────────────────────────────────────┐
│                      DEAD LETTER TOPIC PATTERNS                         │
│                                                                       │
│   Pattern 1: SINGLE DLQ (Simple)                                       │
│   ┌──────────┐                         ┌──────────────┐              │
│   │ Processor│──► failed msgs ────────►│ orders.dlq   │ (single)      │
│   └──────────┘                         └──────────────┘              │
│                                                                       │
│   Pattern 2: PER-TOPIC DLQ (Isolated)                                  │
│   ┌──────────┐                         ┌──────────────┐              │
│   │ Processor│──► orders failures ────►│ orders.dlq   │              │
│   │          │──► payments failures ──►│ payments.dlq │              │
│   └──────────┘                         └──────────────┘              │
│                                                                       │
│   Pattern 3: TIERED DLQ (Retry → Park → Final)                         │
│   ┌──────────┐                                                       │
│   │ Processor│──► retry-1.dlq ──TTL──► retry-2.dlq ──► park.dlq     │
│   └──────────┘                           │                │           │
│                                          │                ▼           │
│                                          │          manual inspect    │
│                                          ▼                             │
│                                      final.dlq (dead forever)         │
│                                                                       │
│   Pattern 4: TOPIC-CHAIN DLQ (Progressive)                             │
│   main-topic ──► retry-1-topic ──► retry-2-topic ──► dlq-topic       │
│   (consume,      (delay 10s,      (delay 1m,       (alert)           │
│    on fail:       on fail:         on fail:                           │
│    → retry-1)     → retry-2)       → dlq)                             │
└───────────────────────────────────────────────────────────────────────┘
```

### 5.2 Dead Letter Record Design

```java
/**
 * Comprehensive Dead Letter Record
 */
@Schema(description = "Dead letter record for unprocessable messages")
public class DeadLetterRecord {

    // ── Original Message Metadata ────────────────────────────
    private String originalTopic;
    private int originalPartition;
    private long originalOffset;
    private long originalTimestamp;
    private String originalKey;

    // ── Original Payload (raw bytes) ─────────────────────────
    private byte[] originalPayload;
    private int schemaId; // Schema Registry ID
    private Map<String, String> originalHeaders;

    // ── Error Context ───────────────────────────────────────
    private String errorType;
    private String errorMessage;
    private String stackTrace;
    private String processorId;     // which consumer/stream task failed
    private String applicationId;   // Streams application.id

    // ── Dead Letter Metadata ────────────────────────────────
    private long dlqTimestamp;
    private int retryCount;
    private String deadLetterReason; // enum: SCHEMA_ERROR, DESERIALIZATION_ERROR,
                                     //       BUSINESS_RULE_VIOLATION, TIMEOUT,
                                     //       POISON_PILL, UNKNOWN
    private Map<String, String> dlqMetadata;

    // ── Route for Replay ────────────────────────────────────
    private String targetTopicForReplay; // where to send on replay
    private boolean replayable;          // can this message be replayed?
}
```

### 5.3 Kafka Streams Dead Letter Branch

```java
// ── Pattern 1: Deserialization Error Handler ──────────────────
// Handled BEFORE the topology — Kafka Streams provides a dedicated handler

Properties props = new Properties();
props.put(StreamsConfig.DEFAULT_DESERIALIZATION_EXCEPTION_HANDLER_CLASS_CONFIG,
    DeadLetterDeserializationHandler.class.getName());


import org.apache.kafka.streams.errors.DeserializationExceptionHandler;
import org.apache.kafka.clients.producer.*;
import java.util.Map;

public class DeadLetterDeserializationHandler implements DeserializationExceptionHandler {

    private Producer<byte[], byte[]> dlqProducer;
    private String dlqTopic;

    @Override
    public void configure(Map<String, ?> configs) {
        Properties props = new Properties();
        props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG,
            configs.get(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG));
        props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, ByteArraySerializer.class);
        props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, ByteArraySerializer.class);

        this.dlqProducer = new KafkaProducer<>(props);
        this.dlqTopic = "streams.deserialization.dlq";
    }

    @Override
    public DeserializationHandlerResponse handle(
            ProcessorContext context,
            ConsumerRecord<byte[], byte[]> record,
            Exception exception) {

        // Build dead letter record
        DeadLetterRecord dlr = DeadLetterRecord.builder()
            .originalTopic(record.topic())
            .originalPartition(record.partition())
            .originalOffset(record.offset())
            .originalTimestamp(record.timestamp())
            .originalPayload(record.value())
            .errorType(exception.getClass().getName())
            .errorMessage(exception.getMessage())
            .processorId(context.taskId().toString())
            .applicationId(context.applicationId())
            .dlqTimestamp(System.currentTimeMillis())
            .deadLetterReason("DESERIALIZATION_ERROR")
            .replayable(false) // can't replay if we can't deserialize
            .build();

        // Send to DLQ topic
        ProducerRecord<byte[], byte[]> dlqRecord = new ProducerRecord<>(
            dlqTopic,
            record.key(),
            SerializationUtils.serialize(dlr)
        );

        dlqProducer.send(dlqRecord, (metadata, ex) -> {
            if (ex != null) {
                System.err.printf("Failed to write DLQ: %s%n", ex.getMessage());
            }
        });

        // CONTINUE = skip the record, move to next
        // FAIL = stop the stream thread
        return DeserializationHandlerResponse.CONTINUE;
    }
}
```

### 5.4 In-Topology Dead Letter Pattern

```java
// ── Pattern 2: Dead letter branch within the topology ────────

KStream<String, Order> orders = builder.stream("orders");

// Split into valid and dead-letter paths
Map<String, KStream<String, Order>> branches = orders
    .split(Named.as("dlq-"))
    .branch(
        (key, order) -> order != null && order.getAmount() != null,
        Branched.as("valid")
    )
    .defaultBranch(Branched.as("invalid"));

// Process valid orders
branches.get("dlq-valid")
    .mapValues(this::enrichOrder)
    .to("enriched-orders", Produced.with(Serdes.String(), enrichedSerde));

// Route invalid to dead letter
branches.get("dlq-invalid")
    .mapValues(order -> DeadLetterRecord.builder()
        .originalPayload(serializeOrder(order))
        .deadLetterReason("BUSINESS_RULE_VIOLATION")
        .errorMessage(order == null ? "null order" : order.getValidationErrors())
        .replayable(false)
        .dlqTimestamp(System.currentTimeMillis())
        .build()
    )
    .to("orders.dlq", Produced.with(Serdes.String(), deadLetterSerde));
```

### 5.5 Retry with Dead Letter (Kafka Streams)

```java
// ── Pattern 3: Retry → Dead Letter Chain ─────────────────────
// Uses a separate retry topic with TTL-based delay

public class RetryableProcessor {

    private static final int MAX_RETRIES = 3;
    private static final Duration RETRY_DELAY = Duration.ofSeconds(10);

    public Topology buildRetryTopology() {
        StreamsBuilder builder = new StreamsBuilder();

        // ── Main processing stream ──────────────────────────
        KStream<String, Order> orders = builder.stream("orders");

        KStream<String, Order> processed = orders
            .transformValues(() -> new ValueTransformerWithKey<>() {
                @Override
                public Order transform(String key, Order value) {
                    try {
                        return processOrder(key, value);
                    } catch (RetryableException e) {
                        // Extract retry count from headers
                        int retryCount = getRetryCount(context.headers());
                        if (retryCount < MAX_RETRIES) {
                            // Forward to retry topic with incremented count
                            context.headers().add("retry-count",
                                String.valueOf(retryCount + 1).getBytes());
                            // Signal to route to retry topic
                            return null; // handled below
                        } else {
                            // Max retries → dead letter
                            sendToDeadLetter(key, value, e, retryCount);
                            return null;
                        }
                    }
                }
            }, "retry-state-store");

        // Route nulls (failed orders) to retry topic
        processed
            .filter((key, order) -> order == null) // null = failed
            .to("orders.retry");

        // ── Retry topic ──────────────────────────────────────
        // This topic has: retention.ms = 1 hour, with message TTL
        // A separate streams app (or punctor) reads it after delay

        // Actually, Kafka doesn't have per-message TTL natively.
        // Instead, use a wall-clock punctor to check for ripe retry messages:

        KStream<String, Order> retries = builder.stream("orders.retry");

        retries
            .transform(() -> new Transformer<>() {
                private KeyValueStore<String, RetryState> store;
                private ProcessorContext context;

                @Override
                public void init(ProcessorContext context) {
                    this.context = context;
                    this.store = context.getStateStore("retry-store");
                    // Check every 5 seconds for messages ready to retry
                    context.schedule(Duration.ofSeconds(5),
                        PunctuationType.WALL_CLOCK_TIME, this::checkRetries);
                }

                @Override
                public KeyValue transform(String key, Order value) {
                    int retryCount = getRetryCount(context.headers());
                    long nextRetryAt = System.currentTimeMillis()
                        + RETRY_DELAY.toMillis() * (long) Math.pow(2, retryCount);

                    store.put(key, new RetryState(value, retryCount, nextRetryAt));
                    return null; // Don't forward yet
                }

                private void checkRetries(long now) {
                    try (KeyValueIterator<String, RetryState> iter = store.all()) {
                        while (iter.hasNext()) {
                            KeyValue<String, RetryState> entry = iter.next();
                            if (entry.value.nextRetryAt <= now) {
                                // Ready to retry — forward to main topic
                                store.delete(entry.key);
                                context.forward(Record
                                    .<String, Order>create(entry.key, entry.value.order)
                                    .withHeaders(new RecordHeaders()
                                        .add("retry-count",
                                            String.valueOf(entry.value.retryCount)
                                                .getBytes())
                                    ));
                            }
                        }
                    }
                }

                @Override
                public void close() {}
            }, "retry-store")
            .to("orders"); // back to main topic for retry

        return builder.build();
    }

    private static class RetryState {
        final Order order;
        final int retryCount;
        final long nextRetryAt;
        RetryState(Order order, int retryCount, long nextRetryAt) {
            this.order = order;
            this.retryCount = retryCount;
            this.nextRetryAt = nextRetryAt;
        }
    }
}
```

### 5.6 Dead Letter Monitoring & Alerting

```java
// ── Dead Letter Monitor ──────────────────────────────────────
// Continuously monitors DLQ topics and alerts on new messages

public class DeadLetterMonitor {

    private final KafkaConsumer<String, DeadLetterRecord> consumer;
    private final AlertingService alerting;
    private static final long POLL_INTERVAL_MS = 5000;

    // Track DLQ message rates per topic
    private final Map<String, SlidingWindowCounter> dlqRates = new ConcurrentHashMap<>();

    public DeadLetterMonitor(String dlqTopics, AlertingService alerting) {
        Properties props = new Properties();
        props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "kafka:9092");
        props.put(ConsumerConfig.GROUP_ID_CONFIG, "dlq-monitor");
        props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
        props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, KafkaAvroDeserializer.class);
        props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "latest");
        props.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, true);

        this.consumer = new KafkaConsumer<>(props);
        this.consumer.subscribe(Pattern.compile(dlqTopics));
        this.alerting = alerting;
    }

    public void startMonitoring() {
        Executors.newSingleThreadScheduledExecutor().scheduleAtFixedRate(() -> {
            ConsumerRecords<String, DeadLetterRecord> records =
                consumer.poll(Duration.ofMillis(POLL_INTERVAL_MS));

            for (ConsumerRecord<String, DeadLetterRecord> record : records) {
                DeadLetterRecord dlr = record.value();

                // Increment rate counter
                dlqRates.computeIfAbsent(record.topic(), k -> new SlidingWindowCounter())
                    .increment();

                // Log with structured context
                System.err.printf(
                    "[DLQ] topic=%s offset=%d reason=%s error=%s original=%s%n",
                    record.topic(), record.offset(),
                    dlr.getDeadLetterReason(), dlr.getErrorMessage(),
                    dlr.getOriginalTopic()
                );

                // Alert if rate threshold exceeded
                double rate = dlqRates.get(record.topic()).getRate();
                if (rate > 10.0) { // >10 DLQ messages per second
                    alerting.send(Alert.critical()
                        .title("DLQ Rate Spike")
                        .detail("Topic: " + record.topic())
                        .detail("Rate: " + String.format("%.1f/s", rate))
                        .detail("Latest reason: " + dlr.getDeadLetterReason())
                        .build()
                    );
                }
            }
        }, 0, POLL_INTERVAL_MS, TimeUnit.MILLISECONDS);
    }
}
```

---

## 6. Message Replay Strategies

### 6.1 Replay Strategy Matrix

```
┌──────────────────────────────────────────────────────────────────────────┐
│                           MESSAGE REPLAY STRATEGIES                        │
│                                                                          │
│  STRATEGY           │  USE CASE                     │  IMPLEMENTATION     │
│  ───────────────────┼───────────────────────────────┼──────────────────── │
│  Full Replay        │ Reprocess all historical      │ Reset to earliest   │
│  (start→now)        │ data after bug fix            │ offset, re-consume  │
│                     │                               │                     │
│  Time-Range Replay  │ Reprocess specific period     │ offsetsForTimes()   │
│  (from→to)          │ (e.g., yesterday's orders)    │ + seek              │
│                     │                               │                     │
│  Offset-Range       │ Reprocess known bad offsets   │ seek(start) +       │
│  Replay             │                               │ poll until end       │
│                     │                               │                     │
│  Per-Partition      │ Reprocess specific partitions │ Manual partition    │
│  Replay             │ (e.g., partition migration)   │ assignment + seek   │
│                     │                               │                     │
│  Replay-to-Topic    │ Side-by-side reprocessing     │ kcat / MirrorMaker  │
│  (new topic)        │ into new topic                │ consume→filter→     │
│                     │                               │ produce             │
│                     │                               │                     │
│  Selective Replay   │ Replay only matching messages │ Consumer filter +   │
│  (by key/header)    │ (e.g., orders for customer X) │ skip non-matching   │
│                     │                               │                     │
│  DLQ Replay         │ Replay dead-lettered messages │ Admin client:       │
│  (repair+replay)    │ after fixing the root cause   │ reset offsets +     │
│                     │                               │ produce to original  │
└──────────────────────────────────────────────────────────────────────────┘
```

### 6.2 Time-Range Replay (Consumer API)

```java
/**
 * Replays messages from a specific time range into a target topic.
 * Useful for reprocessing after a bug fix.
 */
public class TimeRangeReplayService {

    private final KafkaConsumer<String, byte[]> sourceConsumer;
    private final KafkaProducer<String, byte[]> targetProducer;
    private final String sourceTopic;
    private final String targetTopic;

    public TimeRangeReplayService(
            String sourceTopic, String targetTopic,
            String bootstrapServers) {

        this.sourceTopic = sourceTopic;
        this.targetTopic = targetTopic;

        // Source consumer: read from beginning, no offset commits
        Properties consumerProps = new Properties();
        consumerProps.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
        consumerProps.put(ConsumerConfig.GROUP_ID_CONFIG,
            "replay-consumer-" + UUID.randomUUID()); // unique group = fresh offsets
        consumerProps.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG,
            StringDeserializer.class);
        consumerProps.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG,
            ByteArrayDeserializer.class);
        consumerProps.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
        consumerProps.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, false);
        consumerProps.put(ConsumerConfig.MAX_POLL_RECORDS_CONFIG, 5000);

        this.sourceConsumer = new KafkaConsumer<>(consumerProps);

        // Target producer: write replayed messages
        Properties producerProps = new Properties();
        producerProps.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
        producerProps.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG,
            StringSerializer.class);
        producerProps.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG,
            ByteArraySerializer.class);
        producerProps.put(ProducerConfig.COMPRESSION_TYPE_CONFIG, "zstd");
        producerProps.put(ProducerConfig.LINGER_MS_CONFIG, 10);
        producerProps.put(ProducerConfig.BATCH_SIZE_CONFIG, 65536);

        this.targetProducer = new KafkaProducer<>(producerProps);
    }

    /**
     * Replay messages from startTime to endTime.
     *
     * @param startTime Inclusive start timestamp (epoch ms)
     * @param endTime   Exclusive end timestamp (epoch ms)
     * @return Number of messages replayed
     */
    public long replayTimeRange(long startTime, long endTime) {
        // 1. Get partition list
        List<PartitionInfo> partitions = sourceConsumer.partitionsFor(sourceTopic);
        List<TopicPartition> topicPartitions = partitions.stream()
            .map(pi -> new TopicPartition(sourceTopic, pi.partition()))
            .collect(Collectors.toList());

        sourceConsumer.assign(topicPartitions);

        // 2. Find starting offsets for each partition by timestamp
        Map<TopicPartition, Long> startTimestamps = new HashMap<>();
        for (TopicPartition tp : topicPartitions) {
            startTimestamps.put(tp, startTime);
        }
        Map<TopicPartition, OffsetAndTimestamp> startOffsets =
            sourceConsumer.offsetsForTimes(startTimestamps);

        // 3. Seek each partition to its start offset
        for (Map.Entry<TopicPartition, OffsetAndTimestamp> entry : startOffsets.entrySet()) {
            if (entry.getValue() != null) {
                sourceConsumer.seek(entry.getKey(), entry.getValue().offset());
                System.out.printf("Partition %d → seeking to offset %d%n",
                    entry.getKey().partition(), entry.getValue().offset());
            } else {
                // No messages at this timestamp in this partition
                System.out.printf("Partition %d → no messages in range, skipping%n",
                    entry.getKey().partition());
            }
        }

        // 4. Poll and replay until endTime
        long totalReplayed = 0;
        boolean allDone = false;

        while (!allDone) {
            ConsumerRecords<String, byte[]> records =
                sourceConsumer.poll(Duration.ofSeconds(5));

            if (records.isEmpty()) {
                allDone = true; // no more data
                break;
            }

            for (ConsumerRecord<String, byte[]> record : records) {
                // Check if we've passed the end time
                if (record.timestamp() >= endTime) {
                    allDone = true;
                    break;
                }

                // Replay to target topic (preserve key, headers, but new timestamp)
                ProducerRecord<String, byte[]> targetRecord = new ProducerRecord<>(
                    targetTopic,
                    null,                // no partition override (use key hash)
                    record.timestamp(),  // preserve original timestamp
                    record.key(),
                    record.value(),
                    record.headers()
                );

                // Add replay metadata header
                targetRecord.headers().add("replay-source", sourceTopic.getBytes());
                targetRecord.headers().add("replay-offset",
                    String.valueOf(record.offset()).getBytes());

                targetProducer.send(targetRecord, (metadata, ex) -> {
                    if (ex != null) {
                        System.err.printf("Replay failed: %s%n", ex.getMessage());
                    }
                });

                totalReplayed++;
            }

            if (totalReplayed % 10000 == 0) {
                System.out.printf("Replayed %d messages so far...%n", totalReplayed);
            }
        }

        targetProducer.flush();
        sourceConsumer.close();
        targetProducer.close();

        System.out.printf("Replay complete: %d messages from %s [%s → %s]%n",
            totalReplayed, sourceTopic,
            Instant.ofEpochMilli(startTime),
            Instant.ofEpochMilli(endTime));

        return totalReplayed;
    }
}
```

### 6.3 Kafka Streams Replay (Application Reset)

```bash
# ── Method 1: Reset Kafka Streams Application ─────────────────
# This deletes the application's internal state and resets offsets
# to earliest (or specified position), causing full reprocessing.

# Dry run — see what would happen
kafka-streams-application-reset \
  --bootstrap-servers kafka:9092 \
  --application-id order-processing-v2 \
  --input-topics orders,customers \
  --dry-run

# Execute reset (STOP the app first!)
kafka-streams-application-reset \
  --bootstrap-servers kafka:9092 \
  --application-id order-processing-v2 \
  --input-topics orders,customers \
  --to-earliest

# ── Method 2: Reset to specific datetime ──────────────────────
kafka-streams-application-reset \
  --bootstrap-servers kafka:9092 \
  --application-id order-processing-v2 \
  --input-topics orders \
  --to-datetime 2026-06-25T00:00:00.000

# ── Method 3: Reset only specific partitions ──────────────────
# (via AdminClient or kafka-consumer-groups)
kafka-consumer-groups \
  --bootstrap-servers kafka:9092 \
  --group order-processing-v2 \
  --topic orders:0 \
  --reset-offsets \
  --to-offset 12345 \
  --execute
```

### 6.4 Selective Replay — Filter by Message Content

```java
/**
 * Selective replay: only replay messages matching a predicate.
 * Consumes from source, filters, produces to target.
 */
public class SelectiveReplayService {

    public long replayMatching(String sourceTopic, String targetTopic,
                                Predicate<ConsumerRecord<String, Order>> predicate) {

        KafkaConsumer<String, Order> consumer = createConsumer(sourceTopic);
        KafkaProducer<String, Order> producer = createProducer();

        consumer.subscribe(List.of(sourceTopic));
        consumer.poll(Duration.ofSeconds(1)); // dummy poll to get assignment

        // Seek to beginning
        consumer.seekToBeginning(consumer.assignment());

        long replayed = 0;
        long scanned = 0;
        boolean done = false;

        while (!done) {
            ConsumerRecords<String, Order> records =
                consumer.poll(Duration.ofSeconds(5));

            if (records.isEmpty()) {
                done = true;
                break;
            }

            for (ConsumerRecord<String, Order> record : records) {
                scanned++;
                if (predicate.test(record)) {
                    ProducerRecord<String, Order> target = new ProducerRecord<>(
                        targetTopic,
                        record.key(),
                        record.value()
                    );
                    target.headers()
                        .add("replay-reason", "selective-replay".getBytes())
                        .add("replay-source-offset",
                            String.valueOf(record.offset()).getBytes());

                    producer.send(target);
                    replayed++;
                }
            }
        }

        producer.flush();
        consumer.close();
        producer.close();

        System.out.printf("Selective replay: %d/%d messages matched%n",
            replayed, scanned);
        return replayed;
    }

    // Example usage: replay orders for a specific customer
    public long replayCustomerOrders(String customerId) {
        return replayMatching("orders", "orders.replay",
            record -> customerId.equals(record.key()));
    }

    // Example usage: replay corrupted orders (from monitoring)
    public long replayCorruptedOrders(Set<String> corruptedOrderIds) {
        return replayMatching("orders", "orders.replay",
            record -> corruptedOrderIds.contains(record.key()));
    }
}
```

### 6.5 DLQ Replay Service

```java
/**
 * Replay dead-lettered messages back to their original topic
 * after the root cause has been fixed.
 */
public class DeadLetterReplayService {

    private final AdminClient adminClient;
    private final KafkaConsumer<String, DeadLetterRecord> dlqConsumer;
    private final KafkaProducer<byte[], byte[]> replayProducer;

    /**
     * Replay all dead-lettered messages for a specific topic.
     *
     * Strategy:
     * 1. Read all messages from the DLQ topic
     * 2. For messages marked as 'replayable' and matching the target topic:
     *    a. Re-serialize the original payload
     *    b. Produce to the original topic
     * 3. Advance DLQ consumer offset past replayed messages
     */
    public long replayDeadLetters(String dlqTopic, String originalTopic,
                                   long fromTimestamp, long toTimestamp) {

        dlqConsumer.subscribe(List.of(dlqTopic));

        // Seek by timestamp
        Map<TopicPartition, OffsetAndTimestamp> offsets = dlqConsumer
            .offsetsForTimes(Map.of(
                new TopicPartition(dlqTopic, 0), fromTimestamp
            ));
        offsets.forEach((tp, os) -> {
            if (os != null) dlqConsumer.seek(tp, os.offset());
        });

        long replayed = 0;
        long skipped = 0;
        boolean done = false;

        while (!done) {
            ConsumerRecords<String, DeadLetterRecord> records =
                dlqConsumer.poll(Duration.ofSeconds(5));

            if (records.isEmpty()) {
                done = true;
                break;
            }

            for (ConsumerRecord<String, DeadLetterRecord> record : records) {
                DeadLetterRecord dlr = record.value();

                // Stop if past the time range
                if (dlr.getDlqTimestamp() > toTimestamp) {
                    done = true;
                    break;
                }

                // Only replay if:
                //   1. Matches the target original topic
                //   2. Is marked as replayable
                //   3. Original payload is not null
                if (dlr.getOriginalTopic().equals(originalTopic)
                        && dlr.isReplayable()
                        && dlr.getOriginalPayload() != null) {

                    ProducerRecord<byte[], byte[]> replayRecord = new ProducerRecord<>(
                        originalTopic,
                        dlr.getOriginalKey() != null
                            ? dlr.getOriginalKey().getBytes() : null,
                        dlr.getOriginalPayload()
                    );

                    // Add replay context headers
                    replayRecord.headers()
                        .add("dlq-replay", "true".getBytes())
                        .add("dlq-original-offset",
                            String.valueOf(dlr.getOriginalOffset()).getBytes())
                        .add("dlq-error", dlr.getErrorMessage().getBytes());

                    replayProducer.send(replayRecord, (md, ex) -> {
                        if (ex == null) {
                            System.out.printf("Replayed DLQ msg: %s-%d → %s%n",
                                dlr.getOriginalTopic(), dlr.getOriginalOffset(),
                                originalTopic);
                        } else {
                            System.err.printf("Replay failed: %s%n", ex.getMessage());
                        }
                    });

                    replayed++;
                } else {
                    skipped++;
                }
            }

            // Commit DLQ offsets (mark as processed)
            dlqConsumer.commitSync();
        }

        System.out.printf("DLQ replay: %d replayed, %d skipped%n", replayed, skipped);
        return replayed;
    }
}
```

### 6.6 Replay Safety Patterns

```java
/**
 * ── SAFETY PATTERNS FOR PRODUCTION REPLAY ──────────────────
 *
 * 1. IDEMPOTENCY MARKER HEADER
 *    Add a unique replay-ID header so downstream consumers can deduplicate.
 *
 * 2. DRY-RUN MODE
 *    Count matching messages without actually producing.
 *
 * 3. RATE-LIMITED REPLAY
 *    Throttle replay to avoid overwhelming downstream systems.
 *
 * 4. DUAL-WRITE VERIFICATION
 *    Write to both the original topic AND a shadow topic for verification.
 *
 * 5. CHECKPOINTING
 *    Periodically save the last replayed offset so replay can resume.
 */

public class SafeReplayService {

    private final String replayId = UUID.randomUUID().toString();
    private final RateLimiter rateLimiter = RateLimiter.create(1000.0); // 1000 msg/s

    public void safeReplay(ConsumerRecord<String, byte[]> source,
                            String targetTopic, Producer<byte[], byte[]> producer) {

        // ── 1. Add idempotency marker ──────────────────────
        source.headers().add("replay-id", replayId.getBytes());
        source.headers().add("replay-source-offset",
            String.valueOf(source.offset()).getBytes());
        source.headers().add("replay-source-topic",
            source.topic().getBytes());

        // ── 3. Rate limiting ───────────────────────────────
        rateLimiter.acquire();

        ProducerRecord<byte[], byte[]> target = new ProducerRecord<>(
            targetTopic,
            null,
            source.timestamp(), // preserve original timestamp
            source.key(),
            source.value(),
            source.headers()
        );

        producer.send(target, (metadata, exception) -> {
            if (exception == null) {
                System.out.printf("[REPLAY %s] %s-%d → %s-%d%n",
                    replayId, source.topic(), source.offset(),
                    metadata.topic(), metadata.offset());
            }
        });
    }

    // ── 2. Dry-run count ───────────────────────────────────
    public long dryRunCount(String sourceTopic, long startTime, long endTime) {
        AtomicLong count = new AtomicLong(0);

        // Consume without producing
        try (KafkaConsumer<String, byte[]> consumer = createConsumer(sourceTopic)) {
            // Seek and count (implementation similar to TimeRangeReplayService)
            // ... but only count, don't produce
        }
        return count.get();
    }
}
```

---

## 7. Full Reference Implementation

### 7.1 Complete Order Processing Pipeline

This section ties all patterns together into a single, production-ready pipeline:

```
KAFKA TOPICS:
  ┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌──────────────┐
  │ orders      │────►│ enriched-    │────►│ order-       │────►│ notification │
  │ (source)    │     │ orders       │     │ confirmed    │     │ -events      │
  └─────────────┘     └──────┬───────┘     └─────────────┘     └──────────────┘
                             │
                      ┌──────┴───────┐     ┌─────────────┐
                      │ fraud-alerts │────►│ fraud-       │
                      └──────────────┘     │ investigation│
                                           └─────────────┘
                             │
                      ┌──────┴───────┐
                      │ orders.dlq   │ (dead letter)
                      └──────────────┘

SCHEMA REGISTRY SUBJECTS:
  orders-value          ← Order (Avro)
  enriched-orders-value ← EnrichedOrder (Avro)
  orders.dlq-value      ← DeadLetterRecord (Avro)

KAFKA STREAMS APP (order-processing-v2):
  application.id = order-processing-v2
  processing.guarantee = exactly_once_v2
  num.stream.threads = 4
  replication.factor = 3

STATE STORES:
  customers-store        (GlobalKTable, read-only)
  order-counts-window    (WindowStore, 5-min tumbling)
  fraud-detector-store   (KeyValueStore, persistent)
  dedup-store            (KeyValueStore, with TTL)
  retry-store            (KeyValueStore, with punctor)
```

### 7.2 Docker Compose — Full Stack

```yaml
# docker-compose.yml — Complete Kafka + Schema Registry + Streams Stack
version: '3.8'

services:
  # ── Kafka Broker (KRaft mode, no ZooKeeper) ──────────────
  kafka1:
    image: confluentinc/cp-kafka:7.6.0
    hostname: kafka1
    ports:
      - "9092:9092"
      - "9101:9101"  # JMX
    environment:
      CLUSTER_ID: "MkU3OEVBNTcwNTJENDM2Qk"
      KAFKA_NODE_ID: 1
      KAFKA_PROCESS_ROLES: "broker,controller"
      KAFKA_CONTROLLER_QUORUM_VOTERS: "1@kafka1:9093"
      KAFKA_LISTENERS: "PLAINTEXT://kafka1:9092,CONTROLLER://kafka1:9093"
      KAFKA_ADVERTISED_LISTENERS: "PLAINTEXT://kafka1:9092"
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: "PLAINTEXT:PLAINTEXT,CONTROLLER:PLAINTEXT"
      KAFKA_INTER_BROKER_LISTENER_NAME: "PLAINTEXT"
      KAFKA_CONTROLLER_LISTENER_NAMES: "CONTROLLER"
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1
      KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS: 0
      KAFKA_NUM_PARTITIONS: 6
      KAFKA_DEFAULT_REPLICATION_FACTOR: 1
      KAFKA_LOG_RETENTION_HOURS: 168  # 7 days
      KAFKA_LOG_SEGMENT_BYTES: 1073741824  # 1 GB
    volumes:
      - kafka1-data:/var/lib/kafka/data
    healthcheck:
      test: ["CMD", "bash", "-c", "nc -z localhost 9092"]
      interval: 10s
      timeout: 5s
      retries: 5

  # ── Schema Registry ──────────────────────────────────────
  schema-registry:
    image: confluentinc/cp-schema-registry:7.6.0
    hostname: schema-registry
    ports:
      - "8081:8081"
    environment:
      SCHEMA_REGISTRY_HOST_NAME: schema-registry
      SCHEMA_REGISTRY_KAFKASTORE_BOOTSTRAP_SERVERS: "kafka1:9092"
      SCHEMA_REGISTRY_KAFKASTORE_TOPIC: "_schemas"
      SCHEMA_REGISTRY_KAFKASTORE_TOPIC_REPLICATION_FACTOR: 1
      SCHEMA_REGISTRY_LISTENERS: "http://0.0.0.0:8081"
      SCHEMA_REGISTRY_SCHEMA_COMPATIBILITY_LEVEL: "full_transitive"
      SCHEMA_REGISTRY_ACCESS_CONTROL_ENABLED: "false"
    depends_on:
      kafka1:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8081/subjects"]
      interval: 10s
      timeout: 5s
      retries: 5

  # ── Kafka UI (Observability) ─────────────────────────────
  kafka-ui:
    image: provectuslabs/kafka-ui:latest
    ports:
      - "8080:8080"
    environment:
      KAFKA_CLUSTERS_0_NAME: local
      KAFKA_CLUSTERS_0_BOOTSTRAP_SERVERS: "kafka1:9092"
      KAFKA_CLUSTERS_0_SCHEMA_REGISTRY: "http://schema-registry:8081"
      DYNAMIC_CONFIG_ENABLED: "true"
    depends_on:
      - kafka1
      - schema-registry

  # ── Prometheus Metrics Exporter ──────────────────────────
  kafka-exporter:
    image: danielqsj/kafka-exporter:latest
    ports:
      - "9308:9308"
    command:
      - "--kafka.server=kafka1:9092"
      - "--web.listen-address=:9308"
    depends_on:
      - kafka1

  # ── Schema Registry Initializer ──────────────────────────
  schema-init:
    image: confluentinc/cp-schema-registry:7.6.0
    depends_on:
      schema-registry:
        condition: service_healthy
    entrypoint: ["/bin/bash", "-c"]
    command:
      - |
        echo "Registering schemas..."
        for schema in /schemas/*.avsc; do
          subject="$$(basename $$schema .avsc)"
          echo "Registering $$subject..."
          curl -s -X POST \
            "http://schema-registry:8081/subjects/$$subject/versions" \
            -H "Content-Type: application/vnd.schemaregistry.v1+json" \
            -d "$$(jq -Rs '{schema: .}' < $$schema)" || true
        done
        echo "Schema registration complete."
    volumes:
      - ./schemas:/schemas

  # ── Kafka Streams Application (Your App) ─────────────────
  order-streams-app:
    build:
      context: .
      dockerfile: Dockerfile
    environment:
      KAFKA_BOOTSTRAP_SERVERS: "kafka1:9092"
      SCHEMA_REGISTRY_URL: "http://schema-registry:8081"
      APPLICATION_ID: "order-processing-v2"
      PROCESSING_GUARANTEE: "exactly_once_v2"
      NUM_STREAM_THREADS: "4"
      STATE_DIR: "/data/kafka-streams"
      JAVA_OPTS: "-Xms2G -Xmx2G -XX:+UseG1GC"
    volumes:
      - streams-state:/data/kafka-streams
    depends_on:
      kafka1:
        condition: service_healthy
      schema-registry:
        condition: service_healthy
    restart: unless-stopped

volumes:
  kafka1-data:
  streams-state:
```

### 7.3 Kafka Topic Management (Init Script)

```bash
#!/bin/bash
# init-kafka-topics.sh — Create all required topics with correct configs
# Run once during infrastructure bootstrapping

BOOTSTRAP_SERVER="kafka1:9092"
PARTITIONS=6
REPLICATION=3  # Use 1 for single-broker dev, 3 for production

# ── Core Topics ──────────────────────────────────────────────
kafka-topics --bootstrap-server $BOOTSTRAP_SERVER \
  --create --topic orders \
  --partitions $PARTITIONS --replication-factor $REPLICATION \
  --config retention.ms=604800000 \
  --config retention.bytes=107374182400 \
  --config compression.type=zstd \
  --config cleanup.policy=delete

kafka-topics --bootstrap-server $BOOTSTRAP_SERVER \
  --create --topic customers \
  --partitions $PARTITIONS --replication-factor $REPLICATION \
  --config retention.ms=604800000 \
  --config cleanup.policy=compact  # KTable source → compacted

kafka-topics --bootstrap-server $BOOTSTRAP_SERVER \
  --create --topic enriched-orders \
  --partitions $PARTITIONS --replication-factor $REPLICATION \
  --config retention.ms=259200000  # 3 days — intermediate topic

kafka-topics --bootstrap-server $BOOTSTRAP_SERVER \
  --create --topic high-value-orders \
  --partitions 3 --replication-factor $REPLICATION \
  --config retention.ms=86400000   # 1 day

kafka-topics --bootstrap-server $BOOTSTRAP_SERVER \
  --create --topic low-value-orders \
  --partitions 3 --replication-factor $REPLICATION \
  --config retention.ms=86400000

kafka-topics --bootstrap-server $BOOTSTRAP_SERVER \
  --create --topic fraud-alerts \
  --partitions 3 --replication-factor $REPLICATION \
  --config retention.ms=604800000

kafka-topics --bootstrap-server $BOOTSTRAP_SERVER \
  --create --topic order-counts-by-customer \
  --partitions $PARTITIONS --replication-factor $REPLICATION \
  --config retention.ms=86400000 \
  --config cleanup.policy=compact  # Changelog → compacted

# ── Dead Letter Topics ────────────────────────────────────────
kafka-topics --bootstrap-server $BOOTSTRAP_SERVER \
  --create --topic orders.dlq \
  --partitions 3 --replication-factor $REPLICATION \
  --config retention.ms=1209600000  # 14 days — keep longer for investigation
  --config min.insync.replicas=2

kafka-topics --bootstrap-server $BOOTSTRAP_SERVER \
  --create --topic orders.retry \
  --partitions 3 --replication-factor $REPLICATION \
  --config retention.ms=3600000  # 1 hour

kafka-topics --bootstrap-server $BOOTSTRAP_SERVER \
  --create --topic streams.deserialization.dlq \
  --partitions 3 --replication-factor $REPLICATION \
  --config retention.ms=1209600000

# ── Replay Topic ──────────────────────────────────────────────
kafka-topics --bootstrap-server $BOOTSTRAP_SERVER \
  --create --topic orders.replay \
  --partitions $PARTITIONS --replication-factor $REPLICATION \
  --config retention.ms=86400000  # 1 day — short-lived replay target

# ── Audit / Observability ─────────────────────────────────────
kafka-topics --bootstrap-server $BOOTSTRAP_SERVER \
  --create --topic order-audit \
  --partitions $PARTITIONS --replication-factor $REPLICATION \
  --config retention.ms=2592000000  # 30 days
  --config compression.type=zstd

# ── Verify ────────────────────────────────────────────────────
echo "=== Created Topics ==="
kafka-topics --bootstrap-server $BOOTSTRAP_SERVER --list
```

---

## 8. Production Operations & Monitoring

### 8.1 Key Metrics to Monitor

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         KAFKA MONITORING MATRIX                          │
│                                                                         │
│  CATEGORY        │  METRIC                          │  ALERT THRESHOLD  │
│  ────────────────┼──────────────────────────────────┼────────────────── │
│  Broker Health   │  UnderReplicatedPartitions       │  > 0 for > 1 min  │
│                  │  ActiveControllerCount           │  != 1             │
│                  │  OfflinePartitionsCount          │  > 0              │
│                  │  RequestHandlerAvgIdlePercent    │  < 0.3 (70% busy) │
│  ────────────────┼──────────────────────────────────┼────────────────── │
│  Producer        │  RecordErrorRate                 │  > 0.01/s         │
│                  │  RecordRetryRate                 │  > 1% of send rate│
│                  │  RequestLatencyAvg (p99)         │  > 500ms          │
│                  │  OutgoingByteRate                │  (capacity)       │
│  ────────────────┼──────────────────────────────────┼────────────────── │
│  Consumer        │  RecordsLagMax                   │  > 10,000         │
│                  │  RecordsLeadMin                  │  < 0 (data loss)  │
│                  │  ConsumerGroupRebalanceRate       │  > 1 per hour     │
│                  │  FetchRate                        │  (baseline)       │
│  ────────────────┼──────────────────────────────────┼────────────────── │
│  Streams         │  ThreadState (DEAD)              │  > 0 threads      │
│                  │  ProcessRate                      │  (baseline)       │
│                  │  PunctuateRate                    │  < expected       │
│                  │  StateStoreSize                   │  > disk capacity  │
│                  │  ActiveTaskCount                  │  changed          │
│  ────────────────┼──────────────────────────────────┼────────────────── │
│  Dead Letter     │  DLQMessageRate                   │  > 10/s sustained │
│                  │  DLQAge (oldest message)          │  > 1 hour         │
│  ────────────────┼──────────────────────────────────┼────────────────── │
│  Schema Registry │  SchemaRegistrationRate           │  unexpected surge │
│                  │  SchemaCompatibilityFailureRate     │  > 0             │
└─────────────────────────────────────────────────────────────────────────┘
```

### 8.2 Kafka Streams Health Check

```java
/**
 * Embed a health check endpoint into the Streams application.
 * Use with Kubernetes liveness/readiness probes.
 */
public class StreamsHealthCheck {

    private final KafkaStreams streams;

    public StreamsHealthCheck(KafkaStreams streams) {
        this.streams = streams;
    }

    public HealthStatus checkHealth() {
        HealthStatus status = new HealthStatus();

        // ── State check ──────────────────────────────────
        status.state = streams.state().name();

        switch (streams.state()) {
            case RUNNING:
            case REBALANCING:
                status.healthy = true;
                break;
            case ERROR:
            case PENDING_SHUTDOWN:
            case NOT_RUNNING:
                status.healthy = false;
                status.reason = "Streams state: " + streams.state();
                break;
            default:
                status.healthy = false;
                status.reason = "Unknown state: " + streams.state();
        }

        // ── Thread metadata ─────────────────────────────
        status.threadMetadata = streams.metadataForLocalThreads().stream()
            .map(tm -> new ThreadInfo(
                tm.threadName(),
                tm.threadState(),
                tm.activeTasks().size(),
                tm.standbyTasks().size()
            ))
            .collect(Collectors.toList());

        // ── Lag check ───────────────────────────────────
        Map<TopicPartition, Long> lag = new HashMap<>();
        try (AdminClient admin = AdminClient.create(Map.of(
                AdminClientConfig.BOOTSTRAP_SERVERS_CONFIG, "kafka:9092"))) {

            String groupId = streams.store(StoreQueryParameters.fromNameAndType(
                "__application-id", QueryableStoreTypes.keyValueStore()
            ));

            // Get consumer group lag
            admin.listConsumerGroupOffsets(groupId)
                .partitionsToOffsetAndMetadata()
                .whenComplete((offsets, ex) -> {
                    if (ex == null) {
                        // Calculate lag (simplified)
                    }
                });
        }

        // ── State store sizes ───────────────────────────
        long totalStateBytes = 0;
        for (ThreadMetadata tm : streams.metadataForLocalThreads()) {
            totalStateBytes += tm.activeTasks().stream()
                .mapToLong(task -> task.stateStoreNames().stream()
                    .mapToLong(name -> {
                        try {
                            return streams.store(StoreQueryParameters
                                .fromNameAndType(name, QueryableStoreTypes.keyValueStore()))
                                .approximateNumEntries();
                        } catch (Exception e) {
                            return 0;
                        }
                    })
                    .sum()
                )
                .sum();
        }
        status.stateStoreEntries = totalStateBytes;

        // ── Topology description ────────────────────────
        status.topologyDescription = streams.metadataForLocalThreads()
            .toString();

        return status;
    }

    // Expose via HTTP (embed Jetty or use dropwizard metrics)
    public static class HealthStatus {
        public boolean healthy;
        public String state;
        public String reason;
        public List<ThreadInfo> threadMetadata;
        public long stateStoreEntries;
        public String topologyDescription;
    }

    public static class ThreadInfo {
        public String name;
        public String state;
        public int activeTasks;
        public int standbyTasks;
        ThreadInfo(String n, String s, int a, int st) {
            this.name = n; this.state = s;
            this.activeTasks = a; this.standbyTasks = st;
        }
    }
}
```

### 8.3 Operational Runbook — Common Scenarios

```
┌──────────────────────────────────────────────────────────────────────────┐
│                      KAFKA STREAMS OPERATIONAL RUNBOOK                     │
│                                                                          │
│  SCENARIO 1: Consumer Lag Growing                                         │
│  ───────────────────────────────                                          │
│  Symptom: records-lag-max increasing monotonically                        │
│  Causes:                                                                  │
│    • Insufficient partitions → add partitions (requires new topic)       │
│    • Slow processor logic → profile & optimize                            │
│    • External system bottleneck (DB, API) → add caching/async            │
│    • Rebalance storm → use static group membership                        │
│  Resolution:                                                              │
│    1. Check consumer group status: kafka-consumer-groups --describe       │
│    2. Check Streams thread metrics for slow tasks                         │
│    3. Scale up: increase num.stream.threads (up to partition count)       │
│    4. Scale out: add more instances (rebalance distributes partitions)    │
│                                                                          │
│  SCENARIO 2: Streams App in ERROR State                                   │
│  ───────────────────────────────                                          │
│  Symptom: thread state = DEAD, application state = ERROR                 │
│  Causes:                                                                  │
│    • Uncaught exception in processor logic                                │
│    • Deserialization error (poison pill)                                  │
│    • State store corruption                                               │
│    • Disk full (state.dir)                                                │
│  Resolution:                                                              │
│    1. Check logs for exception stacktrace                                 │
│    2. If poison pill: configure DeadLetterDeserializationHandler          │
│    3. If state store corrupt: reset application                           │
│       kafka-streams-application-reset --application-id <app-id>           │
│    4. If disk full: free space and restart                                │
│                                                                          │
│  SCENARIO 3: Schema Compatibility Failure                                  │
│  ───────────────────────────────                                          │
│  Symptom: SerializationException, SchemaRegistryException                │
│  Causes:                                                                  │
│    • Producer sending with incompatible new schema                        │
│    • Consumer reading with too-old schema                                 │
│  Resolution:                                                              │
│    1. Check compatibility:                                                │
│       curl http://schema-registry:8081/compatibility/subjects/<s>/        │
│            versions/latest -d '{"schema": "..."}'                         │
│    2. If producer is wrong: rollback producer, fix schema, redeploy       │
│    3. If consumer is wrong: deploy updated consumer with new schema       │
│    4. Use FULL_TRANSITIVE compatibility to prevent this                   │
│                                                                          │
│  SCENARIO 4: DLQ Filling Up                                               │
│  ───────────────────────────────                                          │
│  Symptom: Dead Letter topic has growing message count                     │
│  Resolution:                                                              │
│    1. Identify failure reason from DLQ message headers                    │
│    2. If transient (DB down): wait — messages will replay                 │
│    3. If permanent (bad data): fix upstream, then replay DLQ              │
│    4. If unrecoverable: archive DLQ messages, clear topic                 │
│                                                                          │
│  SCENARIO 5: Need to Reprocess Historical Data                            │
│  ───────────────────────────────                                          │
│  Resolution:                                                              │
│    1. Determine retention window (can only replay within retention)       │
│    2. If full replay needed and data exists:                              │
│       a. Stop the Streams application                                     │
│       b. Run kafka-streams-application-reset                              │
│       c. Restart the application                                          │
│    3. If side-by-side replay:                                             │
│       a. Create a new topic (orders-replay-v2)                            │
│       b. Use TimeRangeReplayService to copy relevant data                 │
│       c. Point a new Streams app at orders-replay-v2                      │
│       d. Validate results, then switch traffic                            │
└──────────────────────────────────────────────────────────────────────────┘
```

### 8.4 Prometheus Metrics & Grafana Dashboard

```yaml
# prometheus-kafka-rules.yml — Alerting Rules
groups:
  - name: kafka_streams
    rules:
      - alert: KafkaStreamsThreadDead
        expr: kafka_streams_thread_state{state="DEAD"} > 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Kafka Streams thread is DEAD"

      - alert: KafkaConsumerLagHigh
        expr: kafka_consumer_group_lag > 10000
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Consumer lag exceeds 10,000 messages"

      - alert: KafkaDLQRateHigh
        expr: rate(kafka_dlq_messages_total[5m]) > 10
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "High dead letter queue rate"

      - alert: KafkaUnderReplicatedPartitions
        expr: kafka_server_replicamanager_underreplicatedpartitions > 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Under-replicated partitions detected"

      - alert: KafkaSchemaRegistryDown
        expr: up{job="schema-registry"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Schema Registry is down"
```

---

## Appendix A: Quick Reference — Kafka Configuration Cheat Sheet

| Config | Recommended | Purpose |
|---|---|---|
| `acks` | `all` | Wait for all in-sync replicas |
| `enable.idempotence` | `true` | Deduplicate producer retries |
| `transactional.id` | unique per producer | Enable transactions |
| `isolation.level` | `read_committed` | Skip aborted transactions |
| `enable.auto.commit` | `false` | Manual offset control |
| `auto.offset.reset` | `earliest` | Where to start on first consume |
| `processing.guarantee` | `exactly_once_v2` | Kafka Streams EOS |
| `num.stream.threads` | = partition count | Max parallelism |
| `num.standby.replicas` | ≥ 1 | Faster failover |
| `compression.type` | `zstd` | Best compression ratio |
| `min.insync.replicas` | ≥ 2 | Durability floor |
| `retention.ms` | 7 days (intermediate: 1-3) | How long data lives |
| `cleanup.policy` | `delete` (or `compact` for KTables) | Retention strategy |

## Appendix B: Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|---|---|---|
| `auto.offset.reset=latest` | Missed messages on first start | Use `earliest` for streams, `latest` for alert consumers |
| Over-partitioning | Consumer waste, metadata overhead | Partition count = max expected parallelism |
| Under-partitioning | Can't scale consumers | Plan for growth; partitions can only increase |
| No schema registry | Breaking changes, unknown payloads | Always use Schema Registry with Avro/Protobuf |
| Mixing sync/async DB calls in processor | Blocks stream thread, causes lag | Offload to async, use external queues or reactive DB |
| Catching `Exception` broadly | Hides real errors, loses messages | Catch specific exceptions; use DLQ for unknown failures |
| `acks=1` in production | Data loss on leader failure | Use `acks=all` with `min.insync.replicas≥2` |
| No idempotency at application level | Duplicate side-effects | Always check/set idempotency keys in DB |
| Same transactional.id across instances | Producer fencing wars | Unique `transactional.id` per instance |
| Ignoring DLQ messages | Accumulating unrecoverable data | Monitor DLQ, alert on growth, have replay plan |
| `retention.ms=-1` (infinite) | Disk exhaustion | Set finite retention; use tiered storage for compliance |
| No compression | Wasted disk and network | Always enable `zstd` or `lz4` compression |
| Hardcoding topic/partition names | Inflexibility, environment drift | Configuration-driven topic names; use constants |

---

## Appendix C: Kafka Streams vs Alternatives

| Feature | Kafka Streams | Apache Flink | ksqlDB | Spark Streaming |
|---|---|---|---|---|
| **Deployment** | Library (JVM) | Cluster | Server + SQL | Cluster (Spark) |
| **State Management** | RocksDB (local) | RocksDB (managed) | RocksDB (managed) | Checkpoint-based |
| **Exactly-Once** | ✅ EOS-v2 | ✅ | ✅ | ✅ |
| **Language** | Java, Scala | Java, Scala, Python, SQL | SQL | Java, Scala, Python, SQL, R |
| **Windowing** | Tumbling, Hopping, Sliding, Session | Tumbling, Hopping, Sliding, Session, Custom | Tumbling, Hopping, Session | Tumbling, Sliding, Session |
| **Reprocessing** | Application reset | Savepoints | Query restart | Checkpoint recovery |
| **Interactive Queries** | ✅ Built-in | ❌ (external DB) | ✅ Pull queries | ❌ |
| **Operational Complexity** | Low (embedded) | Medium | Low (SQL) | High (Spark cluster) |
| **Best For** | Microservice streaming | Complex event processing | Real-time analytics | Batch + stream unified |

---

*End of Architecture Document — Kafka Streams & Advanced Messaging (C2)*
