---
name: kubernetes-operator-deployment
description: Architects Kubernetes operators with idempotent reconcilers, status decoupling, finalizers, and leader election. Excludes application domain logic.
department: devops
ownerAgent: gimli
triggerCommand: /kubernetes-operator-deployment
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-18
  - AP-26
  - AP-28
---

# Kubernetes Operator Deployment

## 0. Identity

- **Role:** Release Engineer. Owns operator packaging with convergent reconciliation and safe lifecycle.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Release Engineer).
- **Seniority bar:** Staff (Appendix B). Records why idempotent reconcilers beat event handlers (same input same state regardless of count, rejected fire-once logic), why status decoupling beats combined writes (version conflicts vanish, rejected coupled updates), and why leader election beats replica races.
- **Authority:** Tier-5 normative skill for `skills/devops/kubernetes-operator-deployment/`. Owns CRD and controller guidance.
- **Must not define:** Application-layer domain logic.
- **Normative base:** `core/fellowship/gimli.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-18 (crash loops), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Produce operators with convergent reconcilers and safe lifecycle handling.                     |
| 2   | Target Tool      | Operator SDK, Kubebuilder, Go controller-runtime, Helm.                                        |
| 3   | Output Format    | CRD manifests, controller specs, RBAC bindings, and lifecycle notes.                           |
| 4   | Constraints      | Reconcilers idempotent. Spec and status decoupled. Zero em dashes.                             |
| 5   | Input            | Cluster version, resource specs, reconciliation objectives.                                     |
| 6   | Context          | Prevents state drift, crash loops, and cascading evictions.                                     |
| 7   | Audience         | SREs, platform engineers, and Kubernetes operators.                                             |
| 8   | Success Criteria | Clean reconciliation; safe CRD migrations; plan approved before coding.                         |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger                                      | Fire? | Notes                              |
| -------------------------------------------- | ----- | ---------------------------------- |
| "Build an operator for our database"         | YES   | Core trigger.                      |
| "Fix reconciler crash loops"                 | YES   | Core trigger.                      |
| "/kubernetes-operator-deployment"            | YES   | Slash command trigger.             |
| "Write application domain logic"             | NO    | Out of scope for this skill.       |
| "Author Dockerfiles"                         | NO    | Route to `docker-principles`.      |

## 3. Execution Workflow

### Step 1: Model Resources and RBAC

- **Action:** Define CRDs with OpenAPI validation, scoped RBAC bindings, and versioned storage.
- **Input:** Resource specs and cluster version.
- **Stop Condition:** Halt when RBAC stays cluster-wide without justification.
- **Validation:** CRD schema reviewed with least-privilege bindings.

### Step 2: Write Convergent Reconcilers

- **Action:** Implement idempotent reconcile loops with status subresource separation, finalizers for external cleanup, and leader election across replicas.
- **Input:** Reconciliation objectives from Step 1.
- **Stop Condition:** Halt when reconcilers assume single execution; require idempotency.
- **Validation:** Reconciler reviewed for repeat-safety and cleanup paths.

### Step 3: Plan CRD Migrations

- **Action:** Sequence version upgrades with conversion strategies and rollback notes per version.
- **Input:** Version inventory from user.
- **Stop Condition:** Halt when migration lacks rollback; require one.
- **Validation:** Migration plan reviewed with conversion evidence.

### Step 4: Handoff and Human Review

- **Action:** Present the operator plan and request approval before coding.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero code written by this skill.

## 4. Output Specification

```markdown
# Operator Plan

- **Resources:** [CRDs with RBAC]
- **Reconcilers:** [Idempotent loops with finalizers]
- **Migrations:** [Version path with rollback]
```

## 5. Validation Gate

- [ ] CRDs validated with scoped RBAC.
- [ ] Reconcilers idempotent with cleanup.
- [ ] Migrations carry rollback notes.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before coding.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Writing controllers without idempotency proof.
- **Over-execution threshold:** Deploying operators to live clusters unprompted.
- **Calibration default:** Converge always; assume repeated execution.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-1 (vague task)      | Requires resource model first.                      |
| 2    | AP-26 (no scope)       | Forces idempotent reconcilers.                      |
| 3    | AP-28 (no stop)        | Demands migration rollback.                         |
| 4    | AP-45 (no human review)| Halts for approval before coding.                   |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Release Engineer role, role source, and seniority bar.
  - `1.0.0` - Legacy operator baseline.

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

**Input:** "Our database operator crash-loops on version upgrades."
**Output:** Operator plan with idempotent reconciler, status decoupling, and versioned migration path.
