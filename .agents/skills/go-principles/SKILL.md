---
name: go-principles
description: Builds Go microservices with context-first I/O, bounded worker pools, outbox events, saga compensation, and graceful shutdown. Excludes frontend client builds.
department: backend
ownerAgent: gimli
triggerCommand: /go-principles
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-18
  - AP-26
  - AP-28
---

# Go Principles

## 0. Identity

- **Role:** Service Builder. Owns service implementation with reliability guarantees inside scoped files.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Service Builder).
- **Seniority bar:** Staff (Appendix B).
- **Authority:** Tier-5 normative skill for `skills/backend/go-principles/`. Owns layout, error, and concurrency guidance.
- **Must not define:** Frontend clients; infrastructure provisioning.
- **Normative base:** `core/fellowship/gimli.md`, `rules/engineering/architecture-boundaries.md`, `references/anti-patterns.md`, and production Go microservice practice.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-18 (stale state), AP-26 (no scope boundary), and AP-28 (no stop condition).
- **Staff judgment:** Records why bounded pools beat unbounded goroutines (bursts exhaust connection pools, rejected spawn-per-message), why outbox beats dual-write (crash gaps lose events permanently), and why gRPC serves internal calls while REST serves public ones.

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                     |
| --- | ---------------- | ----------------------------------------------------------------------------------------- |
| 1   | Task             | Produce Go services with clean layout, handled errors, and bounded concurrency.           |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.          |
| 3   | Output Format    | Service plan with layout, error policy, and concurrency notes.                            |
| 4   | Constraints      | Errors handled, never ignored. Contexts cancel work. Zero em dashes. Race detector clean. |
| 5   | Input            | API spec, concurrency needs, dependency list, latency budget.                             |
| 6   | Context          | Prevents goroutine leaks and swallowed errors in production Go.                           |
| 7   | Audience         | Backend engineers shipping Go microservices and CLIs.                                     |
| 8   | Success Criteria | Layout standard; errors explicit; plan approved before coding.                            |
| 9   | Examples         | See Section 10.                                                                           |

## 2. Trigger Matrix

| Trigger                                  | Fire? | Notes                               |
| ---------------------------------------- | ----- | ----------------------------------- |
| "Build this microservice in Go"          | YES   | Core trigger.                       |
| "Fix goroutine leaks and error swallows" | YES   | Core trigger.                       |
| "/go-principles"                         | YES   | Slash command trigger.              |
| "Build our web frontend"                 | NO    | Out of scope for this skill.        |
| "Provision our servers"                  | NO    | Out of scope; infra runbook needed. |

## 3. Execution Workflow

### Step 1: Lay Out Packages and Contexts

- **Action:** Structure cmd, internal, and pkg boundaries with imports flowing into internal only. Thread `context.Context` with timeouts through every I/O call so cancellation and deadlines compose down the chain.
- **Input:** Service spec and dependency list.
- **Stop Condition:** Halt when package ownership stays unclear or any blocking call lacks a deadline.
- **Validation:** Layout recorded with import rules; every I/O path carries a context.

### Step 2: Harden Errors and Bound Concurrency

- **Action:** Wrap errors with context at boundaries and never ignore return values. Gate fan-out with semaphore worker pools, retry transient faults with jittered backoff, and open circuit breakers at sustained failure rates.
- **Input:** Failure modes and latency budget.
- **Stop Condition:** Halt when an error return goes unchecked or goroutine lifetime lacks an owner.
- **Validation:** Error policy reviewed with timeout table; pool sizes and shutdown ownership recorded.

### Step 3: Guarantee Event Delivery

- **Action:** Write business state plus outbox rows atomically with CDC publishing afterward. Make every consumer idempotent via processed-ID tracking. Compensate distributed flows with sagas, choreographed for linear flows and orchestrated for branching ones.
- **Input:** Event inventory and consistency needs.
- **Stop Condition:** Halt when a consumer cannot prove idempotency; mark as finding.
- **Validation:** Outbox, dedup, and saga notes reviewed per flow.

### Step 4: Handoff and Human Review

- **Action:** Present the plan and request approval before coding.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero code written by this skill.

## 4. Output Specification

```markdown
# Go Plan

- **Layout:** [Packages with import rules]
- **Errors:** [Policy with timeout table]
- **Concurrency:** [Pools with shutdown notes]
- **Events:** [Outbox and saga notes]
```

## 5. Validation Gate

- [ ] Layout recorded with import rules.
- [ ] Errors handled with context and timeouts.
- [ ] Concurrency bounded with owners.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before coding.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Spawning goroutines without owners or shutdown.
- **Over-execution threshold:** Building frameworks instead of services.
- **Calibration default:** Stdlib first; every dependency must earn its import.

## 7. Anti-Pattern Compliance

| Step | Prevents AP             | Mechanism                                   |
| ---- | ----------------------- | ------------------------------------------- |
| 1    | AP-1 (vague task)       | Requires layout before logic.               |
| 2    | AP-26 (no scope)        | Forces error handling per boundary.         |
| 3    | AP-28 (no stop)         | Demands idempotency and shutdown ownership. |
| 4    | AP-45 (no human review) | Halts for approval before coding.           |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Service Builder role and Staff trade-off records.
  - `1.0.0` (2026-09-26) - Initial release covering Go language gap.

## 9. Portability Matrix

| Runtime     | Status   | Notes                           |
| ----------- | -------- | ------------------------------- |
| Claude Code | verified | Direct slash command execution. |
| Cursor      | verified | Rules and prompt loading.       |
| Copilot     | verified | Custom instructions support.    |
| Windsurf    | verified | Cascade flow integration.       |
| Kiro        | verified | Steering model execution.       |
| Cline       | verified | Task step-by-step flow.         |
| Raw API     | verified | Model-agnostic execution.       |

## 10. Examples

**Input:** "Build a webhook ingestor in Go that never loses messages."
**Output:** Plan with bounded worker pool, context-cancelled handlers, outbox-backed delivery, and explicit error wrapping.
