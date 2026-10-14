---
name: testing-principles
description: Testing pyramid architecture, unit test isolation, integration test transaction rollbacks, Playwright Page Object Models, flakiness elimination, and CI test runner gates.
department: quality
ownerAgent: merry
triggerCommand: /testing-principles
antiPatternsPrevented:
  - AP-1
  - AP-3
  - AP-6
  - AP-9
  - AP-16
  - AP-18
  - AP-28
---

# Testing Principles

## 0. Identity

- **Role:** Test Strategist. Owns coverage plans matched to risk areas across the testing pyramid.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Test Strategist).
- **Seniority bar:** Staff (Appendix B). Records why 70/20/10 allocation beats E2E-heavy suites (fast feedback compounds daily, rejected slow brittle pyramids), why isolation beats shared fixtures (order independence, rejected state bleeding), and why auto-retry beats fixed sleeps.
- **Authority:** Tier-5 normative skill for automated testing across repositories under `skills/quality/testing-principles/`.
- **Must not define:** Application UI styles or backend persistence schemas.
- **Normative base:** `core/fellowship/merry.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`, `context/core-domains/testing-strategy.md`.
- **Anti-pattern gate:** Blocks AP-1 (unbounded test suites), AP-9 (declaring success without verification), and AP-16 (leaking shared state between test runs).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                                |
| --- | ---------------- | ---------------------------------------------------------------------------------------------------- |
| 1   | Task             | Architect, structure, and enforce test suites across Unit, Integration, and End-to-End layers.       |
| 2   | Target Tool      | Vitest, Jest, Playwright, Testcontainers, Supertest, React Testing Library.                          |
| 3   | Output Format    | Deterministic test specs, fixture factories, and CI test execution configurations.                   |
| 4   | Constraints      | 70/20/10 Testing Pyramid. Zero arbitrary timeouts (use auto-retry locators). Zero state bleeding.    |
| 5   | Input            | Feature requirements, API contracts, domain entities, user workflows.                                |
| 6   | Context          | Prevents flaky builds, untestable monolithic code, regression escapes, and slow CI feedback loops.   |
| 7   | Audience         | Software development engineers in test (SDET), developers, QA leads, release managers.               |
| 8   | Success Criteria | 80 percent plus critical path coverage; sub-10ms unit test execution; zero flaky test retries in CI. |
| 9   | Examples         | See Section 10.                                                                                       |

## 2. Trigger Matrix

| Trigger Condition                                            | Fire? | Action / Route                                                       |
| ------------------------------------------------------------ | ----- | -------------------------------------------------------------------- |
| Writing or structuring unit, integration, or E2E test suites | YES   | Apply Testing Pyramid allocation and Arrange-Act-Assert structure.   |
| Test suite exhibits flakiness or non-deterministic failures  | YES   | Quarantine test, replace arbitrary waits with auto-retry assertions. |
| Authoring specific test files or mock fixtures               | NO    | Route to `skills/quality/write-a-test/`.                             |
| Running formal evaluation harnesses on AI agent transcripts  | NO    | Route to `skills/quality/evaluation-harness-framework/`.             |

## 3. Execution Workflow

### Step 1: Allocate the Pyramid

- **Action:** Assign 70 percent unit (pure, isolated, sub-10ms), 20 percent integration (DB rollbacks, service seams), 10 percent E2E (critical journeys in browsers).
- **Input:** Feature requirements from user.
- **Stop Condition:** Halt when suites invert toward E2E-heavy; require rebalancing.
- **Validation:** Allocation recorded with layer owners.

### Step 2: Isolate Every Test

- **Action:** Enforce AAA structure with one concept per test, factory-built fixtures, and zero shared state between runs.
- **Input:** Test inventory from Step 1.
- **Stop Condition:** Halt on order-dependent tests; require isolation.
- **Validation:** Isolation audit complete per suite.

### Step 3: Kill Flakiness at the Source

- **Action:** Replace fixed waits with auto-retry locators and event responses. Mock unowned externals only; never mock domain logic under test.
- **Input:** Flake reports from CI.
- **Stop Condition:** Halt when sleeps persist; require predicates.
- **Validation:** Zero arbitrary timeouts evidenced by search.

### Step 4: Handoff and Human Review

- **Action:** Present the test architecture and request approval before wiring CI gates.
- **Input:** Completed architecture.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero gates wired by this skill.

## 4. Output Specification

```markdown
# Test Architecture

- **Pyramid:** [Allocation with owners]
- **Isolation:** [Factory and state rules]
- **Gates:** [CI enforcement notes]
```

## 5. Validation Gate

- [ ] Pyramid allocated 70/20/10.
- [ ] Tests isolated with factories.
- [ ] Zero arbitrary timeouts.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before gates.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Writing suites without allocation plan.
- **Over-execution threshold:** Wiring CI gates unprompted.
- **Calibration default:** Fast units first; journeys last.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-3 (no success)      | Allocates pyramid numerically.                      |
| 2    | AP-16 (state leaks)    | Isolates with factories.                            |
| 3    | AP-18 (hidden flakes)  | Replaces sleeps with predicates.                    |
| 4    | AP-45 (no human review)| Halts for approval before gates.                    |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Test Strategist role, role source, and seniority bar.
  - `1.0.0` - Legacy testing baseline.

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

**Input:** "Our suite is slow, flaky, and E2E-heavy."
**Output:** Rebalanced 70/20/10 architecture with isolated tests and predicate-based waits.
