---
name: flaky-test-root-cause-resolution
description: Systematic detection, quarantine, and root-cause remediation of asynchronous race conditions and timing leaks in test suites.
department: quality
ownerAgent: legolas
triggerCommand: /flaky-test-root-cause-resolution
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-18
  - AP-26
  - AP-28
---

# Flaky Test Root Cause Resolution

## 0. Identity

- **Role:** Diagnostic Analyst. Owns failure classification with evidence spans from stressed repetitions.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Diagnostic Analyst).
- **Seniority bar:** Staff (Appendix B). Records why quarantine beats deletion (signal preserved while noise contained, rejected silent test removal), why event predicates beat sleep timers (determinism under load, rejected timing hope), and why 100-run proof beats single green runs.
- **Authority:** Tier-5 normative skill for `skills/quality/flaky-test-root-cause-resolution/`. Owns flake diagnosis guidance.
- **Must not define:** Production business domain logic.
- **Normative base:** `core/fellowship/legolas.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`, `context/core-domains/testing-strategy.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-18 (timing leaks), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Detect, quarantine, diagnose, and remediate non-deterministic flaky automated tests.           |
| 2   | Target Tool      | Jest, Vitest, Playwright, Mocha, Stress-test repeaters.                                        |
| 3   | Output Format    | Remediated test files, quarantine tags, and root cause post-mortem documentation.              |
| 4   | Constraints      | Ban fixed sleep timers. Quarantine immediately. Zero em dashes. 100-run proof.                 |
| 5   | Input            | Flaky test error traces, CI run logs, reproduction command scripts.                            |
| 6   | Context          | Prevents broken pipelines, lost CI trust, and missed real regressions.                         |
| 7   | Audience         | Software engineers, test automation engineers, and build reliability teams.                    |
| 8   | Success Criteria | Target test runs 100 times consecutively in parallel with zero failures.                       |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger                                      | Fire? | Notes                              |
| -------------------------------------------- | ----- | ---------------------------------- |
| "This test flakes in CI"                     | YES   | Core trigger.                      |
| "Quarantine and diagnose flaky suites"       | YES   | Core trigger.                      |
| "/flaky-test-root-cause-resolution"          | YES   | Slash command trigger.             |
| "Delete the flaky test"                      | NO    | Refused; quarantine and fix.       |
| "Debug production business logic"            | NO    | Out of scope for this skill.       |

## 3. Execution Workflow

### Step 1: Quarantine Immediately

- **Action:** Move suspects to a non-blocking quarantine suite on first confirmed flake. Preserve the signal; contain the noise.
- **Input:** Flake reports with traces.
- **Stop Condition:** Halt when quarantine lacks tracking issues; require them.
- **Validation:** Quarantine list reviewed with owners.

### Step 2: Reproduce Under Stress

- **Action:** Repeat targeted suites 50 times in parallel under artificial load with hermetic state resets per run.
- **Input:** Quarantined tests from Step 1.
- **Stop Condition:** Halt when reproduction needs shared state; require isolation.
- **Validation:** Reproduction evidence recorded with failure rate.

### Step 3: Remediate Root Causes

- **Action:** Replace sleep timers with event predicates, isolate shared state per test, and fix race windows at their source.
- **Input:** Root causes from Step 2.
- **Stop Condition:** Halt when fixes mask timing instead of removing it.
- **Validation:** 100 consecutive parallel green runs evidenced.

### Step 4: Handoff and Human Review

- **Action:** Present the post-mortem with proof runs and request approval to promote from quarantine.
- **Input:** Completed remediation.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero deletions performed by this skill.

## 4. Output Specification

```markdown
# Flake Post-Mortem

- **Quarantine:** [Tagged list with issues]
- **Cause:** [Race evidence]
- **Fix:** [Remediation with proof runs]
```

## 5. Validation Gate

- [ ] Quarantine immediate with tracking.
- [ ] Reproduction stressed with isolation.
- [ ] 100-run green proof recorded.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before promotion.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Deleting flakes instead of diagnosing.
- **Over-execution threshold:** Rewriting production code unprompted.
- **Calibration default:** Quarantine first; diagnose second; promote last.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-18 (hidden state)   | Isolates state per run.                             |
| 2    | AP-26 (no scope)       | Stresses with recorded rates.                       |
| 3    | AP-28 (no stop)        | Demands 100-run proof.                              |
| 4    | AP-45 (no human review)| Halts for approval before promotion.                |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Diagnostic Analyst role, role source, and seniority bar.
  - `1.0.0` - Legacy flake baseline.

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

**Input:** "Checkout test flakes twice weekly with timeout errors."
**Output:** Post-mortem with response-predicate fix and 100-run green proof.
