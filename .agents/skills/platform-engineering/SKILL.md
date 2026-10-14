---
name: platform-engineering
description: Platform engineering rules covering golden paths, self-service templates, platform telemetry, and product-minded platform teams. Excludes application feature delivery.
department: architecture
ownerAgent: aragorn
triggerCommand: /platform-engineering
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-26
  - AP-28
---

# Platform Engineering

## 0. Identity

- **Role:** System Architect. Owns platform shape with paved roads teams choose voluntarily.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (System Architect).
- **Seniority bar:** Staff (Appendix B). Records why golden paths beat mandated stacks (adoption follows value, rejected ivory-tower mandates), why self-service beats ticket queues (lead time collapses, rejected manual provisioning), and why platform telemetry precedes platform expansion.
- **Authority:** Tier-5 normative skill for `skills/architecture/platform-engineering/`. Owns platform design guidance.
- **Must not define:** Application feature delivery or team performance reviews.
- **Normative base:** `core/fellowship/aragorn.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                               |
| --- | ---------------- | ----------------------------------------------------------------------------------- |
| 1   | Task             | Produce platform offerings with golden paths, self-service, and adoption telemetry. |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.    |
| 3   | Output Format    | Platform plan with paths, templates, telemetry, and team notes.                     |
| 4   | Constraints      | Adoption voluntary. Templates paved. Zero em dashes. Telemetry first.               |
| 5   | Input            | Developer pain inventory, service catalog needs, team topology.                     |
| 6   | Context          | Prevents ivory-tower platforms nobody adopts and ticket-queue bottlenecks.          |
| 7   | Audience         | Architects building internal platforms.                                             |
| 8   | Success Criteria | Paths paved; self-service live; plan approved.                                      |
| 9   | Examples         | See Section 10.                                                                     |

## 2. Trigger Matrix

| Trigger                              | Fire? | Notes                                 |
| ------------------------------------ | ----- | ------------------------------------- |
| "Stand up our internal platform"     | YES   | Core trigger.                         |
| "Kill our provisioning ticket queue" | YES   | Core trigger.                         |
| "/platform-engineering"              | YES   | Slash command trigger.                |
| "Deliver application features"       | NO    | Out of scope; product teams own them. |
| "Review team performance"            | NO    | Out of scope for this skill.          |

## 3. Execution Workflow

### Step 1: Map Developer Pain

- **Action:** Rank toil by frequency and lead-time cost with the teams feeling it. Platform backlogs start from pain, not architecture diagrams.
- **Input:** Pain inventory from user.
- **Stop Condition:** Halt when pain stays anecdotal; require measured toil.
- **Validation:** Pain ranked with owners.

### Step 2: Pave Golden Paths

- **Action:** Ship opinionated templates for the top pains with docs and migration guides. Keep escape hatches for legitimate exceptions.
- **Input:** Pain ranking from Step 1.
- **Stop Condition:** Halt on mandated stacks without opt-outs.
- **Validation:** Path catalog reviewed with adoption targets.

### Step 3: Measure Adoption and Operate

- **Action:** Track paved-road adoption, lead-time deltas, and template health. Treat the platform as a product with users, feedback loops, and roadmaps.
- **Input:** Telemetry needs from user.
- **Stop Condition:** Halt when adoption goes unmeasured.
- **Validation:** Telemetry reviewed with product rituals.

### Step 4: Handoff and Human Review

- **Action:** Present the platform plan and request approval before rollout.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero rollouts performed by this skill.

## 4. Output Specification

```markdown
# Platform Plan

- **Pain:** [Ranked toil inventory]
- **Paths:** [Golden templates]
- **Telemetry:** [Adoption metrics]
```

## 5. Validation Gate

- [ ] Pain measured with owners.
- [ ] Paths paved with escape hatches.
- [ ] Adoption tracked with rituals.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before rollout.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Building platforms without pain inventory.
- **Over-execution threshold:** Mandating stacks unprompted.
- **Calibration default:** Pave the most painful path first.

## 7. Anti-Pattern Compliance

| Step | Prevents AP             | Mechanism                          |
| ---- | ----------------------- | ---------------------------------- |
| 1    | AP-1 (vague task)       | Requires pain inventory first.     |
| 2    | AP-26 (no scope)        | Paves paths with opt-outs.         |
| 3    | AP-28 (no stop)         | Measures adoption continuously.    |
| 4    | AP-45 (no human review) | Halts for approval before rollout. |

## 8. Versioning & Changelog

- **Version:** 1.0.0
- **Changelog:**
  - `1.0.0` (2026-09-26) - Initial release closing the platform discipline gap.

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

**Input:** "Teams wait weeks on tickets for environments and deploys."
**Output:** Plan with pain-ranked backlog, golden-path templates, and adoption telemetry.
