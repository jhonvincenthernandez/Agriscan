---
name: qwik-principles
description: Builds Qwik apps with resumability, lazy loaders, and optimizer-friendly component splits. Excludes server framework selection.
department: frontend
ownerAgent: legolas
triggerCommand: /qwik-principles
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-18
  - AP-26
  - AP-28
---

# Qwik Principles

## 0. Identity

- **Role:** Interface Builder. Owns resumable composition with optimizer-safe splits.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Interface Builder).
- **Seniority bar:** Staff (Appendix B). Records why resumability beats hydration (no replay cost, rejected re-execution), why dollar boundaries beat implicit splits (optimizer certainty, rejected serialization surprises), and why loaders own data over effects.
- **Authority:** Tier-5 normative skill for `skills/frontend/qwik-principles/`. Owns component split and loader guidance.
- **Must not define:** Server framework choice; backend APIs.
- **Normative base:** `core/fellowship/legolas.md`, `rules/engineering/architecture-boundaries.md`, `references/anti-patterns.md`, and Qwik resumability practice.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-18 (stale state), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Produce Qwik routes with resumable components, scoped loaders, and minimal JavaScript.         |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.                |
| 3   | Output Format    | Route plan with loader map, component splits, and JS budget notes.                             |
| 4   | Constraints      | Dollar-sign boundaries respected. Loaders scoped per route. Zero em dashes.                    |
| 5   | Input            | Page specs, data needs, interactivity map, performance budget.                                  |
| 6   | Context          | Prevents hydration-heavy ports that erase Qwik speed gains.                                     |
| 7   | Audience         | Frontend engineers shipping instant-load apps.                                                  |
| 8   | Success Criteria | Splits optimizer-clean; loaders scoped; plan approved before coding.                            |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger                                     | Fire? | Notes                              |
| ------------------------------------------- | ----- | ---------------------------------- |
| "Build this page in Qwik"                   | YES   | Core trigger.                      |
| "Cut our Qwik JavaScript bundle"            | YES   | Core trigger.                      |
| "/qwik-principles"                          | YES   | Slash command trigger.             |
| "Choose our backend framework"              | NO    | Out of scope for this skill.       |
| "Port React hydration patterns as-is"       | NO    | Refused; breaks resumability.      |

## 3. Execution Workflow

### Step 1: Map Routes and Interactivity

- **Action:** List routes with islands of interactivity and static shells per page. Match Qwik strengths to content-plus-interaction pages, not dashboards.
- **Input:** Page specs and interactivity map.
- **Stop Condition:** Halt and ask when interactive islands stay unmarked.
- **Validation:** Island map complete before splits.

### Step 2: Scope Loaders per Route

- **Action:** Assign route loaders for data with cache headers and action handlers for mutations. Keep server work in loaders, client work in tasks with correct timing.
- **Input:** Data needs per route.
- **Stop Condition:** Halt when a loader reaches across routes; require scoping.
- **Validation:** Loader map covers every route need.

### Step 3: Split Components for the Optimizer

- **Action:** Place component boundaries at lazy edges with serializable closures, budget JavaScript per route, and verify splits against optimizer rules.
- **Input:** Island map and budget from Step 1.
- **Stop Condition:** Halt on non-serializable closures crossing boundaries; require refactor.
- **Validation:** Splits reviewed against optimizer rules.

### Step 4: Handoff and Human Review

- **Action:** Present the plan and request approval before coding.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero code written by this skill.

## 4. Output Specification

```markdown
# Qwik Plan

- **Islands:** [Interactive map per route]
- **Loaders:** [Scoped data with cache notes]
- **Splits:** [Optimizer boundaries with JS budget]
```

## 5. Validation Gate

- [ ] Islands marked before splits.
- [ ] Loaders scoped per route.
- [ ] Closures serializable across boundaries.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before coding.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Writing components without island mapping.
- **Over-execution threshold:** Porting hydration patterns that defeat resumability.
- **Calibration default:** Static shell first; hydrate islands only.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-1 (vague task)      | Requires island map first.                          |
| 2    | AP-26 (no scope)       | Scopes loaders per route.                           |
| 3    | AP-18 (stale state)    | Enforces serializable boundaries.                   |
| 4    | AP-45 (no human review)| Halts for approval before coding.                   |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Interface Builder role, role source, and seniority bar.
  - `1.0.0` (2026-09-26) - Initial release covering niche frontend.

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

**Input:** "Rebuild our marketing site in Qwik for instant loads."
**Output:** Plan with static shells, island splits, scoped loaders, and per-route JS budget.
