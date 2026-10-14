---
name: ui-ux-principles
description: Reusable, deterministic UI/UX and UX writing constraints covering accessibility law, visual structure, cognitive load, interactions, theming, and content strategy.
department: frontend
ownerAgent: legolas
triggerCommand: /ui-ux-principles
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-26
  - AP-28
---

# UI UX Principles

## 0. Identity

- **Role:** Interface Builder. Owns interface composition with accessibility law and writing discipline.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Interface Builder).
- **Seniority bar:** Staff (Appendix B). Records why native semantics beat div click handlers (keyboard and readers free, rejected custom control re-implementations), why one term per concept beats synonyms (comprehension compounds, rejected mixed vocabulary), and why destructive confirmations beat undo-toasts for irreversible acts.
- **Authority:** Tier-5 normative skill for `skills/frontend/ui-ux-principles/`. Owns interface and content guidance.
- **Must not define:** Backend APIs; brand identity decisions.
- **Normative base:** `core/fellowship/legolas.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Produce interfaces with legal accessibility, coherent visuals, and honest content.              |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.                |
| 3   | Output Format    | Interface plan with a11y, visual, interaction, and content notes.                              |
| 4   | Constraints      | WCAG AA minimum. One term per concept. Zero em dashes. Verbs lead CTAs.                        |
| 5   | Input            | Screen specs, user flows, brand tokens, content drafts.                                         |
| 6   | Context          | Prevents unlawful interfaces, incoherent visuals, and blame-shifting errors.                    |
| 7   | Audience         | Frontend engineers and designers shipping interfaces.                                           |
| 8   | Success Criteria | A11y lawful; visuals coherent; plan approved before coding.                                     |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger                                      | Fire? | Notes                              |
| -------------------------------------------- | ----- | ---------------------------------- |
| "Audit our interface accessibility"          | YES   | Core trigger.                      |
| "Fix our error messages and CTAs"            | YES   | Core trigger.                      |
| "/ui-ux-principles"                          | YES   | Slash command trigger.             |
| "Design our brand identity"                  | NO    | Out of scope; design owns it.      |
| "Write backend validation logic"             | NO    | Out of scope for this skill.       |

## 3. Execution Workflow

### Step 1: Lock Accessibility Law

- **Action:** Enforce native semantics, keyboard operability with focus traps and escapes, contrast ratios, touch targets, screen-reader labels, and motion plus high-contrast support.
- **Input:** Screen specs from user.
- **Stop Condition:** Halt on div click handlers or missing focus management.
- **Validation:** A11y audit complete per screen.

### Step 2: Structure Visuals Coherently

- **Action:** Apply baseline grid, type hierarchy, shadow tiers, contrast-checked palette, and left-aligned body text with theme variables for both modes.
- **Input:** Brand tokens from user.
- **Stop Condition:** Halt on arbitrary spacing or hardcoded hex in components.
- **Validation:** Visual review complete per screen.

### Step 3: Write Honest Content

- **Action:** Confirm destructive acts modally, validate inline, lead CTAs with verbs, never blank screens, explain errors with fixes, and freeze one term per concept.
- **Input:** Content drafts and user flows.
- **Stop Condition:** Halt on blame-shifting errors or synonym sprawl.
- **Validation:** Content review complete per flow.

### Step 4: Handoff and Human Review

- **Action:** Present the plan and request approval before coding.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero code written by this skill.

## 4. Output Specification

```markdown
# Interface Plan

- **A11y:** [Lawful checklist per screen]
- **Visuals:** [Coherent system notes]
- **Content:** [Honest writing audit]
```

## 5. Validation Gate

- [ ] A11y lawful per screen.
- [ ] Visuals coherent per system.
- [ ] Content honest per flow.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before coding.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Shipping interfaces without a11y audit.
- **Over-execution threshold:** Rebranding products unprompted.
- **Calibration default:** Native semantics first; custom controls with receipts.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-1 (vague task)      | Requires a11y audit first.                          |
| 2    | AP-26 (no scope)       | Freezes visual system per screen.                   |
| 3    | AP-28 (no stop)        | Locks terminology per concept.                      |
| 4    | AP-45 (no human review)| Halts for approval before coding.                   |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Interface Builder role, role source, and seniority bar.
  - `1.0.0` - Legacy interface baseline.

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

**Input:** "Our signup flow confuses users and fails contrast checks."
**Output:** Plan with lawful a11y repairs, coherent visual system, and verb-led CTAs with helpful errors.
