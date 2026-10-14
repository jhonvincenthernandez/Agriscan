---
name: astro-principles
description: Builds Astro content sites with islands, content collections, and zero-JavaScript defaults. Excludes application backend design.
department: frontend
ownerAgent: legolas
triggerCommand: /astro-principles
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-18
  - AP-26
  - AP-28
---

# Astro Principles

## 0. Identity

- **Role:** Interface Builder. Owns static-first page composition with surgical island placement.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Interface Builder).
- **Seniority bar:** Staff (Appendix B). Records why zero-JS defaults beat framework shells on content sites (payload discipline compounds per page, rejected SPA-for-blogs), why directive choice decides performance (hydration timing is the budget, rejected load-everywhere), and why single runtimes beat multi-framework novelty.
- **Authority:** Tier-5 normative skill for `skills/frontend/astro-principles/`. Owns island and collection guidance.
- **Must not define:** Application backends; CMS administration.
- **Normative base:** `core/fellowship/legolas.md`, `rules/engineering/architecture-boundaries.md`, `references/anti-patterns.md`, and Astro 5 practice.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-18 (stale state), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Produce Astro sites with typed collections, islands, and performance budgets.                   |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.                |
| 3   | Output Format    | Site plan with collections, islands, and budget notes.                                         |
| 4   | Constraints      | Zero JavaScript by default. Islands hydrated per directive. Zero em dashes.                    |
| 5   | Input            | Content model, page types, interactive widgets, performance budget.                             |
| 6   | Context          | Prevents framework-heavy builds for content sites that need speed.                              |
| 7   | Audience         | Frontend engineers shipping docs, blogs, and marketing sites.                                   |
| 8   | Success Criteria | Collections typed; islands justified; plan approved before coding.                              |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger                                          | Fire? | Notes                              |
| ------------------------------------------------ | ----- | ---------------------------------- |
| "Build our docs site in Astro"                   | YES   | Core trigger.                      |
| "Cut JavaScript on our marketing pages"          | YES   | Core trigger.                      |
| "/astro-principles"                              | YES   | Slash command trigger.             |
| "Build a realtime dashboard app"                 | NO    | Wrong tool; needs app framework.   |
| "Administer our headless CMS"                    | NO    | Out of scope for this skill.       |

## 3. Execution Workflow

### Step 1: Model Content Collections

- **Action:** Define collections with schemas, slugs, and draft rules per content type. Add server islands for dynamic regions without full-page dynamism.
- **Input:** Content model and page types.
- **Stop Condition:** Halt and ask when a content type lacks schema.
- **Validation:** Collections typed with validation before layout work.

### Step 2: Place Islands Sparingly

- **Action:** Mark interactive widgets as islands with hydration directives matched to urgency (load, visible, idle, media, only). Justify each island and each added framework runtime.
- **Input:** Interactive widget list and budget.
- **Stop Condition:** Halt when an island lacks justification; require static alternative first.
- **Validation:** Island list reviewed with directives.

### Step 3: Enforce Performance Budget

- **Action:** Set JavaScript, image, and font budgets per template with measurement hooks. Share cross-island state through framework-agnostic stores, never component internals.
- **Input:** Performance budget from user.
- **Stop Condition:** Halt when a template exceeds budget; require cuts.
- **Validation:** Budgets recorded with measurement method.

### Step 4: Handoff and Human Review

- **Action:** Present the plan and request approval before coding.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero code written by this skill.

## 4. Output Specification

```markdown
# Astro Plan

- **Collections:** [Typed schemas per type]
- **Islands:** [Widgets with directives]
- **Budget:** [JS and asset caps per template]
```

## 5. Validation Gate

- [ ] Collections typed before layouts.
- [ ] Every island carries justification.
- [ ] Budgets recorded with measurement.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before coding.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Adding islands without budget review.
- **Over-execution threshold:** Building app backends unprompted.
- **Calibration default:** Static first; island only with proof of need.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-1 (vague task)      | Requires typed collections first.                   |
| 2    | AP-26 (no scope)       | Justifies every island.                             |
| 3    | AP-42 (no target)      | Caps budgets with measurement.                      |
| 4    | AP-45 (no human review)| Halts for approval before coding.                   |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Interface Builder role, role source, and seniority bar.
  - `1.0.0` (2026-09-26) - Initial release covering Astro framework gap.

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

**Input:** "Rebuild our blog in Astro with interactive demos."
**Output:** Plan with typed post collection, two justified islands, and JS budget per template.
