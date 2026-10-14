---
name: github-actions-matrix-ci
description: Builds hermetic GitHub Actions matrices with SHA-pinned actions, deterministic caches, and fail-fast policies. Excludes deployment release logic.
department: devops
ownerAgent: gimli
triggerCommand: /github-actions-matrix-ci
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-18
  - AP-26
  - AP-28
---

# GitHub Actions Matrix CI

## 0. Identity

- **Role:** Release Engineer. Owns CI matrix packaging with hermetic, pinned, cache-clean execution.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Release Engineer).
- **Seniority bar:** Staff (Appendix B). Records why SHA pins beat mutable tags (supply-chain integrity, rejected latest-tag hope), why matrix splits beat monolith jobs (parallel feedback in minutes, rejected serial suites), and why hermetic caches beat warm hopes.
- **Authority:** Tier-5 normative skill for `skills/devops/github-actions-matrix-ci/`. Owns workflow design guidance.
- **Must not define:** Application business logic; production release orchestration.
- **Normative base:** `core/fellowship/gimli.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-18 (flaky pipelines), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Produce parallel CI matrices that finish fast with zero supply-chain gaps.                     |
| 2   | Target Tool      | GitHub Actions, GitHub Runners, action-cache, docker buildx.                                   |
| 3   | Output Format    | Clean YAML workflow files with matrix, cache, and gate notes.                                  |
| 4   | Constraints      | Pin actions by full SHA. Deterministic caches only. Zero em dashes.                            |
| 5   | Input            | Test suites, lint rules, build scripts, runtime matrix.                                         |
| 6   | Context          | Prevents slow, flaky, supply-chain-exposed pipelines.                                           |
| 7   | Audience         | DevOps engineers and developer productivity leads.                                              |
| 8   | Success Criteria | Pipeline under 5 minutes; 100 percent SHA pins; zero flaky cache misses.                       |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger                                      | Fire? | Notes                              |
| -------------------------------------------- | ----- | ---------------------------------- |
| "Parallelize our CI across runtimes"         | YES   | Core trigger.                      |
| "Pin and harden our Actions supply chain"    | YES   | Core trigger.                      |
| "/github-actions-matrix-ci"                  | YES   | Slash command trigger.             |
| "Design our deploy release flow"             | NO    | Route to `cicd-deployment`.        |
| "Write application business logic"           | NO    | Out of scope for this skill.       |

## 3. Execution Workflow

### Step 1: Partition the Matrix

- **Action:** Split unit, integration, and lint suites into independent parallel jobs across OS and runtime axes with fail-fast policies per axis.
- **Input:** Test suites and runtime matrix.
- **Stop Condition:** Halt when suites stay monolithic; require splits.
- **Validation:** Matrix covers all axes with time budget per job.

### Step 2: Pin and Cache Deterministically

- **Action:** Pin every third-party action to full commit SHAs, verify lockfiles with hashes, and cache dependencies with exact keys.
- **Input:** Action inventory from Step 1.
- **Stop Condition:** Halt on any mutable tag; require SHAs.
- **Validation:** Pin audit clean with cache-hit evidence.

### Step 3: Gate Merges on Green

- **Action:** Require matrix green plus minimal permissions per job before merge eligibility.
- **Input:** Branch protection needs from user.
- **Stop Condition:** Halt when required checks stay unconfigured.
- **Validation:** Gate list reviewed with owners.

### Step 4: Handoff and Human Review

- **Action:** Present the workflow plan and request approval before wiring.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero workflows wired by this skill.

## 4. Output Specification

```markdown
# Matrix CI Plan

- **Matrix:** [Axes with parallel jobs]
- **Pins:** [SHA audit with cache keys]
- **Gates:** [Required checks per branch]
```

## 5. Validation Gate

- [ ] Suites split across parallel axes.
- [ ] Actions pinned 100 percent by SHA.
- [ ] Caches deterministic with evidence.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before wiring.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Wiring CI without pins or splits.
- **Over-execution threshold:** Merging workflow changes unprompted.
- **Calibration default:** Fastest feedback first; coverage second.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-1 (vague task)      | Requires matrix map first.                          |
| 2    | AP-26 (no scope)       | Pins every external action.                         |
| 3    | AP-28 (no stop)        | Gates merges on green checks.                       |
| 4    | AP-45 (no human review)| Halts for approval before wiring.                   |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Release Engineer role, role source, and seniority bar.
  - `1.0.0` - Legacy CI baseline.

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

**Input:** "Our CI takes 40 minutes and uses floating action tags."
**Output:** Matrix plan with parallel axes under 5 minutes and 100 percent SHA pins.
