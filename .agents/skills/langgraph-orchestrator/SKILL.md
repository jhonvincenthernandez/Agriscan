---
name: langgraph-orchestrator
description: Builds durable stateful agent graphs with checkpoints, conditional routing, and human-in-the-loop interrupts. Excludes model provider selection.
department: ai-engineering
ownerAgent: gandalf
triggerCommand: /langgraph-orchestrator
antiPatternsPrevented:
  - AP-1
  - AP-4
  - AP-6
  - AP-26
  - AP-28
---

# LangGraph Orchestrator

## 0. Identity

- **Role:** Graph Designer. Models agent workflows as explicit nodes, edges, persisted state, and gated side effects.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Graph Designer).
- **Seniority bar:** Staff (Appendix B).
- **Authority:** Tier-5 normative skill for `skills/ai-engineering/langgraph-orchestrator/`. Owns graph topology and checkpoint policy.
- **Must not define:** Retrieval internals (see `llamaindex-retrieval`); production deployment infrastructure.
- **Normative base:** `core/fellowship/gandalf.md`, `rules/engineering/architecture-boundaries.md`, `references/anti-patterns.md`, and batch research on 2026 agent frameworks.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-4 (over-permissive agent), AP-26 (no scope boundary), and AP-28 (no stop condition).
- **Staff judgment:** Records why explicit graphs beat conversational consensus (programmatic routing burns zero inference tokens) and why single-agent-with-tools precedes multi-agent. Rejected: three-agent crews for single-agent problems and in-process interrupts mistaken for security policy.

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                              |
| --- | ---------------- | -------------------------------------------------------------------------------------------------- |
| 1   | Task             | Design an explicit agent graph with state schema, routing edges, checkpoints, and approval pauses. |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.                    |
| 3   | Output Format    | Graph blueprint with nodes, edges, state schema, and interrupt points.                             |
| 4   | Constraints      | Every side effect passes an interrupt. State survives restarts via checkpointer. Zero em dashes.   |
| 5   | Input            | Workflow goal, tool list, approval points, durability requirements.                                 |
| 6   | Context          | Prevents opaque agent loops that cannot pause, resume, or audit their execution path.              |
| 7   | Audience         | AI engineers building production-grade stateful agents.                                             |
| 8   | Success Criteria | Graph renders with all edges explicit; interrupts placed; blueprint approved before coding.         |
| 9   | Examples         | See Section 10.                                                                                     |

## 2. Trigger Matrix

| Trigger                                              | Fire? | Notes                            |
| ---------------------------------------------------- | ----- | -------------------------------- |
| "Build a stateful agent with approval pauses"        | YES   | Core trigger.                    |
| "Model our agent workflow as an explicit graph"      | YES   | Core trigger.                    |
| "/langgraph-orchestrator"                            | YES   | Slash command trigger.           |
| "Spin up a quick role-based demo crew"               | NO    | Prefer lightweight crew pattern. |
| "Index our document corpus for search"               | NO    | Route to `llamaindex-retrieval`. |

## 3. Execution Workflow

### Step 1: Define State Schema

- **Action:** Declare the typed state object shared across nodes, including task status, artifacts, and approval flags. Carry identifiers and summaries, never full histories.
- **Input:** Workflow goal and tool list.
- **Stop Condition:** Halt and ask when side effects lack explicit approval flags.
- **Validation:** State schema recorded with field purposes.

### Step 2: Lay Out Nodes and Edges

- **Action:** Define nodes as single-purpose units and edges as explicit conditional routes, including cycles for validation loops and escalation paths. Keep prompts lean to control token overhead.
- **Input:** State schema from Step 1.
- **Stop Condition:** Halt when any transition stays implicit; every route needs a named edge.
- **Validation:** Graph covers happy path, retry path with caps, and escalation path.

### Step 3: Place Checkpoints and Interrupts

- **Action:** Attach a checkpointer (Postgres or SQLite) for durable persistence and interrupt points before every mutating action with approve, reject, and edit options.
- **Input:** Graph layout from Step 2.
- **Stop Condition:** Halt when a write path lacks an interrupt; mark it as a finding.
- **Validation:** Every side effect maps to an interrupt; external policy gates noted as separate components.

### Step 4: Handoff and Human Review

- **Action:** Present the graph blueprint and request approval before implementation.
- **Input:** Completed blueprint.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero code executed by this skill.

## 4. Output Specification

```markdown
# Agent Graph Blueprint

- **State:** [Schema fields with purposes]
- **Nodes:** [Node list with single responsibilities]
- **Edges:** [Conditional routes including cycles]
- **Interrupts:** [Approval points before side effects]
- **Checkpoints:** [Persistence policy]
```

## 5. Validation Gate

- [ ] State schema declared with purposes.
- [ ] All transitions explicit including retries.
- [ ] Every side effect guarded by an interrupt.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before coding.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Sketching agents without explicit state or edges.
- **Over-execution threshold:** Executing tools or mutating systems during design.
- **Calibration default:** Add friction at approval points; keep all other paths lean.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-1 (vague task)      | Requires typed state before graph layout.           |
| 2    | AP-26 (no scope)       | Forces explicit edges for every transition.         |
| 3    | AP-4 (over-permissive) | Guards every side effect with an interrupt.         |
| 4    | AP-45 (no human review)| Halts for blueprint approval before coding.         |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Graph Designer role and Staff trade-off records.
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

**Input:** "Build a refund agent that checks policy, issues refunds, and logs everything."
**Output:** Graph blueprint with policy node, interrupt before refund execution, ledger node, and Postgres checkpointer policy.
