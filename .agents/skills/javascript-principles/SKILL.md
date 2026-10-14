---
name: javascript-principles
description: Modern JavaScript rules covering ES modules, strict typing discipline, async flow, JSDoc contracts, and SOLID structure. Excludes TypeScript compiler setup.
department: frontend
ownerAgent: legolas
triggerCommand: /javascript-principles
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-26
  - AP-28
---

# JavaScript Principles

## 0. Identity

- **Role:** Syntax Reviewer. Owns language correctness and structural discipline for JavaScript codebases.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Syntax Reviewer).
- **Seniority bar:** Staff (Appendix B). Records why const-first beats var habits (immutability by default, rejected hoisting surprises), why async-await beats promise chains (readable flows, rejected nesting), and why pure small functions beat flag-driven giants.
- **Authority:** Tier-5 normative skill for `skills/frontend/javascript-principles/`. Owns language and structure guidance.
- **Must not define:** TypeScript compiler configuration specifics.
- **Normative base:** `core/fellowship/legolas.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Produce modern, pure, typed-via-contracts JavaScript with safe async flows.                    |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.                |
| 3   | Output Format    | Code plan with module, async, contract, and structure notes.                                   |
| 4   | Constraints      | ES modules only. No var. Zero em dashes. Async with cancellation.                              |
| 5   | Input            | Feature spec, async needs, boundary contracts.                                                  |
| 6   | Context          | Prevents mutation bugs, unhandled rejections, and untyped boundary drift.                       |
| 7   | Audience         | Frontend engineers writing JavaScript logic.                                                    |
| 8   | Success Criteria | Modules pure; async safe; contracts checked; plan approved.                                     |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger                                      | Fire? | Notes                              |
| -------------------------------------------- | ----- | ---------------------------------- |
| "Clean up our JavaScript architecture"       | YES   | Core trigger.                      |
| "Fix unhandled rejections and mutations"     | YES   | Core trigger.                      |
| "/javascript-principles"                     | YES   | Slash command trigger.             |
| "Configure our TypeScript compiler"          | NO    | Route to `typescript-standards`.   |
| "Design our module graph policy"             | NO    | Route to `module-organization`.    |

## 3. Execution Workflow

### Step 1: Structure Modules by Feature

- **Action:** Group by domain with pure functions, event-driven decoupling, and zero barrel files. Freeze shared constants and clone structurally instead of JSON hacks.
- **Input:** Feature spec from user.
- **Stop Condition:** Halt on global mutation or barrel additions.
- **Validation:** Module map reviewed with purity notes.

### Step 2: Modernize Syntax and Async

- **Action:** Enforce const-first declarations with modern array methods, async-await with try-catch cause chains, allSettled parallelism, and AbortSignal cancellation.
- **Input:** Codebase inventory from Step 1.
- **Stop Condition:** Halt on var usage or then-chains in new code.
- **Validation:** Syntax audit complete per module.

### Step 3: Contract Boundaries and Functions

- **Action:** Check JSDoc coverage on public APIs, validate runtime boundaries with schemas, keep functions small with few args and no flags, and honor command-query separation with guard clauses.
- **Input:** Boundary contracts from user.
- **Stop Condition:** Halt when public APIs lack contracts.
- **Validation:** Contract review complete per boundary.

### Step 4: Handoff and Human Review

- **Action:** Present the plan and request approval before coding.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero code written by this skill.

## 4. Output Specification

```markdown
# JavaScript Plan

- **Modules:** [Feature map with purity notes]
- **Async:** [Flow safety notes]
- **Contracts:** [Boundary checks per API]
```

## 5. Validation Gate

- [ ] Modules feature-grouped without barrels.
- [ ] Async safe with cancellation.
- [ ] Contracts cover public APIs.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before coding.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Writing logic without module mapping.
- **Over-execution threshold:** Rewriting working systems unprompted.
- **Calibration default:** Small pure functions over clever ones.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-1 (vague task)      | Requires module map first.                          |
| 2    | AP-26 (no scope)       | Modernizes syntax per module.                       |
| 3    | AP-28 (no stop)        | Contracts every public API.                         |
| 4    | AP-45 (no human review)| Halts for approval before coding.                   |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Syntax Reviewer role, role source, and seniority bar.
  - `1.0.0` - Legacy language baseline.

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

**Input:** "Our JS has mutation bugs and unhandled rejections."
**Output:** Plan with feature modules, async-await migration, and JSDoc boundary contracts.
