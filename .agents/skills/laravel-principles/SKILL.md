---
name: laravel-principles
description: Laravel 11.x and 12.x engineering rules covering thin controllers, Eloquent performance, Livewire and Inertia boundaries, security hardening, and Pest testing. Excludes frontend SPA builds.
department: backend
ownerAgent: frodo
triggerCommand: /laravel-principles
antiPatternsPrevented:
  - AP-1
  - AP-4
  - AP-6
  - AP-26
  - AP-28
---

# Laravel Principles

## 0. Identity

- **Role:** Service Builder. Owns Laravel feature implementation within framework conventions and scoped files.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Service Builder).
- **Seniority bar:** Staff (Appendix B).
- **Authority:** Tier-5 normative skill for `skills/backend/laravel-principles/`. Owns controller, Eloquent, and stack-boundary guidance.
- **Must not define:** Frontend UI layout or client-side hydration routines.
- **Normative base:** `core/fellowship/frodo.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-4 (over-permissive execution), AP-26 (no scope boundary), and AP-28 (no stop condition).
- **Staff judgment:** Records why thin controllers with Action classes beat fat-controller speed (testability compounds, rejected request-validate-inline shortcuts), why strict eager loading beats lazy convenience (N-plus-one taxes every collection view), and why Form Requests beat inline validation (authorization plus rules in one reviewable unit).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                            |
| --- | ---------------- | ------------------------------------------------------------------------------------------------ |
| 1   | Task             | Produce Laravel features with thin controllers, disciplined Eloquent use, and tested boundaries. |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.                 |
| 3   | Output Format    | Feature plan with actions, queries, stack boundaries, and test notes.                            |
| 4   | Constraints      | Strict types everywhere. Policies on every action. Zero em dashes. Pest over PHPUnit default.    |
| 5   | Input            | Feature spec, domain model, realtime needs, auth scheme.                                         |
| 6   | Context          | Prevents fat controllers, N-plus-one views, and unguarded mass assignment.                       |
| 7   | Audience         | Backend engineers shipping Laravel 11.x and 12.x products.                                       |
| 8   | Success Criteria | Controllers thin; queries batched; policies enforced; plan approved before coding.               |
| 9   | Examples         | See Section 10.                                                                                  |

## 2. Trigger Matrix

| Trigger                          | Fire? | Notes                             |
| -------------------------------- | ----- | --------------------------------- |
| "Build this feature in Laravel"  | YES   | Core trigger.                     |
| "Fix N-plus-one and auth gaps"   | YES   | Core trigger.                     |
| "/laravel-principles"            | YES   | Slash command trigger.            |
| "Build a React SPA client"       | NO    | Out of scope for this skill.      |
| "Administer our database server" | NO    | Out of scope; DBA runbook needed. |

## 3. Execution Workflow

### Step 1: Thin the HTTP Layer

- **Action:** Restrict controllers to request parsing, authorization, and response formatting. Declare `strict_types` first in every file, type all signatures, bind interfaces in providers, and validate exclusively through Form Request classes with `authorize` methods.
- **Input:** Feature spec and auth scheme.
- **Stop Condition:** Halt when business logic sits in controllers or validation runs inline.
- **Validation:** Controller audit complete with Action classes mapped per flow.

### Step 2: Discipline Eloquent and Schema

- **Action:** Guard mass assignment with `$fillable`, eager-load collections, wrap multi-table writes in transactions, cast via typed casts and backed enums, and constrain migrations with foreign keys plus composite indexes.
- **Input:** Domain model and hot paths.
- **Stop Condition:** Halt when a collection view lazy-loads; require eager loads.
- **Validation:** Query plan reviewed per hot path.

### Step 3: Bound Stacks and Harden Security

- **Action:** Keep Livewire state in Form Objects with locked properties, serve Inertia pages with typed API Resources instead of raw models, escape Blade output by default, enforce policies per action, authenticate via Sanctum or Fortify, and throttle auth endpoints.
- **Input:** Realtime needs and threat model.
- **Stop Condition:** Halt when an action lacks authorization or raw models cross to clients.
- **Validation:** Security checklist reviewed per surface.

### Step 4: Queue, Test, and Handoff

- **Action:** Offload slow work to idempotent queued jobs with retry limits and failure handlers. Guard races with atomic cache locks. Test with Pest feature specs on isolated databases, then present the plan for approval.
- **Input:** Background needs and test strategy.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero code written by this skill.

## 4. Output Specification

```markdown
# Laravel Plan

- **Controllers:** [Thin layer with Actions mapped]
- **Data:** [Eloquent discipline with indexes]
- **Security:** [Policies, auth, throttling per surface]
- **Tests:** [Pest specs with isolation notes]
```

## 5. Validation Gate

- [ ] Controllers thin with Actions mapped.
- [ ] Eager loading enforced on collections.
- [ ] Policies cover every action.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before coding.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Writing features without Action mapping.
- **Over-execution threshold:** Rewriting working apps unprompted.
- **Calibration default:** Convention first; custom machinery with receipts.

## 7. Anti-Pattern Compliance

| Step | Prevents AP             | Mechanism                         |
| ---- | ----------------------- | --------------------------------- |
| 1    | AP-1 (vague task)       | Requires controller audit first.  |
| 2    | AP-26 (no scope)        | Bounds queries with eager loads.  |
| 3    | AP-4 (over-permissive)  | Enforces policies per action.     |
| 4    | AP-45 (no human review) | Halts for approval before coding. |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Service Builder role and Staff trade-off records.
  - `1.0.0` - Legacy shared principles baseline.

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

**Input:** "Build order checkout in Laravel with queued receipts."
**Output:** Plan with Action-bounded checkout, transactional writes, idempotent receipt job, and Pest specs.
