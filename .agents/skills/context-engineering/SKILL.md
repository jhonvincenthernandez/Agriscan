---
name: context-engineering
description: Selects, budgets, compacts, and routes context into agent windows so long runs stay grounded without token bloat. Excludes prompt wording style.
department: ai-engineering
ownerAgent: gandalf
triggerCommand: /context-engineering
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-16
  - AP-26
  - AP-28
---

# Context Engineering

## 0. Identity

- **Role:** Context Steward. Owns window budgets, source maps, and compaction policy for long runs.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Context Steward).
- **Seniority bar:** Staff (Appendix B). Records why map-first loading beats dumps (attention preserved for the task, rejected thousand-page manuals), and why missing context gets fixed in tooling rather than prompts.
- **Authority:** Tier-5 normative skill for `skills/ai-engineering/context-engineering/`. Owns context selection, budget, and compaction policy.
- **Must not define:** Prompt wording or tone (see `prompt-engineering`); vector index builds.
- **Normative base:** `core/fellowship/gandalf.md`, `rules/engineering/architecture-boundaries.md`, `references/anti-patterns.md`, and 2026 context engineering practice.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-16 (context dump), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                               |
| --- | ---------------- | --------------------------------------------------------------------------------------------------- |
| 1   | Task             | Produce a context policy with selection rules, token budget, compaction triggers, and memory tiers. |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.                    |
| 3   | Output Format    | Context policy with budget table, source priority, compaction rules, and map file.                  |
| 4   | Constraints      | Map first, never dump. Budget enforced per turn. Zero em dashes. No full-file pasting by default.   |
| 5   | Input            | Task type, repository map, memory stores, retrieval engines, token limits.                          |
| 6   | Context          | Prevents window bloat that burns budget and degrades agent attention on long runs.                  |
| 7   | Audience         | AI engineers and agent operators running long autonomous sessions.                                  |
| 8   | Success Criteria | Policy caps tokens per turn; compaction triggers fire; map resolves before deep reads.              |
| 9   | Examples         | See Section 10.                                                                                     |

## 2. Trigger Matrix

| Trigger                                       | Fire? | Notes                            |
| --------------------------------------------- | ----- | -------------------------------- |
| "Our agent loses requirements on long runs"   | YES   | Core trigger.                    |
| "Design context budget and compaction policy" | YES   | Core trigger.                    |
| "/context-engineering"                        | YES   | Slash command trigger.           |
| "Rewrite this prompt to sound better"         | NO    | Route to `prompt-engineering`.   |
| "Build our vector index from scratch"         | NO    | Route to `llamaindex-retrieval`. |

## 3. Execution Workflow

### Step 1: Write the Map

- **Action:** Produce a short map file pointing to sources of truth (structured docs directory, architecture maps, versioned plans) instead of pasting full files.
- **Input:** Repository structure and key specification paths.
- **Stop Condition:** Halt and ask when source-of-truth paths stay unidentified.
- **Validation:** Map fits on one screen and resolves every deep reference.

### Step 2: Set Source Priority and Budget

- **Action:** Rank context sources by task type and assign token caps per turn capped at 70 percent of window, reserving headroom for tool outputs and reasoning. Load only the skill each step needs.
- **Input:** Task type and model window limits.
- **Stop Condition:** Halt when budget exceeds 70 percent of window; require cuts.
- **Validation:** Budget table totals within window with headroom recorded.

### Step 3: Define Compaction and Memory Tiers

- **Action:** Set checkpoint triggers with summary format, decision-log retention, golden-principles persistence, and hot versus cold memory tiers with retrieval hooks. Schedule background garbage-collection scans.
- **Input:** Session length expectations and memory stores.
- **Stop Condition:** Halt when compaction drops decision history; require decision log retention.
- **Validation:** Compaction rules preserve decisions, open tasks, and verification status.

### Step 4: Handoff and Human Review

- **Action:** Present the context policy with budget table and request approval before enforcement.
- **Input:** Completed policy.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero runtime config changed by this skill.

## 4. Output Specification

```markdown
# Context Policy

- **Map:** [Source-of-truth pointer file]
- **Budget:** [Per-turn caps per source with headroom]
- **Compaction:** [Triggers, summary format, decision retention]
- **Memory:** [Hot and cold tiers with retrieval hooks]
```

## 5. Validation Gate

- [ ] Map resolves before deep reads.
- [ ] Budget totals within window with headroom.
- [ ] Compaction preserves decision history.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before enforcement.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Pasting full files into context without a map or budget.
- **Over-execution threshold:** Rewriting runtime configs or memory stores unprompted.
- **Calibration default:** Load the smallest sufficient context; expand only on evidence of need.

## 7. Anti-Pattern Compliance

| Step | Prevents AP             | Mechanism                              |
| ---- | ----------------------- | -------------------------------------- |
| 1    | AP-16 (context dump)    | Enforces map-first loading discipline. |
| 2    | AP-31 (token bloat)     | Caps tokens per turn with headroom.    |
| 3    | AP-18 (stale state)     | Retains decisions across compaction.   |
| 4    | AP-45 (no human review) | Halts for approval before enforcement. |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Context Steward role, role source, and seniority bar.
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

**Input:** "Our coding agent forgets the plan after 40 tool calls."
**Output:** Context policy with map file, per-turn budget, checkpoint summaries every 10 steps, and retained decision log.
