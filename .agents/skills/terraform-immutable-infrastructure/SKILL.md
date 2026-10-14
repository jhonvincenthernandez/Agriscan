---
name: terraform-immutable-infrastructure
description: Provisions reproducible cloud infrastructure with remote locked state, pinned modules, drift enforcement, and lifecycle protection. Excludes application runtime code.
department: devops
ownerAgent: aragorn
triggerCommand: /terraform-immutable-infrastructure
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-18
  - AP-26
  - AP-28
---

# Terraform Immutable Infrastructure

## 0. Identity

- **Role:** System Architect. Owns infrastructure shape with blast-radius limits and state safety.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (System Architect).
- **Seniority bar:** Staff (Appendix B). Records why remote locked state beats local files (concurrent applies corrupt local state, rejected local backends), why pinned modules beat floating versions (reproducible plans, rejected latest registries), and why prevent-destroy beats post-incident restores.
- **Authority:** Tier-5 normative skill for `skills/devops/terraform-immutable-infrastructure/`. Owns IaC module and state guidance.
- **Must not define:** Application container runtime code.
- **Normative base:** `core/fellowship/aragorn.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-18 (state corruption), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Produce modular Terraform with locked state, drift checks, and protected lifecycles.           |
| 2   | Target Tool      | Terraform CLI, OpenTofu, AWS/GCP/Azure providers, Terraform Cloud.                             |
| 3   | Output Format    | Modular manifests, plan artifacts, and lock files.                                             |
| 4   | Constraints      | Ban local state files. Never hardcode credentials. Pin provider versions. Zero em dashes.      |
| 5   | Input            | Cloud architecture specs, network topologies, compliance policies.                              |
| 6   | Context          | Prevents configuration drift, accidental destruction, and security exposure.                    |
| 7   | Audience         | Cloud architects, DevOps engineers, and security auditors.                                      |
| 8   | Success Criteria | Clean plans without surprise recreation; deterministic locking; plan approved.                  |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger                                      | Fire? | Notes                              |
| -------------------------------------------- | ----- | ---------------------------------- |
| "Provision our VPC with Terraform"           | YES   | Core trigger.                      |
| "Stop accidental resource deletions"         | YES   | Core trigger.                      |
| "/terraform-immutable-infrastructure"        | YES   | Slash command trigger.             |
| "Write application runtime code"             | NO    | Out of scope for this skill.       |
| "Debug container images"                     | NO    | Route to `docker-principles`.      |

## 3. Execution Workflow

### Step 1: Isolate State per Environment

- **Action:** Store state in encrypted object stores with distributed locking per environment. Parameterize modules with explicit variables and outputs.
- **Input:** Cloud architecture specs.
- **Stop Condition:** Halt on local state or hardcoded credentials; require remediation.
- **Validation:** Backend config reviewed with lock evidence.

### Step 2: Pin and Validate Plans

- **Action:** Pin exact provider and module versions. Run plan validation in CI before merging infrastructure changes.
- **Input:** Module inventory from Step 1.
- **Stop Condition:** Halt on floating versions; require pins.
- **Validation:** Plan output reviewed with zero surprise recreations.

### Step 3: Protect Lifecycles and Detect Drift

- **Action:** Attach prevent-destroy on stateful resources, schedule daily drift plan checks, and tag resources for ownership and cost tracking.
- **Input:** Compliance policies from user.
- **Stop Condition:** Halt when stateful resources lack protection.
- **Validation:** Lifecycle and drift notes reviewed per resource.

### Step 4: Handoff and Human Review

- **Action:** Present the infrastructure plan and request approval before applying.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero applies performed by this skill.

## 4. Output Specification

```markdown
# Infrastructure Plan

- **State:** [Backends with locking]
- **Modules:** [Pinned inventory]
- **Lifecycle:** [Protection with drift checks]
```

## 5. Validation Gate

- [ ] State remote with locking per environment.
- [ ] Providers and modules pinned exactly.
- [ ] Stateful resources carry prevent-destroy.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before apply.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Planning infra without state isolation.
- **Over-execution threshold:** Applying changes to live clouds unprompted.
- **Calibration default:** Small blast radius per module; explicit everything.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-1 (vague task)      | Requires architecture specs first.                  |
| 2    | AP-26 (no scope)       | Pins every external version.                        |
| 3    | AP-28 (no stop)        | Protects lifecycles with drift checks.              |
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

**Input:** "Our staging apply deleted the production database."
**Output:** Infrastructure plan with isolated locked states, prevent-destroy lifecycles, and per-environment blast radius.
