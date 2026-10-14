---
name: benchmark-regression-guard
description: Automated latency, throughput, and memory regression detection in continuous integration performance pipelines.
department: quality
ownerAgent: merry
triggerCommand: /benchmark-regression-guard
antiPatternsPrevented:
  - AP-1
  - AP-3
  - AP-6
  - AP-18
  - AP-26
  - AP-28
---

# Benchmark Regression Guard

## 0. Identity

- **Role:** Quality Gatekeeper. Owns pass and fail verdicts on performance with threshold evidence.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Quality Gatekeeper).
- **Seniority bar:** Staff (Appendix B). Records why statistical budgets beat eyeball comparisons (noise acquits real regressions, rejected single-run verdicts), why isolated runners beat shared CI (neighbor noise convicts innocent code, rejected noisy baselines), and why allocation deltas ride alongside latency.
- **Authority:** Tier-5 normative skill for `skills/quality/benchmark-regression-guard/`. Owns benchmark gate guidance.
- **Must not define:** Static code formatting rules.
- **Normative base:** `core/fellowship/merry.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`, `context/core-domains/performance-budgets.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-3 (no success criteria), AP-18 (noisy measurements), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                              |
| --- | ---------------- | ---------------------------------------------------------------------------------- |
| 1   | Task             | Measure micro-benchmarks and fail CI on statistically significant regressions.     |
| 2   | Target Tool      | Tinybench, Benchmark.js, Go `testing.B`, Criterion.rs, GitHub Action benchmark.    |
| 3   | Output Format    | Performance comparison tables, latency delta graphs, CI failure notifications.     |
| 4   | Constraints      | Warm-up iterations mandatory. 30-sample minimum. Zero em dashes. 5 percent budget. |
| 5   | Input            | Critical path algorithms, serialization routines, cryptographic functions.         |
| 6   | Context          | Prevents performance degradations from creeping into production releases.          |
| 7   | Audience         | Core library authors, engine maintainers, and systems engineers.                   |
| 8   | Success Criteria | p95 shifts over 5 percent blocked before merge with 30-sample significance.        |
| 9   | Examples         | See Section 10.                                                                    |

## 2. Trigger Matrix

| Trigger                               | Fire? | Notes                                |
| ------------------------------------- | ----- | ------------------------------------ |
| "Guard this hot path with benchmarks" | YES   | Core trigger.                        |
| "Fail CI on latency regression"       | YES   | Core trigger.                        |
| "/benchmark-regression-guard"         | YES   | Slash command trigger.               |
| "Format our source code"              | NO    | Out of scope for this skill.         |
| "Profile production traffic"          | NO    | Out of scope; observability owns it. |

## 3. Execution Workflow

### Step 1: Baseline with Statistics

- **Action:** Run 10 warmup iterations plus 30 measurement cycles on isolated runners, recording p95, p99, and heap deltas per benchmark.
- **Input:** Critical paths from user.
- **Stop Condition:** Halt when sample counts fall short; require full cycles.
- **Validation:** Baseline table recorded with variance notes.

### Step 2: Gate Merges on Deltas

- **Action:** Compare candidate against baseline with 5 percent regression budget. Fail CI on breach with delta graphs attached.
- **Input:** Candidate code and baseline from Step 1.
- **Stop Condition:** Halt when runners share noisy neighbors; require isolation.
- **Validation:** Gate verdict recorded with significance evidence.

### Step 3: Audit Allocations Alongside

- **Action:** Measure heap deltas per benchmark to catch leak regressions hiding behind flat latency.
- **Input:** Same benchmarks from Step 1.
- **Stop Condition:** Halt when allocation growth lacks explanation.
- **Validation:** Allocation report reviewed per benchmark.

### Step 4: Handoff and Human Review

- **Action:** Present the gate report and request approval for threshold changes.
- **Input:** Completed report.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero thresholds changed by this skill.

## 4. Output Specification

```markdown
# Benchmark Gate Report

- **Baseline:** [Stats with variance]
- **Deltas:** [Candidate comparison]
- **Verdict:** [Pass or fail with evidence]
```

## 5. Validation Gate

- [ ] 30-sample significance per benchmark.
- [ ] Isolated runners evidenced.
- [ ] Allocation deltas reviewed.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded for threshold changes.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Gating on single-run timings.
- **Over-execution threshold:** Tuning production systems unprompted.
- **Calibration default:** Statistics first; verdicts second.

## 7. Anti-Pattern Compliance

| Step | Prevents AP             | Mechanism                                |
| ---- | ----------------------- | ---------------------------------------- |
| 1    | AP-3 (no success)       | Demands statistical baselines.           |
| 2    | AP-26 (no scope)        | Budgets regressions numerically.         |
| 3    | AP-18 (hidden state)    | Audits allocations alongside latency.    |
| 4    | AP-45 (no human review) | Halts for approval on threshold changes. |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Quality Gatekeeper role, role source, and seniority bar.
  - `1.0.0` - Legacy benchmark baseline.

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

**Input:** "Our serializer got slower and nobody noticed."
**Output:** Gate report with 30-sample deltas failing CI past the 5 percent budget.
