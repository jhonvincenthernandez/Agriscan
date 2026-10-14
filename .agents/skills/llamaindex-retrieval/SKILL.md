---
name: llamaindex-retrieval
description: Connects agents to enterprise data with connectors, indexes, query engines, and event-driven retrieval workflows. Excludes general agent orchestration.
department: ai-engineering
ownerAgent: frodo
triggerCommand: /llamaindex-retrieval
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-18
  - AP-26
  - AP-28
---

# LlamaIndex Retrieval

## 0. Identity

- **Role:** Pipeline Builder. Owns staged data pipeline topology from connectors through indexes to query routing.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Pipeline Builder).
- **Seniority bar:** Staff (Appendix B). Records why domain-split indexes beat blended mega-indexes with precision evidence, and why retrieval-first layering beats orchestration-first layering.
- **Authority:** Tier-5 normative skill for `skills/ai-engineering/llamaindex-retrieval/`. Owns ingestion, indexing, and query routing.
- **Must not define:** General multi-agent orchestration (see `langgraph-orchestrator`); vector engine provisioning.
- **Normative base:** `core/fellowship/frodo.md`, `rules/engineering/architecture-boundaries.md`, `references/anti-patterns.md`, and batch research on document-centric frameworks.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-18 (stale internal state), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                        |
| --- | ---------------- | -------------------------------------------------------------------------------------------- |
| 1   | Task             | Wire data sources into query engines that agents select by question type.                    |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.              |
| 3   | Output Format    | Retrieval wiring plan with connectors, indexes, query engines, and refresh policy.           |
| 4   | Constraints      | One query engine per data domain. Refresh policy mandatory. Zero em dashes.                  |
| 5   | Input            | Data source inventory, access rules, freshness needs, question types.                         |
| 6   | Context          | Prevents agents that hallucinate enterprise facts because retrieval was never wired.          |
| 7   | Audience         | AI engineers grounding agents in company knowledge.                                           |
| 8   | Success Criteria | Every source maps to an engine; refresh policy set; plan approved before wiring.              |
| 9   | Examples         | See Section 10.                                                                               |

## 2. Trigger Matrix

| Trigger                                          | Fire? | Notes                              |
| ------------------------------------------------ | ----- | ---------------------------------- |
| "Connect our agent to PDFs and Confluence"       | YES   | Core trigger.                      |
| "Build query engines per document domain"        | YES   | Core trigger.                      |
| "/llamaindex-retrieval"                          | YES   | Slash command trigger.             |
| "Design stateful multi-agent approval graphs"    | NO    | Route to `langgraph-orchestrator`. |
| "Evaluate retrieval quality with metrics"        | NO    | Route to `promptfoo-eval-runner`.  |

## 3. Execution Workflow

### Step 1: Inventory Sources and Access

- **Action:** List every source with format, volume, access control, and freshness requirement. Capture permission metadata at ingestion so filters enforce access at retrieval, not at display.
- **Input:** Stakeholder source list plus repository data configs.
- **Stop Condition:** Halt and ask when access rules for a source remain undefined.
- **Validation:** Source table complete with owners and refresh needs.

### Step 2: Define Indexes per Domain

- **Action:** Assign one index per data domain with chunking policy and metadata schema for permission filtering. Blend nothing across domains.
- **Input:** Source inventory from Step 1.
- **Stop Condition:** Halt when permission metadata cannot map to index filters; flag as finding.
- **Validation:** Each domain has exactly one index definition.

### Step 3: Route Queries to Engines

- **Action:** Define query engine selection rules by question type with fallback order and refusal when no engine covers the question. Fuse keyword plus semantic signals inside each engine first.
- **Input:** Representative question set.
- **Stop Condition:** Halt when a question type maps to zero engines; surface the gap.
- **Validation:** Routing table covers all question types with fallbacks.

### Step 4: Handoff and Human Review

- **Action:** Present the wiring plan with refresh policy and request approval before implementation.
- **Input:** Completed wiring plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero connectors built by this skill.

## 4. Output Specification

```markdown
# Retrieval Wiring Plan

- **Sources:** [Source table with access and freshness]
- **Indexes:** [One index per domain with filters]
- **Routing:** [Question type to engine mapping]
- **Refresh:** [Re-index cadence per source]
```

## 5. Validation Gate

- [ ] All sources inventoried with access rules.
- [ ] One index defined per domain.
- [ ] Routing covers every question type.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before wiring.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Wiring retrieval without access rules or refresh policy.
- **Over-execution threshold:** Ingesting production data or building connectors unprompted.
- **Calibration default:** Split indexes by domain early; merging later costs less than splitting late.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-1 (vague task)      | Requires source inventory with access rules.        |
| 2    | AP-26 (no scope)       | Enforces one index per domain.                      |
| 3    | AP-18 (stale state)    | Mandates refresh policy per source.                 |
| 4    | AP-45 (no human review)| Halts for approval before wiring.                   |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Pipeline Builder role, role source, and seniority bar.
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

**Input:** "Our support agent must answer from help center, API docs, and ticket history."
**Output:** Wiring plan with three domain indexes, permission-filtered ticket engine, and nightly refresh policy.
