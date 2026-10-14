---
name: htmx-principles
description: Builds hypermedia-driven interfaces with htmx swaps, out-of-band updates, and server-rendered partials. Excludes SPA state framework setup.
department: frontend
ownerAgent: legolas
triggerCommand: /htmx-principles
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-18
  - AP-26
  - AP-28
---

# htmx Principles

## 0. Identity

- **Role:** Interface Builder. Owns hypermedia composition with server-rendered swaps.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Interface Builder).
- **Seniority bar:** Staff (Appendix B). Records why server partials beat client state machines for document flows (single source of truth, rejected dual-model sync bugs), why explicit targets beat defaults (debuggability, rejected implicit swaps), and why OOB beats event buses for correlated regions.
- **Authority:** Tier-5 normative skill for `skills/frontend/htmx-principles/`. Owns swap strategy and partial guidance.
- **Must not define:** SPA framework scaffolds; backend domain logic.
- **Normative base:** `core/fellowship/legolas.md`, `rules/engineering/architecture-boundaries.md`, `references/anti-patterns.md`, and hypermedia systems practice.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-18 (stale state), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                             |
| --- | ---------------- | --------------------------------------------------------------------------------- |
| 1   | Task             | Produce hypermedia interfaces with swap targets, triggers, and partial endpoints. |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.  |
| 3   | Output Format    | Interaction plan with swap map, endpoint contracts, and fallback notes.           |
| 4   | Constraints      | Server renders HTML partials. Degrade without JavaScript. Zero em dashes.         |
| 5   | Input            | Interaction list, page structure, endpoint inventory, fallback needs.             |
| 6   | Context          | Prevents SPA rewrites where hypermedia swaps solve the interaction cheaply.       |
| 7   | Audience         | Full-stack engineers favoring server rendering.                                   |
| 8   | Success Criteria | Swap map complete; partials contracted; plan approved before coding.              |
| 9   | Examples         | See Section 10.                                                                   |

## 2. Trigger Matrix

| Trigger                                  | Fire? | Notes                          |
| ---------------------------------------- | ----- | ------------------------------ |
| "Build this interaction with htmx"       | YES   | Core trigger.                  |
| "Replace our SPA widget with hypermedia" | YES   | Core trigger.                  |
| "/htmx-principles"                       | YES   | Slash command trigger.         |
| "Scaffold a React SPA from scratch"      | NO    | Out of scope for this skill.   |
| "Design our domain business logic"       | NO    | Out of scope; backend owns it. |

## 3. Execution Workflow

### Step 1: List Interactions and Targets

- **Action:** Record every dynamic interaction with trigger events, debounce modifiers, and swap targets per element.
- **Input:** Interaction list and page structure.
- **Stop Condition:** Halt and ask when swap targets stay ambiguous.
- **Validation:** Swap map complete before endpoint work.

### Step 2: Contract Partial Endpoints

- **Action:** Define partial-returning endpoints with response shapes, status codes, out-of-band swap headers, and HX-Trigger coordination where regions correlate.
- **Input:** Swap map from Step 1.
- **Stop Condition:** Halt when an endpoint returns full pages for partial swaps; require partials.
- **Validation:** Contracts reviewed per interaction.

### Step 3: Harden Fallback and Indicators

- **Action:** Ensure forms submit without JavaScript, add loading indicators and confirm steps for destructive swaps, and bound polling with push upgrades where realtime matters.
- **Input:** Fallback needs from user.
- **Stop Condition:** Halt when destructive actions lack confirms; require them.
- **Validation:** Fallback paths verified per critical flow.

### Step 4: Handoff and Human Review

- **Action:** Present the plan and request approval before coding.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero code written by this skill.

## 4. Output Specification

```markdown
# htmx Plan

- **Swaps:** [Trigger to target map]
- **Endpoints:** [Partial contracts]
- **Fallback:** [No-JS and confirm notes]
```

## 5. Validation Gate

- [ ] Swap map complete before endpoints.
- [ ] Endpoints return partials for swaps.
- [ ] Destructive actions carry confirms.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before coding.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Wiring swaps without target mapping.
- **Over-execution threshold:** Building SPA scaffolds unprompted.
- **Calibration default:** Server-render first; sprinkle swaps only.

## 7. Anti-Pattern Compliance

| Step | Prevents AP             | Mechanism                              |
| ---- | ----------------------- | -------------------------------------- |
| 1    | AP-1 (vague task)       | Requires swap map first.               |
| 2    | AP-26 (no scope)        | Contracts partials per interaction.    |
| 3    | AP-28 (no stop)         | Demands confirms on destructive flows. |
| 4    | AP-45 (no human review) | Halts for approval before coding.      |

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

**Input:** "Convert our comment thread to htmx without a framework rewrite."
**Output:** Plan with swap targets per thread node, partial endpoints, and no-JS fallback.
