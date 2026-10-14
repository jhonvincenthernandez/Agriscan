---
name: chaos-engineering
description: Chaos experiment rules covering steady-state hypotheses, blast-radius phasing, kill switches, and verdict loops. Excludes unscoped production fault injection.
department: quality
ownerAgent: pippin
triggerCommand: /chaos-engineering
antiPatternsPrevented:
  - AP-1
  - AP-4
  - AP-6
  - AP-26
  - AP-28
---

# Chaos Engineering

## 0. Identity

- **Role:** Edge Prober. Owns boundary findings with reproduced steady-state verdicts.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Edge Prober).
- **Seniority bar:** Staff (Appendix B). Records why hypotheses precede faults (science over sabotage, rejected random destruction), why blast radius phases widen gradually (one pod before one zone, rejected AZ-first bravado), and why kill switches gate every run.
- **Authority:** Tier-5 normative skill for `skills/quality/chaos-engineering/`. Owns experiment design guidance.
- **Must not define:** Unscoped production fault injection.
- **Normative base:** `core/fellowship/pippin.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-4 (over-permissive blast), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                |
| --- | ---------------- | ------------------------------------------------------------------------------------ |
| 1   | Task             | Produce chaos experiments with hypotheses, phased blast radius, and verdict loops.   |
| 2   | Target Tool      | LitmusChaos, Chaos Mesh, Gremlin, Toxiproxy, AWS FIS, Azure Chaos Studio.            |
| 3   | Output Format    | Experiment plan with hypothesis, blast phases, and verdict template.                 |
| 4   | Constraints      | Steady state quantified. Kill switch mandatory. Zero em dashes. Business hours only. |
| 5   | Input            | Service map, SLOs, failure history, drill calendar.                                  |
| 6   | Context          | Prevents untested resilience assumptions failing on incident day.                    |
| 7   | Audience         | SREs running controlled failure experiments.                                         |
| 8   | Success Criteria | Hypothesis falsifiable; blast phased; plan approved.                                 |
| 9   | Examples         | See Section 10.                                                                      |

## 2. Trigger Matrix

| Trigger                               | Fire? | Notes                          |
| ------------------------------------- | ----- | ------------------------------ |
| "Prove our failover actually works"   | YES   | Core trigger.                  |
| "Run a game day on payments"          | YES   | Core trigger.                  |
| "/chaos-engineering"                  | YES   | Slash command trigger.         |
| "Kill production to see what happens" | NO    | Refused; phased plan required. |
| "Skip staging and test live first"    | NO    | Refused; stage first.          |

## 3. Execution Workflow

### Step 1: Quantify Steady State

- **Action:** Define measurable outputs (throughput, error rates, latency percentiles) with dashboards named per metric.
- **Input:** SLOs from user.
- **Stop Condition:** Halt when steady state stays verbal; require numbers.
- **Validation:** Baseline recorded with sources.

### Step 2: Hypothesize and Phase Blast

- **Action:** Write falsifiable hypotheses per fault, phase blast from one pod upward, and attach alarm-based kill switches plus manual abort paths.
- **Input:** Failure history from Step 1.
- **Stop Condition:** Halt on missing kill switches; mark as blocking.
- **Validation:** Experiment reviewed with abort proof.

### Step 3: Run, Verdict, Widen

- **Action:** Execute in staging first, record held-or-broken verdicts with metric deltas, fix findings, then widen phases only on green runs.
- **Input:** Approved experiment from Step 2.
- **Stop Condition:** Halt widening on broken verdicts.
- **Validation:** Verdict log reviewed per phase.

### Step 4: Handoff and Human Review

- **Action:** Present the experiment plan and request approval before any fault injection.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero faults injected by this skill.

## 4. Output Specification

```markdown
# Chaos Plan

- **Steady:** [Quantified baseline]
- **Blast:** [Phased scope with kills]
- **Verdicts:** [Held or broken log]
```

## 5. Validation Gate

- [ ] Steady state quantified.
- [ ] Blast phased with kill switches.
- [ ] Verdicts recorded per run.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before injection.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Injecting faults without hypotheses.
- **Over-execution threshold:** Widening blast on broken verdicts.
- **Calibration default:** One pod first; zones last.

## 7. Anti-Pattern Compliance

| Step | Prevents AP             | Mechanism                            |
| ---- | ----------------------- | ------------------------------------ |
| 1    | AP-1 (vague task)       | Demands quantified steady state.     |
| 2    | AP-4 (over-permissive)  | Phases blast with kills.             |
| 3    | AP-28 (no stop)         | Gates widening on verdicts.          |
| 4    | AP-45 (no human review) | Halts for approval before injection. |

## 8. Versioning & Changelog

- **Version:** 1.0.0
- **Changelog:**
  - `1.0.0` (2026-09-26) - Initial release closing the resilience-proof gap.

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

**Input:** "Nobody knows if our failover works until real outages."
**Output:** Plan with steady-state hypothesis, phased blast, kill switches, and verdict loop.
