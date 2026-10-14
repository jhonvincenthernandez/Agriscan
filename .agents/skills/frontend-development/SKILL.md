---
name: frontend-development
description: Framework-agnostic frontend engineering standards for component architecture, state colocation, Core Web Vitals performance, Error Boundaries, responsive layouts, and WCAG accessibility.
department: frontend
ownerAgent: legolas
triggerCommand: /frontend-development
antiPatternsPrevented:
  - AP-1
  - AP-4
  - AP-12
  - AP-18
  - AP-26
  - AP-28
---

# Frontend Development Principles

## 0. Identity

- **Role:** Interface Builder. Owns screen composition and interaction wiring with resilience guarantees.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Interface Builder).
- **Seniority bar:** Staff (Appendix B). Records why four-state boundaries beat happy-path rendering (async reality has four outcomes, rejected loading-only optimism), why colocated state beats global stores (ownership follows use, rejected prop-drilling pyramids), and why explicit media dimensions beat layout-shift apologies.
- **Authority:** Tier-5 normative skill for frontend applications under `skills/frontend/frontend-development/`.
- **Must not define:** Backend database migrations or server persistence logic.
- **Normative base:** `core/fellowship/legolas.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1 (unbounded client state), AP-12 (forgotten lifecycle management), and AP-26 (leaking backend driver errors into client UI).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                                       |
| --- | ---------------- | ----------------------------------------------------------------------------------------------------------- |
| 1   | Task             | Architect, implement, and review production-grade client-side user interfaces and state hierarchies.        |
| 2   | Target Tool      | React 19, Next.js App Router, Vue 3, Svelte 5, Tailwind CSS, TanStack Virtual, Web Vitals.                  |
| 3   | Output Format    | Modular component architectures, typed custom hooks, and responsive accessible layout templates.            |
| 4   | Constraints      | Mandatory four-state UI handling (Loading, Success, Empty, Error). Zero unhandled Error Boundaries.         |
| 5   | Input            | User experience designs, wireframes, REST/GraphQL API contracts, accessibility requirements.                |
| 6   | Context          | Prevents layout thrashing, component cascade re-renders, unresponsive interactions, and accessibility gaps. |
| 7   | Audience         | Frontend developers, UI/UX engineers, full-stack developers, design systems leads.                          |
| 8   | Success Criteria | 100 percent WCAG 2.2 Level AA compliance; zero Cumulative Layout Shift; sub-100ms INP response times.       |
| 9   | Examples         | See Section 10.                                                                                              |

## 2. Trigger Matrix

| Trigger Condition                                              | Fire? | Action / Route                                                   |
| -------------------------------------------------------------- | ----- | ---------------------------------------------------------------- |
| Designing new client-side UI components or state management    | YES   | Enforce state colocation and four-state boundary resilience.     |
| Optimizing Core Web Vitals (LCP, CLS, INP)                     | YES   | Apply explicit media dimensions and non-blocking event handlers. |
| Authoring React-specific hooks and Server Component boundaries | NO    | Route to `skills/frontend/react-principles/`.                    |
| Writing backend route controllers or database queries          | NO    | Route to `skills/backend/backend-development/`.                  |

## 3. Execution Workflow

### Step 1: Break Components Semantically

- **Action:** Decompose designs into atomic presentation components plus container orchestration with clear props interfaces and no type escapes. Ban div click handlers in favor of native semantics.
- **Input:** Designs and wireframes from user.
- **Stop Condition:** Halt if presentation components attempt database or low-level network operations.
- **Validation:** Props interfaces defined without type escapes.

### Step 2: Colocate State and Bind URLs

- **Action:** Place local UI state at point of use, shareable filters and pagination in URL query strings, and server state in caches or Server Components. Reserve global stores for truly shared domain state.
- **Input:** State inventory from Step 1.
- **Stop Condition:** Halt when shareable state hides in component memory; require URL binding.
- **Validation:** Reloading preserves filter and view state.

### Step 3: Harden Vitals and Accessibility

- **Action:** Fix media dimensions with aspect ratios, preload hero assets, keep handlers lean with transitions or workers, enforce 24px targets with visible focus rings, and wrap async subtrees in Error Boundaries with skeleton, empty, and error states.
- **Input:** Performance budgets and a11y requirements.
- **Stop Condition:** Halt when async regions lack any of the four states.
- **Validation:** Four-state coverage verified per async boundary.

### Step 4: Handoff and Human Review

- **Action:** Present the interface plan and request approval before implementation.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero code written by this skill.

## 4. Output Specification

```markdown
# Interface Plan

- **Components:** [Atomic breakdown with props]
- **State:** [Colocation map with URL bindings]
- **Resilience:** [Four-state coverage per boundary]
- **Vitals:** [CLS, LCP, INP notes]
```

## 5. Validation Gate

- [ ] All asynchronous components implement Loading, Success, Empty, and Error states.
- [ ] Media elements declare explicit dimensions or CSS aspect ratios to prevent CLS.
- [ ] Interactive elements feature visible `:focus-visible` focus rings.
- [ ] Shareable filter and pagination parameters are bound to URL query state.
- [ ] Human approval recorded before implementation.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Rendering async data without four-state coverage.
- **Over-execution threshold:** Building backend persistence unprompted.
- **Calibration default:** Colocate first; globalize with receipts.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-1 (vague task)      | Requires component breakdown first.                 |
| 2    | AP-26 (no scope)       | Binds shareable state to URLs.                      |
| 3    | AP-12 (lifecycle gaps) | Covers all four async states.                       |
| 4    | AP-45 (no human review)| Halts for approval before implementation.           |

## 8. Versioning & Changelog

- **Version:** 3.0.0
- **Changelog:**
  - `3.0.0` (2026-09-26) - Full Tier-5 template conformance with Interface Builder role, role source, and seniority bar.
  - `2.0.0` (2026-09-20) - Elevated to Sauron Tier-5 specification with four-state resilience and Core Web Vitals patterns.

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

**Input:** "Build a resilient item list with loading and error states."
**Output:** Four-state container component with skeleton loaders, retry affordance, empty message, and keyed list rendering.
