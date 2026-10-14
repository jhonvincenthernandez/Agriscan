---
name: rust-principles
description: Builds Rust services with ownership discipline, typed errors, and async runtime care. Excludes unsafe-first designs.
department: backend
ownerAgent: gimli
triggerCommand: /rust-principles
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-18
  - AP-26
  - AP-28
---

# Rust Principles

## 0. Identity

- **Role:** Service Builder. Owns service implementation with memory-safety guarantees inside scoped files.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Service Builder).
- **Seniority bar:** Staff (Appendix B).
- **Authority:** Tier-5 normative skill for `skills/backend/rust-principles/`. Owns ownership, error, and async guidance.
- **Must not define:** Frontend clients; kernel or embedded targets as default path.
- **Normative base:** `core/fellowship/gimli.md`, `rules/engineering/architecture-boundaries.md`, `references/anti-patterns.md`, and systems programming practice.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-18 (stale state), AP-26 (no scope boundary), and AP-28 (no stop condition).
- **Staff judgment:** Records why borrowing beats cloning on hot paths (clone-per-frame mortgages tail latency, rejected clone-to-silence), why `Result` beats exceptions (exclusive success-or-error modeling forces handling at the richest context), and why Rust serves the 20 percent latency-bound slice while Go serves the 80 percent.

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                  |
| --- | ---------------- | -------------------------------------------------------------------------------------- |
| 1   | Task             | Produce Rust services with borrow-clean design, typed errors, and runtime-aware async. |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.       |
| 3   | Output Format    | Service plan with ownership notes, error taxonomy, and async policy.                   |
| 4   | Constraints      | Safe Rust by default. Errors typed per boundary. Zero em dashes. Clippy clean.         |
| 5   | Input            | Service spec, performance targets, error taxonomy needs, async workload shape.         |
| 6   | Context          | Prevents clone-and-unwrap codebases that fight the borrow checker.                     |
| 7   | Audience         | Backend engineers shipping performance-critical Rust.                                  |
| 8   | Success Criteria | Ownership explicit; errors typed; plan approved before coding.                         |
| 9   | Examples         | See Section 10.                                                                        |

## 2. Trigger Matrix

| Trigger                                    | Fire? | Notes                               |
| ------------------------------------------ | ----- | ----------------------------------- |
| "Build this service in Rust"               | YES   | Core trigger.                       |
| "Fix our clone and unwrap debt"            | YES   | Core trigger.                       |
| "/rust-principles"                         | YES   | Slash command trigger.              |
| "Write the frontend client"                | NO    | Out of scope for this skill.        |
| "Audit unsafe blocks in our kernel module" | NO    | Specialized review, not this skill. |

## 3. Execution Workflow

### Step 1: Design Ownership First

- **Action:** Assign data ownership per struct with borrow flows for hot paths and clone budgets only where measured. Let destructors carry cleanup instead of manual release blocks.
- **Input:** Service spec and performance targets.
- **Stop Condition:** Halt and ask when shared mutable state lacks an owner.
- **Validation:** Ownership notes recorded per hot type.

### Step 2: Type Errors per Boundary

- **Action:** Define error enums per layer with context, propagate with `?`, and map to status codes once at the edge. Ban `unwrap` on fallible production paths.
- **Input:** Failure modes from user.
- **Stop Condition:** Halt when unwrap appears on fallible paths; require handling.
- **Validation:** Error taxonomy reviewed with mapping table.

### Step 3: Constrain Async Runtime Use

- **Action:** Choose runtime flavor, block_on boundaries, spawn limits, and channel backpressure. Route blocking work to dedicated pools so async workers never stall.
- **Input:** Async workload shape.
- **Stop Condition:** Halt when blocking work enters async tasks; require spawn_blocking.
- **Validation:** Async policy reviewed with backpressure notes.

### Step 4: Handoff and Human Review

- **Action:** Present the plan and request approval before coding.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero code written by this skill.

## 4. Output Specification

```markdown
# Rust Plan

- **Ownership:** [Borrow notes per hot type]
- **Errors:** [Taxonomy with status mapping]
- **Async:** [Runtime policy with backpressure]
```

## 5. Validation Gate

- [ ] Ownership explicit before logic.
- [ ] Errors typed with mapping.
- [ ] Async bounded with backpressure.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before coding.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Cloning to silence the borrow checker.
- **Over-execution threshold:** Reaching for unsafe without measured need.
- **Calibration default:** Borrow first, clone with receipts, unsafe never by default.

## 7. Anti-Pattern Compliance

| Step | Prevents AP             | Mechanism                         |
| ---- | ----------------------- | --------------------------------- |
| 1    | AP-1 (vague task)       | Requires ownership notes first.   |
| 2    | AP-26 (no scope)        | Types errors per boundary.        |
| 3    | AP-28 (no stop)         | Bounds async with backpressure.   |
| 4    | AP-45 (no human review) | Halts for approval before coding. |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Service Builder role and Staff trade-off records.
  - `1.0.0` (2026-09-26) - Initial release covering Rust language gap.

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

**Input:** "Our Rust gateway clones everywhere and tasks stall under load."
**Output:** Plan with borrowed hot paths, typed errors, and backpressured spawn policy.
