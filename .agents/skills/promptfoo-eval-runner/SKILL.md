---
name: promptfoo-eval-runner
description: Evaluates RAG retrieval and generation separately with factuality, grounding, recall, and relevance metrics to block regressions. Excludes pipeline redesign.
department: ai-engineering
ownerAgent: merry
triggerCommand: /promptfoo-eval-runner
antiPatternsPrevented:
  - AP-1
  - AP-3
  - AP-6
  - AP-26
  - AP-28
---

# Promptfoo Eval Runner

## 0. Identity

- **Role:** Quality Gatekeeper. Owns pass and fail verdicts on RAG stages with threshold evidence.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Quality Gatekeeper).
- **Seniority bar:** Staff (Appendix B). Records why stage-separated metrics beat blended scores (blended hides the broken stage, rejected single-number quality), and why proven-to-fail gates beat untested gates.
- **Authority:** Tier-5 normative skill for `skills/ai-engineering/promptfoo-eval-runner/`. Owns eval configs and pass thresholds.
- **Must not define:** Pipeline redesign (see `rag-pipeline-builder`); production traffic routing.
- **Normative base:** `core/fellowship/merry.md`, `rules/engineering/architecture-boundaries.md`, `references/anti-patterns.md`, and batch research on RAG evaluation practice.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-3 (no success criteria), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Build eval configs that grade retrieval and generation separately and block regressions.       |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.                |
| 3   | Output Format    | Eval config with test cases, assertions, thresholds, and pass report.                          |
| 4   | Constraints      | Retrieval eval runs before generation eval. Thresholds explicit per metric. Zero em dashes.    |
| 5   | Input            | Query set with ground truth, retrieval script, generation path, quality thresholds.            |
| 6   | Context          | Prevents silent RAG regressions where answers drift while nobody measures grounding.           |
| 7   | Audience         | QA engineers and AI engineers owning RAG quality.                                               |
| 8   | Success Criteria | Config runs green; metrics reported per stage; gate blocks merges on failure.                   |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger                                     | Fire? | Notes                            |
| ------------------------------------------- | ----- | -------------------------------- |
| "Evaluate our RAG retrieval and answers"    | YES   | Core trigger.                    |
| "Add a quality gate that blocks bad RAG"    | YES   | Core trigger.                    |
| "/promptfoo-eval-runner"                    | YES   | Slash command trigger.           |
| "Redesign our chunking and retrieval"       | NO    | Route to `chunking-evaluator`.   |
| "Tune hybrid fusion weights"                | NO    | Route to `reranker-optimizer`.   |

## 3. Execution Workflow

### Step 1: Build Retrieval Eval

- **Action:** Create test cases that run live retrieval per query with context recall and context relevance assertions against ground-truth documents.
- **Input:** Query set with expected documents.
- **Stop Condition:** Halt and ask when ground truth documents are missing.
- **Validation:** Retrieval config runs and reports per-query scores.

### Step 2: Build Generation Eval

- **Action:** Create test cases that grade answers with factuality and answer relevance assertions against fixed contexts. Match assertion type to claim type: substring checks for exact facts, judge models for nuance, code assertions for shape.
- **Input:** Query plus context pairs with expected answers.
- **Stop Condition:** Halt when expected answers lack verifiable facts.
- **Validation:** Generation config runs and reports per-query scores.

### Step 3: Wire End-to-End Gate

- **Action:** Combine retrieval and generation providers into one config that compares pipeline variants and fails the build on threshold breach. Prove the gate by injecting a regression and watching it trip.
- **Input:** Both configs from Steps 1 and 2.
- **Stop Condition:** Halt when thresholds stay undefined; require explicit numbers.
- **Validation:** Gate fails on injected regression and passes on clean run.

### Step 4: Handoff and Human Review

- **Action:** Present the eval report with per-stage scores and request approval to enforce the gate in CI.
- **Input:** Passing eval report.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded before CI enforcement.

## 4. Output Specification

```markdown
# RAG Eval Report

- **Retrieval:** [Recall and relevance scores per query]
- **Generation:** [Factuality and answer relevance per query]
- **Gate:** [Thresholds with pass or fail verdict]
- **Config:** [Eval file paths]
```

## 5. Validation Gate

- [ ] Retrieval evaluated separately from generation.
- [ ] Thresholds explicit per metric.
- [ ] Gate proven to fail on injected regression.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before CI enforcement.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Grading full answers without isolated retrieval scores.
- **Over-execution threshold:** Changing pipeline code to chase eval scores without review.
- **Calibration default:** Block on high-severity grounding failures; warn on relevance dips.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                              |
| ---- | ---------------------- | ------------------------------------------------------ |
| 1    | AP-3 (no success)      | Requires ground truth before retrieval eval.           |
| 2    | AP-3 (no success)      | Requires verifiable facts before generation eval.      |
| 3    | AP-28 (no stop)        | Fails builds on threshold breach.                      |
| 4    | AP-45 (no human review)| Halts for approval before CI enforcement.              |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Quality Gatekeeper role, role source, and seniority bar.
  - `1.0.0` (2026-09-26) - Initial release from AI engineering batch research.

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

**Input:** "Our RAG answers changed after the last deploy and nobody noticed."
**Output:** Eval config with retrieval recall gate plus factuality gate that fails CI on the regression.
