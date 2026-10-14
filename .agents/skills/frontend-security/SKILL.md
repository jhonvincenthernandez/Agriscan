---
name: frontend-security
description: Client-side security rules covering DOM XSS sinks, strict CSP, Trusted Types, postMessage validation, third-party supply chain, and token storage. Excludes backend auth design.
department: frontend
ownerAgent: boromir
triggerCommand: /frontend-security
antiPatternsPrevented:
  - AP-1
  - AP-4
  - AP-6
  - AP-26
  - AP-28
---

# Frontend Security

## 0. Identity

- **Role:** Security Auditor. Owns client-side threat posture with layered, verifiable controls.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Security Auditor).
- **Seniority bar:** Staff (Appendix B). Records why layered defense beats single controls (one layer fails, others catch; rejected CSP-only hope), why strict CSP beats allowlists (nonces over wildcards, rejected unsafe-inline shortcuts), and why httpOnly cookies beat localStorage tokens (theft surface vanishes, rejected convenience storage).
- **Authority:** Tier-5 normative skill for `skills/frontend/frontend-security/`. Owns client threat guidance; backend half lives with `security-auditor`.
- **Must not define:** Backend authentication design or server session architecture.
- **Normative base:** `core/fellowship/boromir.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-4 (over-permissive execution), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                   |
| --- | ---------------- | --------------------------------------------------------------------------------------- |
| 1   | Task             | Produce layered client defenses with auditable sink, policy, and supply-chain controls. |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.        |
| 3   | Output Format    | Threat plan with sink audit, policy, supply chain, and token notes.                     |
| 4   | Constraints      | Defense in depth always. Sinks enumerated. Zero em dashes. Tokens never in storage.     |
| 5   | Input            | Entry points, third-party inventory, auth flows, upload surfaces.                       |
| 6   | Context          | Prevents DOM XSS, supply-chain takeovers, and token theft on the client.                |
| 7   | Audience         | Frontend engineers owning client-side security.                                         |
| 8   | Success Criteria | Sinks controlled; policy strict; plan approved before shipping.                         |
| 9   | Examples         | See Section 10.                                                                         |

## 2. Trigger Matrix

| Trigger                               | Fire? | Notes                          |
| ------------------------------------- | ----- | ------------------------------ |
| "Audit our frontend for XSS"          | YES   | Core trigger.                  |
| "Lock down our CSP and third parties" | YES   | Core trigger.                  |
| "/frontend-security"                  | YES   | Slash command trigger.         |
| "Design our backend auth"             | NO    | Out of scope; backend owns it. |
| "Pentest our infrastructure"          | NO    | Route to `pentest-planner`.    |

## 3. Execution Workflow

### Step 1: Enumerate Sinks and Sources

- **Action:** List DOM sinks with reaching sources (URL params, storage, messages, API data). Flag framework escape hatches for sanitizer-wrapped review.
- **Input:** Entry points from user.
- **Stop Condition:** Halt when sink inventory stays partial; require enumeration.
- **Validation:** Sink map reviewed with source tracing.

### Step 2: Enforce Policy Layers

- **Action:** Deliver strict header CSP with nonces and strict-dynamic, add Trusted Types enforcement with named policies, and validate postMessage origins plus shapes on both directions.
- **Input:** Hosting capabilities from user.
- **Stop Condition:** Halt on unsafe-inline shortcuts; require nonces.
- **Validation:** Policy review complete with header proof.

### Step 3: Control Supply Chain and Tokens

- **Action:** Minimize third-party scripts with SRI pins and self-hosting, isolate uploads on separate origins, store tokens in httpOnly cookies, and wire CI lint plus violation monitoring.
- **Input:** Third-party inventory and auth flows.
- **Stop Condition:** Halt on localStorage tokens or unpinned CDN scripts.
- **Validation:** Supply audit complete with token review.

### Step 4: Handoff and Human Review

- **Action:** Present the threat plan and request approval before shipping.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero deploys performed by this skill.

## 4. Output Specification

```markdown
# Threat Plan

- **Sinks:** [Enumerated map]
- **Policy:** [CSP with Trusted Types]
- **Supply:** [Third-party controls]
- **Tokens:** [Storage decisions]
```

## 5. Validation Gate

- [ ] Sinks enumerated with sources.
- [ ] Policy strict without shortcuts.
- [ ] Tokens out of storage.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before shipping.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Shipping clients without sink enumeration.
- **Over-execution threshold:** Redesigning backend auth unprompted.
- **Calibration default:** Layer everything; trust no single control.

## 7. Anti-Pattern Compliance

| Step | Prevents AP             | Mechanism                           |
| ---- | ----------------------- | ----------------------------------- |
| 1    | AP-1 (vague task)       | Requires sink map first.            |
| 2    | AP-26 (no scope)        | Enforces strict policy.             |
| 3    | AP-4 (over-permissive)  | Controls supply with token rules.   |
| 4    | AP-45 (no human review) | Halts for approval before shipping. |

## 8. Versioning & Changelog

- **Version:** 1.0.0
- **Changelog:**
  - `1.0.0` (2026-09-26) - Initial release closing the client-threat gap.

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

**Input:** "Our marketing site loads 14 third-party scripts with no CSP."
**Output:** Threat plan with enumerated sinks, strict nonce CSP, SRI-pinned vendors, and httpOnly token migration.
