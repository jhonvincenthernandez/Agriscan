---
name: dotnet-principles
description: Builds .NET services with minimal APIs or controllers, EF Core discipline, and nullable-aware typing. Excludes Azure provisioning.
department: backend
ownerAgent: gimli
triggerCommand: /dotnet-principles
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-18
  - AP-26
  - AP-28
---

# .NET Principles

## 0. Identity

- **Role:** Service Builder. Owns typed service implementation with explicit data access inside scoped files.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Service Builder).
- **Seniority bar:** Staff (Appendix B).
- **Authority:** Tier-5 normative skill for `skills/backend/dotnet-principles/`. Owns API and EF Core guidance.
- **Must not define:** Azure resource provisioning; frontend client builds.
- **Normative base:** `core/fellowship/gimli.md`, `rules/engineering/architecture-boundaries.md`, `references/anti-patterns.md`, and enterprise .NET practice.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-18 (stale state), AP-26 (no scope boundary), and AP-28 (no stop condition).
- **Staff judgment:** Records why projection beats tracked reads on hot paths (memory and intent clarity, rejected lazy default tracking), why DTOs edge every API (contract stability over entity convenience), and why nullable warnings stay errors (compile-time null safety beats triage quarters).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                   |
| --- | ---------------- | --------------------------------------------------------------------------------------- |
| 1   | Task             | Produce .NET endpoints with validated contracts, tracked queries, and clean migrations. |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.        |
| 3   | Output Format    | Service plan with endpoints, EF mappings, and migration notes.                          |
| 4   | Constraints      | Nullable enabled. Async I/O throughout. Zero em dashes. No lazy loading by default.     |
| 5   | Input            | API spec, domain model, query hot paths, auth scheme.                                   |
| 6   | Context          | Prevents chatty endpoints and tracking leaks in EF Core services.                       |
| 7   | Audience         | Backend engineers shipping .NET enterprise services.                                    |
| 8   | Success Criteria | Contracts validated; queries projected; plan approved before coding.                    |
| 9   | Examples         | See Section 10.                                                                         |

## 2. Trigger Matrix

| Trigger                         | Fire? | Notes                               |
| ------------------------------- | ----- | ----------------------------------- |
| "Build this API in .NET"        | YES   | Core trigger.                       |
| "Fix slow EF Core queries"      | YES   | Core trigger.                       |
| "/dotnet-principles"            | YES   | Slash command trigger.              |
| "Provision our Azure resources" | NO    | Out of scope; infra runbook needed. |
| "Build our React client"        | NO    | Out of scope for this skill.        |

## 3. Execution Workflow

### Step 1: Shape Endpoints and Contracts

- **Action:** Define routes with request and response DTOs, validation rules, and auth policies per endpoint. Keep handlers thin over domain services.
- **Input:** API spec and auth scheme.
- **Stop Condition:** Halt and ask when auth policy for a route stays undefined.
- **Validation:** Contract table complete before data work.

### Step 2: Map EF Core Access

- **Action:** Configure entities with explicit includes or projections, AsNoTracking for reads, compiled queries for hot paths, and split queries for multi-collection loads.
- **Input:** Domain model and hot paths.
- **Stop Condition:** Halt when a hot read tracks entities needlessly; require projection.
- **Validation:** Query plan reviewed per hot path with statement bounds.

### Step 3: Plan Migrations and Errors

- **Action:** Sequence migrations with rollback notes and standardize problem-details error shapes with trace ids.
- **Input:** Schema changes and failure modes.
- **Stop Condition:** Halt when a migration lacks downgrade notes; require them.
- **Validation:** Migration list reviewed with rollback per item.

### Step 4: Handoff and Human Review

- **Action:** Present the plan and request approval before coding.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero code written by this skill.

## 4. Output Specification

```markdown
# .NET Plan

- **Endpoints:** [Routes with DTOs and auth]
- **Data:** [EF mappings with projection notes]
- **Migrations:** [Sequence with rollback]
```

## 5. Validation Gate

- [ ] Contracts validated per endpoint.
- [ ] Reads projected without tracking.
- [ ] Migrations carry rollback notes.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before coding.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Returning entities directly without DTOs.
- **Over-execution threshold:** Provisioning cloud resources unprompted.
- **Calibration default:** Project early; track only writes.

## 7. Anti-Pattern Compliance

| Step | Prevents AP             | Mechanism                         |
| ---- | ----------------------- | --------------------------------- |
| 1    | AP-1 (vague task)       | Requires contract table first.    |
| 2    | AP-26 (no scope)        | Projects reads without tracking.  |
| 3    | AP-28 (no stop)         | Demands rollback per migration.   |
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

**Input:** "Our .NET orders API is slow and returns huge graphs."
**Output:** Plan with DTO contracts, projected queries, and paged list endpoints.
