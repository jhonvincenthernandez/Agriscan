---
name: grpc-protobuf-contracts
description: High-throughput gRPC service definitions, protocol buffer compilation, binary serialization, and client streaming.
department: backend
ownerAgent: aragorn
triggerCommand: /grpc-protobuf-contracts
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-18
  - AP-26
---

# gRPC Protobuf Contracts

## 0. Identity

- **Role:** API Designer. Owns binary contract specifications with compatibility rules and performance budgets.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (API Designer).
- **Seniority bar:** Staff (Appendix B). Records why protobuf contracts beat JSON for internal paths (binary efficiency with schema teeth, rejected untyped REST internally) and why field-number discipline beats casual schema edits.
- **Authority:** Normative specification under `skills/backend/grpc-protobuf-contracts/`.
- **Must not define:** Browser-facing client layouts.
- **Normative base:** `core/fellowship/frodo.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                    |
| --- | ---------------- | ---------------------------------------------------------------------------------------- |
| 1   | Task             | Define high-performance binary RPC interfaces and backward-compatible protobuf schemas.  |
| 2   | Target Tool      | Protocol Buffers compiler (protoc), gRPC Node, gRPC Go, Buf CLI.                         |
| 3   | Output Format    | Strict `.proto` schema definitions and compiled client/server stubs.                     |
| 4   | Constraints      | Field numbers are immutable once assigned. Deleted fields must use `reserved`.           |
| 5   | Input            | Microservice interface contracts and latency requirements.                               |
| 6   | Context          | Prevents serialization overhead, schema breaking changes, and cross-service RPC crashes. |
| 7   | Audience         | Backend engineers and distributed infrastructure architects.                             |
| 8   | Success Criteria | Sub-millisecond serialization overhead, zero field tag collisions, clean lint via Buf.   |
| 9   | Examples         | See Section 5.                                                                           |

## 2. Core Directives

1. **Field Number Permanence:** Never change, reuse, or renumber existing field tags. Deprecated fields must be designated `reserved`.
2. **Streaming Flow Control:** Use client/server streaming with backpressure windowing for payloads exceeding 4MB.
3. **Deadlines and Cancellation:** Every gRPC call must carry an explicit context deadline and listen for client cancellation signals.
4. **Metadata and Context Propagation:** Propagate OpenTelemetry trace context and request IDs across gRPC metadata headers.

## 3. Execution Workflow

### Step 1: Schema Authoring

- **Action:** Author proto definition following Buf style conventions (snake_case fields, CamelCase services).
- **Validation:** `buf lint` passes with zero errors.

### Step 2: Breaking Change Audit

- **Action:** Run `buf breaking --against .git#branch=main` before merging.
- **Validation:** No field numbers altered or removed without `reserved` markers.

## 4. Proto Schema Example

```protobuf
syntax = "proto3";

package billing.v1;

service PaymentGatewayService {
  rpc ProcessPayment (ProcessPaymentRequest) returns (ProcessPaymentResponse);
  rpc StreamPaymentEvents (StreamEventsRequest) returns (stream PaymentEvent);
}

message ProcessPaymentRequest {
  string transaction_id = 1;
  int64 amount_cents = 2;
  string currency = 3;
  reserved 4; // previously card_token
}

message ProcessPaymentResponse {
  enum Status {
    STATUS_UNSPECIFIED = 0;
    STATUS_SUCCESS = 1;
    STATUS_DECLINED = 2;
  }
  Status status = 1;
  string authorization_code = 2;
}
```
