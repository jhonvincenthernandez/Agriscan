---
name: agent-guard
description: Pre-execution safety hook, destructive command interceptor, and credential shield for autonomous AI coding agents across Claude Code and Copilot CLI.
department: security
ownerAgent: boromir
triggerCommand: /agent-guard
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-14
  - AP-20
  - AP-26
  - AP-57
---

# Agent Guard

## 0. Identity

- **Role:** Security Auditor. Owns pre-execution threat posture with fail-closed interception evidence.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Security Auditor).
- **Seniority bar:** Staff (Appendix B). Records why fail-closed beats fail-open on guard errors (unknown state must block, rejected permissive fallthrough), why deterministic matching beats clever parsing (predictable blocks, rejected regex cleverness that misses), and why CI headless paths fail instead of hanging.
- **Authority:** Tier-5 normative skill for `skills/security/agent-guard/`. Owns hook policy and interception guidance.
- **Must not define:** Application business logic or CI pipeline design.
- **Normative base:** `core/fellowship/boromir.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-14 (leaking secrets), AP-20 (untracked destructive work), AP-26 (no scope boundary), and AP-57 (untracked CI side effects).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Produce hook policies with block, gate, and permit tiers plus fail-closed defaults.            |
| 2   | Target Tool      | Claude Code hooks, Copilot CLI hooks, POSIX shells.                                            |
| 3   | Output Format    | Guard plan with policy matrix, hook notes, and verification evidence.                          |
| 4   | Constraints      | Fail closed always. Deterministic matching. Zero em dashes. No headless hangs.                 |
| 5   | Input            | Tool inventory, credential map, destructive command list.                                       |
| 6   | Context          | Prevents agent-driven wipes, history rewrites, and secret leaks into model context.            |
| 7   | Audience         | Engineers gating autonomous agent execution.                                                    |
| 8   | Success Criteria | Tiers enforced; failures closed; plan approved before wiring.                                   |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger                                      | Fire? | Notes                              |
| -------------------------------------------- | ----- | ---------------------------------- |
| "Gate our agents destructive commands"       | YES   | Core trigger.                      |
| "Shield credentials from agent context"      | YES   | Core trigger.                      |
| "/agent-guard"                               | YES   | Slash command trigger.             |
| "Write application business logic"           | NO    | Out of scope for this skill.       |
| "Design our CI pipelines"                    | NO    | Out of scope for this skill.       |

## 3. Execution Workflow

### Step 1: Tier Every Action

- **Action:** Classify tool calls into hard block (credentials, wipes, force pushes, drops), confirmation gate (single deletes, cleanups, branch force), and auto-permit (status, diffs, tests, reads).
- **Input:** Tool inventory from user.
- **Stop Condition:** Halt when destructive commands lack tiers.
- **Validation:** Policy matrix reviewed per tier.

### Step 2: Wire Hooks Fail-Closed

- **Action:** Install pre-execution hooks with normalized deterministic matching, exit-1 defaults on errors, and graceful headless failures instead of hangs.
- **Input:** Hook surfaces per runtime.
- **Stop Condition:** Halt on fail-open error paths; require closed defaults.
- **Validation:** Hook behavior proven per tier with tests.

### Step 3: Shield Secrets Absolutely

- **Action:** Block credential file reads into model context, forbid env dumps, and audit every secret-adjacent pattern with evidence.
- **Input:** Credential map from Step 1.
- **Stop Condition:** Halt when any secret path stays readable; mark as blocking.
- **Validation:** Secret audit clean with proof.

### Step 4: Handoff and Human Review

- **Action:** Present the guard plan and request approval before wiring.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero hooks wired by this skill.

## 4. Output Specification

```markdown
# Guard Plan

- **Tiers:** [Block, gate, permit matrix]
- **Hooks:** [Fail-closed wiring notes]
- **Secrets:** [Shield audit]
```

## 5. Validation Gate

- [ ] Actions tiered per risk.
- [ ] Hooks fail closed with proof.
- [ ] Secrets unreadable to agents.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before wiring.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Gating agents without tier mapping.
- **Over-execution threshold:** Rewriting application code unprompted.
- **Calibration default:** Block by default; permit with receipts.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-1 (vague task)      | Requires tier map first.                            |
| 2    | AP-26 (no scope)       | Fails closed per hook.                              |
| 3    | AP-14 (leaking secrets)| Shields credentials absolutely.                     |
| 4    | AP-45 (no human review)| Halts for approval before wiring.                   |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Security Auditor role, role source, and seniority bar.
  - `1.0.0` - Legacy guard baseline.

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

**Input:** "Our agent force-pushed main and printed env secrets."
**Output:** Guard plan with hard blocks on force pushes, credential read bans, and fail-closed hook wiring.
