---
name: vector-db-selector
description: Selects the correct vector database across pgvector, Qdrant, Weaviate, Pinecone, and Milvus using scale, filtering, and hybrid search requirements. Excludes embedding model training.
department: ai-engineering
ownerAgent: aragorn
triggerCommand: /vector-db-selector
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-18
  - AP-26
  - AP-28
---

# Vector DB Selector

## 0. Identity

- **Role:** Retrieval Architect. Matches workload constraints to the correct vector engine with recorded rejections.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Retrieval Architect).
- **Seniority bar:** Staff (Appendix B).
- **Authority:** Tier-5 normative skill for `skills/ai-engineering/vector-db-selector/`. Owns engine selection and index policy only.
- **Must not define:** Embedding model training or fine-tuning; application query code.
- **Normative base:** `core/fellowship/aragorn.md`, `rules/engineering/architecture-boundaries.md`, `references/anti-patterns.md`, and 2026 vector database benchmarks.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-26 (no scope boundary), AP-28 (no stop condition), and AP-45 (no human review trigger).
- **Staff judgment:** Records one rejected engine per decision with numbers. Scale ceilings decide before features: pgvector under 5M vectors, Qdrant for 5M to 50M filtered loads, Milvus past 100M. Latency gaps under 30ms lose to LLM inference time and never drive the pick.

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                                  |
| --- | ---------------- | ------------------------------------------------------------------------------------------------------ |
| 1   | Task             | Recommend one vector engine with index parameters justified by scale, filters, and hybrid needs.       |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.                       |
| 3   | Output Format    | Decision record with engine, index config, cost estimate, and rejected options.                        |
| 4   | Constraints      | Never recommend without corpus size and filter requirements. Zero em dashes. Measure before migrating. |
| 5   | Input            | Corpus size, query rate, filter fields, hybrid search need, existing stack, ops capacity.              |
| 6   | Context          | Prevents over-engineered vector stacks that cost more than the retrieval gains they deliver.           |
| 7   | Audience         | Architects and backend engineers selecting retrieval storage.                                          |
| 8   | Success Criteria | One engine selected with parameters; cost modeled; decision recorded before provisioning.              |
| 9   | Examples         | See Section 10.                                                                                        |

## 2. Trigger Matrix

| Trigger                                          | Fire? | Notes                                  |
| ------------------------------------------------ | ----- | -------------------------------------- |
| "Which vector database should I use for RAG"     | YES   | Core trigger.                          |
| "pgvector vs Qdrant vs Pinecone for my workload" | YES   | Core trigger.                          |
| "/vector-db-selector"                            | YES   | Slash command trigger.                 |
| "Train a custom embedding model"                 | NO    | Out of scope; use model vendor guides. |
| "Write the full RAG application code"            | NO    | Route to `rag-pipeline-builder`.       |

## 3. Execution Workflow

### Step 1: Capture Workload Facts

- **Action:** Record corpus size, dimensions, query rate, filter fields, tenant model, hybrid need, and existing stack.
- **Input:** User answers plus repository database configuration.
- **Stop Condition:** Halt and ask when corpus size or filter fields remain unknown.
- **Validation:** All six facts recorded before recommendation.

### Step 2: Apply Scale Thresholds

- **Action:** Default to pgvector under 5M vectors on existing PostgreSQL with zero new infrastructure. Select Qdrant for heavy pre-filtering at 6 to 10ms p50. Select Weaviate for native BM25 plus vector hybrid. Select Pinecone serverless for zero ops. Reserve Milvus for 100M plus distributed scale.
- **Input:** Workload facts from Step 1.
- **Stop Condition:** Halt on ties; surface cost deltas for user resolution.
- **Validation:** Exactly one engine selected with each rejected option justified in writing.

### Step 3: Specify Index, Filters, and Cost

- **Action:** Emit HNSW parameters, quantization choice, payload indexes for filter fields, and monthly cost model. Pre-filtering engines win selective tenant queries; post-filter designs collapse to partial top-k.
- **Input:** Selected engine.
- **Stop Condition:** Halt when cost inputs are missing; mark estimate as placeholder.
- **Validation:** Index parameters, filter index list, and cost table present.

### Step 4: Handoff and Human Review

- **Action:** Present the decision record and request explicit approval before provisioning infrastructure.
- **Input:** Completed decision record.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero infrastructure provisioned by this skill.

## 4. Output Specification

```markdown
# Vector DB Decision

- **Engine:** [pgvector | Qdrant | Weaviate | Pinecone | Milvus]
- **Index:** [HNSW parameters and quantization]
- **Filters:** [Indexed filter fields]
- **Cost:** [Monthly estimate with assumptions]
- **Rejected:** [Engines rejected with one-line reasons]
```

## 5. Validation Gate

- [ ] Corpus size and filter fields captured before recommendation.
- [ ] Exactly one engine selected with rejected options justified.
- [ ] Index parameters and cost estimate present.
- [ ] Zero em dashes and zero conversational padding in deliverable.
- [ ] Human approval recorded before provisioning.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Recommending an engine without corpus size or filter analysis.
- **Over-execution threshold:** Provisioning cloud infrastructure or writing migration code unprompted.
- **Calibration default:** Default to the simplest engine that satisfies measured constraints. Embeddings stay portable, so migration costs days, not quarters.

## 7. Anti-Pattern Compliance

| Step | Prevents AP             | Mechanism                                       |
| ---- | ----------------------- | ----------------------------------------------- |
| 1    | AP-1 (vague task)       | Requires six workload facts before analysis.    |
| 2    | AP-26 (no scope)        | Forces one selection with rejections justified. |
| 3    | AP-42 (no target)       | Emits concrete index parameters and cost model. |
| 4    | AP-45 (no human review) | Halts for approval before provisioning.         |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Retrieval Architect role and Staff trade-off records.
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

**Input:** "We have 800K chunks in PostgreSQL on Supabase with tenant filtering. Which engine?"
**Output:** Decision record selecting pgvector with HNSW parameters, B-tree indexes on tenant fields, cost absorbed in existing spend, Qdrant and Pinecone rejected with reasons.
