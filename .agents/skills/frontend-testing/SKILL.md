---
name: frontend-testing
description: Frontend test strategy rules covering trophy-shaped investment, Vitest integration tests, Playwright journeys, visual regression, and CI sharding. Excludes backend API testing.
department: frontend
ownerAgent: merry
triggerCommand: /frontend-testing
antiPatternsPrevented:
  - AP-1
  - AP-3
  - AP-6
  - AP-26
  - AP-28
---

# Frontend Testing

## 0. Identity

- **Role:** Test Strategist. Owns coverage plans matched to risk areas across the frontend trophy.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Test Strategist).
- **Seniority bar:** Staff (Appendix B). Records why integration-heavy trophies beat unit-heavy pyramids on UI (behavior stability over refactor fragility, rejected prop-rename breakage), why Playwright covers journeys over features (maintenance cost compounds per test, rejected E2E-everything), and why visual tests run perpendicular to functional tiers.
- **Authority:** Tier-5 normative skill for `skills/frontend/frontend-testing/`. Owns test strategy guidance.
- **Must not define:** Backend API test suites; production monitoring.
- **Normative base:** `core/fellowship/merry.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-3 (no success criteria), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                  |
| --- | ---------------- | -------------------------------------------------------------------------------------- |
| 1   | Task             | Produce a trophy-shaped test plan with tooling, ratios, and CI wiring per tier.        |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.       |
| 3   | Output Format    | Test plan with tier ratios, tool choices, and CI sharding notes.                       |
| 4   | Constraints      | Integration widest. E2E journeys only. Zero em dashes. Static analysis counts as base. |
| 5   | Input            | Critical journeys, component inventory, CI budget, flake history.                      |
| 6   | Context          | Prevents inverted pyramids that burn maintenance without confidence.                   |
| 7   | Audience         | Frontend engineers owning UI quality.                                                  |
| 8   | Success Criteria | Tiers sized by ROI; journeys covered; plan approved before wiring.                     |
| 9   | Examples         | See Section 10.                                                                        |

## 2. Trigger Matrix

| Trigger                             | Fire? | Notes                                |
| ----------------------------------- | ----- | ------------------------------------ |
| "Design our frontend test strategy" | YES   | Core trigger.                        |
| "Fix flaky E2E suites"              | YES   | Core trigger.                        |
| "/frontend-testing"                 | YES   | Slash command trigger.               |
| "Test our backend APIs"             | NO    | Out of scope for this skill.         |
| "Monitor production uptime"         | NO    | Out of scope; observability owns it. |

## 3. Execution Workflow

### Step 1: Size Tiers by ROI

- **Action:** Allocate roughly 60 percent integration (RTL with MSW), 25 percent unit (Vitest pure logic), 10 percent E2E (Playwright journeys), 5 percent visual, over a static-analysis base of types plus lint.
- **Input:** Critical journeys and component inventory.
- **Stop Condition:** Halt when tiers invert toward E2E-heavy; require rebalancing.
- **Validation:** Ratio table recorded with tool per tier.

### Step 2: Wire Realistic Rendering

- **Action:** Drive components with userEvent in Testing Library, mock networks at MSW boundary, reuse Storybook play functions across Vitest and Playwright, and reserve real-browser component tests for visual-critical surfaces.
- **Input:** Component inventory from Step 1.
- **Stop Condition:** Halt on implementation-detail assertions; require user-visible assertions.
- **Validation:** Interaction coverage reviewed per critical flow.

### Step 3: Gate Journeys and Visuals in CI

- **Action:** Cover 10 to 20 journeys with Page Object Models, snapshot critical pages across browsers, shard runners with cached browsers, and quarantine flakes with owner deadlines instead of deletions.
- **Input:** CI budget and flake history.
- **Stop Condition:** Halt when flakes lack owners; require assignment.
- **Validation:** CI plan reviewed with shard and quarantine notes.

### Step 4: Handoff and Human Review

- **Action:** Present the test plan and request approval before wiring.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero suites wired by this skill.

## 4. Output Specification

```markdown
# Test Plan

- **Tiers:** [Ratios with tools]
- **Journeys:** [Covered flows with models]
- **CI:** [Sharding with flake policy]
```

## 5. Validation Gate

- [ ] Tiers sized by ROI evidence.
- [ ] Interactions asserted user-visibly.
- [ ] Flakes owned with deadlines.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before wiring.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Writing E2E for everything without tiers.
- **Over-execution threshold:** Wiring CI suites unprompted.
- **Calibration default:** Integration widest; journeys few; visuals perpendicular.

## 7. Anti-Pattern Compliance

| Step | Prevents AP             | Mechanism                         |
| ---- | ----------------------- | --------------------------------- |
| 1    | AP-3 (no success)       | Sizes tiers with ratios.          |
| 2    | AP-26 (no scope)        | Asserts user-visible behavior.    |
| 3    | AP-28 (no stop)         | Quarantines flakes with owners.   |
| 4    | AP-45 (no human review) | Halts for approval before wiring. |

## 8. Versioning & Changelog

- **Version:** 1.0.0
- **Changelog:**
  - `1.0.0` (2026-09-26) - Initial release closing the UI testing gap.

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

**Input:** "Our E2E suite flakes daily and unit tests break on renames."
**Output:** Plan with integration-trophy ratios, MSW boundaries, journey-scoped Playwright, and flake quarantine policy.
