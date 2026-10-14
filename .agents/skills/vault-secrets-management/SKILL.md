---
name: vault-secrets-management
description: Operates Vault with dynamic secrets, rotation schedules, least-privilege policies, and audited break-glass paths. Excludes application business logic.
department: devops
ownerAgent: boromir
triggerCommand: /vault-secrets-management
antiPatternsPrevented:
  - AP-1
  - AP-4
  - AP-6
  - AP-26
  - AP-28
  - AP-44
---

# Vault Secrets Management

## 0. Identity

- **Role:** Security Auditor. Owns secret lifecycle posture with audited issuance and rotation.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Security Auditor).
- **Seniority bar:** Staff (Appendix B). Records why dynamic secrets beat long-lived ones (theft windows shrink to TTLs, rejected static credential sprawl), why rotation beats manual changes (exposure closes on schedule, rejected hope-based hygiene), and why break-glass paths stay audited instead of absent.
- **Authority:** Tier-5 normative skill for `skills/devops/vault-secrets-management/`. Owns secrets lifecycle guidance.
- **Must not define:** Application business logic; identity provider administration.
- **Normative base:** `core/fellowship/boromir.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-4 (over-permissive access), AP-26 (no scope boundary), and AP-44 (leaked secrets).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Produce secret lifecycles with dynamic issuance, rotation, and least-privilege access.         |
| 2   | Target Tool      | HashiCorp Vault, External Secrets Operator, cloud secret managers.                             |
| 3   | Output Format    | Secrets plan with engines, policies, rotation, and audit notes.                                |
| 4   | Constraints      | Least privilege per path. Rotation scheduled. Zero em dashes. No long-lived static secrets.    |
| 5   | Input            | Secret inventory, consumer map, compliance needs, break-glass contacts.                         |
| 6   | Context          | Prevents credential sprawl, stale secrets, and unaudited emergency access.                      |
| 7   | Audience         | Security and platform engineers owning secret estates.                                          |
| 8   | Success Criteria | Secrets dynamic or rotated; access minimal; plan approved.                                      |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger                                      | Fire? | Notes                              |
| -------------------------------------------- | ----- | ---------------------------------- |
| "Move our secrets to Vault"                  | YES   | Core trigger.                      |
| "Rotate stale credentials everywhere"        | YES   | Core trigger.                      |
| "/vault-secrets-management"                  | YES   | Slash command trigger.             |
| "Run our identity provider"                  | NO    | Out of scope for this skill.       |
| "Write application business logic"           | NO    | Out of scope for this skill.       |

## 3. Execution Workflow

### Step 1: Inventory Secrets and Consumers

- **Action:** List every secret with consumers, lifetimes, and blast radius. Classify static versus dynamic candidates.
- **Input:** Secret inventory from user.
- **Stop Condition:** Halt when unknown consumers exist; require mapping.
- **Validation:** Inventory complete with lifetime per secret.

### Step 2: Issue Dynamic First, Rotate the Rest

- **Action:** Prefer dynamic short-lived issuance per consumer. Schedule rotation for remaining static secrets with blue-green credential swaps.
- **Input:** Inventory from Step 1.
- **Stop Condition:** Halt on long-lived shared credentials without rotation dates.
- **Validation:** Issuance map reviewed with TTLs.

### Step 3: Constrain Access and Break Glass

- **Action:** Scope policies to least-privilege paths, audit every read, and define break-glass flow with approvers plus automatic expiry.
- **Input:** Compliance needs and contacts.
- **Stop Condition:** Halt when break-glass lacks approvers or expiry.
- **Validation:** Policy review complete with audit evidence.

### Step 4: Handoff and Human Review

- **Action:** Present the secrets plan and request approval before migration.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero migrations performed by this skill.

## 4. Output Specification

```markdown
# Secrets Plan

- **Inventory:** [Secrets with lifetimes]
- **Issuance:** [Dynamic map with TTLs]
- **Access:** [Policies with break-glass]
```

## 5. Validation Gate

- [ ] Inventory complete with lifetimes.
- [ ] Dynamic preferred with rotation dated.
- [ ] Access least-privilege with audit.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before migration.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Migrating secrets without inventory.
- **Over-execution threshold:** Rotating production credentials unprompted.
- **Calibration default:** Shortest lifetimes the system tolerates.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-1 (vague task)      | Requires inventory first.                           |
| 2    | AP-26 (no scope)       | Bounds lifetimes per secret.                        |
| 3    | AP-44 (leaked secrets) | Audits access with break-glass.                     |
| 4    | AP-45 (no human review)| Halts for approval before migration.                |

## 8. Versioning & Changelog

- **Version:** 1.0.0
- **Changelog:**
  - `1.0.0` (2026-09-26) - Initial release covering secrets lifecycle gap.

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

**Input:** "Our AWS keys are three years old and shared across teams."
**Output:** Secrets plan with dynamic issuance per service, dated rotation, and audited break-glass flow.
