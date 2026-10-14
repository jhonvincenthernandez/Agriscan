---
name: cicd-deployment
description: Continuous Integration and Continuous Deployment (CI/CD) standards covering fast-feedback loops, build security, artifact provenance, blue-green deployments, canary rollouts, and automated health-gated rollbacks.
department: devops
ownerAgent: gimli
triggerCommand: /cicd-deployment
antiPatternsPrevented:
  - AP-1
  - AP-4
  - AP-18
  - AP-26
  - AP-28
  - AP-44
---

# CI/CD & Progressive Deployment Principles

## 0. Identity

- **Role:** Release Engineer. Owns packaging, versioning, and rollback paths for delivery pipelines.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Release Engineer).
- **Seniority bar:** Staff (Appendix B). Records why immutable artifacts beat rebuild-per-environment (identical digests across stages, rejected recompile drift), why SHA-pinned actions beat mutable tags (supply-chain integrity, rejected latest-tag hope), and why canary gates beat big-bang deploys.
- **Authority:** Tier-5 normative skill for deployment pipelines under `skills/devops/cicd-deployment/`.
- **Must not define:** Application UI components or database table DDL.
- **Normative base:** `core/fellowship/gimli.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1 (unbounded pipeline steps), AP-4 (unverified production deployments), and AP-44 (unlocked deployment pipelines).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                                         |
| --- | ---------------- | ------------------------------------------------------------------------------------------------------------- |
| 1   | Task             | Architect, configure, and automate continuous integration, deployment pipelines, and release gates.           |
| 2   | Target Tool      | GitHub Actions, GitLab CI, ArgoCD, Tekton, Docker Buildx, Cosign, Sigstore.                                   |
| 3   | Output Format    | Declarative CI/CD pipeline workflows, deployment manifests, and automated health checks.                      |
| 4   | Constraints      | Pipeline execution under 10 minutes. Zero hardcoded secrets. Pin all actions to commit SHAs.                  |
| 5   | Input            | Git commits, pull requests, container specifications, deployment targets, health metrics.                     |
| 6   | Context          | Prevents broken builds reaching production, deployment downtime, security leaks, and manual release friction. |
| 7   | Audience         | DevOps engineers, site reliability engineers, software developers, security teams.                            |
| 8   | Success Criteria | 100 percent of PRs validated by automated CI; zero-downtime releases; automated rollback on health failure.   |
| 9   | Examples         | See Section 10.                                                                                                |

## 2. Trigger Matrix

| Trigger Condition                                                 | Fire? | Action / Route                                                     |
| ----------------------------------------------------------------- | ----- | ------------------------------------------------------------------ |
| Configuring CI pipeline for linting, testing, and building code   | YES   | Implement fast-feedback pipeline with parallelized test jobs.      |
| Deploying software releases to staging or production environments | YES   | Enforce canary or blue-green strategy with automated health gates. |
| Pipeline failure or post-deployment error rate spike              | YES   | Trigger automated rollback to previous verified artifact tag.      |
| Authoring raw container Dockerfiles                               | NO    | Route to `skills/devops/docker-principles/`.                       |

## 3. Execution Workflow

### Step 1: Static Verification and Fast Failure

- **Action:** Execute formatting checks, linter audits, and type verification first in parallel with unit tests. Cache dependency directories deterministically. Keep total CI execution under 10 minutes and halt downstream jobs on static failure.
- **Input:** Pull requests and commit SHAs.
- **Stop Condition:** Halt immediately if static checks fail; do not launch downstream build or test jobs.
- **Validation:** Clean syntax and type check execution within time budget.

### Step 2: Parallel Testing with Pinned Supply Chain

- **Action:** Run unit and integration tests across parallel matrix runners. Pin all third-party actions and base images to immutable commit SHAs or digests. Generate SBOMs and sign artifacts with Cosign.
- **Input:** Verified code from Step 1.
- **Stop Condition:** Halt when any action floats on mutable tags; require pins.
- **Validation:** Test suite green; signed container image pushed to immutable registry.

### Step 3: Immutable Promotion and Progressive Rollout

- **Action:** Build artifacts exactly once per commit SHA and promote identical digests across environments. Deploy via canary or blue-green rings with readiness and liveness probes plus graceful drain. Roll back automatically past 0.5 percent error rates or failed probes.
- **Input:** Signed artifact from Step 2.
- **Stop Condition:** Halt promotion on health breach; roll back without human delay.
- **Validation:** Telemetry confirms zero error regressions before full traffic.

### Step 4: Handoff and Human Review

- **Action:** Present the pipeline blueprint with gate evidence and request approval before production wiring.
- **Input:** Completed pipeline design.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero production wiring performed by this skill.

## 4. Output Specification

```markdown
# Pipeline Blueprint

- **CI:** [Stages with time budget and pins]
- **Artifacts:** [Build-once digests with signatures]
- **Rollout:** [Canary rings with health gates]
- **Rollback:** [Automatic triggers per signal]
```

## 5. Validation Gate

- [ ] CI pipeline executes to completion in under 10 minutes.
- [ ] All external actions are pinned to immutable 40-character commit SHAs.
- [ ] Artifacts are built once and tagged with commit SHA or semantic version.
- [ ] Zero secrets or private credentials exist in pipeline definition files.
- [ ] Deployment manifests include liveness and readiness probes.
- [ ] Human approval recorded before production wiring.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Wiring pipelines without pins, signatures, or time budgets.
- **Over-execution threshold:** Deploying to production environments unprompted.
- **Calibration default:** Gate every promotion; automate rollback before manual heroics.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-1 (vague task)      | Requires staged pipeline with time budget.          |
| 2    | AP-44 (unlocked data)  | Pins supply chain with signed artifacts.            |
| 3    | AP-4 (over-permissive) | Gates rollouts with automatic rollback.             |
| 4    | AP-45 (no human review)| Halts for approval before production wiring.        |

## 8. Versioning & Changelog

- **Version:** 3.0.0
- **Changelog:**
  - `3.0.0` (2026-09-26) - Full Tier-5 template conformance with Release Engineer role, role source, and seniority bar.
  - `2.0.0` (2026-09-20) - Elevated to Sauron Tier-5 specification with action pinning, artifact signing, and canary health gates.

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

**Input:** "Our deploys rebuild per environment and rollbacks need heroes."
**Output:** Pipeline blueprint with build-once digests, SHA-pinned actions, canary health gates, and automatic rollback triggers.
