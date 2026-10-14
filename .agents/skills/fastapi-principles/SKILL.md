---
name: fastapi-principles
description: FastAPI production rules covering Pydantic boundary validation, async correctness, dependency injection, lifespan startup, and queue graduation. Excludes ML model training.
department: backend
ownerAgent: frodo
triggerCommand: /fastapi-principles
antiPatternsPrevented:
  - AP-1
  - AP-4
  - AP-6
  - AP-26
  - AP-28
---

# FastAPI Principles

## 0. Identity

- **Role:** Service Builder. Owns typed API implementation with boundary validation inside scoped files.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Service Builder).
- **Seniority bar:** Staff (Appendix B). Records why Pydantic boundaries beat scattered validation (framework rejects malformed data before handlers run, rejected manual if-chains), why async-correct routes beat async-everywhere (blocking calls freeze the loop, rejected blind async), and why real queues beat BackgroundTasks for durable work.
- **Authority:** Tier-5 normative skill for `skills/backend/fastapi-principles/`. Owns route, schema, and DI guidance.
- **Must not define:** ML model training or data pipeline orchestration.
- **Normative base:** `core/fellowship/frodo.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-4 (over-permissive execution), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                    |
| --- | ---------------- | ---------------------------------------------------------------------------------------- |
| 1   | Task             | Produce FastAPI services with validated contracts, correct async usage, and testable DI. |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.         |
| 3   | Output Format    | Service plan with schemas, dependencies, async map, and test strategy.                   |
| 4   | Constraints      | Pydantic at every boundary. Async only where awaited. Zero em dashes. No dict bodies.    |
| 5   | Input            | API spec, auth scheme, data model, concurrency needs.                                    |
| 6   | Context          | Prevents prototype-grade APIs from reaching production with unvalidated inputs.          |
| 7   | Audience         | Backend engineers shipping Python APIs and AI service layers.                            |
| 8   | Success Criteria | Contracts validated; async correct; DI testable; plan approved before coding.            |
| 9   | Examples         | See Section 10.                                                                          |

## 2. Trigger Matrix

| Trigger                                      | Fire? | Notes                         |
| -------------------------------------------- | ----- | ----------------------------- |
| "Build this API in FastAPI"                  | YES   | Core trigger.                 |
| "Fix blocking event loop and slow endpoints" | YES   | Core trigger.                 |
| "/fastapi-principles"                        | YES   | Slash command trigger.        |
| "Train our ML model"                         | NO    | Out of scope for this skill.  |
| "Build a Django monolith instead"            | NO    | Route to `django-principles`. |

## 3. Execution Workflow

### Step 1: Model Boundaries with Pydantic

- **Action:** Split request and response models per direction with field constraints and validators. Reject `dict` and `Any` bodies. Hide secrets and internal ids in response models.
- **Input:** API spec and data model.
- **Stop Condition:** Halt when endpoints accept untyped payloads; require schemas.
- **Validation:** Every route carries request plus response models.

### Step 2: Get Async Right

- **Action:** Use `async def` only where `await` runs inside, plain `def` for sync libraries offloaded to threadpools, and async SQLAlchemy or httpx clients on async paths. Never block the loop with sync calls, sleeps, or CPU work.
- **Input:** Concurrency needs and library inventory.
- **Stop Condition:** Halt when blocking calls sit inside async routes; require offload.
- **Validation:** Async map reviewed per route with client choices.

### Step 3: Inject, Start Up, and Offload

- **Action:** Wire DB sessions, auth, and config through chained `Depends` with yield cleanup and `dependency_overrides` test seams. Acquire pools once in lifespan, graduate durable work to real queues with 202 Accepted, and set explicit status codes plus tags per route.
- **Input:** Auth scheme and background needs.
- **Stop Condition:** Halt when globals replace injection or heavy work rides BackgroundTasks.
- **Validation:** DI graph reviewed with lifespan and queue decisions.

### Step 4: Handoff and Human Review

- **Action:** Present the plan and request approval before coding.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero code written by this skill.

## 4. Output Specification

```markdown
# FastAPI Plan

- **Schemas:** [Request plus response models]
- **Async:** [Route map with client choices]
- **DI:** [Dependency graph with test seams]
- **Jobs:** [Queue graduation decisions]
```

## 5. Validation Gate

- [ ] Every route carries typed schemas.
- [ ] Async correct per route with no loop blocks.
- [ ] DI testable via overrides.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before coding.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Shipping dict-bodied routes without schemas.
- **Over-execution threshold:** Building ML pipelines unprompted.
- **Calibration default:** Start simple; introduce DI layers as complexity earns them.

## 7. Anti-Pattern Compliance

| Step | Prevents AP             | Mechanism                             |
| ---- | ----------------------- | ------------------------------------- |
| 1    | AP-1 (vague task)       | Requires schemas before logic.        |
| 2    | AP-26 (no scope)        | Maps async correctly per route.       |
| 3    | AP-4 (over-permissive)  | Forces DI seams and queue graduation. |
| 4    | AP-45 (no human review) | Halts for approval before coding.     |

## 8. Versioning & Changelog

- **Version:** 1.0.0
- **Changelog:**
  - `1.0.0` (2026-09-26) - Initial release closing the Python API framework gap.

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

**Input:** "Build an inference gateway in FastAPI with auth and rate limits."
**Output:** Plan with Pydantic boundaries, async httpx fan-out, Depends auth chain, and Celery graduation for batch jobs.
