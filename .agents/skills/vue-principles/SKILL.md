---
name: vue-principles
description: Builds Vue 3 interfaces with Composition API, Pinia stores, and router discipline. Excludes backend API design.
department: frontend
ownerAgent: legolas
triggerCommand: /vue-principles
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-18
  - AP-26
  - AP-28
---

# Vue Principles

## 0. Identity

- **Role:** Interface Builder. Owns screen composition and interaction wiring within Vue conventions.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Interface Builder).
- **Seniority bar:** Staff (Appendix B). Records why Composition API beats Options sprawl (feature-grouped logic stays readable, rejected scattered option blocks), why Pinia actions beat direct mutation (traceable state changes, rejected store anarchy), and why Nuxt 4 stays the greenfield default until Vapor proves stable.
- **Authority:** Tier-5 normative skill for `skills/frontend/vue-principles/`. Owns component and store guidance.
- **Must not define:** Backend APIs; global design tokens (see design suite).
- **Normative base:** `core/fellowship/legolas.md`, `rules/engineering/architecture-boundaries.md`, `references/anti-patterns.md`, and Vue 3.5 plus Nuxt 4 practice.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-18 (stale state), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Produce Vue 3 features with composables, Pinia stores, and guarded routes.                     |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.                |
| 3   | Output Format    | Feature plan with composables, store map, and route guards.                                    |
| 4   | Constraints      | Composition API only. Stores own shared state. Zero em dashes. Props down, events up.          |
| 5   | Input            | Screen specs, shared state list, route map, API contracts.                                      |
| 6   | Context          | Prevents Options API sprawl and unowned shared state across views.                              |
| 7   | Audience         | Frontend engineers shipping Vue 3 apps.                                                         |
| 8   | Success Criteria | Composables reusable; stores bounded; plan approved before coding.                              |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger                                     | Fire? | Notes                              |
| ------------------------------------------- | ----- | ---------------------------------- |
| "Build this screen in Vue 3"                | YES   | Core trigger.                      |
| "Refactor our Vuex store to Pinia"          | YES   | Core trigger.                      |
| "/vue-principles"                           | YES   | Slash command trigger.             |
| "Design our backend API"                    | NO    | Out of scope for this skill.       |
| "Audit our Tailwind tokens"                 | NO    | Route to design suite.             |

## 3. Execution Workflow

### Step 1: Map Screens and Shared State

- **Action:** List screens with local versus shared state, route guard needs, and API contracts. Group related logic into feature composables instead of scattering across option blocks.
- **Input:** Screen specs and route map.
- **Stop Condition:** Halt and ask when shared state ownership stays unclear.
- **Validation:** State map complete with composable boundaries.

### Step 2: Extract Composables and Stores

- **Action:** Place reusable logic in typed composables and shared state in Pinia stores mutated exclusively through actions. Prefer VueUse catalog utilities over hand-rolled equivalents.
- **Input:** State map from Step 1.
- **Stop Condition:** Halt when components mutate store state directly; require actions.
- **Validation:** Store map reviewed with action boundaries.

### Step 3: Guard Routes and Async States

- **Action:** Add navigation guards for auth roles with fallbacks, serialize SSR state through fetch composables to avoid hydration double-fetching, and cover loading plus error branches per async view.
- **Input:** Auth scheme and API contracts.
- **Stop Condition:** Halt when a guarded route lacks fallback; require one.
- **Validation:** Guards and branches verified per route.

### Step 4: Handoff and Human Review

- **Action:** Present the plan and request approval before coding.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero code written by this skill.

## 4. Output Specification

```markdown
# Vue Plan

- **Composables:** [Reusable logic units]
- **Stores:** [Bounded Pinia map]
- **Routes:** [Guards with async branches]
```

## 5. Validation Gate

- [ ] State map complete before components.
- [ ] Mutations flow through store actions.
- [ ] Routes guarded with fallbacks.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before coding.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Writing views without state mapping.
- **Over-execution threshold:** Building backends unprompted.
- **Calibration default:** Composables for logic, stores for sharing, nothing else.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-1 (vague task)      | Requires state map first.                           |
| 2    | AP-26 (no scope)       | Bounds stores with actions.                         |
| 3    | AP-18 (stale state)    | Covers async branches per view.                     |
| 4    | AP-45 (no human review)| Halts for approval before coding.                   |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Interface Builder role, role source, and seniority bar.
  - `1.0.0` (2026-09-26) - Initial release covering Vue framework gap.

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

**Input:** "Build an admin panel in Vue 3 with role-based routes."
**Output:** Plan with auth composable, Pinia session store, and guarded routes with fallbacks.
