---
name: zero-trust-identity-architecture
description: Mutual TLS service communication, SPIFFE/SPIRE identity attestation, and least-privilege token exchange.
department: security
ownerAgent: boromir
triggerCommand: /zero-trust-identity-architecture
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-18
  - AP-26
  - AP-28
---

# Zero Trust Identity Architecture

## 0. Identity

- **Role:** Security Auditor. Owns identity posture with attested workload verification evidence.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Security Auditor).
- **Seniority bar:** Staff (Appendix B). Records why attested identity beats network location (compromised networks lie, rejected perimeter trust), why short-lived credentials beat static secrets (theft windows shrink to minutes, rejected eternal tokens), and why every packet authenticates.
- **Authority:** Tier-5 normative skill for `skills/security/zero-trust-identity-architecture/`. Owns identity architecture guidance.
- **Must not define:** Application UI theme tokens.
- **Normative base:** `core/fellowship/boromir.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`, `rules/security/owasp-defensive-shield.md`, `context/core-domains/security-policies.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-18 (implicit trust), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Architect workload attestation, ephemeral exchange, and mutual TLS across services.             |
| 2   | Target Tool      | SPIFFE / SPIRE, Istio service mesh, HashiCorp Vault, Envoy proxy.                              |
| 3   | Output Format    | SPIFFE ID definitions, attestation policies, Envoy mTLS manifests.                             |
| 4   | Constraints      | Zero implicit trust. Every packet authenticates. Zero em dashes. Short-lived credentials.       |
| 5   | Input            | Cluster topology, service mesh specs, IAM policies.                                             |
| 6   | Context          | Prevents lateral movement after breaches and credential replay attacks.                         |
| 7   | Audience         | Infrastructure security engineers and platform architects.                                      |
| 8   | Success Criteria | Full mTLS enforcement with sub-hour rotations evidenced.                                        |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger                                      | Fire? | Notes                              |
| -------------------------------------------- | ----- | ---------------------------------- |
| "Move our mesh to zero trust"                | YES   | Core trigger.                      |
| "Kill static service secrets"                | YES   | Core trigger.                      |
| "/zero-trust-identity-architecture"          | YES   | Slash command trigger.             |
| "Theme our admin UI"                         | NO    | Out of scope for this skill.       |
| "Write application features"                 | NO    | Out of scope for this skill.       |

## 3. Execution Workflow

### Step 1: Attest Every Workload

- **Action:** Issue short-lived verifiable identities per workload instance with attestation policies bound to platform facts.
- **Input:** Cluster topology from user.
- **Stop Condition:** Halt on unattested workloads in scope.
- **Validation:** Identity inventory reviewed with lifetimes.

### Step 2: Encrypt Every Hop

- **Action:** Enforce mutual TLS on all inter-service calls with client certificate requirements and mesh-wide policy.
- **Input:** Mesh specs from Step 1.
- **Stop Condition:** Halt on plaintext inter-service paths.
- **Validation:** mTLS coverage evidenced per hop.

### Step 3: Minimize Credential Lifetimes

- **Action:** Replace static secrets with ephemeral scoped tokens, rotate on short schedules, and audit issuance continuously.
- **Input:** IAM policies from user.
- **Stop Condition:** Halt on eternal credentials without rotation.
- **Validation:** Lifetime audit clean with rotation proof.

### Step 4: Handoff and Human Review

- **Action:** Present the identity plan and request approval before enforcement.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero enforcement done by this skill.

## 4. Output Specification

```markdown
# Identity Plan

- **Attestation:** [Workload inventory]
- **Encryption:** [mTLS coverage]
- **Lifetimes:** [Rotation proof]
```

## 5. Validation Gate

- [ ] Workloads attested per instance.
- [ ] Hops encrypted with mTLS.
- [ ] Credentials short-lived with proof.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before enforcement.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Trusting networks without attestation.
- **Over-execution threshold:** Rekeying infrastructure unprompted.
- **Calibration default:** Trust nothing; verify everything.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-1 (vague task)      | Requires topology first.                            |
| 2    | AP-26 (no scope)       | Encrypts every hop.                                 |
| 3    | AP-28 (no stop)        | Rotates on schedules.                               |
| 4    | AP-45 (no human review)| Halts for approval before enforcement.              |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Security Auditor role, role source, and seniority bar.
  - `1.0.0` - Legacy identity baseline.

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

**Input:** "Our east-west traffic is plaintext with static keys."
**Output:** Identity plan with attested workloads, mTLS coverage, and sub-hour rotations.
