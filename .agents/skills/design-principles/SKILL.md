---
name: design-principles
description: Structural design axioms for application code covering SOLID, composition over inheritance, DRY, KISS, YAGNI, AHA, Law of Demeter, and object-data duality.
department: quality
ownerAgent: aragorn
triggerCommand: /design-principles
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-26
  - AP-28
---

# Design Principles

## 0. Identity

- **Role:** System Architect. Owns structural axiom enforcement with rent-paying abstractions.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (System Architect).
- **Seniority bar:** Staff (Appendix B). Records why SRP beats DRY in conflicts (one owner beats shared coupling, rejected clever sharing), why mild duplication beats wrong abstractions (cheap to carry, rejected premature coupling), and why every abstraction pays rent or gets deleted.
- **Authority:** Tier-5 normative skill for structural design across repositories under `skills/quality/design-principles/`.
- **Must not define:** Product backlog rankings or marketing requirements.
- **Normative base:** `core/fellowship/aragorn.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Apply structural axioms to modules, components, and hierarchies with explicit trade-offs.       |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.                |
| 3   | Output Format    | Design review with axiom verdicts and abstraction rent audit.                                   |
| 4   | Constraints      | Axioms cited per decision. Abstractions pay rent. Zero em dashes.                              |
| 5   | Input            | Modules, components, or hierarchies under review.                                               |
| 6   | Context          | Prevents accidental structure that accrues abstraction debt.                                    |
| 7   | Audience         | Engineers designing modules and class hierarchies.                                              |
| 8   | Success Criteria | Decisions principled; abstractions justified; plan approved.                                     |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger                                      | Fire? | Notes                              |
| -------------------------------------------- | ----- | ---------------------------------- |
| "Review this module structure"               | YES   | Core trigger.                      |
| "Settle this abstraction debate"             | YES   | Core trigger.                      |
| "/design-principles"                         | YES   | Slash command trigger.             |
| "Rank our product backlog"                   | NO    | Out of scope for this skill.       |
| "Write marketing requirements"               | NO    | Out of scope for this skill.       |

## 3. Execution Workflow

### Step 1: Apply SOLID per Decision

- **Action:** Check single responsibility, extension by composition, substitutability, narrow interfaces, and dependency direction per structure under review.
- **Input:** Modules from user.
- **Stop Condition:** Halt when decisions lack cited axioms.
- **Validation:** Axiom verdicts recorded per decision.

### Step 2: Price Every Abstraction

- **Action:** Resolve SRP-versus-DRY toward SRP, prefer duplication over hasty coupling, demand YAGNI evidence for new surface, and audit rent per abstraction.
- **Input:** Abstraction inventory from Step 1.
- **Stop Condition:** Halt on speculative features; require current requirements.
- **Validation:** Rent audit complete with keep-or-delete calls.

### Step 3: Bound Data and Behavior

- **Action:** Enforce Demeter call limits, tell-don't-ask commands, true encapsulation, data-or-object purity, and pure cores with imperative shells.
- **Input:** Type inventory from Step 2.
- **Stop Condition:** Halt on anemic hybrids; require splits.
- **Validation:** Boundary review complete per type.

### Step 4: Handoff and Human Review

- **Action:** Present the review and request approval before refactoring.
- **Input:** Completed review.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero refactors performed by this skill.

## 4. Output Specification

```markdown
# Design Review

- **Verdicts:** [Axiom per decision]
- **Abstractions:** [Rent audit]
- **Boundaries:** [Data and behavior notes]
```

## 5. Validation Gate

- [ ] Axioms cited per decision.
- [ ] Abstractions pay rent or die.
- [ ] Data and behavior separated.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before refactoring.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Structuring code without cited axioms.
- **Over-execution threshold:** Refactoring codebases unprompted.
- **Calibration default:** Simple structures first; abstractions earn entry.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-1 (vague task)      | Requires axiom verdicts first.                      |
| 2    | AP-26 (no scope)       | Prices abstractions explicitly.                     |
| 3    | AP-28 (no stop)        | Bounds data and behavior.                           |
| 4    | AP-45 (no human review)| Halts for approval before refactoring.              |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with System Architect role, role source, and seniority bar.
  - `1.0.0` - Legacy axioms baseline.

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

**Input:** "Should we abstract these three similar flows?"
**Output:** Review settling on duplication until the third repeat, with rent audit scheduled.
