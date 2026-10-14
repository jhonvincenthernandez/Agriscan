---
name: bootstrap-principles
description: Bootstrap 5.3 engineering rules covering grid system, utility classes, Sass customization, dark mode, accessibility (WCAG 2.2 AA), Core Web Vitals performance, and responsive design patterns for modern web development.
department: frontend
ownerAgent: legolas
triggerCommand: /bootstrap-principles
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-26
  - AP-28
---

# Bootstrap Principles

## 0. Identity

- **Role:** Interface Builder. Owns Bootstrap-driven composition with token discipline and performance budgets.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Interface Builder).
- **Seniority bar:** Staff (Appendix B). Records why Sass variables beat important overrides (theme-level control, rejected specificity wars), why selective imports beat full bundles (40 to 60 percent CSS savings, rejected CDN-everything), and why data-attribute components beat hand-rolled JavaScript.
- **Authority:** Tier-5 normative skill for `skills/frontend/bootstrap-principles/`. Owns grid, utility, and theme guidance.
- **Must not define:** Application-specific design tokens or framework core instructions.
- **Normative base:** `core/fellowship/legolas.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Produce Bootstrap 5.3 interfaces with correct grids, tokens, dark mode, and budgets.           |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.                |
| 3   | Output Format    | Styling plan with grid, tokens, dark mode, and performance notes.                              |
| 4   | Constraints      | Mobile-first grids. Sass before import. Zero em dashes. Selective JS imports.                  |
| 5   | Input            | Layout specs, theme needs, dark mode targets, performance budget.                               |
| 6   | Context          | Prevents container nesting bugs, important sprawl, and bundle bloat.                            |
| 7   | Audience         | Frontend engineers styling with Bootstrap 5.3.                                                  |
| 8   | Success Criteria | Grids valid; tokens centralized; plan approved before coding.                                   |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger                                      | Fire? | Notes                              |
| -------------------------------------------- | ----- | ---------------------------------- |
| "Fix our Bootstrap grid nesting"             | YES   | Core trigger.                      |
| "Add dark mode the Bootstrap way"            | YES   | Core trigger.                      |
| "/bootstrap-principles"                      | YES   | Slash command trigger.             |
| "Design our brand palette"                   | NO    | Out of scope; design owns it.      |
| "Write JavaScript business logic"            | NO    | Out of scope for this skill.       |

## 3. Execution Workflow

### Step 1: Grid Mobile-First Correctly

- **Action:** Enforce container to row to column hierarchy without nested containers, progress columns mobile-first, and space with gap utilities instead of margin hacks.
- **Input:** Layout specs from user.
- **Stop Condition:** Halt on nested containers; require flattening.
- **Validation:** Grid audit complete per template.

### Step 2: Centralize Tokens via Sass

- **Action:** Override Sass variables before import, expose runtime tokens as custom properties with RGB variants, extend utilities through the utility API, and name tokens semantically.
- **Input:** Theme needs from Step 1.
- **Stop Condition:** Halt on important overrides; require variable fixes.
- **Validation:** Token map reviewed with dark-mode coverage.

### Step 3: Darken, Perform, and Respond

- **Action:** Drive dark mode through theme attributes with aware utilities, purge unused CSS with selective JS imports, optimize fonts and images, defer non-critical scripts, and verify responsive tables plus navigation on real devices.
- **Input:** Dark mode targets and performance budget.
- **Stop Condition:** Halt when budgets breach; require cuts.
- **Validation:** Budget evidence recorded per surface.

### Step 4: Handoff and Human Review

- **Action:** Present the plan and request approval before coding.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero code written by this skill.

## 4. Output Specification

```markdown
# Bootstrap Plan

- **Grid:** [Hierarchy audit]
- **Tokens:** [Sass map with dark coverage]
- **Performance:** [Budget evidence]
```

## 5. Validation Gate

- [ ] Grids valid without nesting.
- [ ] Tokens centralized via Sass.
- [ ] Budgets met per surface.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before coding.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Styling without grid audit.
- **Over-execution threshold:** Redesigning brand palettes unprompted.
- **Calibration default:** Variables first; overrides never.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-1 (vague task)      | Requires grid audit first.                          |
| 2    | AP-26 (no scope)       | Centralizes tokens per theme.                       |
| 3    | AP-28 (no stop)        | Enforces budgets per surface.                       |
| 4    | AP-45 (no human review)| Halts for approval before coding.                   |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Interface Builder role, role source, and seniority bar.
  - `1.0.0` - Legacy styling baseline.

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

**Input:** "Our Bootstrap pages nest containers and ship full bundles."
**Output:** Plan with flattened grids, Sass token map, and selective imports under budget.
