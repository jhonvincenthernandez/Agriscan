---
name: docker-principles
description: Docker and containerization standards covering multi-stage builds, minimal base images, non-root user execution, layer caching discipline, BuildKit secrets, and vulnerability scanning.
department: devops
ownerAgent: gimli
triggerCommand: /docker-principles
antiPatternsPrevented:
  - AP-1
  - AP-4
  - AP-18
  - AP-26
  - AP-44
---

# Docker & Containerization Principles

## 0. Identity

- **Role:** Release Engineer. Owns image packaging with minimal attack surface and verifiable provenance.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Release Engineer).
- **Seniority bar:** Staff (Appendix B). Records why multi-stage builds beat single-stage bloat (compilers never ship, rejected fat images), why digest pins beat mutable tags (tested content equals running content, rejected latest tags), and why BuildKit secrets beat ENV credentials.
- **Authority:** Tier-5 normative skill for containerization across repositories under `skills/devops/docker-principles/`.
- **Must not define:** Kubernetes Custom Resource Definitions (see `kubernetes-operator-deployment`).
- **Normative base:** `core/fellowship/gimli.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-4 (root-user container execution), AP-26 (leaking secrets in image layers), and AP-44 (unlocked container configurations).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                            |
| --- | ---------------- | ------------------------------------------------------------------------------------------------ |
| 1   | Task             | Author, optimize, and secure container images and runtime Docker configurations.                 |
| 2   | Target Tool      | Docker, Docker BuildKit, Podman, Trivy, Docker Scout, Distroless, Alpine.                        |
| 3   | Output Format    | Optimized multi-stage Dockerfiles, .dockerignore files, and container compose manifests.         |
| 4   | Constraints      | Mandatory non-root user execution. Zero hardcoded secrets. Pin base image SHA digests.           |
| 5   | Input            | Application source trees, runtime dependencies, build toolchains, deployment targets.            |
| 6   | Context          | Prevents container privilege escalation, massive image bloat, and slow CI build times.           |
| 7   | Audience         | Backend engineers, DevOps architects, site reliability engineers, security auditors.             |
| 8   | Success Criteria | Production image size under 100MB; zero critical/high CVEs; 100 percent non-root user execution. |
| 9   | Examples         | See Section 10.                                                                                   |

## 2. Trigger Matrix

| Trigger Condition                                                | Fire? | Action / Route                                            |
| ---------------------------------------------------------------- | ----- | --------------------------------------------------------- |
| Writing or optimizing Dockerfiles for application deployment     | YES   | Implement multi-stage build with minimal runtime base.    |
| Container security scan detects high or critical vulnerabilities | YES   | Update base image digest and remove development packages. |
| Container processes running with root (UID 0) privileges         | YES   | Inject dedicated system user and set USER directive.      |
| Managing Kubernetes cluster orchestration and CRD controllers    | NO    | Route to `skills/devops/kubernetes-operator-deployment/`. |

## 3. Execution Workflow

### Step 1: Stage Builds for Minimal Runtimes

- **Action:** Separate builder stages from runtime stages on distroless or Alpine bases. Order instructions from least to most frequently changing for cache hits. Exclude build context waste with .dockerignore.
- **Input:** Application source trees and build toolchains.
- **Stop Condition:** Halt when compilers or secrets risk shipping in runtime stages.
- **Validation:** Build context excludes .git, local modules, and environment files.

### Step 2: Harden Users and Secrets

- **Action:** Create dedicated non-root users with USER directives, drop capabilities, and pass build credentials exclusively through BuildKit secret mounts. Scan with Trivy for zero critical CVEs.
- **Input:** Security requirements and secret inventory.
- **Stop Condition:** Halt on root execution or ENV-baked secrets; require fixes.
- **Validation:** Process launches with non-zero UID; scan reports clean.

### Step 3: Pin, Probe, and Ship

- **Action:** Pin base images to SHA digests, declare readiness and liveness probes, set resource limits, and tag outputs immutably for promotion.
- **Input:** Deployment targets from user.
- **Stop Condition:** Halt when tags float on latest or probes stay missing.
- **Validation:** Digest-pinned manifest with probes reviewed.

### Step 4: Handoff and Human Review

- **Action:** Present the image plan with scan evidence and request approval before registry push.
- **Input:** Completed image design.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero pushes performed by this skill.

## 4. Output Specification

```markdown
# Image Blueprint

- **Stages:** [Builder versus runtime split]
- **Security:** [User, secrets, scan evidence]
- **Pins:** [Digest-pinned bases with probes]
```

## 5. Validation Gate

- [ ] Dockerfile uses multi-stage architecture with distinct builder and runner stages.
- [ ] Base images are pinned to explicit versions or immutable digests.
- [ ] Process executes under an explicit non-root user (`USER` directive present).
- [ ] `.dockerignore` file exists and excludes build artifacts and secrets.
- [ ] Human approval recorded before registry push.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Shipping single-stage images with root users.
- **Over-execution threshold:** Pushing images to shared registries unprompted.
- **Calibration default:** Minimal base first; add packages with receipts.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-1 (vague task)      | Requires staged build plan first.                   |
| 2    | AP-44 (unlocked data)  | Bans secrets in layers with scans.                  |
| 3    | AP-4 (over-permissive) | Enforces pins and probes.                           |
| 4    | AP-45 (no human review)| Halts for approval before push.                     |

## 8. Versioning & Changelog

- **Version:** 3.0.0
- **Changelog:**
  - `3.0.0` (2026-09-26) - Full Tier-5 template conformance with Release Engineer role, role source, and seniority bar.
  - `2.0.0` (2026-09-20) - Elevated to Sauron Tier-5 specification with multi-stage non-root hardening patterns.

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

**Input:** "Our Node image is 1.2GB, runs as root, and ships dev dependencies."
**Output:** Multi-stage Dockerfile under 100MB with non-root user, digest-pinned base, BuildKit secrets, and clean Trivy scan.
