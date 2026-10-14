---
name: pact-contract-testing
description: Consumer-driven API contract verification, pact broker publishing, and verification gates across microservice boundaries.
department: quality
ownerAgent: merry
triggerCommand: /pact-contract-testing
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-18
  - AP-26
  - AP-28
---

# Pact Contract Testing

## 0. Identity

- **Role:** Quality Gatekeeper. Owns deploy verdicts on contract compatibility with broker evidence.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Quality Gatekeeper).
- **Seniority bar:** Staff (Appendix B). Records why consumer-driven contracts beat provider-assumed compatibility (expectations live with callers, rejected handshake hope), why broker gates beat E2E suites for compatibility (cheap per deploy, rejected heavy integration runs), and why state handlers beat static fixtures.
- **Authority:** Tier-5 normative skill for `skills/quality/pact-contract-testing/`. Owns contract lifecycle guidance.
- **Must not define:** Internal service unit test implementations.
- **Normative base:** `core/fellowship/merry.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`, `context/core-domains/api-contracts.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-18 (untested boundaries), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Define consumer expectations, generate pacts, and verify providers before release.             |
| 2   | Target Tool      | Pact-JS, Pact-JVM, Pact Broker, Can-I-Deploy CLI.                                              |
| 3   | Output Format    | Contract JSON files, provider state handlers, and verification reports.                        |
| 4   | Constraints      | Consumers dictate expectations. Providers verify pre-release. Zero em dashes.                  |
| 5   | Input            | API endpoints, mock interactions, provider states.                                             |
| 6   | Context          | Prevents breaking API changes across independent microservices without expensive E2E suites.   |
| 7   | Audience         | Backend engineers, integration teams, and platform architects.                                  |
| 8   | Success Criteria | can-i-deploy green for all service versions in pipeline.                                       |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger                                      | Fire? | Notes                              |
| -------------------------------------------- | ----- | ---------------------------------- |
| "Contract-test our service boundaries"       | YES   | Core trigger.                      |
| "Gate deploys on compatibility"              | YES   | Core trigger.                      |
| "/pact-contract-testing"                     | YES   | Slash command trigger.             |
| "Write internal unit tests"                  | NO    | Out of scope for this skill.       |
| "Run full E2E suites instead"                | NO    | Out of scope; contracts are cheaper. |

## 3. Execution Workflow

### Step 1: Define Consumer Expectations

- **Action:** Write consumer tests with strict response matchers and status expectations per interaction.
- **Input:** API endpoints from user.
- **Stop Condition:** Halt when expectations stay loose; require matchers.
- **Validation:** Pact files generated with version tags.

### Step 2: Publish and Verify Providers

- **Action:** Publish pacts to the broker with commit SHAs, inject fixtures via state handlers, and verify providers against contracts.
- **Input:** Pact files from Step 1.
- **Stop Condition:** Halt when state handlers stay static; require dynamic fixtures.
- **Validation:** Verification matrix reviewed per service.

### Step 3: Gate Deploys on Compatibility

- **Action:** Block releases unless can-i-deploy confirms full matrix compatibility.
- **Input:** Version inventory from Step 2.
- **Stop Condition:** Halt deploys on red matrix; no overrides without owners.
- **Validation:** Gate evidence recorded per deploy.

### Step 4: Handoff and Human Review

- **Action:** Present the verification report and request approval for gate changes.
- **Input:** Completed report.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero gates changed by this skill.

## 4. Output Specification

```markdown
# Contract Report

- **Pacts:** [Consumer expectations]
- **Verification:** [Provider matrix]
- **Gate:** [Deploy verdicts]
```

## 5. Validation Gate

- [ ] Expectations strict with matchers.
- [ ] Broker holds versioned pacts.
- [ ] Deploys gated on green matrix.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded for gate changes.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Deploying without contract verification.
- **Over-execution threshold:** Writing service unit tests unprompted.
- **Calibration default:** Contracts per boundary; E2E for journeys only.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-1 (vague task)      | Requires strict expectations first.                 |
| 2    | AP-26 (no scope)       | Versions pacts per deploy.                          |
| 3    | AP-28 (no stop)        | Gates deploys on matrix.                            |
| 4    | AP-45 (no human review)| Halts for approval on gate changes.                 |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Quality Gatekeeper role, role source, and seniority bar.
  - `1.0.0` - Legacy contract baseline.

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

**Input:** "Our user service breaks the frontend on every deploy."
**Output:** Consumer pacts with broker verification gating deploys on green matrix.
