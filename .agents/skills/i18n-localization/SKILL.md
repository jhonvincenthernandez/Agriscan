---
name: i18n-localization
description: Internationalization rules covering locale routing, ICU messages, RTL layouts, locale-aware formatting, and SEO per locale. Excludes translation vendor management.
department: frontend
ownerAgent: legolas
triggerCommand: /i18n-localization
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-26
  - AP-28
---

# i18n Localization

## 0. Identity

- **Role:** Interface Builder. Owns locale-correct composition from routing to formatting.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Interface Builder).
- **Seniority bar:** Staff (Appendix B). Records why day-one i18n beats retrofits (10x cheaper than rewiring strings, rejected hardcoded-first speed), why ICU beats concatenation (plurals vary per language, rejected template literals), and why logical properties beat directional CSS (automatic RTL flips, rejected margin-left sprawl).
- **Authority:** Tier-5 normative skill for `skills/frontend/i18n-localization/`. Owns locale routing and message guidance.
- **Must not define:** Translation vendor contracts or machine translation quality review.
- **Normative base:** `core/fellowship/legolas.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                |
| --- | ---------------- | ------------------------------------------------------------------------------------ |
| 1   | Task             | Produce locale-aware apps with routed locales, typed messages, and RTL-safe layouts. |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.     |
| 3   | Output Format    | Locale plan with routing, messages, formatting, and SEO notes.                       |
| 4   | Constraints      | No hardcoded strings. ICU for plurals. Zero em dashes. Logical properties only.      |
| 5   | Input            | Locale list, RTL needs, SEO targets, content inventory.                              |
| 6   | Context          | Prevents untranslatable strings, broken RTL, and invisible regional pages.           |
| 7   | Audience         | Frontend engineers shipping multi-region products.                                   |
| 8   | Success Criteria | Strings keyed; RTL verified; plan approved before coding.                            |
| 9   | Examples         | See Section 10.                                                                      |

## 2. Trigger Matrix

| Trigger                              | Fire? | Notes                          |
| ------------------------------------ | ----- | ------------------------------ |
| "Add Arabic and Japanese to our app" | YES   | Core trigger.                  |
| "Fix broken RTL layouts"             | YES   | Core trigger.                  |
| "/i18n-localization"                 | YES   | Slash command trigger.         |
| "Hire our translators"               | NO    | Out of scope; vendor decision. |
| "Write backend locale APIs"          | NO    | Out of scope for this skill.   |

## 3. Execution Workflow

### Step 1: Route Locales Explicitly

- **Action:** Prefix locale segments in routing, detect preferences with cookie override, and split message namespaces per page for lean bundles.
- **Input:** Locale list from user.
- **Stop Condition:** Halt when default-locale strategy stays undecided.
- **Validation:** Routing map reviewed per locale.

### Step 2: Key Messages with ICU

- **Action:** Extract every string into namespaced keys at build time, express plurals and selects in ICU syntax, and fail builds on missing keys.
- **Input:** Content inventory from Step 1.
- **Stop Condition:** Halt on hardcoded JSX strings; require extraction.
- **Validation:** Key audit clean with ICU review.

### Step 3: Flip Layouts and Formats

- **Action:** Set document direction per locale, replace directional CSS with logical properties, format dates and currencies via Intl APIs, and generate hreflang alternates plus sitemaps per locale.
- **Input:** RTL needs and SEO targets.
- **Stop Condition:** Halt when layouts assume left-to-right; require logical rewrite.
- **Validation:** RTL and SEO review complete per locale.

### Step 4: Handoff and Human Review

- **Action:** Present the plan and request approval before coding.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero code written by this skill.

## 4. Output Specification

```markdown
# Locale Plan

- **Routing:** [Locale map with detection]
- **Messages:** [Keyed ICU inventory]
- **Layout:** [RTL with SEO notes]
```

## 5. Validation Gate

- [ ] Locales routed explicitly.
- [ ] Strings keyed with ICU plurals.
- [ ] RTL verified per layout.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before coding.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Shipping strings without keys.
- **Over-execution threshold:** Contracting translators unprompted.
- **Calibration default:** Day-one i18n; retrofit never.

## 7. Anti-Pattern Compliance

| Step | Prevents AP             | Mechanism                         |
| ---- | ----------------------- | --------------------------------- |
| 1    | AP-1 (vague task)       | Requires locale map first.        |
| 2    | AP-26 (no scope)        | Keys every string.                |
| 3    | AP-28 (no stop)         | Verifies RTL per layout.          |
| 4    | AP-45 (no human review) | Halts for approval before coding. |

## 8. Versioning & Changelog

- **Version:** 1.0.0
- **Changelog:**
  - `1.0.0` (2026-09-26) - Initial release closing the localization gap.

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

**Input:** "Expand our app to Arabic with proper RTL."
**Output:** Plan with locale routing, ICU key inventory, logical-property layouts, and hreflang SEO.
