---
name: solidjs-principles
description: Builds SolidJS interfaces with fine-grained reactivity, stores, and router discipline. Excludes backend API design.
department: frontend
ownerAgent: legolas
triggerCommand: /solidjs-principles
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-18
  - AP-26
  - AP-28
---

# SolidJS Principles

## 0. Identity

- **Role:** Interface Builder. Owns fine-grained reactive composition without virtual-DOM overhead.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Interface Builder).
- **Seniority bar:** Staff (Appendix B). Records why signals beat VDOM diffing on update cost (only dependents recompute, rejected whole-tree renders), why memos beat effect derivations (no self-writing loops, rejected effect-computed values), and why resources beat manual fetch-then-set.
- **Authority:** Tier-5 normative skill for `skills/frontend/solidjs-principles/`. Owns component and state guidance.
- **Must not define:** Backend APIs; global design tokens (see design suite).
- **Normative base:** `core/fellowship/legolas.md`, `rules/engineering/architecture-boundaries.md`, `references/anti-patterns.md`, and SolidJS signals practice.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-18 (stale state), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Produce SolidJS components with signal discipline, derived memos, and clean effects.           |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.                |
| 3   | Output Format    | Component plan with state map, effect list, and route guards.                                  |
| 4   | Constraints      | Signals for state, memos for derivations, effects for sync only. Zero em dashes.               |
| 5   | Input            | Screen specs, data sources, route map, interaction list.                                        |
| 6   | Context          | Prevents effect storms and prop-drilled stores in fine-grained apps.                            |
| 7   | Audience         | Frontend engineers shipping SolidJS apps.                                                       |
| 8   | Success Criteria | State map complete; effects justified; plan approved before coding.                             |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger                                     | Fire? | Notes                              |
| ------------------------------------------- | ----- | ---------------------------------- |
| "Build this screen in SolidJS"              | YES   | Core trigger.                      |
| "Fix our SolidJS effect loops"              | YES   | Core trigger.                      |
| "/solidjs-principles"                       | YES   | Slash command trigger.             |
| "Design our backend API"                    | NO    | Out of scope for this skill.       |
| "Audit our Tailwind tokens"                 | NO    | Route to design suite.             |

## 3. Execution Workflow

### Step 1: Map State and Routes

- **Action:** List signals, stores, and route guards per screen with ownership. Keep state roots minimal and derive everything possible.
- **Input:** Screen specs and route map.
- **Stop Condition:** Halt and ask when data ownership stays unclear.
- **Validation:** State map complete before component work.

### Step 2: Derive with Memos

- **Action:** Express computed values as memos and isolate side effects to narrow effects with cleanup. Never derive inside effects that write what they read.
- **Input:** State map from Step 1.
- **Stop Condition:** Halt when an effect writes signals it also reads; require refactor.
- **Validation:** Effects listed with triggers and cleanup notes.

### Step 3: Compose Components and Resources

- **Action:** Build components around resources for async data with error and loading branches per route. Pair with Astro islands where shells stay static.
- **Input:** Data sources and interaction list.
- **Stop Condition:** Halt when async states lack error branches; require them.
- **Validation:** Every async path covers loading and error.

### Step 4: Handoff and Human Review

- **Action:** Present the plan and request approval before coding.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero code written by this skill.

## 4. Output Specification

```markdown
# SolidJS Plan

- **State:** [Signals and stores with owners]
- **Effects:** [Triggers with cleanup notes]
- **Routes:** [Guards with async branches]
```

## 5. Validation Gate

- [ ] State map complete before components.
- [ ] Derivations use memos, not effects.
- [ ] Async paths cover loading and error.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before coding.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Writing components without a state map.
- **Over-execution threshold:** Building backends unprompted.
- **Calibration default:** Fewer, narrower effects beat clever ones.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-1 (vague task)      | Requires state map first.                           |
| 2    | AP-18 (stale state)    | Forces memo derivations.                            |
| 3    | AP-26 (no scope)       | Bounds async branches per route.                    |
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

**Input:** "Build a realtime dashboard in SolidJS without render churn."
**Output:** Plan with store-backed signals, memo derivations, and resource branches per widget.
