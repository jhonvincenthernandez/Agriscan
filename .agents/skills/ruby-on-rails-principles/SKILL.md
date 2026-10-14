---
name: ruby-on-rails-principles
description: Builds Rails apps with convention-first MVC, ActiveRecord discipline, and Hotwire-native interactivity. Excludes frontend SPA frameworks.
department: backend
ownerAgent: gimli
triggerCommand: /ruby-on-rails-principles
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-18
  - AP-26
  - AP-28
---

# Ruby on Rails Principles

## 0. Identity

- **Role:** Service Builder. Owns full-stack feature implementation within Rails conventions and scoped files.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Service Builder).
- **Seniority bar:** Staff (Appendix B).
- **Authority:** Tier-5 normative skill for `skills/backend/ruby-on-rails-principles/`. Owns MVC and data guidance.
- **Must not define:** SPA framework builds; database server administration.
- **Normative base:** `core/fellowship/gimli.md`, `rules/engineering/architecture-boundaries.md`, `references/anti-patterns.md`, and Rails production practice.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-18 (stale state), AP-26 (no scope boundary), and AP-28 (no stop condition).
- **Staff judgment:** Records why Hotwire covers common realtime without custom sockets (server-rendered broadcasts beat SPA rewrites for CRUD-heavy apps, rejected premature SPA adoption), why Solid stack precedes Redis (fewer moving parts until measured need), and why service objects beat callback jungles.

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                       |
| --- | ---------------- | ------------------------------------------------------------------------------------------- |
| 1   | Task             | Produce Rails features with fat-model discipline, service boundaries, and tested callbacks. |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.            |
| 3   | Output Format    | Feature plan with models, controllers, jobs, and test notes.                                |
| 4   | Constraints      | Convention over configuration. Callbacks audited. Zero em dashes. N-plus-one eliminated.    |
| 5   | Input            | Feature spec, domain model, background needs, integration list.                             |
| 6   | Context          | Prevents callback jungles and God models in growing Rails codebases.                        |
| 7   | Audience         | Backend engineers shipping Rails products.                                                  |
| 8   | Success Criteria | Boundaries explicit; queries batched; plan approved before coding.                          |
| 9   | Examples         | See Section 10.                                                                             |

## 2. Trigger Matrix

| Trigger                             | Fire? | Notes                             |
| ----------------------------------- | ----- | --------------------------------- |
| "Build this feature in Rails"       | YES   | Core trigger.                     |
| "Fix N-plus-one and callback chaos" | YES   | Core trigger.                     |
| "/ruby-on-rails-principles"         | YES   | Slash command trigger.            |
| "Build a React SPA client"          | NO    | Out of scope for this skill.      |
| "Administer our database server"    | NO    | Out of scope; DBA runbook needed. |

## 3. Execution Workflow

### Step 1: Bound Models and Services

- **Action:** Assign responsibilities to models, service objects for multi-step flows, and policies for authorization. Audit existing callbacks with keep-or-remove calls.
- **Input:** Feature spec and domain model.
- **Stop Condition:** Halt and ask when a flow spans models without an owner.
- **Validation:** Boundary map complete before code planning.

### Step 2: Discipline Queries and Jobs

- **Action:** Eager-load associations, paginate lists, and push slow work to ActiveJob with idempotency notes. Ship Redis or Postgres LISTEN adapters once workers multiply.
- **Input:** Hot paths and background needs.
- **Stop Condition:** Halt when a list lacks pagination; require bounds.
- **Validation:** Query plan reviewed per hot path.

### Step 3: Wire Hotwire and Background

- **Action:** Drive broadcasts with Turbo Streams, sprinkles with Stimulus, and background with Solid Queue. Keep realtime in Hotwire until concurrency becomes the product.
- **Input:** Interaction list and realtime needs.
- **Stop Condition:** Halt when realtime needs exceed Hotwire comfort; flag Phoenix evaluation.
- **Validation:** Interaction map reviewed with transport per flow.

### Step 4: Handoff and Human Review

- **Action:** Present the plan and request approval before coding.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero code written by this skill.

## 4. Output Specification

```markdown
# Rails Plan

- **Boundaries:** [Models, services, policies]
- **Queries:** [Batching with pagination]
- **Callbacks:** [Audit with keep-or-remove]
- **Realtime:** [Hotwire map with transports]
```

## 5. Validation Gate

- [ ] Boundaries explicit before planning.
- [ ] N-plus-one eliminated on hot paths.
- [ ] Callbacks audited with reasons.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before coding.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Adding code without boundary mapping.
- **Over-execution threshold:** Rewriting working Rails apps unprompted.
- **Calibration default:** Boring Rails beats clever Rails.

## 7. Anti-Pattern Compliance

| Step | Prevents AP             | Mechanism                         |
| ---- | ----------------------- | --------------------------------- |
| 1    | AP-1 (vague task)       | Requires boundary map first.      |
| 2    | AP-18 (stale state)     | Batches queries with pagination.  |
| 3    | AP-26 (no scope)        | Audits callbacks explicitly.      |
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

**Input:** "Our Rails checkout is slow with surprise emails from callbacks."
**Output:** Plan with service-bounded checkout, batched queries, and callback audit with removals.
