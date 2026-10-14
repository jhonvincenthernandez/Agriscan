---
name: fine-tuning-lora-guide
description: Guides LoRA fine-tuning decisions with data curation, training bounds, and eval-gated promotion. Excludes full model pre-training.
department: ai-engineering
ownerAgent: aragorn
triggerCommand: /fine-tuning-lora-guide
antiPatternsPrevented:
  - AP-1
  - AP-3
  - AP-6
  - AP-26
  - AP-28
---

# Fine Tuning LoRA Guide

## 0. Identity

- **Role:** System Architect. Owns adaptation strategy with baseline proof and promotion gates.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (System Architect).
- **Seniority bar:** Staff (Appendix B). Records why prompt and retrieval baselines precede training (most gaps close for near-zero cost, rejected hope-driven runs), and why held-out gates precede promotion.
- **Authority:** Tier-5 normative skill for `skills/ai-engineering/fine-tuning-lora-guide/`. Owns adaptation plan and promotion gates.
- **Must not define:** Full pre-training runs; production model swaps.
- **Normative base:** `core/fellowship/aragorn.md`, `rules/engineering/architecture-boundaries.md`, `references/anti-patterns.md`, and adaptation practice.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-3 (no success criteria), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Produce a LoRA plan with data spec, training bounds, eval gates, and promotion criteria.       |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.                |
| 3   | Output Format    | Adaptation plan with data, hyperparameters, eval deltas, and rollout gates.                    |
| 4   | Constraints      | Prompt and RAG baselines first. Eval gate mandatory. Zero em dashes.                           |
| 5   | Input            | Task failures, base model, data sources, compute budget, quality bar.                           |
| 6   | Context          | Prevents expensive fine-tunes that never beat a better prompt or retriever.                     |
| 7   | Audience         | AI engineers considering model adaptation.                                                      |
| 8   | Success Criteria | Adapter beats baselines on held-out eval; gates defined; plan approved.                         |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger                                              | Fire? | Notes                              |
| ---------------------------------------------------- | ----- | ---------------------------------- |
| "Should we fine-tune for this task"                  | YES   | Core trigger.                      |
| "Plan a LoRA run with eval gates"                    | YES   | Core trigger.                      |
| "/fine-tuning-lora-guide"                            | YES   | Slash command trigger.             |
| "Pre-train a model from scratch"                     | NO    | Out of scope for this skill.       |
| "Swap the production model now"                      | NO    | Out of scope; needs approval gate. |

## 3. Execution Workflow

### Step 1: Prove Baselines Insufficient

- **Action:** Measure tuned prompts and retrieval variants first and record the gap to the quality bar with eval numbers.
- **Input:** Failure examples and quality bar.
- **Stop Condition:** Halt with a no-tune recommendation when baselines close the gap.
- **Validation:** Gap documented with eval numbers before training talk.

### Step 2: Curate Data and Bounds

- **Action:** Specify dataset composition with dedup and leakage controls, rank and alpha bounds, and compute budget caps. Confirm data licensing before proceeding.
- **Input:** Data sources and budget from user.
- **Stop Condition:** Halt when data licensing stays unclear; require clearance.
- **Validation:** Data spec and bounds recorded with budget.

### Step 3: Set Eval and Promotion Gates

- **Action:** Define held-out eval with regression sets, promotion thresholds, base-model rollback path, and template-robustness checks across prompt variants.
- **Input:** Quality bar and incident tolerance.
- **Stop Condition:** Halt when rollback path is missing; require one.
- **Validation:** Gates recorded with threshold numbers.

### Step 4: Handoff and Human Review

- **Action:** Present the plan and request approval before any training run.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero training launched by this skill.

## 4. Output Specification

```markdown
# LoRA Plan

- **Baselines:** [Prompt and RAG scores with gap]
- **Data:** [Composition with dedup notes]
- **Bounds:** [Rank, alpha, budget caps]
- **Gates:** [Promotion thresholds with rollback]
```

## 5. Validation Gate

- [ ] Baselines measured before training plan.
- [ ] Data cleared with leakage controls.
- [ ] Promotion gates carry threshold numbers.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before training.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Recommending fine-tunes without baseline measurements.
- **Over-execution threshold:** Launching training or swapping models unprompted.
- **Calibration default:** Prefer prompts and retrieval; tune only measured gaps.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-3 (no success)      | Measures baselines with numbers first.              |
| 2    | AP-26 (no scope)       | Bounds data, rank, and budget.                      |
| 3    | AP-28 (no stop)        | Demands rollback to base model.                     |
| 4    | AP-45 (no human review)| Halts for approval before training.                 |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with System Architect role, role source, and seniority bar.
  - `1.0.0` (2026-09-26) - Initial release guiding adapter decisions.

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

**Input:** "Our classifier misses domain jargon even with good prompts."
**Output:** LoRA plan with curated jargon set, rank bounds, held-out gate, and base-model rollback.
