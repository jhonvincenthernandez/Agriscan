---
name: reranker-optimizer
description: Tunes hybrid fusion and rerank stages so retrieved context maximizes answer utility instead of topical similarity alone. Excludes generator prompt design.
department: ai-engineering
ownerAgent: legolas
triggerCommand: /reranker-optimizer
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-18
  - AP-26
  - AP-28
---

# Reranker Optimizer

## 0. Identity

- **Role:** Relevance Tuner. Aligns ranking stages with downstream answer quality using judged evidence.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Relevance Tuner).
- **Seniority bar:** Staff (Appendix B).
- **Authority:** Tier-5 normative skill for `skills/ai-engineering/reranker-optimizer/`. Owns fusion weights and rerank policy.
- **Must not define:** Answer generation prompts (see `rag-pipeline-builder`); vector index builds.
- **Normative base:** `core/fellowship/legolas.md`, `rules/engineering/architecture-boundaries.md`, `references/anti-patterns.md`, and batch research on hybrid fusion and rerank alignment.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-26 (no scope boundary), AP-28 (no stop condition), and AP-42 (no target state).
- **Staff judgment:** Records why RRF fusion beats score blending on the target mix, and why utility-first ordering beats similarity ranking with answer-quality deltas. Rejected: deep pools without rerankers and global blends serving all query types.

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                           |
| --- | ---------------- | ----------------------------------------------------------------------------------------------- |
| 1   | Task             | Set fusion weights, candidate depth, and rerank top-k so final context serves the generator.    |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.                |
| 3   | Output Format    | Rerank policy with fusion config, depth, model, and utility metrics.                            |
| 4   | Constraints      | Optimize for answer utility, not raw similarity scores. Zero em dashes. Bounded candidate cost. |
| 5   | Input            | First-stage retrieval output, query types, generator behavior, latency budget.                  |
| 6   | Context          | Prevents topically relevant but answer-useless context from reaching the generator.             |
| 7   | Audience         | AI engineers tuning RAG relevance and cost.                                                     |
| 8   | Success Criteria | Fusion and rerank set; utility metrics improve on eval set; policy recorded.                    |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger                                          | Fire? | Notes                            |
| ------------------------------------------------ | ----- | -------------------------------- |
| "Tune our hybrid search fusion weights"          | YES   | Core trigger.                    |
| "Our reranker returns relevant but useless docs" | YES   | Core trigger.                    |
| "/reranker-optimizer"                            | YES   | Slash command trigger.           |
| "Design the full RAG pipeline from scratch"      | NO    | Route to `rag-pipeline-builder`. |
| "Write the answer generation prompt"             | NO    | Out of scope for this skill.     |

## 3. Execution Workflow

### Step 1: Diagnose Retrieval Failure Mode

- **Action:** Classify misses as keyword blindness, title over-anchoring, stale ranks, or utility mismatch with the generator.
- **Input:** Query logs with judged relevance and answer quality.
- **Stop Condition:** Halt and ask when judged samples are missing.
- **Validation:** Failure mode recorded with example queries.

### Step 2: Set Fusion and Depth

- **Action:** Configure dense plus sparse fusion with RRF or weighted blend, per-query-type weights, candidate depth, and filter interaction inside the latency budget.
- **Input:** Failure diagnosis from Step 1.
- **Stop Condition:** Halt when latency budget blocks deeper pools; record the bound.
- **Validation:** Fusion config and depth recorded with cost note.

### Step 3: Set Rerank Policy

- **Action:** Select rerank model, top-k cutoff, and utility-first ordering favoring documents the generator actually uses. Pin pet-query exceptions with query rules instead of global retunes.
- **Input:** Generator feedback on context utility.
- **Stop Condition:** Halt when eval shows no utility gain; keep the cheaper policy.
- **Validation:** Rerank policy recorded with before and after utility metrics.

### Step 4: Handoff and Human Review

- **Action:** Present the policy with metric deltas and request approval before rollout.
- **Input:** Final rerank policy.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero production rollout performed.

## 4. Output Specification

```markdown
# Rerank Policy

- **Fusion:** [Method and per-type weights]
- **Depth:** [Candidate pool size with latency note]
- **Rerank:** [Model and top-k cutoff]
- **Utility:** [Before and after answer-utility metrics]
```

## 5. Validation Gate

- [ ] Failure mode diagnosed with examples.
- [ ] Fusion weights and depth recorded.
- [ ] Rerank policy recorded with utility deltas.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before rollout.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Adjusting weights without judged query samples.
- **Over-execution threshold:** Rolling out rerank changes to production unprompted.
- **Calibration default:** Keep candidate pools shallow until utility measurement demands depth.

## 7. Anti-Pattern Compliance

| Step | Prevents AP             | Mechanism                                      |
| ---- | ----------------------- | ---------------------------------------------- |
| 1    | AP-1 (vague task)       | Requires failure classification with examples. |
| 2    | AP-26 (no scope)        | Bounds fusion and depth with latency notes.    |
| 3    | AP-42 (no target)       | Records utility deltas on eval set.            |
| 4    | AP-45 (no human review) | Halts for approval before rollout.             |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Relevance Tuner role and Staff trade-off records.
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

**Input:** "Hybrid search returns our pricing page for every query. Fix the fusion."
**Output:** Rerank policy lowering title weight for paraphrase queries with measured utility gain on eval set.
