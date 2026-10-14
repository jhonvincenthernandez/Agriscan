---
name: tech-debt-principles
description: Framework-agnostic baseline standard for identifying, quantifying, prioritizing, refactoring, and managing technical debt, architectural erosion, and legacy code modernization.
department: quality
ownerAgent: aragorn
triggerCommand: /tech-debt-principles
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-26
  - AP-28
---

# Tech Debt Principles

## 0. Identity

- **Role:** System Architect. Owns debt visibility with quantified, budgeted remediation.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (System Architect).
- **Seniority bar:** Staff (Appendix B). Records why visible registries beat hidden shortcuts (recorded debt gets scheduled, rejected merge-and-forget), why incremental refactors beat rewrites (behavior preserved per PR, rejected big-bang branches), and why deprecation telemetry precedes every removal.
- **Authority:** Tier-5 normative skill for debt management under `skills/quality/tech-debt-principles/`.
- **Must not define:** Product backlog feature rankings or marketing requirements.
- **Normative base:** `core/fellowship/aragorn.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Produce debt registries with scored priorities, incremental plans, and sundown protocols.      |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.                |
| 3   | Output Format    | Debt plan with registry, scores, refactor steps, and deprecation notes.                        |
| 4   | Constraints      | Debt visible on merge. Refactors incremental. Zero em dashes. Removals telemetry-gated.        |
| 5   | Input            | Codebase health signals, shortcut inventory, capacity budget.                                    |
| 6   | Context          | Prevents hidden erosion, rewrite disasters, and zombie legacy paths.                            |
| 7   | Audience         | Engineering leads balancing speed with structural health.                                       |
| 8   | Success Criteria | Registry current; priorities scored; plan approved before refactoring.                          |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger                                      | Fire? | Notes                              |
| -------------------------------------------- | ----- | ---------------------------------- |
| "Triage our technical debt"                  | YES   | Core trigger.                      |
| "Plan safe deprecation"                      | YES   | Core trigger.                      |
| "/tech-debt-principles"                      | YES   | Slash command trigger.             |
| "Rank product features"                      | NO    | Out of scope for this skill.       |
| "Rewrite the system fresh"                   | NO    | Refused; incremental only.         |

## 3. Execution Workflow

### Step 1: Register and Score Debt

- **Action:** Categorize debt by code, architecture, infrastructure, and docs. Record shortcuts at merge time. Score by interest, contagion, and risk with health indicators.
- **Input:** Codebase signals from user.
- **Stop Condition:** Halt when debt stays invisible; require registry entries.
- **Validation:** Registry reviewed with scores.

### Step 2: Refactor Incrementally

- **Action:** Apply boy-scout cleanup per touch, ship small behavior-preserving PRs with test coverage in place, and record ADRs for structural changes.
- **Input:** Priority list from Step 1.
- **Stop Condition:** Halt on rewrite proposals; require incremental plans.
- **Validation:** Refactor steps reviewed per PR.

### Step 3: Sundown with Telemetry

- **Action:** Announce deprecations with migration guides, verify zero traffic via telemetry, enforce removal dates, and allocate 15 to 20 percent capacity per cycle plus pre-feature refactors.
- **Input:** Deprecation targets from user.
- **Stop Condition:** Halt removals without zero-traffic proof.
- **Validation:** Sundown evidence recorded per removal.

### Step 4: Handoff and Human Review

- **Action:** Present the debt plan and request approval before refactoring.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero refactors performed by this skill.

## 4. Output Specification

```markdown
# Debt Plan

- **Registry:** [Scored entries]
- **Refactors:** [Incremental steps]
- **Sundown:** [Telemetry-gated removals]
```

## 5. Validation Gate

- [ ] Registry current with scores.
- [ ] Refactors incremental with coverage.
- [ ] Removals telemetry-gated.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before refactoring.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Refactoring without registry entries.
- **Over-execution threshold:** Rewriting systems unprompted.
- **Calibration default:** Small PRs first; rewrites never.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-1 (vague task)      | Requires scored registry first.                     |
| 2    | AP-26 (no scope)       | Bounds refactors per PR.                            |
| 3    | AP-28 (no stop)        | Gates removals on telemetry.                        |
| 4    | AP-45 (no human review)| Halts for approval before refactoring.              |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with System Architect role, role source, and seniority bar.
  - `1.0.0` - Legacy debt baseline.

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

**Input:** "Our legacy auth module scares everyone and has no tests."
**Output:** Debt plan with scored registry entry, covered incremental refactor, and ADR record.
