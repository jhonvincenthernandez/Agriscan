---
name: evaluation-harness-framework
description: Formal evaluation framework for autonomous agents implementing Eval-Driven Development (EDD), pass@k reliability metrics, code-based deterministic grading, and regression testing.
department: quality
ownerAgent: merry
triggerCommand: /evaluation-harness-framework
antiPatternsPrevented:
  - AP-1
  - AP-3
  - AP-6
  - AP-9
  - AP-18
  - AP-28
  - AP-53
---

# Evaluation Harness Framework

## 0. Identity

- **Role:** Quality Gatekeeper. Owns eval verdicts on agent capability with deterministic grading evidence.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Quality Gatekeeper).
- **Seniority bar:** Staff (Appendix B). Records why evals precede code (acceptance defined before implementation, rejected build-then-measure), why code graders beat model graders where verifiable (exit codes over opinions, rejected LLM judges for checkable outcomes), and why pass^k governs critical paths.
- **Authority:** Tier-5 normative skill for `skills/quality/evaluation-harness-framework/`. Owns eval design guidance.
- **Must not define:** Application UI components or database table schemas.
- **Normative base:** `core/fellowship/merry.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`, `context/core-domains/testing-strategy.md`.
- **Anti-pattern gate:** Blocks AP-3 (unclear success criteria), AP-9 (declaring success without verified execution), and AP-53 (blind tool confidence).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                                      |
| --- | ---------------- | ---------------------------------------------------------------------------------------------------------- |
| 1   | Task             | Define, execute, and score automated capability and regression evals for AI agent workflows.               |
| 2   | Target Tool      | Sauron test suites, Jest, Vitest, Python pytest, Bash verification scripts, model graders.                 |
| 3   | Output Format    | Structured Eval Definitions, Pass/Fail Execution Logs, and pass@k Summary Reports.                         |
| 4   | Constraints      | Code-based deterministic grading preferred over subjective model grading. Always define evals before code. |
| 5   | Input            | Capability specifications, agent transcripts, expected code artifacts, regression test suites.             |
| 6   | Context          | Prevents silent capability drift, brittle prompt edits, and unreliable agent task completion.              |
| 7   | Audience         | Quality engineers, agent platform architects, autonomous workflow operators.                               |
| 8   | Success Criteria | 100 percent deterministic grading for code tasks; minimum pass@3 score of 90 percent on critical paths.    |
| 9   | Examples         | See Section 10.                                                                                             |

## 2. Trigger Matrix

| Trigger Condition                                                    | Fire? | Action / Route                                                                             |
| -------------------------------------------------------------------- | ----- | ------------------------------------------------------------------------------------------ |
| Designing acceptance criteria for complex autonomous agent workflows | YES   | Formulate Capability and Regression Evals.                                                 |
| Measuring agent consistency across repeated trials                   | YES   | Calculate pass@k and pass^k reliability metrics.                                           |
| Testing application business logic or backend endpoints              | NO    | Route to `skills/workflow/autonomous-dev/05-quality-and-testing/test-driven-development/`. |
| Running security audits or vulnerability scans                        | NO    | Route to `skills/security/security-auditor/`.                                              |

## 3. Execution Workflow

### Step 1: Define Evals Before Code

- **Action:** Write capability evals with grading logic and regression evals with baselines before implementation starts.
- **Input:** Capability specifications from user.
- **Stop Condition:** Halt when success criteria stay verbal; require measurable evals.
- **Validation:** Eval definitions reviewed with grading tiers.

### Step 2: Grade Deterministically First

- **Action:** Apply code graders (exit codes, schemas, file diffs) wherever verifiable. Reserve model graders with scored rubrics for open-ended quality, and human gates for high-risk paths.
- **Input:** Agent outputs from trial runs.
- **Stop Condition:** Halt when LLM judges grade checkable outcomes; require code graders.
- **Validation:** Grader tier justified per eval.

### Step 3: Score Reliability and Regressions

- **Action:** Compute pass@k across trials and pass^k on critical paths. Track capability drift across prompt edits with regression suites.
- **Input:** Trial results from Step 2.
- **Stop Condition:** Halt below reliability bars; require remediation.
- **Validation:** Score report reviewed with drift notes.

### Step 4: Handoff and Human Review

- **Action:** Present the eval report and request approval for threshold changes.
- **Input:** Completed report.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero thresholds changed by this skill.

## 4. Output Specification

```markdown
# Eval Report

- **Definitions:** [Capability with grading tiers]
- **Scores:** [pass@k with drift notes]
- **Verdict:** [Pass or fail with evidence]
```

## 5. Validation Gate

- [ ] Evals defined before code.
- [ ] Deterministic grading preferred.
- [ ] Reliability scored with bars.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded for threshold changes.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Shipping agent behavior without evals.
- **Over-execution threshold:** Changing thresholds unprompted.
- **Calibration default:** Code graders first; models last.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-3 (no success)      | Demands measurable evals first.                     |
| 2    | AP-53 (blind trust)    | Prefers verifiable graders.                         |
| 3    | AP-9 (unverified wins) | Scores reliability with bars.                       |
| 4    | AP-45 (no human review)| Halts for approval on threshold changes.            |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Quality Gatekeeper role, role source, and seniority bar.
  - `1.0.0` - Legacy eval baseline.

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

**Input:** "Our agent passes once then fails twice on the same task."
**Output:** Eval harness with pass@3 scoring proving inconsistency and gating promotion.
