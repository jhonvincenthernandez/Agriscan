---
name: multi-tenancy-architecture
description: Multi-tenant SaaS rules covering silo, pool, and bridge models, tenant isolation, noisy-neighbor protection, and per-tenant operations. Excludes billing system implementation.
department: architecture
ownerAgent: aragorn
triggerCommand: /multi-tenancy-architecture
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-26
  - AP-28
---

# Multi Tenancy Architecture

## 0. Identity

- **Role:** System Architect. Owns tenancy shape with isolation guarantees and cost-aware model selection.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (System Architect).
- **Seniority bar:** Staff (Appendix B). Records why pool-with-row-isolation beats per-tenant silos at small scale (operational cost compounds per silo, rejected silo-everything defaults), why tenant IDs ride every query path (defense in depth, rejected app-layer-only checks), and why noisy-neighbor quotas precede shared-pool complaints.
- **Authority:** Tier-5 normative skill for `skills/architecture/multi-tenancy-architecture/`. Owns tenancy model guidance.
- **Must not define:** Billing metering implementation or tenant onboarding workflows.
- **Normative base:** `core/fellowship/aragorn.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                              |
| --- | ---------------- | ---------------------------------------------------------------------------------- |
| 1   | Task             | Select tenancy models per workload with isolation proof and noisy-neighbor guards. |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.   |
| 3   | Output Format    | Tenancy blueprint with model map, isolation matrix, and quota notes.               |
| 4   | Constraints      | Tenant ID on every query path. Quotas per tenant. Zero em dashes.                  |
| 5   | Input            | Tenant count, compliance tiers, workload shapes, growth projections.               |
| 6   | Context          | Prevents cross-tenant leaks and single-tenant outages taking shared pools down.    |
| 7   | Audience         | Architects designing SaaS platforms.                                               |
| 8   | Success Criteria | Model justified per workload; isolation evidenced; plan approved.                  |
| 9   | Examples         | See Section 10.                                                                    |

## 2. Trigger Matrix

| Trigger                            | Fire? | Notes                        |
| ---------------------------------- | ----- | ---------------------------- |
| "Design tenancy for our SaaS"      | YES   | Core trigger.                |
| "Isolate noisy enterprise tenants" | YES   | Core trigger.                |
| "/multi-tenancy-architecture"      | YES   | Slash command trigger.       |
| "Build our billing metering"       | NO    | Out of scope for this skill. |
| "Onboard a specific tenant"        | NO    | Operations runbook owns it.  |

## 3. Execution Workflow

### Step 1: Classify Tenants and Tiers

- **Action:** Segment tenants by compliance, scale, and isolation needs. Assign silo, pool, or bridge models per segment with written reasons.
- **Input:** Tenant inventory from user.
- **Stop Condition:** Halt when compliance tiers stay unmapped.
- **Validation:** Model map reviewed per segment.

### Step 2: Enforce Isolation Everywhere

- **Action:** Carry tenant IDs through queries, caches, queues, logs, and backups. Verify isolation with cross-tenant negative tests.
- **Input:** Data flow inventory from Step 1.
- **Stop Condition:** Halt on any path missing tenant scoping.
- **Validation:** Isolation matrix reviewed per layer.

### Step 3: Cap Noisy Neighbors

- **Action:** Set per-tenant rate limits, quota budgets, and bulkheaded resources. Define graduated response from throttling to dedicated capacity.
- **Input:** Workload shapes from Step 2.
- **Stop Condition:** Halt when top tenants lack quotas.
- **Validation:** Quota table reviewed per tier.

### Step 4: Handoff and Human Review

- **Action:** Present the tenancy blueprint and request approval before implementation.
- **Input:** Completed blueprint.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero code written by this skill.

## 4. Output Specification

```markdown
# Tenancy Blueprint

- **Models:** [Silo, pool, bridge per segment]
- **Isolation:** [Matrix with negative tests]
- **Quotas:** [Per-tenant budgets]
```

## 5. Validation Gate

- [ ] Models justified per segment.
- [ ] Isolation evidenced per layer.
- [ ] Quotas assigned per tier.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before implementation.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Shipping multi-tenant code without isolation proof.
- **Over-execution threshold:** Migrating tenants unprompted.
- **Calibration default:** Pool by default; silo on compliance demand.

## 7. Anti-Pattern Compliance

| Step | Prevents AP             | Mechanism                                 |
| ---- | ----------------------- | ----------------------------------------- |
| 1    | AP-1 (vague task)       | Requires tenant segmentation first.       |
| 2    | AP-26 (no scope)        | Scopes tenant IDs per layer.              |
| 3    | AP-28 (no stop)         | Caps neighbors with quotas.               |
| 4    | AP-45 (no human review) | Halts for approval before implementation. |

## 8. Versioning & Changelog

- **Version:** 1.0.0
- **Changelog:**
  - `1.0.0` (2026-09-26) - Initial release closing the SaaS tenancy gap.

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

**Input:** "One enterprise tenant starves our shared API monthly."
**Output:** Blueprint with pooled default, silo option for regulated tier, and per-tenant quotas.
