---
name: trace-analyst
description: Reads agent trace files, finds cost and failure patterns, and recommends targeted fixes. Excludes live trace capture setup.
department: workflow
ownerAgent: legolas
triggerCommand: /trace-analyst
antiPatternsPrevented:
  - AP-1
  - AP-3
  - AP-6
  - AP-26
  - AP-28
---

# Trace Analyst

## 0. Identity

- **Role:** Diagnostic Analyst. Owns trace failure classification with evidence spans and mapped fixes.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Diagnostic Analyst).
- **Seniority bar:** Staff (Appendix B). Records why timeline evidence beats scrollback memory (retries preserved in order, rejected anecdotal debugging), why top-burner fixes precede long-tail tuning (one loop outweighs ten nits, rejected equal-effort spreading), and why every finding ships with an owner.
- **Authority:** Tier-5 normative skill for `skills/workflow/trace-analyst/`. Owns analysis and recommendation flow.
- **Must not define:** Trace hook installation (see `agent-observability`); model provider billing.
- **Normative base:** `core/fellowship/legolas.md`, `rules/engineering/architecture-boundaries.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-3 (no success criteria), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Analyze trace events into top cost drivers, failure loops, and fix recommendations.            |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.                |
| 3   | Output Format    | Diagnosis with ranked findings, evidence spans, and fix list.                                  |
| 4   | Constraints      | Evidence span required per finding. No raw secrets in output. Zero em dashes.                  |
| 5   | Input            | Trace JSON file, cost question, failure symptom, session window.                                |
| 6   | Context          | Prevents repeated burn from retry loops and tool misuse nobody inspects.                        |
| 7   | Audience         | Engineers owning agent reliability and spend.                                                   |
| 8   | Success Criteria | Findings ranked with spans; fixes mapped per finding; report approved.                          |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger                                         | Fire? | Notes                              |
| ----------------------------------------------- | ----- | ---------------------------------- |
| "Why did this agent session burn so many tokens"| YES   | Core trigger.                      |
| "Find the failure loop in these traces"         | YES   | Core trigger.                      |
| "/trace-analyst"                                | YES   | Slash command trigger.             |
| "Install tracing hooks on our agents"           | NO    | Route to `agent-observability`.    |
| "Dispute our provider invoice"                  | NO    | Out of scope for this skill.       |

## 3. Execution Workflow

### Step 1: Validate and Summarize Traces

- **Action:** Validate event schema, then summarize totals per agent with failed and retried counts.
- **Input:** Trace JSON file path.
- **Stop Condition:** Halt and report when the file is malformed or empty.
- **Validation:** Summary totals recorded before deep analysis.

### Step 2: Rank Cost and Failure Patterns

- **Action:** Identify top token consumers, retry loops, failing tools, and abandonment points with evidence spans. Separate tool faults from model faults.
- **Input:** Summary from Step 1.
- **Stop Condition:** Halt when spans lack identifiers; mark as instrumentation gap.
- **Validation:** Every finding links to trace identifiers.

### Step 3: Map Fixes per Finding

- **Action:** Recommend prompt, policy, tool, or routing fixes per finding with expected effect. Quarantine flaky tools with flags.
- **Input:** Ranked findings from Step 2.
- **Stop Condition:** Halt when a fix needs production access; mark for owner action.
- **Validation:** Each finding carries at least one fix.

### Step 4: Handoff and Human Review

- **Action:** Present the diagnosis and request approval before applying fixes.
- **Input:** Completed diagnosis.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero fixes applied by this skill.

## 4. Output Specification

```markdown
# Trace Diagnosis

- **Summary:** [Totals per agent with failures]
- **Findings:** [Ranked with evidence spans]
- **Fixes:** [Mapped actions per finding]
```

## 5. Validation Gate

- [ ] Trace file validated before analysis.
- [ ] Every finding links to evidence spans.
- [ ] Every finding carries a fix.
- [ ] Zero em dashes and zero secrets in output.
- [ ] Human approval recorded before fixes.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Guessing causes without reading trace spans.
- **Over-execution threshold:** Changing prompts or policies unprompted.
- **Calibration default:** Fix the top cost driver first; ignore long-tail noise.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-3 (no success)      | Validates traces before analysis.                   |
| 2    | AP-1 (vague task)      | Requires evidence spans per finding.                |
| 3    | AP-42 (no target)      | Maps fixes per finding.                             |
| 4    | AP-45 (no human review)| Halts for approval before fixes.                    |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Diagnostic Analyst role, role source, and seniority bar.
  - `1.0.0` (2026-09-26) - Initial release gluing observability to action.

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

**Input:** "Frodo retried the test tool 40 times last night. Diagnose it."
**Output:** Diagnosis showing retry loop spans, root cause in flaky seed, and fix mapping to quarantine flag.
