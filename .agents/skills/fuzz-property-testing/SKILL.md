---
name: fuzz-property-testing
description: Property-based and fuzz testing rules covering invariant properties, generator design, coverage-guided fuzzing, and crash triage. Excludes penetration testing.
department: quality
ownerAgent: merry
triggerCommand: /fuzz-property-testing
antiPatternsPrevented:
  - AP-1
  - AP-3
  - AP-6
  - AP-26
  - AP-28
---

# Fuzz Property Testing

## 0. Identity

- **Role:** Test Strategist. Owns edge-case coverage with property invariants and fuzz corpora.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Test Strategist).
- **Seniority bar:** Staff (Appendix B). Records why properties beat examples (invariants hold across inputs, rejected hand-picked cases), why shrinking beats raw crashes (minimal repros fix fast, rejected megabyte dumps), and why corpora persist across runs.
- **Authority:** Tier-5 normative skill for `skills/quality/fuzz-property-testing/`. Owns property and fuzz guidance.
- **Must not define:** Penetration testing or security exploit development.
- **Normative base:** `core/fellowship/merry.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-3 (no success criteria), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Produce property suites and fuzz harnesses with shrinking corpora and triage flow.              |
| 2   | Target Tool      | fast-check, Hypothesis, proptest, libFuzzer, AFL++, Jazzer.                                    |
| 3   | Output Format    | Property plan with invariants, generators, corpora, and triage notes.                          |
| 4   | Constraints      | Properties over examples. Shrinking mandatory. Zero em dashes. Time-boxed runs.                |
| 5   | Input            | Invariant candidates, input domains, parser surfaces, time budget.                              |
| 6   | Context          | Prevents edge-case escapes that example tests never imagine.                                    |
| 7   | Audience         | Engineers testing parsers, serializers, and stateful logic.                                     |
| 8   | Success Criteria | Invariants hold across generated inputs; crashes triaged; plan approved.                        |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger                                      | Fire? | Notes                              |
| -------------------------------------------- | ----- | ---------------------------------- |
| "Property-test our parser"                   | YES   | Core trigger.                      |
| "Fuzz our file format handling"              | YES   | Core trigger.                      |
| "/fuzz-property-testing"                     | YES   | Slash command trigger.             |
| "Pentest our login flow"                     | NO    | Route to `pentest-planner`.        |
| "Write example unit tests"                   | NO    | Route to `write-a-test`.           |

## 3. Execution Workflow

### Step 1: State Invariants as Properties

- **Action:** Express round-trips, idempotence, ordering, and metamorphic relations as checkable properties per target.
- **Input:** Invariant candidates from user.
- **Stop Condition:** Halt when properties restate examples; require invariants.
- **Validation:** Property list reviewed per target.

### Step 2: Generate and Shrink Inputs

- **Action:** Build generators covering valid plus malformed inputs, wire shrinking to minimal repros, and seed corpora from real traffic plus regressions.
- **Input:** Input domains from Step 1.
- **Stop Condition:** Halt on example-only generators; require generators.
- **Validation:** Generator review complete with shrink proof.

### Step 3: Fuzz with Triage Discipline

- **Action:** Run coverage-guided fuzzing time-boxed per target, deduplicate crashes by stack, file issues with repros, and persist corpora across runs.
- **Input:** Harnesses from Step 2.
- **Stop Condition:** Halt on untriaged crash piles; require filing.
- **Validation:** Triage log reviewed per crash class.

### Step 4: Handoff and Human Review

- **Action:** Present the property plan and request approval before wiring CI.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero suites wired by this skill.

## 4. Output Specification

```markdown
# Property Plan

- **Invariants:** [Properties per target]
- **Generators:** [Domains with shrink]
- **Triage:** [Crash workflow]
```

## 5. Validation Gate

- [ ] Invariants stated per target.
- [ ] Generators shrink to minimal.
- [ ] Crashes triaged with repros.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before wiring.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Fuzzing without stated invariants.
- **Over-execution threshold:** Weaponizing crashes unprompted.
- **Calibration default:** Properties first; fuzzing second.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-3 (no success)      | States invariants first.                            |
| 2    | AP-26 (no scope)       | Bounds generators per domain.                       |
| 3    | AP-28 (no stop)        | Time-boxes runs with triage.                        |
| 4    | AP-45 (no human review)| Halts for approval before wiring.                   |

## 8. Versioning & Changelog

- **Version:** 1.0.0
- **Changelog:**
  - `1.0.0` (2026-09-26) - Initial release closing the edge-case gap.

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

**Input:** "Our CSV importer crashes on weird files monthly."
**Output:** Plan with round-trip properties, malformed generators, and triaged crash corpus.
