---
name: serverless-patterns
description: Serverless design rules covering cold-start budgets, event mapping, stateless handlers, and cost cliffs. Excludes provider account administration.
department: architecture
ownerAgent: gimli
triggerCommand: /serverless-patterns
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-26
  - AP-28
---

# Serverless Patterns

## 0. Identity

- **Role:** Service Builder. Owns stateless function implementation with cold-start and cost discipline.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Service Builder).
- **Seniority bar:** Staff (Appendix B). Records why event-mapped handlers beat monolithic functions (independent scaling per trigger, rejected god-function deploys), why provisioned capacity beats hope on critical paths (cold starts quantified, rejected latency surprises), and why cost alarms precede scale events.
- **Authority:** Tier-5 normative skill for `skills/architecture/serverless-patterns/`. Owns function design guidance.
- **Must not define:** Provider account administration or VPC plumbing.
- **Normative base:** `core/fellowship/gimli.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                            |
| --- | ---------------- | -------------------------------------------------------------------------------- |
| 1   | Task             | Produce serverless designs with event maps, cold budgets, and cost guards.       |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API. |
| 3   | Output Format    | Serverless plan with functions, events, budgets, and cost notes.                 |
| 4   | Constraints      | Handlers stateless. Cold starts budgeted. Zero em dashes. Cost alarms on.        |
| 5   | Input            | Event inventory, latency SLOs, traffic shape, budget caps.                       |
| 6   | Context          | Prevents cold-start outages and surprise serverless bills.                       |
| 7   | Audience         | Engineers building event-driven serverless systems.                              |
| 8   | Success Criteria | Events mapped; colds budgeted; plan approved.                                    |
| 9   | Examples         | See Section 10.                                                                  |

## 2. Trigger Matrix

| Trigger                           | Fire? | Notes                        |
| --------------------------------- | ----- | ---------------------------- |
| "Move this workload serverless"   | YES   | Core trigger.                |
| "Fix cold starts and bill spikes" | YES   | Core trigger.                |
| "/serverless-patterns"            | YES   | Slash command trigger.       |
| "Open our cloud accounts"         | NO    | Out of scope for this skill. |
| "Run long-lived stateful servers" | NO    | Wrong model; needs servers.  |

## 3. Execution Workflow

### Step 1: Map Events to Functions

- **Action:** Assign one trigger per function with input contracts and idempotency keys for retried deliveries.
- **Input:** Event inventory from user.
- **Stop Condition:** Halt on multi-trigger god functions; require splits.
- **Validation:** Event map reviewed per function.

### Step 2: Budget Cold Starts

- **Action:** Measure init times per runtime, right-size memory for CPU share, and provision concurrency on latency-critical paths only.
- **Input:** Latency SLOs from Step 1.
- **Stop Condition:** Halt when critical paths lack provisioned capacity proof.
- **Validation:** Cold budget recorded with evidence.

### Step 3: Guard Costs and State

- **Action:** Cap concurrency, alarm on spend anomalies, externalize all state to managed stores, and set retention on logs and traces.
- **Input:** Budget caps from user.
- **Stop Condition:** Halt on uncapped concurrency or local-only state.
- **Validation:** Cost guards reviewed with state map.

### Step 4: Handoff and Human Review

- **Action:** Present the serverless plan and request approval before implementation.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero deploys performed by this skill.

## 4. Output Specification

```markdown
# Serverless Plan

- **Events:** [Trigger map]
- **Colds:** [Budgets with evidence]
- **Costs:** [Caps with alarms]
```

## 5. Validation Gate

- [ ] Events mapped per function.
- [ ] Colds budgeted with evidence.
- [ ] Costs capped with alarms.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before implementation.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Deploying functions without event maps.
- **Over-execution threshold:** Provisioning accounts unprompted.
- **Calibration default:** Stateless always; provisioned only where SLOs demand.

## 7. Anti-Pattern Compliance

| Step | Prevents AP             | Mechanism                                 |
| ---- | ----------------------- | ----------------------------------------- |
| 1    | AP-1 (vague task)       | Requires event map first.                 |
| 2    | AP-26 (no scope)        | Budgets colds numerically.                |
| 3    | AP-28 (no stop)         | Caps costs with alarms.                   |
| 4    | AP-45 (no human review) | Halts for approval before implementation. |

## 8. Versioning & Changelog

- **Version:** 1.0.0
- **Changelog:**
  - `1.0.0` (2026-09-26) - Initial release closing the serverless design gap.

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

**Input:** "Our serverless bill tripled and logins freeze on cold mornings."
**Output:** Plan with event-mapped functions, provisioned auth path, and capped concurrency with alarms.
