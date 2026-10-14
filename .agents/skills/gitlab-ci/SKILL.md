---
name: gitlab-ci
description: Designs GitLab pipelines with shared templates, rules-based flow, DAG needs, protected environments, review apps, and Vault-backed secrets. Excludes runner fleet sizing.
department: devops
ownerAgent: gimli
triggerCommand: /gitlab-ci
antiPatternsPrevented:
  - AP-1
  - AP-4
  - AP-6
  - AP-26
  - AP-28
---

# GitLab CI

## 0. Identity

- **Role:** Release Engineer. Owns pipeline packaging with template governance and environment gates.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Release Engineer).
- **Seniority bar:** Staff (Appendix B). Records why shared templates beat per-repo YAML (one change updates everyone, rejected copy-paste drift), why needs-DAGs beat pure stages (wall-clock collapses, rejected serial waits), and why protected environments beat script gates (policy enforced by platform, rejected self-granted deploys).
- **Authority:** Tier-5 normative skill for `skills/devops/gitlab-ci/`. Owns pipeline and environment guidance.
- **Must not define:** Runner fleet sizing; application business logic.
- **Normative base:** `core/fellowship/gimli.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-4 (over-permissive deploys), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                                   |
| --- | ---------------- | ------------------------------------------------------------------------------------------------------- |
| 1   | Task             | Produce template-governed pipelines with DAG speed and gated environments.                              |
| 2   | Target Tool      | GitLab CI, include and extends, needs DAGs, protected environments, review apps.                        |
| 3   | Output Format    | Pipeline plan with templates, flow rules, environment gates, and secret notes.                          |
| 4   | Constraints      | Rules over only-except. Artifacts forward, cache speeds. Zero em dashes. Secrets masked plus protected. |
| 5   | Input            | Repo layout, environment tiers, secret inventory, runner tags.                                          |
| 6   | Context          | Prevents monolith YAML drift, double pipelines, and self-granted production access.                     |
| 7   | Audience         | Platform engineers running GitLab delivery.                                                             |
| 8   | Success Criteria | Templates shared; DAGs fast; environments gated; plan approved.                                         |
| 9   | Examples         | See Section 10.                                                                                         |

## 2. Trigger Matrix

| Trigger                                | Fire? | Notes                        |
| -------------------------------------- | ----- | ---------------------------- |
| "Standardize our GitLab pipelines"     | YES   | Core trigger.                |
| "Fix double pipelines and slow stages" | YES   | Core trigger.                |
| "/gitlab-ci"                           | YES   | Slash command trigger.       |
| "Size our runner fleet"                | NO    | Out of scope for this skill. |
| "Write application business logic"     | NO    | Out of scope for this skill. |

## 3. Execution Workflow

### Step 1: Template the Platform

- **Action:** Centralize shared jobs in include libraries with extends composition. Replace only-except with rules plus workflow guards killing double pipelines.
- **Input:** Repo layout from user.
- **Stop Condition:** Halt when pipelines duplicate without shared includes.
- **Validation:** Template inventory reviewed with adoption map.

### Step 2: DAG the Critical Path

- **Action:** Wire needs dependencies bypassing stage waits, separate cache (best-effort deps) from artifacts (guaranteed outputs), and build once for downstream promotion.
- **Input:** Stage timings from Step 1.
- **Stop Condition:** Halt when serial stages gate independent jobs; require DAG edges.
- **Validation:** Wall-clock measured before and after.

### Step 3: Gate Environments and Secrets

- **Action:** Protect production with approvals and deployer lists, spin review apps per MR with auto-stop, mask plus protect variables, and prefer Vault JWT short-lived secrets. Gate merges on new-critical scans with review apps for visual proof.
- **Input:** Environment tiers and secret inventory.
- **Stop Condition:** Halt on unprotected production or long-lived secrets where Vault fits.
- **Validation:** Environment policy reviewed with secret audit.

### Step 4: Handoff and Human Review

- **Action:** Present the pipeline plan and request approval before rollout.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero rollouts performed by this skill.

## 4. Output Specification

```markdown
# GitLab Plan

- **Templates:** [Shared library with adoption]
- **Flow:** [Rules with DAG edges]
- **Environments:** [Gates with review apps]
- **Secrets:** [Masked, protected, Vault notes]
```

## 5. Validation Gate

- [ ] Templates shared across repos.
- [ ] DAGs collapse serial waits.
- [ ] Production protected with approvals.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before rollout.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Shipping per-repo YAML without shared templates.
- **Over-execution threshold:** Changing platform settings unprompted.
- **Calibration default:** Template first; DAG second; gates always.

## 7. Anti-Pattern Compliance

| Step | Prevents AP             | Mechanism                             |
| ---- | ----------------------- | ------------------------------------- |
| 1    | AP-1 (vague task)       | Requires repo layout first.           |
| 2    | AP-26 (no scope)        | DAGs bound to measured waits.         |
| 3    | AP-4 (over-permissive)  | Protects environments with approvals. |
| 4    | AP-45 (no human review) | Halts for approval before rollout.    |

## 8. Versioning & Changelog

- **Version:** 1.0.0
- **Changelog:**
  - `1.0.0` (2026-09-26) - Initial release covering GitLab platform gap.

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

**Input:** "Our GitLab pipelines double-run and every repo drifts apart."
**Output:** Plan with shared templates, workflow guards, needs DAGs, and protected production with review apps.
