---
name: svelte-principles
description: Builds SvelteKit apps with runes, load functions, and form actions done idiomatically. Excludes backend service design.
department: frontend
ownerAgent: legolas
triggerCommand: /svelte-principles
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-18
  - AP-26
  - AP-28
---

# Svelte Principles

## 0. Identity

- **Role:** Interface Builder. Owns screen composition and interaction wiring within Svelte runes discipline.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Interface Builder).
- **Seniority bar:** Staff (Appendix B). Records why explicit runes beat legacy magic (debuggability at scale, rejected implicit reactivity), why loaders own data over mount fetching (single source per route, rejected double-fetch effects), and why actions carry mutations (progressive enhancement free, rejected ad-hoc fetch calls).
- **Authority:** Tier-5 normative skill for `skills/frontend/svelte-principles/`. Owns runes and SvelteKit guidance.
- **Must not define:** Backend services; global design tokens.
- **Normative base:** `core/fellowship/legolas.md`, `rules/engineering/architecture-boundaries.md`, `references/anti-patterns.md`, and Svelte 5 plus SvelteKit practice.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-18 (stale state), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Produce SvelteKit routes with runes state, loaders, and progressive-enhancement forms.         |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.                |
| 3   | Output Format    | Route plan with runes map, loaders, and action contracts.                                      |
| 4   | Constraints      | Runes for reactivity. Loaders own data. Zero em dashes. Forms work without JavaScript.         |
| 5   | Input            | Page specs, data needs, mutation list, auth scheme.                                             |
| 6   | Context          | Prevents store-everything habits that fight Svelte compiler strengths.                          |
| 7   | Audience         | Frontend engineers shipping SvelteKit apps.                                                     |
| 8   | Success Criteria | Runes scoped; loaders cover routes; plan approved before coding.                                |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger                                     | Fire? | Notes                              |
| ------------------------------------------- | ----- | ---------------------------------- |
| "Build this page in SvelteKit"              | YES   | Core trigger.                      |
| "Migrate our Svelte 4 stores to runes"      | YES   | Core trigger.                      |
| "/svelte-principles"                        | YES   | Slash command trigger.             |
| "Design our backend services"               | NO    | Out of scope for this skill.       |
| "Scaffold a React app instead"              | NO    | Out of scope; different paradigm.  |

## 3. Execution Workflow

### Step 1: Map Routes and Data Needs

- **Action:** List routes with loader data, params validation, and error layouts per branch. Assign server-only logic to server modules.
- **Input:** Page specs and data needs.
- **Stop Condition:** Halt and ask when a route data need stays unowned.
- **Validation:** Route map complete before state work.

### Step 2: Scope Runes per Component

- **Action:** Place state, derived, and effect runes at the narrowest component owning the behavior. Derive with `$derived`, synchronize externals with `$effect`, and keep server state out of client runes.
- **Input:** Interaction list per route.
- **Stop Condition:** Halt when runes leak to global scope needlessly; require scoping.
- **Validation:** Runes map reviewed with ownership.

### Step 3: Wire Forms and Actions

- **Action:** Build form actions with validation, progressive enhancement, and optimistic notes where safe. Add remote functions for typed server calls instead of hand endpoints.
- **Input:** Mutation list from user.
- **Stop Condition:** Halt when a destructive action lacks confirm; require one.
- **Validation:** Actions cover validate, fail, and redirect paths.

### Step 4: Handoff and Human Review

- **Action:** Present the plan and request approval before coding.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero code written by this skill.

## 4. Output Specification

```markdown
# Svelte Plan

- **Routes:** [Loaders with error layouts]
- **Runes:** [Scoped reactivity map]
- **Actions:** [Form contracts with paths]
```

## 5. Validation Gate

- [ ] Routes mapped before state work.
- [ ] Runes scoped narrowly with owners.
- [ ] Forms work without JavaScript.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before coding.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Writing components without route mapping.
- **Over-execution threshold:** Building backend services unprompted.
- **Calibration default:** Compiler-friendly simplicity over clever abstractions.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-1 (vague task)      | Requires route map first.                           |
| 2    | AP-26 (no scope)       | Scopes runes narrowly.                              |
| 3    | AP-18 (stale state)    | Covers action failure paths.                        |
| 4    | AP-45 (no human review)| Halts for approval before coding.                   |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Interface Builder role, role source, and seniority bar.
  - `1.0.0` (2026-09-26) - Initial release covering Svelte framework gap.

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

**Input:** "Build a settings area in SvelteKit with validated forms."
**Output:** Plan with scoped runes, route loaders, and progressive-enhancement actions.
