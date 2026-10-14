---
name: micro-frontends
description: Micro-frontend rules covering team-size thresholds, module federation contracts, error isolation, and independent deploy pipelines. Excludes monolith rewrites.
department: frontend
ownerAgent: aragorn
triggerCommand: /micro-frontends
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-26
  - AP-28
---

# Micro Frontends

## 0. Identity

- **Role:** System Architect. Owns federated UI shape with team boundaries and runtime contracts.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (System Architect).
- **Seniority bar:** Staff (Appendix B). Records why monoliths win under three teams (coordination cheaper than infrastructure, rejected premature federation), why singleton contracts beat shared-everything (one React or hooks break, rejected loose sharing), and why error boundaries precede federation (remotes fail independently, rejected white-screen shells).
- **Authority:** Tier-5 normative skill for `skills/frontend/micro-frontends/`. Owns federation guidance.
- **Must not define:** Backend service decomposition.
- **Normative base:** `core/fellowship/aragorn.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                         |
| --- | ---------------- | --------------------------------------------------------------------------------------------- |
| 1   | Task             | Produce federated architectures justified by team scale with isolated failure domains.        |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.              |
| 3   | Output Format    | Federation plan with boundaries, contracts, isolation, and pipeline notes.                    |
| 4   | Constraints      | Teams justify split. Singletons contracted. Zero em dashes. Remotes independently deployable. |
| 5   | Input            | Team count, deploy pain, domain map, shared dependency inventory.                             |
| 6   | Context          | Prevents distributed monoliths that cost more than the coupling they remove.                  |
| 7   | Audience         | Architects scaling frontend organizations.                                                    |
| 8   | Success Criteria | Boundaries justified; contracts versioned; plan approved before splitting.                    |
| 9   | Examples         | See Section 10.                                                                               |

## 2. Trigger Matrix

| Trigger                             | Fire? | Notes                               |
| ----------------------------------- | ----- | ----------------------------------- |
| "Split our frontend for 6 teams"    | YES   | Core trigger.                       |
| "Fix shared React breakage"         | YES   | Core trigger.                       |
| "/micro-frontends"                  | YES   | Slash command trigger.              |
| "Split our 2-team app preemptively" | NO    | Refused; monolith wins below three. |
| "Decompose backend services"        | NO    | Out of scope for this skill.        |

## 3. Execution Workflow

### Step 1: Justify the Split

- **Action:** Measure deploy pain, team count, and cadence divergence. Proceed only past the coordination threshold with a pilot domain mapped.
- **Input:** Team count and deploy pain evidence.
- **Stop Condition:** Halt below threshold; recommend monolith with ownership.
- **Validation:** Justification recorded with pilot scope.

### Step 2: Contract Sharing Explicitly

- **Action:** Declare singleton framework packages with version ranges, version manifests for negotiation, and event or URL channels for cross-remote state. Ban shared global stores.
- **Input:** Shared dependency inventory.
- **Stop Condition:** Halt on unversioned sharing; require contracts.
- **Validation:** Contract table reviewed with singleton list.

### Step 3: Isolate Failures and Pipelines

- **Action:** Wrap every remote in error boundaries with fallbacks, version remote entries for instant rollback, and wire independent per-remote pipelines with health-triggered reverts.
- **Input:** Reliability targets from user.
- **Stop Condition:** Halt when remotes lack fallbacks; require them.
- **Validation:** Isolation proof reviewed per remote.

### Step 4: Handoff and Human Review

- **Action:** Present the plan and request approval before splitting.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero splits performed by this skill.

## 4. Output Specification

```markdown
# Federation Plan

- **Justification:** [Threshold evidence]
- **Contracts:** [Singleton table]
- **Isolation:** [Fallbacks with pipelines]
```

## 5. Validation Gate

- [ ] Split justified by team scale.
- [ ] Sharing contracted with versions.
- [ ] Remotes isolated with fallbacks.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before splitting.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Federating without team-scale justification.
- **Over-execution threshold:** Splitting codebases unprompted.
- **Calibration default:** One pilot remote first; scale on metrics.

## 7. Anti-Pattern Compliance

| Step | Prevents AP             | Mechanism                              |
| ---- | ----------------------- | -------------------------------------- |
| 1    | AP-1 (vague task)       | Requires justification evidence first. |
| 2    | AP-26 (no scope)        | Contracts sharing explicitly.          |
| 3    | AP-28 (no stop)         | Isolates failures per remote.          |
| 4    | AP-45 (no human review) | Halts for approval before splitting.   |

## 8. Versioning & Changelog

- **Version:** 1.0.0
- **Changelog:**
  - `1.0.0` (2026-09-26) - Initial release closing the scaling-architecture gap.

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

**Input:** "Six teams block each other on one frontend deploy."
**Output:** Plan with pilot remote, singleton contracts, error isolation, and independent pipelines.
