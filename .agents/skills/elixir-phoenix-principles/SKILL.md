---
name: elixir-phoenix-principles
description: Builds Elixir and Phoenix systems with OTP supervision, Ecto discipline, and LiveView-native interactivity. Excludes frontend SPA builds.
department: backend
ownerAgent: gimli
triggerCommand: /elixir-phoenix-principles
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-18
  - AP-26
  - AP-28
---

# Elixir Phoenix Principles

## 0. Identity

- **Role:** Service Builder. Owns fault-tolerant service implementation with supervised processes inside scoped files.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Service Builder).
- **Seniority bar:** Staff (Appendix B).
- **Authority:** Tier-5 normative skill for `skills/backend/elixir-phoenix-principles/`. Owns OTP and Ecto guidance.
- **Must not define:** SPA client builds; infrastructure provisioning.
- **Normative base:** `core/fellowship/gimli.md`, `rules/engineering/architecture-boundaries.md`, `references/anti-patterns.md`, and BEAM production practice.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-18 (stale state), AP-26 (no scope boundary), and AP-28 (no stop condition).
- **Staff judgment:** Records why LiveView replaces realtime JavaScript where concurrency is the product (single socket with server-held state, rejected dual-socket Hotwire shapes for collaborative loads), why changesets beat callbacks (explicit validation order over framework magic), and why strangler migration beats rewrites (every step ships value independently).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                        |
| --- | ---------------- | -------------------------------------------------------------------------------------------- |
| 1   | Task             | Produce Phoenix contexts with supervised processes, changesets, and LiveView flows.          |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.             |
| 3   | Output Format    | System plan with contexts, supervision trees, and LiveView notes.                            |
| 4   | Constraints      | Contexts bound domains. Changesets validate. Zero em dashes. Let it crash under supervisors. |
| 5   | Input            | Domain spec, concurrency needs, realtime flows, integration list.                            |
| 6   | Context          | Prevents god contexts and unvalidated writes in concurrent systems.                          |
| 7   | Audience         | Backend engineers shipping Elixir services.                                                  |
| 8   | Success Criteria | Contexts bounded; supervision explicit; plan approved before coding.                         |
| 9   | Examples         | See Section 10.                                                                              |

## 2. Trigger Matrix

| Trigger                               | Fire? | Notes                               |
| ------------------------------------- | ----- | ----------------------------------- |
| "Build this service in Phoenix"       | YES   | Core trigger.                       |
| "Fix our LiveView memory and crashes" | YES   | Core trigger.                       |
| "/elixir-phoenix-principles"          | YES   | Slash command trigger.              |
| "Build a React SPA client"            | NO    | Out of scope for this skill.        |
| "Provision our servers"               | NO    | Out of scope; infra runbook needed. |

## 3. Execution Workflow

### Step 1: Bound Contexts

- **Action:** Split the domain into contexts with public functions hiding schemas from web layers. Keep business logic out of LiveView handlers.
- **Input:** Domain spec.
- **Stop Condition:** Halt and ask when two contexts share tables directly.
- **Validation:** Context map complete before process design.

### Step 2: Supervise Processes

- **Action:** Place workers under supervision trees with restart strategies matched to failure modes. Prefer Oban over Redis-backed queues and ETS for node-local cache.
- **Input:** Concurrency needs from user.
- **Stop Condition:** Halt when a critical worker runs unsupervised; require a supervisor.
- **Validation:** Supervision tree reviewed per worker.

### Step 3: Validate with Changesets and LiveView

- **Action:** Gate writes with changesets and build LiveView flows with stream bounds for large lists. Track presence with built-in distributed primitives instead of hand-rolled classes.
- **Input:** Write paths and realtime flows.
- **Stop Condition:** Halt when writes skip changesets; require them.
- **Validation:** Changeset coverage reviewed per write path.

### Step 4: Handoff and Human Review

- **Action:** Present the plan and request approval before coding.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero code written by this skill.

## 4. Output Specification

```markdown
# Phoenix Plan

- **Contexts:** [Bounded domains]
- **Supervision:** [Trees with strategies]
- **LiveView:** [Flows with stream bounds]
```

## 5. Validation Gate

- [ ] Contexts bounded before design.
- [ ] Workers supervised with strategies.
- [ ] Writes gated by changesets.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before coding.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Writing schemas without context boundaries.
- **Over-execution threshold:** Provisioning servers unprompted.
- **Calibration default:** Small contexts with explicit APIs.

## 7. Anti-Pattern Compliance

| Step | Prevents AP             | Mechanism                         |
| ---- | ----------------------- | --------------------------------- |
| 1    | AP-1 (vague task)       | Requires context map first.       |
| 2    | AP-26 (no scope)        | Supervises every worker.          |
| 3    | AP-18 (stale state)     | Gates writes with changesets.     |
| 4    | AP-45 (no human review) | Halts for approval before coding. |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Service Builder role and Staff trade-off records.
  - `1.0.0` (2026-09-26) - Initial release covering legacy backend.

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

**Input:** "Our Phoenix chat drops connections and LiveView leaks memory."
**Output:** Plan with presence supervision, stream-bounded lists, and changeset-gated writes.
