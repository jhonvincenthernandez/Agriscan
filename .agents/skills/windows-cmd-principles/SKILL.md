---
name: windows-cmd-principles
description: Enforces hardened Windows batch scripting with scope isolation, exit-code discipline, quoted expansion, and injection defense. Excludes PowerShell module builds.
department: devops
ownerAgent: gimli
triggerCommand: /windows-cmd-principles
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-14
  - AP-26
  - AP-28
  - AP-52
---

# Windows CMD Principles

## 0. Identity

- **Role:** Service Builder. Owns batch wrapper implementation with explicit exit semantics inside scoped files.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Service Builder).
- **Seniority bar:** Staff (Appendix B). Records why delayed expansion beats immediate reads in blocks (stale values corrupt loops, rejected percent-expansion guessing), why allowlisted arguments beat raw passthrough (chaining characters execute, rejected unquoted percent-args), and why call-keyword invocation beats bare calls.
- **Authority:** Tier-5 normative skill for `skills/devops/windows-cmd-principles/`. Owns batch scripting guidance.
- **Must not define:** PowerShell module builds.
- **Normative base:** `core/fellowship/gimli.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-14 (leaking secrets), AP-26 (no scope boundary), and AP-52 (fake fixes).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Produce hardened batch wrappers with verified exit codes and sanitized inputs.                  |
| 2   | Target Tool      | Windows CMD, CI Windows runners, wrapper utilities.                                             |
| 3   | Output Format    | Wrapper plan with scope, exit, and sanitization notes.                                         |
| 4   | Constraints      | Scope isolated. Exits explicit. Zero em dashes. Inputs allowlisted.                             |
| 5   | Input            | Wrapper goals, argument inventory, prerequisite checks.                                          |
| 6   | Context          | Prevents injection chains, lost exit codes, and bypassed cleanup paths.                         |
| 7   | Audience         | Engineers shipping Windows runners and CLI wrappers.                                            |
| 8   | Success Criteria | Exits propagate; inputs sanitized; plan approved before rollout.                                |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger                                      | Fire? | Notes                              |
| -------------------------------------------- | ----- | ---------------------------------- |
| "Harden our batch wrappers"                  | YES   | Core trigger.                      |
| "Fix lost exit codes on Windows CI"          | YES   | Core trigger.                      |
| "/windows-cmd-principles"                    | YES   | Slash command trigger.             |
| "Build PowerShell modules"                   | NO    | Route to `powershell-principles`.  |
| "Write Linux shell scripts"                  | NO    | Route to `shell-scripting-principles`. |

## 3. Execution Workflow

### Step 1: Isolate Scope and Resolve Paths

- **Action:** Open with echo suppression plus extensions and delayed expansion, close with endlocal, and resolve directories from script location instead of working directory.
- **Input:** Wrapper goals from user.
- **Stop Condition:** Halt on missing scope isolation; require it.
- **Validation:** Scope review complete per script.

### Step 2: Propagate Exit Codes

- **Action:** Check error levels after every external call, exit with explicit numeric codes, and never mask failures with silenced redirects.
- **Input:** Prerequisite checks from Step 1.
- **Stop Condition:** Halt on unchecked calls or bare exits.
- **Validation:** Exit audit complete per call site.

### Step 3: Sanitize Inputs and Temp Files

- **Action:** Quote every path, strip enclosing quotes before re-quoting, allowlist arguments against chaining characters, invoke sub-scripts with call keywords, and clean temp files on both exit paths.
- **Input:** Argument inventory from user.
- **Stop Condition:** Halt on raw passthrough or missing cleanup.
- **Validation:** Sanitization review complete per argument.

### Step 4: Handoff and Human Review

- **Action:** Present the plan and request approval before rollout.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero rollouts performed by this skill.

## 4. Output Specification

```markdown
# Batch Plan

- **Scope:** [Isolation with path notes]
- **Exits:** [Propagation audit]
- **Inputs:** [Sanitization per argument]
```

## 5. Validation Gate

- [ ] Scope isolated per script.
- [ ] Exits propagate numerically.
- [ ] Inputs allowlisted per argument.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before rollout.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Shipping wrappers without exit audits.
- **Over-execution threshold:** Changing runner configs unprompted.
- **Calibration default:** Explicit everything; assume hostile inputs.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-1 (vague task)      | Requires scope review first.                        |
| 2    | AP-26 (no scope)       | Propagates exits per call.                          |
| 3    | AP-14 (leaking secrets)| Sanitizes inputs with cleanup.                      |
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

**Input:** "Our Windows wrapper swallows failures and skips cleanup."
**Output:** Plan with explicit exit propagation, allowlisted arguments, and dual-path temp cleanup.
