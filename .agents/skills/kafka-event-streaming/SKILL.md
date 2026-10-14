---
name: kafka-event-streaming
description: Distributed event messaging, consumer group offset management, idempotent producer semantics, and dead-letter queues.
department: backend
ownerAgent: frodo
triggerCommand: /kafka-event-streaming
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-18
  - AP-26
---

# Kafka Event Streaming Patterns

## 0. Identity

- **Role:** Pipeline Builder. Owns staged event pipeline topology with partitioning and delivery semantics.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Pipeline Builder).
- **Seniority bar:** Staff (Appendix B). Records why exactly-once semantics beat at-most-once fire-and-forget (duplicates corrupt projections, rejected no-guarantee publishing) and why consumer-group discipline precedes throughput tuning.
- **Authority:** Normative specification under `skills/backend/kafka-event-streaming/`.
- **Must not define:** Synchronous HTTP REST payload contracts.
- **Normative base:** `core/fellowship/frodo.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                     |
| --- | ---------------- | ----------------------------------------------------------------------------------------- |
| 1   | Task             | Architect fault-tolerant event streams, schema evolution, and dead-letter pipelines.      |
| 2   | Target Tool      | Apache Kafka, Confluent Cloud, Redpanda, KafkaJS, Sarama.                                 |
| 3   | Output Format    | Event schemas (Avro/JSON Schema), producer configuration profiles, consumer topologies.   |
| 4   | Constraints      | Enable idempotent producers (`enable.idempotence=true`). Enforce explicit partition keys. |
| 5   | Input            | Business transaction streams, domain events, integration contracts.                       |
| 6   | Context          | Prevents message loss, out-of-order event consumption, and consumer group starvation.     |
| 7   | Audience         | Distributed backend engineers and data platform specialists.                              |
| 8   | Success Criteria | Zero uncommitted offset data loss, deterministic consumer lag recovery under stress.      |
| 9   | Examples         | See Section 5.                                                                            |

## 2. Trigger Matrix

| Trigger                                             | Fire? | Notes                       |
| --------------------------------------------------- | ----- | --------------------------- |
| Designing asynchronous event-driven architectures   | YES   | Core messaging pattern.     |
| Handling out-of-order event streams and rebalancing | YES   | Partition key strategy.     |
| Quarantining unprocessable poison-pill messages     | YES   | Dead-letter queue pipeline. |
| Simple synchronous point-to-point RPC               | NO    | Route to gRPC or REST.      |

## 3. Reliability Directives

1. **Producer Semantics:** Always set `acks=all`, `retries=MAX_INT`, and keep `max.in.flight.requests.per.connection <= 5`.
2. **Consumer Offset Commit Strategy:** Commit offsets synchronously only after downstream business persistence transaction succeeds.
3. **Dead-Letter Queue (DLQ) Quarantine:** Route unparseable or continuously failing messages to a dedicated DLQ topic after 3 retries with exponential backoff.
4. **Schema Evolution:** Enforce backward and forward compatibility rules via schema registry to prevent consumer crashes.

## 4. Execution Workflow

### Step 1: Partitioning Key Selection

- **Action:** Select partition keys based on business ordering boundaries (such as `orderId` or `userId`).
- **Validation:** Zero partition hotspots; traffic evenly distributed across broker partitions.

### Step 2: Idempotent Consumer Processing

- **Action:** Implement deduplication checks using database transaction unique constraints before applying state mutations.
- **Validation:** Re-delivering duplicate events produces identical persistent state.

## 5. Consumer Configuration Example

```typescript
const consumer = kafka.consumer({
  groupId: "order-billing-sync",
  retry: { retries: 5 },
});

await consumer.run({
  autoCommit: false,
  eachMessage: async ({ topic, partition, message }) => {
    try {
      await processBillingTransaction(message.value);
      await consumer.commitOffsets([
        { topic, partition, offset: (BigInt(message.offset) + 1n).toString() },
      ]);
    } catch (err) {
      await routeToDeadLetterQueue(topic, message, err);
      await consumer.commitOffsets([
        { topic, partition, offset: (BigInt(message.offset) + 1n).toString() },
      ]);
    }
  },
});
```
