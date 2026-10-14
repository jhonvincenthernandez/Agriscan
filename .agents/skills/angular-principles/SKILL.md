---
name: angular-principles
description: Angular v20+ engineering rules covering standalone components, signals reactivity, zoneless change detection, and strict project setup. Excludes backend API design.
department: frontend
ownerAgent: legolas
triggerCommand: /angular-principles
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-26
  - AP-28
---

# Angular Principles

## 0. Identity

- **Role:** Interface Builder. Owns screen composition and interaction wiring within Angular signals discipline.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Interface Builder).
- **Seniority bar:** Staff (Appendix B). Records why standalone components beat NgModules (explicit dependencies, rejected module ceremony), why signals beat zone-based reactivity (targeted updates, rejected whole-tree checks), and why RxJS keeps time-based async while signals own state.
- **Authority:** Tier-5 normative skill for `skills/frontend/angular-principles/`. Owns component and reactivity guidance.
- **Must not define:** Backend APIs; global design tokens.
- **Normative base:** `core/fellowship/legolas.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Produce Angular features with standalone components, signals state, and strict setup.           |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.                |
| 3   | Output Format    | Feature plan with component map, reactivity notes, and setup checklist.                        |
| 4   | Constraints      | Standalone only. Signals first. Zero em dashes. Strict TypeScript on.                          |
| 5   | Input            | Screen specs, state inventory, async needs, form complexity.                                    |
| 6   | Context          | Prevents module sprawl, zone overhead, and untyped templates.                                   |
| 7   | Audience         | Frontend engineers shipping Angular v20+ apps.                                                  |
| 8   | Success Criteria | Components standalone; reactivity explicit; plan approved before coding.                         |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger                                      | Fire? | Notes                              |
| -------------------------------------------- | ----- | ---------------------------------- |
| "Build this screen in Angular"               | YES   | Core trigger.                      |
| "Migrate our app to signals"                 | YES   | Core trigger.                      |
| "/angular-principles"                        | YES   | Slash command trigger.             |
| "Design our backend API"                     | NO    | Out of scope for this skill.       |
| "Write React components instead"             | NO    | Out of scope; different paradigm.  |

## 3. Execution Workflow

### Step 1: Structure Features Standalone

- **Action:** Organize by feature domain with standalone components, route-level lazy loading, and defer blocks for template parts.
- **Input:** Screen specs from user.
- **Stop Condition:** Halt on new NgModules; require standalone.
- **Validation:** Feature map reviewed with lazy boundaries.

### Step 2: Assign Reactivity Correctly

- **Action:** Hold local state in signals with computed derivations, reserve RxJS for time-based async bridged via toSignal, and escalate only complex global state to SignalStore.
- **Input:** State inventory from Step 1.
- **Stop Condition:** Halt when effects replace derivations; require computed.
- **Validation:** Reactivity map reviewed per feature.

### Step 3: Harden Templates and Setup

- **Action:** Use modern control flow with tracked keys, signal inputs and outputs, strict templates without any, zoneless change detection, and CLI strict scaffolding with esbuild builds.
- **Input:** Template inventory and setup needs.
- **Stop Condition:** Halt on template-driven forms or untyped expressions.
- **Validation:** Template audit complete with setup checklist.

### Step 4: Handoff and Human Review

- **Action:** Present the plan and request approval before coding.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero code written by this skill.

## 4. Output Specification

```markdown
# Angular Plan

- **Components:** [Standalone map with lazy bounds]
- **Reactivity:** [Signals with RxJS bridges]
- **Setup:** [Strict CLI checklist]
```

## 5. Validation Gate

- [ ] Components standalone by default.
- [ ] Reactivity explicit per feature.
- [ ] Templates typed without any.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before coding.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Writing components without feature mapping.
- **Over-execution threshold:** Building backends unprompted.
- **Calibration default:** Signals first; RxJS for time; stores for complexity.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-1 (vague task)      | Requires feature map first.                         |
| 2    | AP-26 (no scope)       | Assigns reactivity per feature.                     |
| 3    | AP-28 (no stop)        | Enforces typed templates.                           |
| 4    | AP-45 (no human review)| Halts for approval before coding.                   |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Interface Builder role, role source, and seniority bar.
  - `1.0.0` - Legacy Angular baseline.

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

**Input:** "Build a dashboard in Angular with live charts."
**Output:** Plan with standalone feature modules, signal state with RxJS streams, and zoneless setup.
