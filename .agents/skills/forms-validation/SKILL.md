---
name: forms-validation
description: Form engineering rules covering schema-first validation, accessible inputs, async checks, and server reconciliation. Excludes backend persistence logic.
department: frontend
ownerAgent: legolas
triggerCommand: /forms-validation
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-26
  - AP-28
---

# Forms Validation

## 0. Identity

- **Role:** Interface Builder. Owns form composition with validated, accessible submission flows.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Interface Builder).
- **Seniority bar:** Staff (Appendix B). Records why schema-first beats handler validation (single source of truth, rejected scattered checks), why inline feedback beats submit-only errors (correction cost lowest at entry, rejected surprise rejections), and why server reconciliation beats client trust.
- **Authority:** Tier-5 normative skill for `skills/frontend/forms-validation/`. Owns form and validation guidance.
- **Must not define:** Backend persistence logic.
- **Normative base:** `core/fellowship/legolas.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                               |
| --- | ---------------- | ----------------------------------------------------------------------------------- |
| 1   | Task             | Produce forms with schema contracts, accessible inputs, and reconciled submissions. |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.    |
| 3   | Output Format    | Form plan with schemas, states, a11y notes, and submission flow.                    |
| 4   | Constraints      | Schemas first. Labels always. Zero em dashes. Server has final say.                 |
| 5   | Input            | Form specs, validation rules, async check needs, submit targets.                    |
| 6   | Context          | Prevents unvalidated submissions, inaccessible inputs, and silent failures.         |
| 7   | Audience         | Frontend engineers building data-entry flows.                                       |
| 8   | Success Criteria | Schemas cover fields; inputs labeled; plan approved before coding.                  |
| 9   | Examples         | See Section 10.                                                                     |

## 2. Trigger Matrix

| Trigger                             | Fire? | Notes                        |
| ----------------------------------- | ----- | ---------------------------- |
| "Build a validated checkout form"   | YES   | Core trigger.                |
| "Fix our form errors and a11y gaps" | YES   | Core trigger.                |
| "/forms-validation"                 | YES   | Slash command trigger.       |
| "Design our database schema"        | NO    | Out of scope for this skill. |
| "Write backend persistence"         | NO    | Out of scope for this skill. |

## 3. Execution Workflow

### Step 1: Schema Every Field

- **Action:** Define validation schemas per form with types, constraints, and cross-field rules shared between client and server where possible.
- **Input:** Form specs and validation rules.
- **Stop Condition:** Halt when fields lack schemas; require them.
- **Validation:** Schema map reviewed per form.

### Step 2: Label and State Inputs

- **Action:** Pair every input with programmatic labels, autocomplete tokens, error slots with aria-live regions, and disabled plus loading states during submission.
- **Input:** Accessibility targets from user.
- **Stop Condition:** Halt on unlabeled inputs; require labels.
- **Validation:** A11y audit complete per form.

### Step 3: Reconcile Submissions

- **Action:** Validate inline on blur with debounced async uniqueness checks, submit optimistically where safe, and reconcile server rejections back into field errors without data loss.
- **Input:** Submit targets and async needs.
- **Stop Condition:** Halt when server errors drop user input; require preservation.
- **Validation:** Submission flow reviewed end to end.

### Step 4: Handoff and Human Review

- **Action:** Present the plan and request approval before coding.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero code written by this skill.

## 4. Output Specification

```markdown
# Form Plan

- **Schemas:** [Contracts per form]
- **Inputs:** [Labeled states]
- **Submission:** [Reconciliation flow]
```

## 5. Validation Gate

- [ ] Schemas cover every field.
- [ ] Inputs labeled with live errors.
- [ ] Submissions preserve data on reject.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before coding.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Building forms without schemas.
- **Over-execution threshold:** Writing backend persistence unprompted.
- **Calibration default:** Validate early; trust server finally.

## 7. Anti-Pattern Compliance

| Step | Prevents AP             | Mechanism                          |
| ---- | ----------------------- | ---------------------------------- |
| 1    | AP-1 (vague task)       | Requires schemas first.            |
| 2    | AP-26 (no scope)        | Labels every input.                |
| 3    | AP-28 (no stop)         | Reconciles submissions explicitly. |
| 4    | AP-45 (no human review) | Halts for approval before coding.  |

## 8. Versioning & Changelog

- **Version:** 1.0.0
- **Changelog:**
  - `1.0.0` (2026-09-26) - Initial release closing the forms gap.

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

**Input:** "Our signup form rejects silently and screen readers miss errors."
**Output:** Plan with field schemas, live error regions, and reconciled submissions preserving input.
