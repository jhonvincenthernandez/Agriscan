---
name: test-data-management
description: Test data strategy rules covering factories, ephemeral environments, PII-safe datasets, and seed versioning. Excludes production data pipelines.
department: quality
ownerAgent: samwise
triggerCommand: /test-data-management
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-26
  - AP-28
  - AP-44
---

# Test Data Management

## 0. Identity

- **Role:** State Keeper. Owns test data integrity with versioned, privacy-safe datasets.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (State Keeper).
- **Seniority bar:** Staff (Appendix B). Records why factories beat shared fixtures (isolation per test, rejected order-dependent suites), why ephemeral environments beat shared staging (no cross-talk, rejected flaky shared DBs), and why synthetic data beats production dumps.
- **Authority:** Tier-5 normative skill for `skills/quality/test-data-management/`. Owns test data guidance.
- **Must not define:** Production data pipelines or analytics warehouses.
- **Normative base:** `core/fellowship/samwise.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-26 (no scope boundary), AP-28 (no stop condition), and AP-44 (leaked PII).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Produce test data strategy with factories, environments, privacy rules, and seed versions.     |
| 2   | Target Tool      | Factory libraries, Testcontainers, ephemeral preview envs, PII vaults.                          |
| 3   | Output Format    | Data plan with factory map, environment matrix, and privacy notes.                             |
| 4   | Constraints      | Factories over fixtures. Ephemeral over shared. Zero em dashes. No production PII.             |
| 5   | Input            | Domain models, environment inventory, compliance needs, seed requirements.                      |
| 6   | Context          | Prevents flaky shared-state suites and PII leaks into test systems.                             |
| 7   | Audience         | Engineers owning test reliability and data privacy.                                             |
| 8   | Success Criteria | Factories cover domains; envs isolated; plan approved.                                          |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger                                      | Fire? | Notes                              |
| -------------------------------------------- | ----- | ---------------------------------- |
| "Fix our shared staging flakiness"           | YES   | Core trigger.                      |
| "Seed PII-safe test datasets"                | YES   | Core trigger.                      |
| "/test-data-management"                      | YES   | Slash command trigger.             |
| "Build our analytics warehouse"              | NO    | Out of scope for this skill.       |
| "Dump production data for tests"             | NO    | Refused; synthetic only.           |

## 3. Execution Workflow

### Step 1: Factory-ize Domains

- **Action:** Build factories per domain with explicit traits and sequences. Ban shared mutable fixtures across tests.
- **Input:** Domain models from user.
- **Stop Condition:** Halt on fixture sharing; require factories.
- **Validation:** Factory map reviewed per domain.

### Step 2: Isolate Environments

- **Action:** Provision ephemeral environments per run with containerized dependencies and seeded baselines. Version seeds alongside schema migrations.
- **Input:** Environment inventory from Step 1.
- **Stop Condition:** Halt on shared staging for tests; require isolation.
- **Validation:** Environment matrix reviewed with seed versions.

### Step 3: Scrub Privacy Ruthlessly

- **Action:** Generate synthetic PII-shaped data, vault real secrets out of test systems, and audit datasets for production leakage.
- **Input:** Compliance needs from user.
- **Stop Condition:** Halt on production dumps in tests.
- **Validation:** Privacy audit clean with evidence.

### Step 4: Handoff and Human Review

- **Action:** Present the data plan and request approval before rollout.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero rollouts performed by this skill.

## 4. Output Specification

```markdown
# Data Plan

- **Factories:** [Per-domain map]
- **Environments:** [Ephemeral matrix]
- **Privacy:** [Scrub audit]
```

## 5. Validation Gate

- [ ] Factories cover domains.
- [ ] Environments isolated per run.
- [ ] Privacy audit clean.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before rollout.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Testing against shared staging.
- **Over-execution threshold:** Copying production data unprompted.
- **Calibration default:** Synthetic first; ephemeral always.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-1 (vague task)      | Requires factory map first.                         |
| 2    | AP-26 (no scope)       | Isolates envs per run.                              |
| 3    | AP-44 (leaked PII)     | Scrubs with audit evidence.                         |
| 4    | AP-45 (no human review)| Halts for approval before rollout.                  |

## 8. Versioning & Changelog

- **Version:** 1.0.0
- **Changelog:**
  - `1.0.0` (2026-09-26) - Initial release closing the test-data gap.

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

**Input:** "Tests flake on shared staging and use real emails."
**Output:** Plan with domain factories, ephemeral envs, and synthetic PII datasets.
