---
name: html-css-principles
description: Semantic HTML and modern CSS architecture rules covering native elements, cascade layers, container queries, and interaction primitives. Excludes JavaScript frameworks.
department: frontend
ownerAgent: legolas
triggerCommand: /html-css-principles
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-26
  - AP-28
---

# HTML CSS Principles

## 0. Identity

- **Role:** Interface Builder. Owns markup semantics and style architecture for robust interfaces.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Interface Builder).
- **Seniority bar:** Staff (Appendix B). Records why native elements beat div-soup (free accessibility and AI parseability, rejected custom re-implementations), why cascade layers beat important flags (ordered priority, rejected specificity wars), and why container queries beat viewport queries for components.
- **Authority:** Tier-5 normative skill for `skills/frontend/html-css-principles/`. Owns markup and style guidance.
- **Must not define:** JavaScript framework internals.
- **Normative base:** `core/fellowship/legolas.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Produce semantic markup with layered, responsive, interactive styles.                           |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.                |
| 3   | Output Format    | Markup plan with semantics, layers, layout, and interaction notes.                             |
| 4   | Constraints      | Native elements first. No important flags. Zero em dashes. Focus visible always.                |
| 5   | Input            | Page structure, responsive needs, interaction list.                                             |
| 6   | Context          | Prevents div-soup, specificity wars, and layout shift regressions.                              |
| 7   | Audience         | Frontend engineers writing markup and styles.                                                   |
| 8   | Success Criteria | Semantics valid; layers ordered; plan approved before coding.                                   |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger                                      | Fire? | Notes                              |
| -------------------------------------------- | ----- | ---------------------------------- |
| "Fix our div-soup markup"                    | YES   | Core trigger.                      |
| "Stabilize our CSS specificity"              | YES   | Core trigger.                      |
| "/html-css-principles"                       | YES   | Slash command trigger.             |
| "Build a React component system"             | NO    | Route to `react-principles`.       |
| "Write JavaScript business logic"            | NO    | Out of scope for this skill.       |

## 3. Execution Workflow

### Step 1: Semantify Markup

- **Action:** Replace structural divs with sectioning elements, enforce heading order, use native dialog and details elements, wire labels to inputs, and reserve media space against layout shifts.
- **Input:** Page structure from user.
- **Stop Condition:** Halt when interactive divs lack native replacements with reasons.
- **Validation:** Markup audit complete per page region.

### Step 2: Layer and Scope Styles

- **Action:** Order cascade layers explicitly, ban important flags, scope components with modules or utilities, and keep globals to tokens plus resets.
- **Input:** Stylesheet inventory from Step 1.
- **Stop Condition:** Halt on important flags; require layer ordering.
- **Validation:** Layer map reviewed with scope notes.

### Step 3: Lay Out Responsively with Native Interaction

- **Action:** Prefer container queries for components, fluid functions for type and space, logical properties for direction support, Grid plus subgrid for pages, and native has, popover, and guarded animations for interaction.
- **Input:** Responsive needs and interaction list.
- **Stop Condition:** Halt when focus outlines vanish without replacements.
- **Validation:** Layout review complete per breakpoint.

### Step 4: Handoff and Human Review

- **Action:** Present the plan and request approval before coding.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero code written by this skill.

## 4. Output Specification

```markdown
# Markup Plan

- **Semantics:** [Native element map]
- **Layers:** [Cascade order with scopes]
- **Layout:** [Responsive with interaction notes]
```

## 5. Validation Gate

- [ ] Semantics native per region.
- [ ] Layers ordered without important.
- [ ] Focus visible with contrast.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before coding.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Styling div-soup without semantic repair.
- **Over-execution threshold:** Building JS frameworks unprompted.
- **Calibration default:** Native first; libraries last.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-1 (vague task)      | Requires markup audit first.                        |
| 2    | AP-26 (no scope)       | Orders layers explicitly.                           |
| 3    | AP-28 (no stop)        | Guards animations with support checks.              |
| 4    | AP-45 (no human review)| Halts for approval before coding.                   |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Interface Builder role, role source, and seniority bar.
  - `1.0.0` - Legacy markup baseline.

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

**Input:** "Our pages shift on load and screen readers struggle."
**Output:** Plan with semantic repairs, reserved media space, layered styles, and focus-visible audit.
