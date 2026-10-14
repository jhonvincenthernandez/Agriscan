---
name: license-compliance-checker
description: Audits dependency licenses against allowlists, flags copyleft risks, and records attribution duties. Excludes legal counsel opinions.
department: workflow
ownerAgent: boromir
triggerCommand: /license-compliance-checker
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-26
  - AP-28
  - AP-45
---

# License Compliance Checker

## 0. Identity

- **Role:** Compliance Mapper. Owns license-to-policy traceability with bucket verdicts.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Compliance Mapper).
- **Seniority bar:** Staff (Appendix B). Records why three-source reconciliation beats manifest trust (declared licenses lie, rejected single-source audits), why transitive closure beats direct-only scans (risk hides transitively, rejected shallow audits), and why PR-stage gates beat annual reviews.
- **Authority:** Tier-5 normative skill for `skills/workflow/license-compliance-checker/`. Owns audit and remediation list.
- **Must not define:** Legal advice or binding counsel opinions; code rewrites.
- **Normative base:** `core/fellowship/boromir.md`, `rules/engineering/architecture-boundaries.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-26 (no scope boundary), AP-28 (no stop condition), and AP-45 (no human review trigger).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Audit licenses, flag policy violations, and list attribution and replacement actions.           |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.                |
| 3   | Output Format    | Compliance report with verdicts, evidence, and action list.                                    |
| 4   | Constraints      | Policy file required. Unknown licenses fail closed. Zero em dashes. No legal conclusions.      |
| 5   | Input            | Lockfile, license policy, distribution model, modified-code list.                               |
| 6   | Context          | Prevents copyleft contamination in closed distributions and missing attributions.               |
| 7   | Audience         | Engineering leads and compliance reviewers.                                                     |
| 8   | Success Criteria | Every dependency carries a verdict; violations mapped to actions; report approved.              |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger                                          | Fire? | Notes                              |
| ------------------------------------------------ | ----- | ---------------------------------- |
| "Audit our dependency licenses"                  | YES   | Core trigger.                      |
| "Check GPL risk before our release"              | YES   | Core trigger.                      |
| "/license-compliance-checker"                    | YES   | Slash command trigger.             |
| "Give us binding legal advice"                   | NO    | Refused; counsel decides.          |
| "Rewrite the flagged library"                    | NO    | Out of scope; owner action needed. |

## 3. Execution Workflow

### Step 1: Load Policy and Inventory

- **Action:** Read the allowlist and blocklist buckets, then inventory every locked dependency with declared licenses across metadata, files, and source headers.
- **Input:** Policy file and lockfile.
- **Stop Condition:** Halt and ask when policy file is missing.
- **Validation:** Inventory complete before verdicts.

### Step 2: Render Verdicts per Package

- **Action:** Mark allow, review, or block per package with license evidence and distribution impact notes. Fail unknown licenses closed.
- **Input:** Inventory from Step 1.
- **Stop Condition:** Halt on unknown licenses; mark block pending review.
- **Validation:** Every package carries a verdict with evidence.

### Step 3: Assign Attribution and Replacement

- **Action:** List attribution notices owed and replacement candidates for blocked packages with expiring exception records where counsel approves.
- **Input:** Verdicts from Step 2.
- **Stop Condition:** Halt when a blocked package lacks replacement research; mark for owner.
- **Validation:** Actions assigned per violation.

### Step 4: Handoff and Human Review

- **Action:** Present the report and request sign-off before release.
- **Input:** Completed report.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero code changed by this skill.

## 4. Output Specification

```markdown
# License Report

- **Verdicts:** [Allow, review, block per package]
- **Attribution:** [Notices owed]
- **Actions:** [Replacements per violation]
```

## 5. Validation Gate

- [ ] Policy loaded before inventory.
- [ ] Every dependency carries a verdict.
- [ ] Unknown licenses fail closed.
- [ ] Zero em dashes in deliverable.
- [ ] Human sign-off recorded before release.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Passing packages without license evidence.
- **Over-execution threshold:** Issuing legal conclusions or rewriting code.
- **Calibration default:** Block first on doubt; clear with counsel, not with hope.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-1 (vague task)      | Requires policy before inventory.                   |
| 2    | AP-26 (no scope)       | Verdicts cover every dependency.                    |
| 3    | AP-42 (no target)      | Assigns actions per violation.                      |
| 4    | AP-45 (no human review)| Halts for sign-off before release.                  |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Compliance Mapper role, role source, and seniority bar.
  - `1.0.0` (2026-09-26) - Initial release for supply chain compliance.

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

**Input:** "We ship a closed SDK next month. Audit licenses now."
**Output:** Report with two GPL blocks, three attribution notices, and replacement candidates.
