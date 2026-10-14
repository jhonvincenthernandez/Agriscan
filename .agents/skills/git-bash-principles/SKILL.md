---
name: git-bash-principles
description: Enforces Git Bash compatibility with path translation discipline, line-ending hygiene, and cross-boundary execution safety. Excludes POSIX-only server scripting.
department: devops
ownerAgent: gimli
triggerCommand: /git-bash-principles
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-14
  - AP-26
  - AP-27
---

# Git Bash Principles

## 0. Identity

- **Role:** Service Builder. Owns cross-platform script implementation that runs clean on Windows and POSIX.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Service Builder).
- **Seniority bar:** Staff (Appendix B). Records why cygpath beats string replacement (drive-letter hacks break on edge cases, rejected sed path surgery), why LF enforcement beats per-machine fixes (one gitattributes rule ends CRLF errors forever, rejected dos2unix whack-a-mole), and why quoted expansions beat bare variables.
- **Authority:** Tier-5 normative skill for `skills/devops/git-bash-principles/`. Owns compatibility and safety guidance.
- **Must not define:** POSIX-only server scripting internals.
- **Normative base:** `core/fellowship/gimli.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-14 (leaking secrets), AP-26 (no scope boundary), and AP-27 (missing setup instructions).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Produce scripts that execute identically under Git Bash and POSIX shells.                      |
| 2   | Target Tool      | Git Bash MSYS2, cygpath, dos2unix, Node.js, Python.                                            |
| 3   | Output Format    | Compatibility plan with path, ending, and execution notes.                                     |
| 4   | Constraints      | LF endings enforced. Paths quoted. Zero em dashes. No unverified remote execution.             |
| 5   | Input            | Script inventory, Windows executable bridges, CI matrix.                                        |
| 6   | Context          | Prevents path-conversion surprises and carriage-return failures on Windows checkouts.          |
| 7   | Audience         | Engineers shipping cross-platform tooling and CI.                                               |
| 8   | Success Criteria | Scripts green on Linux and Git Bash; endings enforced; plan approved.                          |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger                                      | Fire? | Notes                              |
| -------------------------------------------- | ----- | ---------------------------------- |
| "Make our scripts work on Git Bash"          | YES   | Core trigger.                      |
| "Fix CRLF parse errors on Windows"           | YES   | Core trigger.                      |
| "/git-bash-principles"                       | YES   | Slash command trigger.             |
| "Write Linux-only server scripts"            | NO    | Route to `shell-scripting-principles`. |
| "Author Windows batch files"                 | NO    | Route to `windows-cmd-principles`. |

## 3. Execution Workflow

### Step 1: Fix Endings and Translation

- **Action:** Enforce LF via gitattributes on scripts, docs, and sources. Disable path conversion for native flag calls and convert boundaries programmatically with cygpath.
- **Input:** Repository file inventory.
- **Stop Condition:** Halt when gitattributes lacks LF rules; require them.
- **Validation:** Checkouts verified clean on Windows hosts.

### Step 2: Quote and Isolate Execution

- **Action:** Double-quote every expansion, resolve directories from script location instead of working directory, and wrap interactive tools for terminal quirks without breaking pipes.
- **Input:** Script list from Step 1.
- **Stop Condition:** Halt on unquoted expansions in reviewed scripts.
- **Validation:** ShellCheck clean with quoting audit.

### Step 3: Harden Against Exfiltration

- **Action:** Ban unverified remote piping, pin executable bits via git index, and forbid blind environment dumps that leak Windows tokens.
- **Input:** Security requirements from user.
- **Stop Condition:** Halt on curl-pipe patterns; require hash verification.
- **Validation:** Security review complete per script.

### Step 4: Handoff and Human Review

- **Action:** Present the compatibility plan and request approval before rollout.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero rollouts performed by this skill.

## 4. Output Specification

```markdown
# Git Bash Plan

- **Endings:** [Enforcement with verification]
- **Paths:** [Translation strategy]
- **Safety:** [Execution hardening notes]
```

## 5. Validation Gate

- [ ] LF enforced via gitattributes.
- [ ] Expansions quoted per script.
- [ ] Remote execution verified or banned.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before rollout.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Shipping scripts untested on Windows checkouts.
- **Over-execution threshold:** Modifying developer machines unprompted.
- **Calibration default:** Test both shells before every merge.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-27 (missing setup)  | Enforces endings via attributes.                    |
| 2    | AP-26 (no scope)       | Quotes every expansion.                             |
| 3    | AP-14 (leaking secrets)| Bans env dumps and unverified pipes.                |
| 4    | AP-45 (no human review)| Halts for approval before rollout.                  |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Service Builder role, role source, and seniority bar.
  - `1.0.0` - Legacy compatibility baseline.

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

**Input:** "Our install script fails on Windows with carriage-return errors."
**Output:** Compatibility plan with LF enforcement, cygpath bridges, and dual-shell verification.
