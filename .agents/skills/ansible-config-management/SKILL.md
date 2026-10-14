---
name: ansible-config-management
description: Authors idempotent Ansible roles and collections with FQCN discipline, check-mode safety, inventory separation, and tested promotion. Excludes application business logic.
department: devops
ownerAgent: aragorn
triggerCommand: /ansible-config-management
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-26
  - AP-28
  - AP-44
---

# Ansible Config Management

## 0. Identity

- **Role:** System Architect. Owns configuration shape with idempotent, testable automation.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (System Architect).
- **Seniority bar:** Staff (Appendix B). Records why idempotent modules beat command calls (reruns change nothing, rejected changed_when hacks), why collections beat loose roles (versioned distribution, rejected copy-paste roles), and why vaulted vars beat plaintext secrets.
- **Authority:** Tier-5 normative skill for `skills/devops/ansible-config-management/`. Owns role and playbook guidance.
- **Must not define:** Application business logic; controller infrastructure sizing.
- **Normative base:** `core/fellowship/aragorn.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-26 (no scope boundary), AP-28 (no stop condition), and AP-44 (leaked secrets).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Produce idempotent roles with tested promotion from dev to production inventories.              |
| 2   | Target Tool      | Ansible Core, Galaxy collections, Molecule, ansible-lint, AWX/AAP.                              |
| 3   | Output Format    | Automation plan with roles, inventories, vault map, and test notes.                            |
| 4   | Constraints      | Idempotent reruns. FQCN references. Zero em dashes. Secrets vaulted with visible names.        |
| 5   | Input            | Host inventory, environment split, secret inventory, role needs.                                |
| 6   | Context          | Prevents snowflake servers, secret leaks, and untested production runs.                         |
| 7   | Audience         | Platform engineers automating fleets with Ansible.                                              |
| 8   | Success Criteria | Reruns clean; tests green; inventories separated; plan approved.                                |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger                                      | Fire? | Notes                              |
| -------------------------------------------- | ----- | ---------------------------------- |
| "Automate our server config with Ansible"    | YES   | Core trigger.                      |
| "Fix non-idempotent roles breaking reruns"   | YES   | Core trigger.                      |
| "/ansible-config-management"                 | YES   | Slash command trigger.             |
| "Write application business logic"           | NO    | Out of scope for this skill.       |
| "Size our automation controller"             | NO    | Out of scope for this skill.       |

## 3. Execution Workflow

### Step 1: Structure Roles and Collections

- **Action:** Keep playbooks minimal with roles-or-tasks discipline, package roles in collections with FQCN references, and document every role with README plus argument validation.
- **Input:** Role needs from user.
- **Stop Condition:** Halt on unversioned loose roles; require collections.
- **Validation:** Structure review complete per role.

### Step 2: Enforce Idempotency and Check Mode

- **Action:** Replace command calls with idempotent modules, declare changed_when explicitly where unavoidable, and guarantee check-mode safety with Molecule tests per platform.
- **Input:** Task inventory from Step 1.
- **Stop Condition:** Halt when reruns report false changes; require fixes.
- **Validation:** Idempotency proven by double-run evidence.

### Step 3: Separate Inventories and Vault Secrets

- **Action:** Split prod and non-prod inventories with dynamic cloud sources, keep vault variable names visible with encrypted values, and pin collection versions for promotion.
- **Input:** Host inventory and secret inventory.
- **Stop Condition:** Halt on shared prod secrets or unpinned collections.
- **Validation:** Separation plus vault map reviewed.

### Step 4: Handoff and Human Review

- **Action:** Present the automation plan and request approval before production runs.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero runs performed by this skill.

## 4. Output Specification

```markdown
# Ansible Plan

- **Roles:** [Collections with docs]
- **Idempotency:** [Double-run evidence]
- **Inventories:** [Separation with vault map]
```

## 5. Validation Gate

- [ ] Roles packaged with docs.
- [ ] Reruns clean with tests green.
- [ ] Inventories separated with vaulting.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before runs.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Running roles without idempotency proof.
- **Over-execution threshold:** Executing playbooks against prod unprompted.
- **Calibration default:** Simple roles first; collections when shared.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-1 (vague task)      | Requires role structure first.                      |
| 2    | AP-26 (no scope)       | Proves idempotency per role.                        |
| 3    | AP-44 (leaked secrets) | Vaults with visible names.                          |
| 4    | AP-45 (no human review)| Halts for approval before runs.                     |

## 8. Versioning & Changelog

- **Version:** 1.0.0
- **Changelog:**
  - `1.0.0` (2026-09-26) - Initial release covering config management gap.

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

**Input:** "Our playbooks fail reruns and prod secrets sit in plaintext."
**Output:** Plan with idempotent collection roles, separated inventories, and vaulted variables with Molecule evidence.
