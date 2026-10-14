---
name: error-handling
description: Rules for exception design covering separation of concerns, contract-first catches, exception translation at third-party boundaries, Error.cause chaining, type-safe catch inspection, and the ban on exceptions as control flow.
department: quality
ownerAgent: legolas
triggerCommand: /error-handling
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-26
  - AP-28
---

# Error Handling

## 0. Identity

- **Role:** Syntax Reviewer. Owns failure-contract correctness with owned, chained, predictable errors.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Syntax Reviewer).
- **Seniority bar:** Staff (Appendix B). Records why contract-first catches beat scattered handling (callers depend on documented throws, rejected surprise failures), why adapter translation beats leaked vendor types (swap safety, rejected foreign exceptions in domains), and why single-boundary logging beats log-and-rethrow.
- **Authority:** Tier-5 normative skill for failure contracts under `skills/quality/error-handling/`.
- **Must not define:** Business domain rules or transport protocols.
- **Normative base:** `core/fellowship/legolas.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Produce failure contracts with owned types, chained causes, and single logging points.         |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.                |
| 3   | Output Format    | Error plan with contracts, translation map, and logging notes.                                 |
| 4   | Constraints      | Contracts first. Causes chained. Zero em dashes. No empty catches.                             |
| 5   | Input            | Failure surfaces, third-party boundaries, logging targets.                                      |
| 6   | Context          | Prevents unreadable failures, leaked vendor types, and duplicated error logs.                   |
| 7   | Audience         | Engineers writing fallible code paths.                                                          |
| 8   | Success Criteria | Contracts documented; causes chained; plan approved before coding.                              |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger                                      | Fire? | Notes                              |
| -------------------------------------------- | ----- | ---------------------------------- |
| "Design our error contracts"                 | YES   | Core trigger.                      |
| "Fix swallowed errors and dup logs"          | YES   | Core trigger.                      |
| "/error-handling"                            | YES   | Slash command trigger.             |
| "Design business domain rules"               | NO    | Out of scope for this skill.       |
| "Configure log transports"                   | NO    | Out of scope for this skill.       |

## 3. Execution Workflow

### Step 1: Contract Failures First

- **Action:** Define thrown types per function with tests asserting throws before logic exists. Keep algorithms linear with single-boundary handling.
- **Input:** Failure surfaces from user.
- **Stop Condition:** Halt when throws stay undocumented; require contracts.
- **Validation:** Contract map reviewed per function.

### Step 2: Translate at Boundaries

- **Action:** Wrap third-party exceptions in domain types behind adapters with chained causes. Narrow caught unknowns explicitly; never swallow silently.
- **Input:** Third-party boundaries from Step 1.
- **Stop Condition:** Halt on vendor types escaping domains.
- **Validation:** Translation map reviewed per boundary.

### Step 3: Log Once at Boundaries

- **Action:** Log at halting boundaries only, forbid log-and-rethrow duplicates, and reserve throwing for genuine breakage with Result types for expected absences.
- **Input:** Logging targets from user.
- **Stop Condition:** Halt on duplicate log points or control-flow throws.
- **Validation:** Logging audit complete per boundary.

### Step 4: Handoff and Human Review

- **Action:** Present the error plan and request approval before coding.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero code written by this skill.

## 4. Output Specification

```markdown
# Error Plan

- **Contracts:** [Throw map]
- **Translation:** [Adapter map]
- **Logging:** [Single-point notes]
```

## 5. Validation Gate

- [ ] Contracts documented per function.
- [ ] Causes chained per rethrow.
- [ ] Logging single-point per boundary.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before coding.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Throwing without contracts.
- **Over-execution threshold:** Redesigning domains unprompted.
- **Calibration default:** Contract first; handle once.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-1 (vague task)      | Requires contracts first.                           |
| 2    | AP-26 (no scope)       | Translates at boundaries.                           |
| 3    | AP-28 (no stop)        | Logs once per boundary.                             |
| 4    | AP-45 (no human review)| Halts for approval before coding.                   |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Syntax Reviewer role, role source, and seniority bar.
  - `1.0.0` - Legacy error baseline.

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

**Input:** "Our logs triple-count errors and vendor types leak everywhere."
**Output:** Plan with documented throws, adapter translation, and single-point logging.
