---
name: disaster-recovery-design
description: Disaster recovery rules covering RTO and RPO targets, backup verification, multi-region failover, and game-day rehearsals. Excludes backup vendor selection.
department: architecture
ownerAgent: aragorn
triggerCommand: /disaster-recovery-design
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-26
  - AP-28
---

# Disaster Recovery Design

## 0. Identity

- **Role:** System Architect. Owns continuity shape with tested recovery paths per tier.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (System Architect).
- **Seniority bar:** Staff (Appendix B). Records why rehearsed restores beat documented procedures (untested backups are rumors, rejected paper plans), why tiered RTO beats one-size recovery (critical paths deserve budgets, rejected uniform hope), and why game days precede real incidents.
- **Authority:** Tier-5 normative skill for `skills/architecture/disaster-recovery-design/`. Owns continuity planning guidance.
- **Must not define:** Backup vendor selection or incident command staffing.
- **Normative base:** `core/fellowship/aragorn.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                               |
| --- | ---------------- | ----------------------------------------------------------------------------------- |
| 1   | Task             | Produce tiered recovery plans with tested restores and rehearsed failovers.         |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.    |
| 3   | Output Format    | Continuity plan with tiers, restore proofs, and rehearsal notes.                    |
| 4   | Constraints      | RTO and RPO numeric per tier. Restores tested. Zero em dashes. Game days scheduled. |
| 5   | Input            | Service tiers, data inventory, compliance needs, drill calendar.                    |
| 6   | Context          | Prevents untested backups and unrehearsed failovers failing on incident day.        |
| 7   | Audience         | Architects owning continuity for production systems.                                |
| 8   | Success Criteria | Tiers targeted; restores proven; plan approved.                                     |
| 9   | Examples         | See Section 10.                                                                     |

## 2. Trigger Matrix

| Trigger                              | Fire? | Notes                        |
| ------------------------------------ | ----- | ---------------------------- |
| "Design DR for our platform"         | YES   | Core trigger.                |
| "Prove our backups actually restore" | YES   | Core trigger.                |
| "/disaster-recovery-design"          | YES   | Slash command trigger.       |
| "Pick our backup vendor"             | NO    | Out of scope for this skill. |
| "Staff our incident command"         | NO    | Out of scope for this skill. |

## 3. Execution Workflow

### Step 1: Tier Services and Data

- **Action:** Assign RTO and RPO numbers per tier with compliance floors where regulated data applies.
- **Input:** Service tiers from user.
- **Stop Condition:** Halt when tiers lack numeric targets.
- **Validation:** Tier table reviewed with targets.

### Step 2: Prove Restores Work

- **Action:** Restore backups into isolated environments on schedule, verify data integrity post-restore, and record recovery times against targets.
- **Input:** Backup inventory from Step 1.
- **Stop Condition:** Halt on untested backup sets; require proof restores.
- **Validation:** Restore evidence recorded per dataset.

### Step 3: Rehearse Failover

- **Action:** Run game days failing regions and dependencies on calendar, promote standby paths, and fix every surprise before the next drill.
- **Input:** Drill calendar from user.
- **Stop Condition:** Halt when rehearsals stay unscheduled.
- **Validation:** Drill reports reviewed with action items.

### Step 4: Handoff and Human Review

- **Action:** Present the continuity plan and request approval before adoption.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero failovers performed by this skill.

## 4. Output Specification

```markdown
# Continuity Plan

- **Tiers:** [RTO and RPO table]
- **Restores:** [Proof evidence]
- **Drills:** [Game-day schedule]
```

## 5. Validation Gate

- [ ] Tiers targeted numerically.
- [ ] Restores proven with evidence.
- [ ] Drills scheduled with owners.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before adoption.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Planning continuity without restore proof.
- **Over-execution threshold:** Failing over systems unprompted.
- **Calibration default:** Test restores first; write plans second.

## 7. Anti-Pattern Compliance

| Step | Prevents AP             | Mechanism                           |
| ---- | ----------------------- | ----------------------------------- |
| 1    | AP-1 (vague task)       | Requires numeric tiers first.       |
| 2    | AP-26 (no scope)        | Proves restores per dataset.        |
| 3    | AP-28 (no stop)         | Schedules drills with owners.       |
| 4    | AP-45 (no human review) | Halts for approval before adoption. |

## 8. Versioning & Changelog

- **Version:** 1.0.0
- **Changelog:**
  - `1.0.0` (2026-09-26) - Initial release closing the continuity planning gap.

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

**Input:** "Nobody knows if our backups restore or how long failover takes."
**Output:** Plan with tiered targets, proven restores, and scheduled game days.
