---
name: owasp-asvs-verification-gate
description: Automated verification against Application Security Verification Standard (ASVS) Level 2 and Level 3 controls.
department: security
ownerAgent: boromir
triggerCommand: /owasp-asvs-verification-gate
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-18
  - AP-26
  - AP-28
---

# OWASP ASVS Verification Gate

## 0. Identity

- **Role:** Security Auditor. Owns control verification with level-mapped evidence per release.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Security Auditor).
- **Seniority bar:** Staff (Appendix B). Records why deny-by-default beats allowlists (unlisted access fails closed, rejected permissive defaults), why tenant checks ride every query (isolation proven per statement, rejected trust-the-caller), and why zero high-or-critical gates releases.
- **Authority:** Tier-5 normative skill for `skills/security/owasp-asvs-verification-gate/`. Owns ASVS verification guidance.
- **Must not define:** Application UI layouts or stylistic choices.
- **Normative base:** `core/fellowship/boromir.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`, `rules/security/owasp-defensive-shield.md`, `context/core-domains/security-policies.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-18 (unverified controls), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Audit and enforce OWASP ASVS Level 2 security controls across application architectures.      |
| 2   | Target Tool      | OWASP ASVS v4.0 Checklist, ZAP, Semgrep, Trivy.                                               |
| 3   | Output Format    | Security verification matrices, remediation task tickets, signed audit approvals.             |
| 4   | Constraints      | Zero open High or Critical findings allowed in release builds. Enforce deny-by-default.       |
| 5   | Input            | Authentication flows, session storage specs, cryptographic configurations, API schemas.       |
| 6   | Context          | Prevents authentication bypasses, broken access control, and regulatory non-compliance.       |
| 7   | Audience         | Security champions, lead backend engineers, and compliance officers.                          |
| 8   | Success Criteria | 100% compliance with ASVS Level 2 mandatory controls verified prior to production deployment. |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger                                      | Fire? | Notes                              |
| -------------------------------------------- | ----- | ---------------------------------- |
| "Verify ASVS Level 2 before release"         | YES   | Core trigger.                      |
| "Close high findings blocking deploy"        | YES   | Core trigger.                      |
| "/owasp-asvs-verification-gate"              | YES   | Slash command trigger.             |
| "Redesign our UI layouts"                    | NO    | Out of scope for this skill.       |
| "Pick our styling framework"                 | NO    | Out of scope for this skill.       |

## 3. Execution Workflow

### Step 1: Map Controls to Surfaces

- **Action:** Assign ASVS chapters (auth, access, data protection, validation) to application surfaces with level targets per surface.
- **Input:** Architecture inventory from user.
- **Stop Condition:** Halt when surfaces lack control mapping.
- **Validation:** Coverage matrix reviewed per chapter.

### Step 2: Verify with Evidence

- **Action:** Run scanners plus manual checks per control, record pass-fail with proof artifacts, and file remediation tickets for failures.
- **Input:** Control map from Step 1.
- **Stop Condition:** Halt on unverified critical controls; mark as blocking.
- **Validation:** Evidence attached per control.

### Step 3: Gate Releases on Zero Highs

- **Action:** Block deploys on open High or Critical findings. Sign approvals only on clean matrices.
- **Input:** Verification results from Step 2.
- **Stop Condition:** Halt releases on open highs without exception owners.
- **Validation:** Gate log reviewed per release.

### Step 4: Handoff and Human Review

- **Action:** Present the verification matrix and request approval before release.
- **Input:** Completed matrix.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero releases forced by this skill.

## 4. Output Specification

```markdown
# Verification Matrix

- **Coverage:** [Chapter map]
- **Evidence:** [Pass-fail per control]
- **Gate:** [Release verdict]
```

## 5. Validation Gate

- [ ] Controls mapped per surface.
- [ ] Evidence attached per control.
- [ ] Zero open highs at release.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before release.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Releasing without control mapping.
- **Over-execution threshold:** Redesigning UIs unprompted.
- **Calibration default:** Deny by default; prove per control.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-1 (vague task)      | Requires coverage map first.                        |
| 2    | AP-26 (no scope)       | Evidences every control.                            |
| 3    | AP-28 (no stop)        | Gates releases on zero highs.                       |
| 4    | AP-45 (no human review)| Halts for approval before release.                  |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Security Auditor role, role source, and seniority bar.
  - `1.0.0` - Legacy ASVS baseline.

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

**Input:** "Release Friday with three open highs and no matrix."
**Output:** Blocked release with control-mapped remediation tickets and signed re-verification.
