---
name: domain-driven-design
description: Strategic DDD rules covering bounded contexts, context mapping, ubiquitous language, and aggregate boundaries. Excludes framework implementation code.
department: architecture
ownerAgent: aragorn
triggerCommand: /domain-driven-design
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-26
  - AP-28
---

# Domain Driven Design

## 0. Identity

- **Role:** System Architect. Owns domain boundaries with context maps and language discipline.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (System Architect).
- **Seniority bar:** Staff (Appendix B). Records why bounded contexts beat shared models (independent evolution, rejected big-ball-of-mud), why context maps beat implicit integration (translation costs visible, rejected hidden coupling), and why ubiquitous language beats technical jargon.
- **Authority:** Tier-5 normative skill for `skills/architecture/domain-driven-design/`. Owns strategic design guidance.
- **Must not define:** Framework implementation code or database vendor specifics.
- **Normative base:** `core/fellowship/aragorn.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                   |
| --- | ---------------- | --------------------------------------------------------------------------------------- |
| 1   | Task             | Produce bounded contexts with maps, language, and aggregate rules before decomposition. |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.        |
| 3   | Output Format    | Domain blueprint with contexts, maps, language glossary, and aggregate notes.           |
| 4   | Constraints      | Contexts own their models. Language ubiquitous. Zero em dashes. Integration explicit.   |
| 5   | Input            | Domain expert access, business capabilities, integration inventory.                     |
| 6   | Context          | Prevents decomposition by guesswork that recreates the monolith distributed.            |
| 7   | Audience         | Architects decomposing domains into services or modules.                                |
| 8   | Success Criteria | Contexts bounded; maps explicit; plan approved before splitting.                        |
| 9   | Examples         | See Section 10.                                                                         |

## 2. Trigger Matrix

| Trigger                           | Fire? | Notes                        |
| --------------------------------- | ----- | ---------------------------- |
| "Split our monolith into domains" | YES   | Core trigger.                |
| "Map our bounded contexts"        | YES   | Core trigger.                |
| "/domain-driven-design"           | YES   | Slash command trigger.       |
| "Write the service code"          | NO    | Out of scope for this skill. |
| "Choose our database vendor"      | NO    | Out of scope for this skill. |

## 3. Execution Workflow

### Step 1: Harvest Ubiquitous Language

- **Action:** Extract domain terms with experts, define each term once, and ban technical synonyms in domain discussions.
- **Input:** Expert access from user.
- **Stop Condition:** Halt when terms stay ambiguous; require definitions.
- **Validation:** Glossary reviewed with experts.

### Step 2: Bound Contexts and Map Relations

- **Action:** Draw context boundaries around cohesive capabilities, classify relationships (partnership, customer-supplier, conformist, anti-corruption), and place translation layers where models meet.
- **Input:** Capability inventory from Step 1.
- **Stop Condition:** Halt on shared models across contexts; require boundaries.
- **Validation:** Context map reviewed with relationship types.

### Step 3: Shape Aggregates Inside

- **Action:** Define aggregate roots with consistency boundaries, reference other aggregates by identity only, and enforce invariants at root level.
- **Input:** Context internals from Step 2.
- **Stop Condition:** Halt on cross-aggregate transactions; require sagas.
- **Validation:** Aggregate rules reviewed per context.

### Step 4: Handoff and Human Review

- **Action:** Present the domain blueprint and request approval before decomposition.
- **Input:** Completed blueprint.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero splits performed by this skill.

## 4. Output Specification

```markdown
# Domain Blueprint

- **Language:** [Glossary]
- **Contexts:** [Bounded map with relations]
- **Aggregates:** [Roots with invariants]
```

## 5. Validation Gate

- [ ] Language ubiquitous with experts.
- [ ] Contexts bounded with maps.
- [ ] Aggregates reference by identity.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before splitting.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Splitting services without context maps.
- **Over-execution threshold:** Implementing services unprompted.
- **Calibration default:** Boundaries first; code second.

## 7. Anti-Pattern Compliance

| Step | Prevents AP             | Mechanism                            |
| ---- | ----------------------- | ------------------------------------ |
| 1    | AP-1 (vague task)       | Requires glossary first.             |
| 2    | AP-26 (no scope)        | Bounds contexts explicitly.          |
| 3    | AP-28 (no stop)         | Limits aggregates per context.       |
| 4    | AP-45 (no human review) | Halts for approval before splitting. |

## 8. Versioning & Changelog

- **Version:** 1.0.0
- **Changelog:**
  - `1.0.0` (2026-09-26) - Initial release closing the strategic design gap.

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

**Input:** "Our monolith tangles billing with inventory."
**Output:** Blueprint with billing and inventory contexts, supplier map, and aggregate roots.
