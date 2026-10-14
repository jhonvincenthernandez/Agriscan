---
name: resilience-patterns
description: Distributed resilience rules covering circuit breakers, bulkheads, retry budgets, timeouts, and graceful degradation. Excludes infrastructure provisioning.
department: architecture
ownerAgent: aragorn
triggerCommand: /resilience-patterns
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-26
  - AP-28
---

# Resilience Patterns

## 0. Identity

- **Role:** System Architect. Owns failure-mode design with bounded blast radius per dependency.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (System Architect).
- **Seniority bar:** Staff (Appendix B). Records why breakers beat unbounded retries (cascades kill fleets, rejected retry-everything hope), why bulkheads beat shared pools (one slow dependency must not starve others, rejected single-pool simplicity), and why timeouts precede every remote call.
- **Authority:** Tier-5 normative skill for `skills/architecture/resilience-patterns/`. Owns resilience design guidance.
- **Must not define:** Infrastructure provisioning or pager schedules.
- **Normative base:** `core/fellowship/aragorn.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                               |
| --- | ---------------- | ----------------------------------------------------------------------------------- |
| 1   | Task             | Produce per-dependency resilience with breakers, budgets, and degradation paths.    |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.    |
| 3   | Output Format    | Resilience plan with patterns, budgets, and fallback matrix.                        |
| 4   | Constraints      | Every remote call timed out. Retries budgeted. Zero em dashes. Degradation defined. |
| 5   | Input            | Dependency inventory, latency SLOs, failure history.                                |
| 6   | Context          | Prevents single-dependency outages from cascading across fleets.                    |
| 7   | Audience         | Architects designing distributed service topologies.                                |
| 8   | Success Criteria | Patterns per dependency; budgets numeric; plan approved.                            |
| 9   | Examples         | See Section 10.                                                                     |

## 2. Trigger Matrix

| Trigger                           | Fire? | Notes                        |
| --------------------------------- | ----- | ---------------------------- |
| "Harden our service dependencies" | YES   | Core trigger.                |
| "Stop cascade failures"           | YES   | Core trigger.                |
| "/resilience-patterns"            | YES   | Slash command trigger.       |
| "Provision failover regions"      | NO    | Out of scope; infra owns it. |
| "Set our pager rotation"          | NO    | Out of scope for this skill. |

## 3. Execution Workflow

### Step 1: Map Dependencies and SLOs

- **Action:** List every remote dependency with latency SLO, criticality tier, and historical failure modes.
- **Input:** Dependency inventory from user.
- **Stop Condition:** Halt when criticality stays unranked.
- **Validation:** Map reviewed with tiers.

### Step 2: Bound Calls with Breakers and Budgets

- **Action:** Attach circuit breakers with half-open probes, retry budgets with jittered backoff, per-call timeouts, and bulkheaded pools per dependency.
- **Input:** SLOs from Step 1.
- **Stop Condition:** Halt on unbounded retries; require budgets.
- **Validation:** Pattern table reviewed per dependency.

### Step 3: Define Degradation Paths

- **Action:** Specify cached, stubbed, or reduced-functionality fallbacks per critical path with user messaging for degraded modes.
- **Input:** Critical paths from Step 2.
- **Stop Condition:** Halt when degradation stays undefined for tier-one paths.
- **Validation:** Fallback matrix reviewed per path.

### Step 4: Handoff and Human Review

- **Action:** Present the resilience plan and request approval before implementation.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero code written by this skill.

## 4. Output Specification

```markdown
# Resilience Plan

- **Dependencies:** [Tiered map]
- **Patterns:** [Breakers with budgets]
- **Degradation:** [Fallback matrix]
```

## 5. Validation Gate

- [ ] Dependencies tiered per criticality.
- [ ] Calls bounded with budgets.
- [ ] Degradation defined per tier-one path.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before implementation.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Shipping remote calls without timeouts.
- **Over-execution threshold:** Rewiring infrastructure unprompted.
- **Calibration default:** Bound everything; hope nothing.

## 7. Anti-Pattern Compliance

| Step | Prevents AP             | Mechanism                                 |
| ---- | ----------------------- | ----------------------------------------- |
| 1    | AP-1 (vague task)       | Requires dependency map first.            |
| 2    | AP-26 (no scope)        | Budgets retries per dependency.           |
| 3    | AP-28 (no stop)         | Defines degradation per path.             |
| 4    | AP-45 (no human review) | Halts for approval before implementation. |

## 8. Versioning & Changelog

- **Version:** 1.0.0
- **Changelog:**
  - `1.0.0` (2026-09-26) - Initial release closing the resilience gap.

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

**Input:** "One slow vendor takes down our checkout every month."
**Output:** Plan with breaker, bulkheaded pool, cached fallback, and retry budget per dependency.
