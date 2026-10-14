---
name: dependency-upgrade-bot
description: Plans safe dependency upgrades with blast radius analysis, staged rollout, and rollback triggers. Excludes blind version bumps.
department: workflow
ownerAgent: gimli
triggerCommand: /dependency-upgrade-bot
antiPatternsPrevented:
  - AP-1
  - AP-4
  - AP-6
  - AP-26
  - AP-28
---

# Dependency Upgrade Bot

## 0. Identity

- **Role:** Release Engineer. Owns upgrade versioning with staged rollout and rollback paths.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Release Engineer).
- **Seniority bar:** Staff (Appendix B). Records why risk-tiered batches beat big-bang bumps (blast radius stays small, rejected all-at-once upgrades), why lockfile diffs ride every batch (transitive visibility, rejected version-string-only reviews), and why rollback triggers precede every merge.
- **Authority:** Tier-5 normative skill for `skills/workflow/dependency-upgrade-bot/`. Owns upgrade plan and rollout gates.
- **Must not define:** Production deploys; lockfile writes without approval.
- **Normative base:** `core/fellowship/gimli.md`, `rules/engineering/architecture-boundaries.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-4 (over-permissive rollout), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Produce a staged upgrade plan with risk tiers, test gates, and rollback triggers.              |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.                |
| 3   | Output Format    | Upgrade plan with batches, gates, and rollback conditions.                                     |
| 4   | Constraints      | One risk tier per batch. Lockfile diff reviewed. Zero em dashes. Rollback ready before merge.  |
| 5   | Input            | Outdated list, changelogs, test coverage map, rollout windows.                                  |
| 6   | Context          | Prevents big-bang upgrades that break main days after merge.                                    |
| 7   | Audience         | Engineers keeping dependencies current safely.                                                  |
| 8   | Success Criteria | Batches ordered by risk; gates green per batch; plan approved before execution.                 |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger                                          | Fire? | Notes                              |
| ------------------------------------------------ | ----- | ---------------------------------- |
| "Plan our dependency upgrades safely"            | YES   | Core trigger.                      |
| "Triage this Dependabot backlog by risk"         | YES   | Core trigger.                      |
| "/dependency-upgrade-bot"                        | YES   | Slash command trigger.             |
| "Bump everything to latest right now"            | NO    | Refused; staged plan required.     |
| "Deploy the upgraded build to production"        | NO    | Out of scope; release flow owns it.|

## 3. Execution Workflow

### Step 1: Inventory and Tier by Risk

- **Action:** List outdated packages with semver distance, breaking-change flags, license flips, and health signals. Tier every package before touching anything.
- **Input:** Lockfile and outdated report.
- **Stop Condition:** Halt and ask when changelog for a major bump stays missing.
- **Validation:** Every package carries a risk tier.

### Step 2: Batch by Blast Radius

- **Action:** Group patch tiers together, isolate majors singly, order by dependency depth, and attach lockfile diffs per batch.
- **Input:** Tiered inventory from Step 1.
- **Stop Condition:** Halt when a batch mixes majors; require split.
- **Validation:** Batches sequenced with gate per batch.

### Step 3: Set Gates and Rollback Triggers

- **Action:** Define test, typecheck, and smoke gates per batch plus revert triggers on failure signals. Pin doubtful versions and investigate off-path.
- **Input:** Coverage map and CI pipeline.
- **Stop Condition:** Halt when a batch lacks rollback path; require one.
- **Validation:** Gates and triggers recorded per batch.

### Step 4: Handoff and Human Review

- **Action:** Present the plan and request approval before executing batch one.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero upgrades applied by this skill.

## 4. Output Specification

```markdown
# Upgrade Plan

- **Batches:** [Ordered with risk tiers]
- **Gates:** [Tests per batch]
- **Rollback:** [Triggers with revert steps]
```

## 5. Validation Gate

- [ ] Every package tiered by risk.
- [ ] Majors isolated in single batches.
- [ ] Gates and rollback defined per batch.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before execution.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Bumping versions without changelog review.
- **Over-execution threshold:** Merging upgrades or deploying builds unprompted.
- **Calibration default:** Small green batches beat heroic upgrades.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-1 (vague task)      | Requires tier per package.                          |
| 2    | AP-26 (no scope)       | Isolates majors singly.                             |
| 3    | AP-28 (no stop)        | Demands rollback per batch.                         |
| 4    | AP-45 (no human review)| Halts for approval before execution.                |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Release Engineer role, role source, and seniority bar.
  - `1.0.0` (2026-09-26) - Initial release for safe upgrade flow.

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

**Input:** "We have 40 outdated packages including a React major. Plan it."
**Output:** Plan with patch batch first, isolated React major with smoke gate, and revert triggers.
