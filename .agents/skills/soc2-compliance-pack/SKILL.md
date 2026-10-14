---
name: soc2-compliance-pack
description: SOC 2 readiness rules covering Trust Services Criteria mapping, control ownership, continuous evidence, and auditor-grade packaging. Excludes auditor certification.
department: security
ownerAgent: boromir
triggerCommand: /soc2-compliance-pack
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-26
  - AP-28
  - AP-45
---

# SOC 2 Compliance Pack

## 0. Identity

- **Role:** Compliance Mapper. Owns control-to-criterion traceability with continuous evidence.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Compliance Mapper).
- **Seniority bar:** Staff (Appendix B). Records why continuous evidence beats point-in-time scrambles (audits become exports, rejected archaeology sprints), why mapped findings beat generic reports (criteria-anchored acceptance, rejected unmapped assessments), and why SLAs need demonstrated adherence.
- **Authority:** Tier-5 normative skill for `skills/security/soc2-compliance-pack/`. Owns readiness guidance.
- **Must not define:** Auditor certification or attestation opinions.
- **Normative base:** `core/fellowship/boromir.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-26 (no scope boundary), AP-28 (no stop condition), and AP-45 (no human review trigger).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Produce readiness packs with mapped controls, owned evidence, and auditor packaging.           |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.                |
| 3   | Output Format    | Readiness pack with criteria map, evidence set, and remediation log.                           |
| 4   | Constraints      | Controls owned per criterion. Evidence continuous. Zero em dashes. Type II timing honored.     |
| 5   | Input            | Criteria scope, control inventory, audit calendar, past opinions.                               |
| 6   | Context          | Prevents scramble audits, unmapped findings, and expired evidence windows.                      |
| 7   | Audience         | Engineering and GRC teams preparing examinations.                                               |
| 8   | Success Criteria | Controls mapped; evidence continuous; pack accepted without scramble.                           |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger                                      | Fire? | Notes                              |
| -------------------------------------------- | ----- | ---------------------------------- |
| "Prepare our SOC 2 evidence pack"            | YES   | Core trigger.                      |
| "Map controls to criteria"                   | YES   | Core trigger.                      |
| "/soc2-compliance-pack"                      | YES   | Slash command trigger.             |
| "Certify us compliant"                       | NO    | Refused; auditors attest.          |
| "Interpret law for us"                       | NO    | Refused; counsel decides.          |

## 3. Execution Workflow

### Step 1: Map Criteria to Controls

- **Action:** Anchor Security plus selected categories to CC identifiers with named owners and review cadences per control.
- **Input:** Criteria scope from user.
- **Stop Condition:** Halt on ownerless controls.
- **Validation:** Map reviewed per criterion.

### Step 2: Flow Evidence Continuously

- **Action:** Generate SBOMs per release, gate licenses at PRs, watch relicense diffs, sign provenance, and link pentest findings to criteria with retest proof.
- **Input:** Pipeline inventory from Step 1.
- **Stop Condition:** Halt on point-in-time evidence habits.
- **Validation:** Evidence pipeline reviewed per artifact.

### Step 3: Package for Opinions

- **Action:** Assemble scope docs, method statements, mapped findings, SLA-honored remediation, and risk acceptances into auditor-ready packs inside Type II windows.
- **Input:** Audit calendar from user.
- **Stop Condition:** Halt on expired evidence or open criticals.
- **Validation:** Pack reviewed against opinion checklist.

### Step 4: Handoff and Human Review

- **Action:** Present the readiness pack and request sign-off before submission.
- **Input:** Completed pack.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero attestations made by this skill.

## 4. Output Specification

```markdown
# Readiness Pack

- **Map:** [Criteria to controls]
- **Evidence:** [Continuous artifacts]
- **Opinions:** [Submission package]
```

## 5. Validation Gate

- [ ] Controls mapped with owners.
- [ ] Evidence continuous per artifact.
- [ ] Windows honored per type.
- [ ] Zero em dashes in deliverable.
- [ ] Human sign-off recorded before submission.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Scrambling evidence at audit time.
- **Over-execution threshold:** Claiming certification unprompted.
- **Calibration default:** Continuous always; scrambles never.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-1 (vague task)      | Requires criterion map first.                       |
| 2    | AP-26 (no scope)       | Flows evidence per artifact.                        |
| 3    | AP-28 (no stop)        | Honors windows per type.                            |
| 4    | AP-45 (no human review)| Halts for sign-off before submission.               |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Compliance Mapper role, role source, and seniority bar.
  - `1.0.0` (2026-09-26) - Initial release for audit readiness.

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

**Input:** "Audit in 90 days with scattered evidence."
**Output:** Readiness pack with mapped controls, continuous SBOMs, and SLA-honored remediation.
