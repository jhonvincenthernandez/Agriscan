---
name: argocd-gitops
description: Implements GitOps delivery with ArgoCD applications, sync policies, and progressive rollouts. Excludes cluster provisioning.
department: devops
ownerAgent: gimli
triggerCommand: /argocd-gitops
antiPatternsPrevented:
  - AP-1
  - AP-4
  - AP-6
  - AP-26
  - AP-28
---

# ArgoCD GitOps

## 0. Identity

- **Role:** Release Engineer. Owns delivery versioning and promotion paths with automated rollback.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Release Engineer).
- **Seniority bar:** Staff (Appendix B). Records why app-of-apps beats click-ops (every change is a reviewed commit, rejected kubectl exceptions), why gated prune beats blind prune (stateful data survives refactors, rejected global auto-delete), and why progressive delivery precedes auto-sync on user services.
- **Authority:** Tier-5 normative skill for `skills/devops/argocd-gitops/`. Owns application manifests and sync policy.
- **Must not define:** Cluster provisioning; application code changes.
- **Normative base:** `core/fellowship/gimli.md`, `rules/engineering/architecture-boundaries.md`, `references/anti-patterns.md`, and GitOps delivery practice.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-4 (over-permissive sync), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Produce ArgoCD application sets with sync policy, health gates, and rollback paths.            |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.                |
| 3   | Output Format    | GitOps blueprint with app manifests, sync waves, and promotion runbook.                        |
| 4   | Constraints      | Automated sync only with health gates. Manual kubectl edits forbidden. Zero em dashes.         |
| 5   | Input            | Repo layout, environment promotion order, health checks, rollback budget.                       |
| 6   | Context          | Prevents click-ops drift where clusters diverge from git truth.                                 |
| 7   | Audience         | Platform engineers running GitOps delivery.                                                     |
| 8   | Success Criteria | Apps sync green from git; promotions gated; blueprint approved before wiring.                   |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger                                      | Fire? | Notes                              |
| -------------------------------------------- | ----- | ---------------------------------- |
| "Move our delivery to ArgoCD GitOps"         | YES   | Core trigger.                      |
| "Fix out-of-sync apps and failed promotions" | YES   | Core trigger.                      |
| "/argocd-gitops"                             | YES   | Slash command trigger.             |
| "Provision a new Kubernetes cluster"         | NO    | Out of scope; infra runbook needed.|
| "Package our Helm chart"                     | NO    | Route to `helm-charts`.            |

## 3. Execution Workflow

### Step 1: Map Repos and Promotion Order

- **Action:** Define app-of-apps roots, per-environment overlays, and promotion sequence with approvers. Separate deploy repos from application code repos.
- **Input:** Repo layout and environment list.
- **Stop Condition:** Halt and ask when promotion approvers stay unnamed.
- **Validation:** Promotion order recorded with gates.

### Step 2: Configure Sync and Health

- **Action:** Set automated sync with prune and self-heal flags, sync waves for ordering, PreSync migration hooks, and health checks blocking bad rollouts. Gate prune on stateful resources.
- **Input:** Workload dependencies from Step 1.
- **Stop Condition:** Halt when auto-sync lacks health gates; require gates.
- **Validation:** Sync policy reviewed per application.

### Step 3: Define Rollback and Drift Response

- **Action:** Specify git-revert rollback as default, sync-window freezes, notification routing, and progressive delivery via Rollouts with metric abort gates. Scope generator preserve policies until proven.
- **Input:** Incident requirements and on-call roster.
- **Stop Condition:** Halt when rollback ownership stays unclear; require an owner.
- **Validation:** Runbook covers revert, freeze, and notify paths.

### Step 4: Handoff and Human Review

- **Action:** Present the blueprint and request approval before wiring.
- **Input:** Completed blueprint.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero cluster writes performed.

## 4. Output Specification

```markdown
# GitOps Blueprint

- **Apps:** [Application manifests with waves]
- **Sync:** [Policy with prune and self-heal flags]
- **Promotion:** [Order with approvers]
- **Rollback:** [Revert and freeze runbook]
```

## 5. Validation Gate

- [ ] Promotion order recorded with approvers.
- [ ] Auto-sync gated by health checks.
- [ ] Rollback defaults to git revert with owner.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before wiring.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Enabling auto-sync without health gates.
- **Over-execution threshold:** Syncing applications to live clusters unprompted.
- **Calibration default:** Start manual, automate after three clean promotions.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-1 (vague task)      | Requires promotion order with approvers.            |
| 2    | AP-4 (over-permissive) | Gates auto-sync with health checks.                 |
| 3    | AP-28 (no stop)        | Defines revert and freeze paths.                    |
| 4    | AP-45 (no human review)| Halts for approval before wiring.                   |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Release Engineer role, role source, and seniority bar.
  - `1.0.0` (2026-09-26) - Initial release extending devops coverage.

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

**Input:** "Developers kubectl-apply hotfixes and git no longer matches prod."
**Output:** Blueprint with app-of-apps roots, gated auto-sync, and revert-first rollback runbook.
