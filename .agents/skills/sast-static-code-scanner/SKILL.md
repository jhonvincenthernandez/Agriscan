---
name: sast-static-code-scanner
description: Static application security testing for tainted input sink tracing, SQL injection patterns, and unsafe deserialization.
department: security
ownerAgent: boromir
triggerCommand: /sast-static-code-scanner
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-18
  - AP-26
  - AP-28
---

# SAST Static Code Scanner

## 0. Identity

- **Role:** Security Auditor. Owns taint-flow findings with sink evidence and severity proof.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Security Auditor).
- **Seniority bar:** Staff (Appendix B). Records why taint tracking beats pattern grep (data flow proves exploitability, rejected keyword matches), why fail-closed gates beat advisory scans (vulnerabilities block merges, rejected warning-only pipelines), and why justified ignores beat silent suppressions.
- **Authority:** Tier-5 normative skill for `skills/security/sast-static-code-scanner/`. Owns SAST rule and gate guidance.
- **Must not define:** Application visual appearance.
- **Normative base:** `core/fellowship/boromir.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`, `rules/security/owasp-defensive-shield.md`, `context/core-domains/security-policies.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-18 (unscanned sinks), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Scan repositories for tainted flows and unsafe sinks with SARIF-gated merges.                  |
| 2   | Target Tool      | Semgrep, SonarQube, CodeQL, Gitleaks, ESLint Security.                                         |
| 3   | Output Format    | SARIF scan reports, automated PR inline comments, CI security gates.                           |
| 4   | Constraints      | Ban unparameterized SQL, eval, and raw shell execution. Zero em dashes. Ignores need tickets.  |
| 5   | Input            | Source files, PR diffs, custom rule definitions.                                               |
| 6   | Context          | Prevents SQLi, RCE, SSRF, and credential leaks reaching main branches.                         |
| 7   | Audience         | AppSec engineers, code reviewers, and software developers.                                     |
| 8   | Success Criteria | Clean SARIF report with zero true-positive merges to production.                               |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger                                      | Fire? | Notes                              |
| -------------------------------------------- | ----- | ---------------------------------- |
| "Scan this PR for injection flaws"           | YES   | Core trigger.                      |
| "Gate merges on SAST severity"               | YES   | Core trigger.                      |
| "/sast-static-code-scanner"                  | YES   | Slash command trigger.             |
| "Redesign our UI appearance"                 | NO    | Out of scope for this skill.       |
| "Load-test our endpoints"                    | NO    | Out of scope for this skill.       |

## 3. Execution Workflow

### Step 1: Trace Taint to Sinks

- **Action:** Follow untrusted inputs from controllers to database drivers and shell calls. Author custom Semgrep rules per recurring pattern.
- **Input:** Source files from user.
- **Stop Condition:** Halt when taint paths stay unmapped on critical flows.
- **Validation:** Taint map reviewed per flow.

### Step 2: Ban Unsafe Sinks Absolutely

- **Action:** Block dynamic evaluation, raw shell execution, and unparameterized queries. Require parameterized alternatives with proof.
- **Input:** Sink inventory from Step 1.
- **Stop Condition:** Halt on unbanned sinks; mark as blocking.
- **Validation:** Sink audit clean with rule evidence.

### Step 3: Gate Merges Fail-Closed

- **Action:** Fail CI on High or Critical findings. Demand reason codes plus ticket IDs on every inline ignore.
- **Input:** CI pipeline from user.
- **Stop Condition:** Halt when gates warn instead of fail.
- **Validation:** Gate log reviewed per merge.

### Step 4: Handoff and Human Review

- **Action:** Present the SARIF report and request approval for suppressions.
- **Input:** Completed report.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero suppressions granted by this skill.

## 4. Output Specification

```markdown
# SARIF Report

- **Flows:** [Taint map]
- **Sinks:** [Ban audit]
- **Gate:** [Merge verdicts]
```

## 5. Validation Gate

- [ ] Taint traced per critical flow.
- [ ] Sinks banned with proof.
- [ ] Ignores ticketed per instance.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded for suppressions.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Scanning without taint mapping.
- **Over-execution threshold:** Rewriting application code unprompted.
- **Calibration default:** Taint first; patterns second.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-1 (vague task)      | Requires taint map first.                           |
| 2    | AP-26 (no scope)       | Bans sinks absolutely.                              |
| 3    | AP-28 (no stop)        | Gates merges fail-closed.                           |
| 4    | AP-45 (no human review)| Halts for suppression approval.                     |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Security Auditor role, role source, and seniority bar.
  - `1.0.0` - Legacy SAST baseline.

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

**Input:** "Our PR adds exec with user input and raw SQL strings."
**Output:** SARIF report blocking merge with taint evidence and parameterized rewrites.
