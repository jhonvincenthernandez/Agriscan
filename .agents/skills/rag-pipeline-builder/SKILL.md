---
name: rag-pipeline-builder
description: Designs retrieval augmented generation pipelines across chunking, embedding, hybrid retrieval, rerank, and generation stages with isolated evaluation. Excludes vector engine provisioning.
department: ai-engineering
ownerAgent: aragorn
triggerCommand: /rag-pipeline-builder
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-18
  - AP-26
  - AP-28
---

# RAG Pipeline Builder

## 0. Identity

- **Role:** System Architect. Designs stage-by-stage retrieval pipelines with measurable quality gates per stage.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (System Architect).
- **Seniority bar:** Staff (Appendix B).
- **Authority:** Tier-5 normative skill for `skills/ai-engineering/rag-pipeline-builder/`. Owns pipeline topology and stage contracts.
- **Must not define:** Vector engine provisioning (see `vector-db-selector`); model weights or training runs.
- **Normative base:** `core/fellowship/aragorn.md`, `rules/engineering/architecture-boundaries.md`, `references/anti-patterns.md`, and batch research on hybrid retrieval systems.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-26 (no scope boundary), AP-28 (no stop condition), and AP-45 (no human review trigger).
- **Staff judgment:** Records why hybrid fusion beats pure vector on the target query mix with recall numbers, and why stage-separated evals beat blended scores. Rejected: single-blob designs that hide which stage breaks.

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                              |
| --- | ---------------- | -------------------------------------------------------------------------------------------------- |
| 1   | Task             | Produce a staged RAG design with chunking, embedding, retrieval, rerank, and generation contracts. |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.                    |
| 3   | Output Format    | Pipeline blueprint with stage configs, data contracts, and eval hooks.                             |
| 4   | Constraints      | Separate retrieval eval from generation eval. Never skip the eval hook per stage. Zero em dashes.   |
| 5   | Input            | Corpus description, query types, latency budget, quality targets, engine decision.                  |
| 6   | Context          | Prevents single-blob RAG designs that fail silently on keyword queries and multi-hop questions.    |
| 7   | Audience         | Backend engineers and AI engineers building knowledge assistants.                                   |
| 8   | Success Criteria | Five stages specified with contracts; eval hooks defined; blueprint approved before coding.         |
| 9   | Examples         | See Section 10.                                                                                     |

## 2. Trigger Matrix

| Trigger                                     | Fire? | Notes                            |
| ------------------------------------------- | ----- | -------------------------------- |
| "Design a RAG pipeline over our docs"       | YES   | Core trigger.                    |
| "Fix our RAG missing exact keyword matches" | YES   | Core trigger; routes to hybrid.  |
| "/rag-pipeline-builder"                     | YES   | Slash command trigger.           |
| "Which vector database should I provision"  | NO    | Route to `vector-db-selector`.   |
| "Evaluate my existing RAG deployment"       | NO    | Route to `promptfoo-eval-runner`.|

## 3. Execution Workflow

### Step 1: Profile Corpus and Queries

- **Action:** Classify corpus structure and query types (exact match, paraphrase, implied intent, distractor) with example questions per class.
- **Input:** Sample documents and representative questions.
- **Stop Condition:** Halt and ask when query distribution remains unknown.
- **Validation:** Query categories recorded with examples.

### Step 2: Specify Chunking and Embedding

- **Action:** Set chunking strategy with size and overlap plus embedding model and dimensions. Default to 512-token chunks with 25 overlap; use 64 to 128 tokens for fact-dense content and title enrichment as the cheap ranking upgrade.
- **Input:** Corpus profile from Step 1.
- **Stop Condition:** Halt when document format blocks parsing; surface the blocker.
- **Validation:** Chunk parameters and embedding model recorded with rationale.

### Step 3: Specify Hybrid Retrieval and Rerank

- **Action:** Define dense plus BM25 hybrid fusion with RRF weights, metadata pre-filters, candidate depth, and rerank stage tuned for answer utility over similarity.
- **Input:** Query profile showing keyword sensitivity.
- **Stop Condition:** Halt when filter fields lack indexes; flag for `vector-db-selector` follow-up.
- **Validation:** Fusion method, candidate depth, and rerank model specified.

### Step 4: Specify Generation Contract and Eval Hooks

- **Action:** Define answer contract (citations required, refusal on out-of-corpus, length bounds) and attach retrieval eval plus generation eval hooks per stage.
- **Input:** Quality targets from user.
- **Stop Condition:** Await user approval of the blueprint before implementation.
- **Validation:** Eval hooks reference `promptfoo-eval-runner` metrics explicitly.

## 4. Output Specification

```markdown
# RAG Blueprint

- **Chunking:** [Strategy, size, overlap]
- **Embedding:** [Model and dimensions]
- **Retrieval:** [Hybrid fusion, filters, candidate depth]
- **Rerank:** [Model and top-k policy]
- **Generation:** [Answer contract and refusal rules]
- **Eval:** [Retrieval metrics and generation metrics]
```

## 5. Validation Gate

- [ ] Query categories profiled with examples.
- [ ] Chunking and embedding specified with rationale.
- [ ] Hybrid fusion and rerank specified.
- [ ] Eval hooks attached to retrieval and generation separately.
- [ ] Human approval recorded before coding.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Emitting a single-vector-search design without hybrid or eval stages.
- **Over-execution threshold:** Writing production application code or provisioning infrastructure.
- **Calibration default:** Prefer simple token chunking until measurement proves a costlier method wins.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                          |
| ---- | ---------------------- | -------------------------------------------------- |
| 1    | AP-1 (vague task)      | Requires query distribution before design.         |
| 2    | AP-26 (no scope)       | Bounds each stage with explicit contracts.         |
| 3    | AP-42 (no target)      | Specifies fusion weights and candidate depth.      |
| 4    | AP-45 (no human review)| Halts for blueprint approval before coding.        |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with System Architect role and Staff trade-off records.
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

**Input:** "Design RAG over our API docs. Users search by error codes and by plain questions."
**Output:** Blueprint with header-aware chunking, hybrid BM25 plus dense fusion for code queries, rerank top-20 to top-5, and citation-required answer contract.
