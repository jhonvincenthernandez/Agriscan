---
name: helm-charts
description: Authors versioned Helm charts with templated manifests, values schema, and safe upgrade paths. Excludes cluster administration.
department: devops
ownerAgent: gimli
triggerCommand: /helm-charts
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-26
  - AP-28
  - AP-44
---

# Helm Charts

## 0. Identity

- **Role:** Release Engineer. Owns packaging, versioning, and rollback paths for chart releases.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Release Engineer).
- **Seniority bar:** Staff (Appendix B). Records why values schemas beat undocumented values (typos fail at install, rejected silent breakage), why atomic deploys beat manual rollbacks (self-healing releases, rejected panic-driven recovery), and why external secrets beat values-committed credentials.
- **Authority:** Tier-5 normative skill for `skills/devops/helm-charts/`. Owns chart structure and upgrade guidance.
- **Must not define:** Cluster provisioning or node administration; application code changes.
- **Normative base:** `core/fellowship/gimli.md`, `rules/engineering/architecture-boundaries.md`, `references/anti-patterns.md`, and Helm production practice.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-26 (no scope boundary), AP-28 (no stop condition), and AP-44 (unlocked deploys).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Produce a lint-clean chart with values schema, secrets handling, and rollback-safe upgrades.   |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.                |
| 3   | Output Format    | Chart blueprint with values, templates, hooks, and upgrade runbook.                            |
| 4   | Constraints      | Secrets via references only. Lint and dry-run mandatory. Zero em dashes.                       |
| 5   | Input            | Workload manifests, environment matrix, secret sources, upgrade policy.                         |
| 6   | Context          | Prevents copy-paste YAML sprawl that drifts per environment.                                    |
| 7   | Audience         | Platform engineers packaging Kubernetes releases.                                               |
| 8   | Success Criteria | Chart lints clean; values validated; upgrade and rollback rehearsed on paper.                   |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger                                     | Fire? | Notes                              |
| ------------------------------------------- | ----- | ---------------------------------- |
| "Package our service as a Helm chart"       | YES   | Core trigger.                      |
| "Fix our chart upgrade failures"            | YES   | Core trigger.                      |
| "/helm-charts"                              | YES   | Slash command trigger.             |
| "Provision our Kubernetes cluster"          | NO    | Out of scope; infra runbook needed.|
| "Write our application code"                | NO    | Out of scope for this skill.       |

## 3. Execution Workflow

### Step 1: Inventory Workloads and Environments

- **Action:** List deployments, services, config maps, and per-environment value deltas. Default values must be production-safe; development overlays loosen, never tighten.
- **Input:** Existing manifests and environment matrix.
- **Stop Condition:** Halt and ask when environment deltas stay undocumented.
- **Validation:** Inventory complete before templating.

### Step 2: Template with Values Schema

- **Action:** Build templates with values schema enforcing required keys, resource limits, probes, and labels. Pin image digests, enforce non-root security contexts, annotate config checksums for restarts, and reference secrets externally only.
- **Input:** Inventory from Step 1.
- **Stop Condition:** Halt when secrets appear inline; require external references.
- **Validation:** Helm lint passes and dry-run renders per environment.

### Step 3: Define Upgrade and Rollback

- **Action:** Set migration hooks with delete policies, revision history caps, atomic deploys with waits and timeouts, and diff previews before every production apply.
- **Input:** Upgrade policy and downtime budget.
- **Stop Condition:** Halt when rollback stays untested on paper; require walkthrough.
- **Validation:** Runbook covers upgrade, verify, and rollback paths.

### Step 4: Handoff and Human Review

- **Action:** Present the chart plan and request approval before packaging.
- **Input:** Completed blueprint.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero cluster writes performed.

## 4. Output Specification

```markdown
# Helm Blueprint

- **Chart:** [Structure with values schema]
- **Secrets:** [Reference strategy]
- **Upgrade:** [Hook order with rollback steps]
- **Verification:** [Lint and dry-run evidence]
```

## 5. Validation Gate

- [ ] Environments inventoried before templating.
- [ ] Values schema enforces required keys.
- [ ] Secrets referenced, never inline.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before packaging.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Templating without values schema or lint evidence.
- **Over-execution threshold:** Deploying charts to live clusters unprompted.
- **Calibration default:** One chart per service; share via library chart for common parts.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-1 (vague task)      | Requires inventory before templating.               |
| 2    | AP-44 (unlocked data)  | Bans inline secrets.                                |
| 3    | AP-28 (no stop)        | Demands rollback walkthrough.                       |
| 4    | AP-45 (no human review)| Halts for approval before packaging.                |

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

**Input:** "Our staging and prod YAML drifted apart and upgrades break."
**Output:** Chart blueprint with values schema per environment and hook-ordered upgrade runbook.
