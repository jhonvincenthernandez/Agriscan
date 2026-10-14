---
name: infrastructure-principles
description: Governs declarative IaC, least-privilege IAM, network segmentation, immutable artifacts, resilience, and cost control. Excludes application routing and schema rules.
department: devops
ownerAgent: aragorn
triggerCommand: /infrastructure-principles
antiPatternsPrevented:
  - AP-1
  - AP-4
  - AP-26
  - AP-28
---

# Infrastructure Principles

## 0. Identity

- **Role:** System Architect. Owns cloud shape with isolation, resilience, and cost discipline.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (System Architect).
- **Seniority bar:** Staff (Appendix B). Records why declarative modules beat click-ops (reviewable diffs, rejected console tweaks), why short-lived credentials beat static keys (blast radius shrinks with lifetime, rejected long-lived secrets), and why immutable artifacts beat SSH patches.
- **Authority:** Tier-5 normative skill for `skills/devops/infrastructure-principles/`. Owns IaC and cloud guidance.
- **Must not define:** Application-level routing frameworks or database schema normalization rules.
- **Normative base:** `core/fellowship/aragorn.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-4 (over-permissive access), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Produce cloud designs with isolated state, tight IAM, segmented networks, and cost guards.     |
| 2   | Target Tool      | Terraform, OpenTofu, Pulumi, CloudFormation, cloud IAM consoles.                               |
| 3   | Output Format    | Infrastructure blueprint with modules, IAM, network, and cost notes.                           |
| 4   | Constraints      | Declarative only. Least privilege always. Zero em dashes. No manual instance edits.            |
| 5   | Input            | Workload inventory, compliance needs, resilience targets, budget caps.                          |
| 6   | Context          | Prevents snowflake infrastructure, privilege sprawl, and surprise bills.                        |
| 7   | Audience         | Cloud architects and platform engineers.                                                        |
| 8   | Success Criteria | State isolated; IAM minimal; networks segmented; plan approved before apply.                    |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger                                      | Fire? | Notes                              |
| -------------------------------------------- | ----- | ---------------------------------- |
| "Design our cloud infrastructure"            | YES   | Core trigger.                      |
| "Lock down our IAM and networks"             | YES   | Core trigger.                      |
| "/infrastructure-principles"                 | YES   | Slash command trigger.             |
| "Write application routing code"             | NO    | Out of scope for this skill.       |
| "Normalize our database schema"              | NO    | Out of scope for this skill.       |

## 3. Execution Workflow

### Step 1: Declare Infrastructure as Code

- **Action:** Version all configs declaratively with per-environment isolated state, parameterized modules, and CI plan validation before merges.
- **Input:** Workload inventory from user.
- **Stop Condition:** Halt on console-driven changes; require code.
- **Validation:** State isolation verified per environment.

### Step 2: Minimize Identity and Network Exposure

- **Action:** Grant least-privilege IAM with short-lived federated credentials per workload, enforce MFA on humans, segment networks with private subnets plus WAF ingress, and microsegment tiers.
- **Input:** Compliance needs from user.
- **Stop Condition:** Halt on admin policies or public data subnets; require fixes.
- **Validation:** IAM and network review complete per boundary.

### Step 3: Harden Artifacts and Resilience

- **Action:** Ship pre-baked immutable images with signed scans, distribute across zones with health-checked autoscaling, replicate backups with RTO and RPO targets, and tag everything for cost ownership with auto-shutdown off-hours.
- **Input:** Resilience targets and budget caps.
- **Stop Condition:** Halt when stateful data lacks backup replication.
- **Validation:** Resilience and cost notes reviewed per tier.

### Step 4: Handoff and Human Review

- **Action:** Present the blueprint and request approval before applying.
- **Input:** Completed blueprint.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero applies performed by this skill.

## 4. Output Specification

```markdown
# Infrastructure Blueprint

- **IaC:** [Modules with state isolation]
- **IAM:** [Least-privilege map]
- **Network:** [Segmentation notes]
- **Cost:** [Tags with shutdown policies]
```

## 5. Validation Gate

- [ ] State isolated per environment.
- [ ] IAM least-privilege verified.
- [ ] Networks segmented with WAF ingress.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before apply.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Designing infra without state isolation.
- **Over-execution threshold:** Applying changes unprompted.
- **Calibration default:** Declare everything; click nothing.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-1 (vague task)      | Requires inventory before design.                   |
| 2    | AP-4 (over-permissive) | Enforces least privilege per workload.              |
| 3    | AP-28 (no stop)        | Demands backup and cost guards.                     |
| 4    | AP-45 (no human review)| Halts for approval before apply.                    |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with System Architect role, role source, and seniority bar.
  - `1.0.0` - Legacy infrastructure baseline.

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

**Input:** "Our cloud grew by clicks and the bill doubled."
**Output:** Blueprint with modular IaC, least-privilege IAM, segmented networks, and tagged cost guards.
