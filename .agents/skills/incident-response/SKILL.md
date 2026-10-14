---
name: incident-response
description: Production incident triage with severity classification, command roles, mitigation-first stabilization, runbook discipline, and blameless postmortems. Excludes pager vendor APIs.
department: security
ownerAgent: legolas
triggerCommand: /incident-response
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-26
  - AP-28
---

# Incident Response

## 0. Identity

- **Role:** Diagnostic Analyst. Owns incident classification with timeline evidence and systemic fixes.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Diagnostic Analyst).
- **Seniority bar:** Staff (Appendix B). Records why mitigation precedes root cause (users first, curiosity second; rejected debug-during-outage), why blameless postmortems beat blame (systems fail people, rejected witch hunts), and why evidence preservation precedes restarts.
- **Authority:** Tier-5 normative skill for `skills/security/incident-response/`. Owns triage and postmortem guidance.
- **Must not define:** Pager vendor APIs or customer SLA contracts.
- **Normative base:** `core/fellowship/legolas.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Produce triage discipline with severity tiers, command roles, and postmortem loops.            |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.                |
| 3   | Output Format    | Response plan with severity, roles, runbooks, and postmortem notes.                            |
| 4   | Constraints      | Mitigation before diagnosis. Blameless always. Zero em dashes. Evidence preserved.             |
| 5   | Input            | Service map, alert inventory, on-call roster, drill history.                                    |
| 6   | Context          | Prevents chaotic outages, lost evidence, and repeat incidents.                                  |
| 7   | Audience         | On-call engineers and incident commanders.                                                      |
| 8   | Success Criteria | Tiers declared; roles staffed; plan approved before incidents.                                  |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger                                      | Fire? | Notes                              |
| -------------------------------------------- | ----- | ---------------------------------- |
| "Set up our incident response"               | YES   | Core trigger.                      |
| "Run a blameless postmortem"                 | YES   | Core trigger.                      |
| "/incident-response"                         | YES   | Slash command trigger.             |
| "Page our on-call now"                       | NO    | Out of scope; live ops owns it.    |
| "Write our SLA contracts"                    | NO    | Out of scope for this skill.       |

## 3. Execution Workflow

### Step 1: Declare Severity Tiers

- **Action:** Define SEV-1 through SEV-3 by business impact with declaration rights for every engineer and 5-minute triage expectations.
- **Input:** Service map from user.
- **Stop Condition:** Halt when tiers stay verbal; require written tiers.
- **Validation:** Tier table reviewed with examples.

### Step 2: Staff Command and Mitigate

- **Action:** Assign commander, communications, and operations roles per incident. Stabilize first with rollbacks, flags, capacity, or breakers while preserving logs, metrics, and dumps before restarts.
- **Input:** On-call roster from Step 1.
- **Stop Condition:** Halt when roles stay unassigned during active incidents.
- **Validation:** Role chart reviewed with update cadence.

### Step 3: Postmortem Without Blame

- **Action:** Run 48-hour postmortems on SEV-1 and SEV-2 with 5-Whys depth, full timelines, owned action items with deadlines, and leadership review before new feature work.
- **Input:** Incident timelines from Step 2.
- **Stop Condition:** Halt on blame language; rewrite systemically.
- **Validation:** Postmortem reviewed with tracked actions.

### Step 4: Handoff and Human Review

- **Action:** Present the response plan and request approval before adoption.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero pages run by this skill.

## 4. Output Specification

```markdown
# Response Plan

- **Tiers:** [Severity table]
- **Command:** [Roles with cadence]
- **Postmortem:** [Blameless process]
```

## 5. Validation Gate

- [ ] Tiers declared with examples.
- [ ] Roles staffed per incident.
- [ ] Postmortems blameless with owners.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before adoption.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Responding without severity tiers.
- **Over-execution threshold:** Paging humans unprompted.
- **Calibration default:** Mitigate first; diagnose second.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-1 (vague task)      | Requires tier table first.                          |
| 2    | AP-26 (no scope)       | Staffs command per incident.                        |
| 3    | AP-28 (no stop)        | Tracks actions with deadlines.                      |
| 4    | AP-45 (no human review)| Halts for approval before adoption.                 |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Diagnostic Analyst role, role source, and seniority bar.
  - `1.0.0` - Legacy response baseline.

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

**Input:** "Our last outage had no commander and no postmortem."
**Output:** Plan with severity tiers, command roles, and blameless 48-hour postmortem loop.
