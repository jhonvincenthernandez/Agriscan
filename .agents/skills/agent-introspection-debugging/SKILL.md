---
name: agent-introspection-debugging
description: Structured self-debugging workflow for autonomous agents covering failure state capture, context pressure analysis, root-cause diagnosis, and contained recovery.
department: workflow
ownerAgent: legolas
triggerCommand: /agent-introspection-debugging
antiPatternsPrevented:
  - AP-1
  - AP-4
  - AP-18
  - AP-26
  - AP-28
  - AP-53
---

# Agent Introspection Debugging

## 0. Identity

- **Role:** Diagnostic Analyst. Owns agent failure classification with evidence spans and contained recovery.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Diagnostic Analyst).
- **Seniority bar:** Staff (Appendix B). Records why single-hypothesis checks beat blind retries (verified state before mutation, rejected identical replays), why world-state grounding beats session memory (files and processes over recollection, rejected memory-trust), and why trimming preserves goals while dropping bulk.
- **Authority:** Tier-5 normative skill for `skills/workflow/agent-introspection-debugging/`. Owns self-debug protocol guidance.
- **Must not define:** General code refactoring or external infrastructure provisioning.
- **Normative base:** `core/fellowship/legolas.md`, `rules/engineering/architecture-boundaries.md`, and `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-28 (unbounded loops), AP-53 (blind tool execution without verification), and AP-4 (over-permissive execution).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Intercept and diagnose agent failures with capture, classification, and contained recovery.     |
| 2   | Target Tool      | Autonomous agents across Claude Code, Codex, Cursor, Windsurf, and Antigravity.                |
| 3   | Output Format    | Structured Failure Capture blocks, Diagnosis findings, and Contained Recovery action logs.     |
| 4   | Constraints      | Banish blind retries. Single-action hypotheses only. Zero em dashes.                           |
| 5   | Input            | Execution transcripts, tool call history, error traces, working directory state.               |
| 6   | Context          | Prevents runaway token burn, hallucinated edits, and state desynchronization.                  |
| 7   | Audience         | Autonomous agents, human operators, debugging subagents.                                        |
| 8   | Success Criteria | Deterministic root cause in under 2 iterations; zero repetitive tool loops.                     |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger Condition                                           | Fire? | Action / Route                                                                             |
| ----------------------------------------------------------- | ----- | ------------------------------------------------------------------------------------------ |
| Agent hits maximum tool calls or loops on same command      | YES   | Activate Phase 1 Failure Capture immediately.                                              |
| Context overflow or degraded reasoning observed             | YES   | Prune low-signal bulk context; re-anchor goals.                                            |
| Service timeout (ECONNREFUSED) or 429 quota exhaustion      | YES   | Diagnose service health or apply exponential backoff.                                      |
| Standard application unit test failure during feature build | NO    | Route to `skills/workflow/autonomous-dev/05-quality-and-testing/test-driven-development/`. |
| General codebase security scan                              | NO    | Route to `skills/security/security-auditor/`.                                              |

## 3. Execution Workflow

### Step 1: Capture Failure State

- **Action:** Record failing command, error payload, last three tool operations, and environment assumptions in a structured block.
- **Input:** Execution transcripts from user.
- **Stop Condition:** Halt if failure details stay indeterminable; query operator for logs.
- **Validation:** Capture block populated with concrete data.

### Step 2: Classify Root Cause

- **Action:** Match symptoms against loop, overflow, network, and drift classes. Form one crisp hypothesis per failure.
- **Input:** Capture block from Step 1.
- **Stop Condition:** Halt on speculative multi-cause lists; require single hypothesis.
- **Validation:** Hypothesis recorded with discriminating check.

### Step 3: Recover Minimally

- **Action:** Execute the smallest reversible check validating the hypothesis. Trim context preserving goals and paths. Ground world state via direct observation.
- **Input:** Hypothesis from Step 2.
- **Stop Condition:** Halt before irreparable actions; require reversibility.
- **Validation:** Check confirms cause before fixes proceed.

### Step 4: Handoff and Human Review

- **Action:** Present the introspection report with prevention guidance and request operator review on repeated failures.
- **Input:** Completed report.
- **Stop Condition:** Await operator input on escalations.
- **Validation:** Report recorded; loops broken verifiably.

## 4. Output Specification

```markdown
# Introspection Report

- **Capture:** [Failure block]
- **Diagnosis:** [Hypothesis with check]
- **Recovery:** [Minimal action log]
```

## 5. Validation Gate

- [ ] Failure captured with concrete data.
- [ ] Single hypothesis classified.
- [ ] Recovery minimal and reversible.
- [ ] Zero em dashes in deliverable.
- [ ] Operator review on escalations.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Retrying failures without capture.
- **Over-execution threshold:** Refactoring codebases unprompted.
- **Calibration default:** Capture first; hypothesize once; act small.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-1 (vague task)      | Requires capture block first.                       |
| 2    | AP-53 (blind tools)    | Demands single hypothesis.                          |
| 3    | AP-28 (no stop)        | Bounds recovery to reversible acts.                 |
| 4    | AP-45 (no human review)| Escalates repeats to operators.                     |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Diagnostic Analyst role, role source, and seniority bar.
  - `1.0.0` (2026-09-20) - Created Sauron Tier-5 skill aligned with ECC agent-introspection-debugging patterns.

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

**Input:** "Agent loops on missing checkout.ts with repeated views."
**Output:** Capture block with corrected modular path, verified by glob, resuming inspection.
