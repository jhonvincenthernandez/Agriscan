---
name: powershell-principles
description: Enforces hardened PowerShell scripting with strict mode, validated parameters, pipeline hygiene, and injection defense. Excludes Linux shell scripting.
department: devops
ownerAgent: gimli
triggerCommand: /powershell-principles
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-14
  - AP-26
  - AP-28
  - AP-52
---

# PowerShell Principles

## 0. Identity

- **Role:** Service Builder. Owns automation script implementation with fail-closed execution inside scoped files.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Service Builder).
- **Seniority bar:** Staff (Appendix B). Records why strict mode plus approved verbs beat ad-hoc scripts (entire error classes die at runtime, rejected loose scripting), why SecureString beats plaintext (credential theft starts in scripts, rejected string passwords), and why array arguments beat concatenated commands.
- **Authority:** Tier-5 normative skill for `skills/devops/powershell-principles/`. Owns scripting and safety guidance.
- **Must not define:** Linux shell scripting internals.
- **Normative base:** `core/fellowship/gimli.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-14 (leaking secrets), AP-26 (no scope boundary), and AP-52 (fake fixes).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Produce hardened PowerShell automation with validated inputs and safe execution.                |
| 2   | Target Tool      | PowerShell 7, PSScriptAnalyzer, SecretManagement, CI Windows runners.                           |
| 3   | Output Format    | Script plan with hardening notes and analyzer evidence.                                        |
| 4   | Constraints      | Strict mode on. Parameters validated. Zero em dashes. No remote pipes.                         |
| 5   | Input            | Automation goals, credential inventory, execution scope.                                        |
| 6   | Context          | Prevents injection payloads, credential leaks, and silent failures in Windows automation.       |
| 7   | Audience         | Engineers automating Windows fleets and CI.                                                     |
| 8   | Success Criteria | Analyzer clean; secrets vaulted; plan approved before rollout.                                  |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger                                      | Fire? | Notes                              |
| -------------------------------------------- | ----- | ---------------------------------- |
| "Harden our deploy scripts"                  | YES   | Core trigger.                      |
| "Audit PowerShell for injection risks"       | YES   | Core trigger.                      |
| "/powershell-principles"                     | YES   | Slash command trigger.             |
| "Write Linux shell scripts"                  | NO    | Route to `shell-scripting-principles`. |
| "Author batch wrappers"                      | NO    | Route to `windows-cmd-principles`. |

## 3. Execution Workflow

### Step 1: Structure Scripts Strictly

- **Action:** Declare CmdletBinding with param blocks, enforce strict mode with stop-on-error preference, follow approved verb taxonomy, and type every parameter with validation attributes.
- **Input:** Automation goals from user.
- **Stop Condition:** Halt on untyped params or custom verbs; require fixes.
- **Validation:** Structure review complete per script.

### Step 2: Stream Objects Safely

- **Action:** Emit structured objects through process blocks, release handles in finally blocks, and resolve paths absolutely instead of trusting working directories.
- **Input:** Pipeline needs from Step 1.
- **Stop Condition:** Halt when text munging replaces objects; require structured flow.
- **Validation:** Pipeline review complete per function.

### Step 3: Ban Dangerous Sinks

- **Action:** Prohibit Invoke-Expression and remote pipes without hash verification, constrain execution policy to process scope, vault all credentials, and pass native arguments as arrays.
- **Input:** Credential inventory and execution scope.
- **Stop Condition:** Halt on any banned sink; mark as blocking.
- **Validation:** Analyzer clean with safety audit.

### Step 4: Handoff and Human Review

- **Action:** Present the plan and request approval before rollout.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero rollouts performed by this skill.

## 4. Output Specification

```markdown
# PowerShell Plan

- **Structure:** [Strictness with verb audit]
- **Pipeline:** [Object flow notes]
- **Safety:** [Banned sinks with vault map]
```

## 5. Validation Gate

- [ ] Strict mode with validated params.
- [ ] Objects stream through pipelines.
- [ ] Dangerous sinks banned with vaulting.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before rollout.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Shipping loose scripts without analyzer runs.
- **Over-execution threshold:** Changing machine policies unprompted.
- **Calibration default:** Strictest settings first; relax with receipts.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-1 (vague task)      | Requires structure audit first.                     |
| 2    | AP-26 (no scope)       | Streams objects with cleanup.                       |
| 3    | AP-14 (leaking secrets)| Vaults credentials, bans pipes.                     |
| 4    | AP-45 (no human review)| Halts for approval before rollout.                  |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Service Builder role, role source, and seniority bar.
  - `1.0.0` - Legacy scripting baseline.

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

**Input:** "Our deploy scripts use plain passwords and silent failures."
**Output:** Plan with vaulted credentials, strict-mode enforcement, and analyzer-clean scripts.
