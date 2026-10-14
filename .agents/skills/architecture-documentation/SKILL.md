---
name: architecture-documentation
description: Architecture documentation rules covering C4 diagrams, diagrams-as-code, decision logs linkage, and freshness automation. Excludes product marketing content.
department: architecture
ownerAgent: aragorn
triggerCommand: /architecture-documentation
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-18
  - AP-26
  - AP-28
---

# Architecture Documentation

## 0. Identity

- **Role:** System Architect. Owns living architecture records with diagram currency and decision linkage.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (System Architect).
- **Seniority bar:** Staff (Appendix B). Records why diagrams-as-code beats exported images (diffs review like code, rejected binary blobs), why C4 levels beat flat diagrams (audience-matched zoom, rejected one-diagram-fits-all), and why freshness checks beat annual rewrites.
- **Authority:** Tier-5 normative skill for `skills/architecture/architecture-documentation/`. Owns documentation standard guidance.
- **Must not define:** Product marketing content or user manuals.
- **Normative base:** `core/fellowship/aragorn.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-18 (stale diagrams), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                              |
| --- | ---------------- | ---------------------------------------------------------------------------------- |
| 1   | Task             | Produce versioned architecture records with C4 diagrams linked to decision logs.   |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.   |
| 3   | Output Format    | Documentation plan with diagram set, freshness rules, and linkage map.             |
| 4   | Constraints      | Diagrams as code. Levels matched to audience. Zero em dashes. Freshness automated. |
| 5   | Input            | System inventory, audience list, decision log location.                            |
| 6   | Context          | Prevents stale wiki diagrams that mislead every new hire.                          |
| 7   | Audience         | Architects maintaining living system records.                                      |
| 8   | Success Criteria | Diagrams versioned; levels complete; plan approved.                                |
| 9   | Examples         | See Section 10.                                                                    |

## 2. Trigger Matrix

| Trigger                            | Fire? | Notes                        |
| ---------------------------------- | ----- | ---------------------------- |
| "Document our system architecture" | YES   | Core trigger.                |
| "Fix our stale wiki diagrams"      | YES   | Core trigger.                |
| "/architecture-documentation"      | YES   | Slash command trigger.       |
| "Write product marketing pages"    | NO    | Out of scope for this skill. |
| "Author user manuals"              | NO    | Out of scope for this skill. |

## 3. Execution Workflow

### Step 1: Map Audiences to C4 Levels

- **Action:** Assign context, container, component, and code views to executive, team, and engineer audiences. One level per audience need.
- **Input:** Audience list from user.
- **Stop Condition:** Halt when a level serves no named audience.
- **Validation:** Level map reviewed per audience.

### Step 2: Diagram as Code

- **Action:** Author diagrams in text formats under version control with CI-rendered outputs. Ban binary-only diagram files.
- **Input:** System inventory from Step 1.
- **Stop Condition:** Halt on image-only diagrams; require sources.
- **Validation:** Sources reviewed with render pipeline.

### Step 3: Link Decisions and Freshness

- **Action:** Cross-link diagrams to decision records, schedule freshness reviews per volatility, and automate staleness flags on drift.
- **Input:** Decision log location from user.
- **Stop Condition:** Halt when diagrams float without decision links.
- **Validation:** Linkage map reviewed with review cadence.

### Step 4: Handoff and Human Review

- **Action:** Present the documentation plan and request approval before rollout.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero publishing performed by this skill.

## 4. Output Specification

```markdown
# Documentation Plan

- **Diagrams:** [C4 set with sources]
- **Links:** [Decision cross-references]
- **Freshness:** [Review cadence with automation]
```

## 5. Validation Gate

- [ ] Levels matched per audience.
- [ ] Diagrams versioned as code.
- [ ] Decisions cross-linked.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before rollout.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Publishing diagrams without sources.
- **Over-execution threshold:** Rewriting wikis unprompted.
- **Calibration default:** Four levels max; freshness automated.

## 7. Anti-Pattern Compliance

| Step | Prevents AP             | Mechanism                          |
| ---- | ----------------------- | ---------------------------------- |
| 1    | AP-1 (vague task)       | Requires audience map first.       |
| 2    | AP-26 (no scope)        | Versions diagrams as code.         |
| 3    | AP-18 (stale records)   | Automates freshness checks.        |
| 4    | AP-45 (no human review) | Halts for approval before rollout. |

## 8. Versioning & Changelog

- **Version:** 1.0.0
- **Changelog:**
  - `1.0.0` (2026-09-26) - Initial release closing the living-docs gap.

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

**Input:** "New hires learn from diagrams two rewrites old."
**Output:** Plan with C4 levels as code, decision links, and automated freshness flags.
