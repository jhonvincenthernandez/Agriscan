---
name: chunking-evaluator
description: Compares chunking strategies with retrieval and cost metrics to select the cheapest method that meets quality targets. Excludes production re-indexing.
department: ai-engineering
ownerAgent: merry
triggerCommand: /chunking-evaluator
antiPatternsPrevented:
  - AP-1
  - AP-3
  - AP-6
  - AP-26
  - AP-28
---

# Chunking Evaluator

## 0. Identity

- **Role:** Eval Runner. Measures chunking methods on effectiveness plus system cost and selects the cheapest winner.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Eval Runner).
- **Seniority bar:** Staff (Appendix B).
- **Authority:** Tier-5 normative skill for `skills/ai-engineering/chunking-evaluator/`. Owns comparison protocol and selection only.
- **Must not define:** Production index rebuilds; embedding model selection.
- **Normative base:** `core/fellowship/merry.md`, `rules/engineering/architecture-boundaries.md`, `references/anti-patterns.md`, and batch research on multi-objective chunking evaluation.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-3 (no success criteria), AP-26 (no scope boundary), and AP-28 (no stop condition).
- **Staff judgment:** Records why token chunking defends its title on each corpus with throughput numbers, and why expensive methods lose despite marginal NDCG gains. Rejected: adopting semantic or LLM chunking on authority without same-setup measurement.

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                                |
| --- | ---------------- | ---------------------------------------------------------------------------------------------------- |
| 1   | Task             | Compare chunking methods on NDCG, Recall, throughput, and memory, then select the cheapest winner.   |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.                     |
| 3   | Output Format    | Comparison table with metrics, cost columns, and one selected method.                                |
| 4   | Constraints      | Test simple baselines first. Treat costly methods as guilty until measured innocent. Zero em dashes. |
| 5   | Input            | Sample corpus, query set with relevance labels, candidate methods, cost limits.                      |
| 6   | Context          | Prevents expensive semantic pipelines that never beat token chunking on measured quality.            |
| 7   | Audience         | QA engineers and AI engineers tuning retrieval quality.                                              |
| 8   | Success Criteria | Metrics table complete; winner selected by quality per cost; decision recorded.                      |
| 9   | Examples         | See Section 10.                                                                                      |

## 2. Trigger Matrix

| Trigger                                        | Fire? | Notes                              |
| ---------------------------------------------- | ----- | ---------------------------------- |
| "Which chunking strategy fits our corpus"      | YES   | Core trigger.                      |
| "Compare semantic vs token chunking with data" | YES   | Core trigger.                      |
| "/chunking-evaluator"                          | YES   | Slash command trigger.             |
| "Rebuild our production vector index now"      | NO    | Out of scope; needs approval gate. |
| "Pick an embedding model for us"               | NO    | Out of scope for this skill.       |

## 3. Execution Workflow

### Step 1: Fix Baselines and Metrics

- **Action:** Lock token chunking (512 tokens, 25 overlap) as baseline. Define NDCG at 10 for ranking quality, Recall at 100 for first-stage coverage, plus throughput and memory columns.
- **Input:** Query set and cost limits.
- **Stop Condition:** Halt and ask when relevance labels are missing.
- **Validation:** Metrics and baselines recorded before any comparison run.

### Step 2: Run Candidate Comparisons

- **Action:** Evaluate each candidate (sentence, enriched title, enriched summary, semantic, hierarchical) on the same index setup, embedding model, and query set. Prefer title enrichment as the low-cost upgrade; demand proof before summary or LLM methods.
- **Input:** Chunked corpus variants and fixed embedding model.
- **Stop Condition:** Halt when a method fails to build; record the failure instead of silently dropping it.
- **Validation:** Every candidate has complete metric rows or explicit failure notes.

### Step 3: Select by Quality per Cost

- **Action:** Select the cheapest method meeting the quality target. Weigh indexing throughput and memory across a year of re-indexing, not one run.
- **Input:** Completed comparison table.
- **Stop Condition:** Halt on ties; surface cost deltas for user decision.
- **Validation:** One winner selected with quality and cost justification.

### Step 4: Handoff and Human Review

- **Action:** Present the table and recommendation; request approval before any index change.
- **Input:** Final comparison deliverable.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero production writes performed.

## 4. Output Specification

```markdown
# Chunking Comparison

- **Baseline:** [Token chunking config]
- **Winner:** [Method with quality per cost reason]
- **Table:** [Method rows with NDCG, Recall, throughput, memory]
- **Rejected:** [Costly methods with measured deltas]
```

## 5. Validation Gate

- [ ] Baseline and metrics locked before runs.
- [ ] All candidates measured on identical setup.
- [ ] Winner justified by quality per cost.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before index changes.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Declaring a winner without measured metrics on the same query set.
- **Over-execution threshold:** Rebuilding production indexes without approval.
- **Calibration default:** Default to token chunking until a challenger wins by measurement.

## 7. Anti-Pattern Compliance

| Step | Prevents AP             | Mechanism                                        |
| ---- | ----------------------- | ------------------------------------------------ |
| 1    | AP-3 (no success)       | Locks metrics before comparison runs.            |
| 2    | AP-18 (hidden state)    | Records failures instead of dropping candidates. |
| 3    | AP-42 (no target)       | Selects one winner with cost justification.      |
| 4    | AP-45 (no human review) | Halts for approval before index changes.         |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Eval Runner role and Staff trade-off records.
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

**Input:** "Our semantic chunking feels slow. Prove whether it beats token chunking."
**Output:** Comparison table showing token chunking within 1 point of NDCG with 10x indexing throughput, recommending token chunking retention.
