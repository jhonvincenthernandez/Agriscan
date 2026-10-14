---
name: shell-scripting-principles
description: Enforces POSIX shell scripting with strict preambles, defensive quoting, trap cleanup, and injection defense. Excludes Windows batch scripting.
department: devops
ownerAgent: gimli
triggerCommand: /shell-scripting-principles
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-14
  - AP-20
  - AP-26
  - AP-57
---

# Shell Scripting Principles

## 0. Identity

- **Role:** Service Builder. Owns automation script implementation with strict failure semantics inside scoped files.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Service Builder).
- **Seniority bar:** Staff (Appendix B). Records why strict preambles beat bare scripts (failures surface at origin, rejected silent continuations), why arrays beat string-built commands (injection dies at construction, rejected eval assembly), and why hash verification beats curl pipes.
- **Authority:** Tier-5 normative skill for `skills/devops/shell-scripting-principles/`. Owns scripting and safety guidance.
- **Must not define:** Windows batch scripting internals.
- **Normative base:** `core/fellowship/gimli.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-14 (leaking secrets), AP-20 (untracked work), and AP-57 (untracked side effects).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Produce portable hardened shell scripts with verified execution paths.                         |
| 2   | Target Tool      | Bash, POSIX sh, ShellCheck, CI Linux and macOS runners.                                        |
| 3   | Output Format    | Script plan with preamble, quoting, trap, and safety notes.                                    |
| 4   | Constraints      | Strict preamble always. Quote every expansion. Zero em dashes. No remote pipes.                |
| 5   | Input            | Automation goals, temp file needs, download inventory.                                          |
| 6   | Context          | Prevents word-splitting bugs, silent failures, and injection payloads.                          |
| 7   | Audience         | Engineers automating Unix fleets and CI.                                                        |
| 8   | Success Criteria | ShellCheck clean; traps registered; plan approved before rollout.                               |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger                                      | Fire? | Notes                              |
| -------------------------------------------- | ----- | ---------------------------------- |
| "Harden our build scripts"                   | YES   | Core trigger.                      |
| "Audit shell scripts for injection"          | YES   | Core trigger.                      |
| "/shell-scripting-principles"                | YES   | Slash command trigger.             |
| "Write Windows batch files"                  | NO    | Route to `windows-cmd-principles`. |
| "Write PowerShell modules"                   | NO    | Route to `powershell-principles`.  |

## 3. Execution Workflow

### Step 1: Open Strictly Every Time

- **Action:** Start with env-bash shebang plus strict preamble and narrow field separators. Resolve directories from script location, never working directory.
- **Input:** Script inventory from user.
- **Stop Condition:** Halt on missing preambles; require them.
- **Validation:** Preamble audit complete per script.

### Step 2: Quote, Trap, and Contain

- **Action:** Quote every expansion, prefer modern conditionals, register exit traps with mktemp-only temporaries, and canonicalize paths before destructive operations.
- **Input:** Script bodies from Step 1.
- **Stop Condition:** Halt on unquoted expansions or predictable temp paths.
- **Validation:** Quoting and trap review complete per script.

### Step 3: Ban Dangerous Execution

- **Action:** Prohibit curl pipes and eval entirely. Verify downloads with pinned hashes in isolated directories before execution. Build commands as arrays, never concatenated strings.
- **Input:** Download inventory from user.
- **Stop Condition:** Halt on any banned pattern; mark as blocking.
- **Validation:** ShellCheck zero-error evidence recorded.

### Step 4: Handoff and Human Review

- **Action:** Present the plan and request approval before rollout.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero rollouts performed by this skill.

## 4. Output Specification

```markdown
# Shell Plan

- **Preamble:** [Strictness per script]
- **Safety:** [Quoting with trap notes]
- **Execution:** [Banned patterns with verification]
```

## 5. Validation Gate

- [ ] Strict preamble per script.
- [ ] Expansions quoted with traps set.
- [ ] Dangerous patterns banned with hashes.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before rollout.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Shipping scripts without ShellCheck runs.
- **Over-execution threshold:** Mutating machine paths unprompted.
- **Calibration default:** Strictest preamble first; relax nothing silently.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-1 (vague task)      | Requires preamble audit first.                      |
| 2    | AP-26 (no scope)       | Quotes and contains every path.                     |
| 3    | AP-14 (leaking secrets)| Bans pipes and eval with verification.              |
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

**Input:** "Our CI scripts fail silently and one pipes curl to bash."
**Output:** Plan with strict preambles, trap cleanup, hash-verified downloads, and ShellCheck-clean evidence.
