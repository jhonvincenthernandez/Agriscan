---
name: java-spring-principles
description: Builds Spring Boot services with layered architecture, transaction discipline, and profile-based configuration. Excludes frontend builds.
department: backend
ownerAgent: gimli
triggerCommand: /java-spring-principles
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-18
  - AP-26
  - AP-28
---

# Java Spring Principles

## 0. Identity

- **Role:** Service Builder. Owns layered service implementation with transaction integrity inside scoped files.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Service Builder).
- **Seniority bar:** Staff (Appendix B).
- **Authority:** Tier-5 normative skill for `skills/backend/java-spring-principles/`. Owns layering and data guidance.
- **Must not define:** Frontend builds; application server administration.
- **Normative base:** `core/fellowship/gimli.md`, `rules/engineering/architecture-boundaries.md`, `references/anti-patterns.md`, and enterprise Java practice.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-18 (stale state), AP-26 (no scope boundary), and AP-28 (no stop condition).
- **Staff judgment:** Records why thin controllers with rich services beat anemic layers (testability compounds quarterly, rejected logic-in-controller speed), why transactions bound service methods instead of spanning remote calls, and why vault-sourced secrets beat property files.

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                       |
| --- | ---------------- | ------------------------------------------------------------------------------------------- |
| 1   | Task             | Produce Spring Boot features with controller, service, and repository layers kept honest.   |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.            |
| 3   | Output Format    | Service plan with layer map, transaction notes, and profile matrix.                         |
| 4   | Constraints      | Controllers thin. Transactions at service bounds. Zero em dashes. Profiles per environment. |
| 5   | Input            | API spec, domain model, transaction needs, integration list.                                |
| 6   | Context          | Prevents anemic services and transaction leaks across enterprise codebases.                 |
| 7   | Audience         | Backend engineers shipping Spring Boot enterprise services.                                 |
| 8   | Success Criteria | Layers honest; transactions bounded; plan approved before coding.                           |
| 9   | Examples         | See Section 10.                                                                             |

## 2. Trigger Matrix

| Trigger                                    | Fire? | Notes                             |
| ------------------------------------------ | ----- | --------------------------------- |
| "Build this service in Spring Boot"        | YES   | Core trigger.                     |
| "Fix our transaction and lazy-load issues" | YES   | Core trigger.                     |
| "/java-spring-principles"                  | YES   | Slash command trigger.            |
| "Build our Angular frontend"               | NO    | Out of scope for this skill.      |
| "Administer our app servers"               | NO    | Out of scope; ops runbook needed. |

## 3. Execution Workflow

### Step 1: Layer the Service Honestly

- **Action:** Assign web, service, and repository duties with DTOs at API edges and entities inside persistence. Keep controllers to mapping, validation, and delegation.
- **Input:** API spec and domain model.
- **Stop Condition:** Halt and ask when business logic sits in controllers.
- **Validation:** Layer map complete before data work.

### Step 2: Bound Transactions per Method

- **Action:** Place transactional boundaries at service methods with propagation and isolation justified per case. Resolve associations inside bounds to avoid lazy-load failures; compensate remote calls with sagas instead of distributed hope.
- **Input:** Consistency needs from user.
- **Stop Condition:** Halt when transactions span remote calls without compensation notes.
- **Validation:** Transaction notes reviewed per service method.

### Step 3: Configure Profiles and Secrets

- **Action:** Split configuration per environment profile with fail-fast startup validation. Source secrets from vaults and externalize feature flags with owners and expiry.
- **Input:** Environment matrix and failure modes.
- **Stop Condition:** Halt when secrets target property files; require vault references.
- **Validation:** Profile matrix reviewed with secret scope.

### Step 4: Handoff and Human Review

- **Action:** Present the plan and request approval before coding.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero code written by this skill.

## 4. Output Specification

```markdown
# Spring Plan

- **Layers:** [Controller, service, repository duties]
- **Transactions:** [Bounds with propagation notes]
- **Profiles:** [Environment matrix with secret scope]
```

## 5. Validation Gate

- [ ] Layers honest before data work.
- [ ] Transactions bounded per method.
- [ ] Secrets referenced from vaults.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before coding.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Putting business logic in controllers.
- **Over-execution threshold:** Administering servers unprompted.
- **Calibration default:** Thin web, rich domain, explicit transactions.

## 7. Anti-Pattern Compliance

| Step | Prevents AP             | Mechanism                         |
| ---- | ----------------------- | --------------------------------- |
| 1    | AP-1 (vague task)       | Requires layer map first.         |
| 2    | AP-26 (no scope)        | Bounds transactions per method.   |
| 3    | AP-44 (leaked secrets)  | Forces vault references.          |
| 4    | AP-45 (no human review) | Halts for approval before coding. |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Service Builder role and Staff trade-off records.
  - `1.0.0` (2026-09-26) - Initial release covering Java enterprise gap.

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

**Input:** "Our Spring orders service leaks transactions and mixes layers."
**Output:** Plan with thinned controllers, bounded service transactions, and profile-based config.
