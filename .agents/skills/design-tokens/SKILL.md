---
name: design-tokens
description: 3-tier token architecture, semantic token naming, OKLCH color ramps, spacing steps, elevation, typography, motion easing and duration assignments, icon sizing tiers, and the component state matrix.
department: quality
ownerAgent: legolas
triggerCommand: /design-tokens
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-26
  - AP-28
---

# Design Tokens

## 0. Identity

- **Role:** Interface Builder. Owns token vocabulary with tier discipline and state coverage.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Interface Builder).
- **Seniority bar:** Staff (Appendix B). Records why three tiers beat flat variables (internals never leak to components, rejected global soup), why semantic names beat literal colors (one change propagates, rejected hex hunts), and why six documented states beat hopeful defaults.
- **Authority:** Tier-5 normative skill for token systems under `skills/quality/design-tokens/`.
- **Must not define:** Behavioral interaction rules beyond state matrix; brand identity decisions.
- **Normative base:** `core/fellowship/legolas.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Produce token systems with tiered architecture, perceptual ramps, and full state matrices.     |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.                |
| 3   | Output Format    | Token plan with tiers, ramps, motion, icons, and state notes.                                  |
| 4   | Constraints      | Three tiers enforced. Semantic names only. Zero em dashes. Six states per component.           |
| 5   | Input            | Theme needs, brand palette, motion targets, icon inventory.                                     |
| 6   | Context          | Prevents token sprawl, contrast failures, and undocumented component states.                    |
| 7   | Audience         | Design engineers building token systems.                                                        |
| 8   | Success Criteria | Tiers respected; ramps perceptual; plan approved before coding.                                 |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger                                      | Fire? | Notes                              |
| -------------------------------------------- | ----- | ---------------------------------- |
| "Tokenize our design system"                 | YES   | Core trigger.                      |
| "Fix contrast and motion gaps"               | YES   | Core trigger.                      |
| "/design-tokens"                             | YES   | Slash command trigger.             |
| "Decide our brand identity"                  | NO    | Out of scope; design owns it.      |
| "Write interaction logic"                    | NO    | Out of scope for this skill.       |

## 3. Execution Workflow

### Step 1: Tier the Vocabulary

- **Action:** Separate primitives from semantic roles from component scopes. Derive ramps perceptually with hyphenated namespaces per role.
- **Input:** Theme needs from user.
- **Stop Condition:** Halt when components consume primitives directly.
- **Validation:** Tier audit complete with namespace review.

### Step 2: Scale Space, Type, and Motion

- **Action:** Fix 4px spacing steps with radius and z-index hierarchies, map type steps with line-height bands, and assign easing plus durations with reduced-motion guards.
- **Input:** Brand palette and motion targets.
- **Stop Condition:** Halt on arbitrary values without token mapping.
- **Validation:** Scale review complete per category.

### Step 3: Cover Icons and States

- **Action:** Standardize one icon set with size tiers and currentColor rendering, then document all six states per interactive component with contrast evidence.
- **Input:** Icon inventory from Step 2.
- **Stop Condition:** Halt on mixed sets or undocumented states.
- **Validation:** Icon and state audit complete.

### Step 4: Handoff and Human Review

- **Action:** Present the token plan and request approval before coding.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero code written by this skill.

## 4. Output Specification

```markdown
# Token Plan

- **Tiers:** [Vocabulary map]
- **Scales:** [Space, type, motion notes]
- **States:** [Six-state coverage]
```

## 5. Validation Gate

- [ ] Tiers respected per token.
- [ ] Scales standardized per category.
- [ ] States documented per component.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before coding.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Theming without tier discipline.
- **Over-execution threshold:** Rebranding products unprompted.
- **Calibration default:** Semantic tokens first; overrides with receipts.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-1 (vague task)      | Requires tier map first.                            |
| 2    | AP-26 (no scope)       | Standardizes scales per category.                   |
| 3    | AP-28 (no stop)        | Documents states per component.                     |
| 4    | AP-45 (no human review)| Halts for approval before coding.                   |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Interface Builder role, role source, and seniority bar.
  - `1.0.0` - Legacy tokens baseline.

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

**Input:** "Our themes drift and focus states are missing."
**Output:** Token plan with tiered vocabulary, perceptual ramps, and six-state coverage.
