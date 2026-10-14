---
name: playwright-visual-testing-fixtures
description: Hermetic browser automation fixtures, visual snapshot diffing, pixel tolerance thresholds, and animation stabilization.
department: quality
ownerAgent: merry
triggerCommand: /playwright-visual-testing-fixtures
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-18
  - AP-26
  - AP-28
---

# Playwright Visual Testing Fixtures

## 0. Identity

- **Role:** Quality Gatekeeper. Owns visual verdicts with deterministic fixtures and tolerance evidence.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Quality Gatekeeper).
- **Seniority bar:** Staff (Appendix B). Records why frozen environments beat live pages (animations and fonts lie, rejected flaky baselines), why tight tolerances beat loose ones (real regressions hide in noise budgets, rejected 5 percent allowances), and why mocked networks beat live APIs in snapshots.
- **Authority:** Tier-5 normative skill for `skills/quality/playwright-visual-testing-fixtures/`. Owns visual fixture guidance.
- **Must not define:** Backend database migrations.
- **Normative base:** `core/fellowship/merry.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`, `context/core-domains/testing-strategy.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-18 (flaky snapshots), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Automate screenshot comparisons with deterministic, isolated browser fixtures.                 |
| 2   | Target Tool      | Playwright Test runner, Chromium, WebKit, Firefox engines.                                     |
| 3   | Output Format    | Visual test scripts, snapshot baselines, and HTML diff reports.                                |
| 4   | Constraints      | Freeze animations. Mock networks. Zero em dashes. Tight tolerances.                            |
| 5   | Input            | Component specs, responsive targets, viewport matrix.                                           |
| 6   | Context          | Prevents silent UI breakages and cross-browser visual drift.                                    |
| 7   | Audience         | Frontend engineers, design systems teams, and QA specialists.                                   |
| 8   | Success Criteria | Zero false-positive diffs with sub-pixel stability evidenced.                                   |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger                                      | Fire? | Notes                              |
| -------------------------------------------- | ----- | ---------------------------------- |
| "Add visual regression to our components"    | YES   | Core trigger.                      |
| "Fix flaky snapshot diffs"                   | YES   | Core trigger.                      |
| "/playwright-visual-testing-fixtures"        | YES   | Slash command trigger.             |
| "Migrate our database"                       | NO    | Out of scope for this skill.       |
| "Test backend APIs only"                     | NO    | Out of scope for this skill.       |

## 3. Execution Workflow

### Step 1: Freeze the Environment

- **Action:** Disable animations, carets, and web-font variance via init scripts. Pin viewport matrix across mobile, tablet, and desktop.
- **Input:** Component specs and viewport targets.
- **Stop Condition:** Halt when animations stay live; require freezes.
- **Validation:** Determinism proof recorded per fixture.

### Step 2: Isolate Networks and Tolerances

- **Action:** Intercept APIs with route mocks, set pixel-ratio tolerances tight enough to catch regressions but above subpixel noise, and version baselines explicitly.
- **Input:** API inventory from Step 1.
- **Stop Condition:** Halt on live-network snapshots; require mocks.
- **Validation:** Tolerance rationale recorded per suite.

### Step 3: Review Diffs as Verdicts

- **Action:** Treat diff reports as pass-fail gates with human approval on baseline updates.
- **Input:** Diff reports from Step 2.
- **Stop Condition:** Halt on auto-accepted baselines; require review.
- **Validation:** Verdict log reviewed per run.

### Step 4: Handoff and Human Review

- **Action:** Present the fixture plan and request approval before wiring.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero suites wired by this skill.

## 4. Output Specification

```markdown
# Visual Plan

- **Fixtures:** [Frozen environments]
- **Tolerances:** [Pixel budgets]
- **Verdicts:** [Gate process]
```

## 5. Validation Gate

- [ ] Environments frozen per fixture.
- [ ] Tolerances tight with rationale.
- [ ] Baselines versioned with review.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before wiring.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Snapshotting live animated pages.
- **Over-execution threshold:** Updating baselines unprompted.
- **Calibration default:** Deterministic first; pixels second.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-18 (hidden state)   | Freezes environments per fixture.                   |
| 2    | AP-26 (no scope)       | Bounds tolerances numerically.                      |
| 3    | AP-28 (no stop)        | Gates baselines on review.                          |
| 4    | AP-45 (no human review)| Halts for approval before wiring.                   |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Quality Gatekeeper role, role source, and seniority bar.
  - `1.0.0` - Legacy visual baseline.

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

**Input:** "Our checkout modal drifts visually every release."
**Output:** Fixture plan with frozen animations, mocked networks, and gated baseline updates.
