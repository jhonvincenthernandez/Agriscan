---
name: django-principles
description: Django plus DRF production rules covering settings splits, N-plus-one elimination, throttling, object permissions, versioning, and deploy hardening. Excludes frontend SPA builds.
department: backend
ownerAgent: frodo
triggerCommand: /django-principles
antiPatternsPrevented:
  - AP-1
  - AP-4
  - AP-6
  - AP-26
  - AP-28
---

# Django Principles

## 0. Identity

- **Role:** Service Builder. Owns batteries-included product implementation with secure defaults inside scoped files.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Service Builder).
- **Seniority bar:** Staff (Appendix B). Records why select-related plus prefetch beats lazy traversal (N-plus-one dominates Django slowness, rejected default querysets on list views), why explicit fields beat `__all__` serializers (mass-assignment surface, rejected convenience wildcards), and why check-deploy gates beat hope in production settings.
- **Authority:** Tier-5 normative skill for `skills/backend/django-principles/`. Owns Django and DRF guidance.
- **Must not define:** Frontend SPA builds; database server administration.
- **Normative base:** `core/fellowship/frodo.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-4 (over-permissive access), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                   |
| --- | ---------------- | --------------------------------------------------------------------------------------- |
| 1   | Task             | Produce Django services with split settings, optimized querysets, and hardened deploys. |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.        |
| 3   | Output Format    | Service plan with settings, queryset, API, and hardening notes.                         |
| 4   | Constraints      | DEBUG False in prod. Paginate every list. Zero em dashes. Check-deploy green in CI.     |
| 5   | Input            | Product spec, auth model, API surface, traffic shape.                                   |
| 6   | Context          | Prevents N-plus-one list views and debug-mode production leaks.                         |
| 7   | Audience         | Backend engineers shipping Django monoliths and DRF APIs.                               |
| 8   | Success Criteria | Querysets batched; auth default-deny; hardening green; plan approved before coding.     |
| 9   | Examples         | See Section 10.                                                                         |

## 2. Trigger Matrix

| Trigger                              | Fire? | Notes                          |
| ------------------------------------ | ----- | ------------------------------ |
| "Build this product in Django"       | YES   | Core trigger.                  |
| "Fix slow DRF lists and auth gaps"   | YES   | Core trigger.                  |
| "/django-principles"                 | YES   | Slash command trigger.         |
| "Build a React SPA client"           | NO    | Out of scope for this skill.   |
| "Serve ML inference over websockets" | NO    | Route to `fastapi-principles`. |

## 3. Execution Workflow

### Step 1: Split Settings and Structure Apps

- **Action:** Divide settings into base, dev, and prod packages with env-sourced secrets. Organize many small focused apps instead of one core monolith.
- **Input:** Product spec and environment matrix.
- **Stop Condition:** Halt when secrets sit in settings files; require env sourcing.
- **Validation:** Settings review complete with secret audit.

### Step 2: Kill N-plus-one in Querysets

- **Action:** Apply select_related on forward relations, prefetch_related on collections, only and defer on wide tables, and annotations for counts. Verify with debug toolbar query counts.
- **Input:** List endpoints and serializer fields.
- **Stop Condition:** Halt when list views query per object; require batching.
- **Validation:** Query counts bounded per endpoint with evidence.

### Step 3: Secure and Version the API

- **Action:** Default permissions to authenticated with object-level checks, throttle sensitive endpoints per scope, version namespaces from day one, paginate every list, and harden deploys with real hosts, scoped CORS, HTTPS, and check-deploy in CI.
- **Input:** Auth model and API surface.
- **Stop Condition:** Halt when AllowAny ships or DEBUG stays true for prod.
- **Validation:** Auth matrix plus hardening checklist reviewed.

### Step 4: Handoff and Human Review

- **Action:** Present the plan and request approval before coding.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero code written by this skill.

## 4. Output Specification

```markdown
# Django Plan

- **Settings:** [Split packages with secret audit]
- **Querysets:** [Batching per endpoint with counts]
- **API:** [Auth, throttle, versioning per surface]
- **Hardening:** [Deploy checklist with CI gate]
```

## 5. Validation Gate

- [ ] Settings split with secrets in env.
- [ ] N-plus-one eliminated with evidence.
- [ ] Auth default-deny with object checks.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before coding.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Shipping `__all__` serializers with AllowAny defaults.
- **Over-execution threshold:** Rewriting working monoliths unprompted.
- **Calibration default:** Batteries included first; custom machinery with receipts.

## 7. Anti-Pattern Compliance

| Step | Prevents AP             | Mechanism                                   |
| ---- | ----------------------- | ------------------------------------------- |
| 1    | AP-1 (vague task)       | Requires settings and app map first.        |
| 2    | AP-26 (no scope)        | Bounds queries per endpoint.                |
| 3    | AP-4 (over-permissive)  | Denies auth by default with hardening gate. |
| 4    | AP-45 (no human review) | Halts for approval before coding.           |

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

**Input:** "Build a marketplace API in Django with seller isolation."
**Output:** Plan with split settings, prefetched catalog querysets, object-level seller permissions, and versioned throttled endpoints.
