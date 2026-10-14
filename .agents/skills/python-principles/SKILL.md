---
name: python-principles
description: Modern Python 3.10 engineering rules covering strict typing, async discipline, dependency hygiene, deserialization safety, and static analysis gates. Excludes frontend UI builds.
department: backend
ownerAgent: frodo
triggerCommand: /python-principles
antiPatternsPrevented:
  - AP-1
  - AP-4
  - AP-6
  - AP-14
  - AP-26
  - AP-28
  - AP-41
  - AP-44
---

# Python Principles

## 0. Identity

- **Role:** Service Builder. Owns type-safe Python implementation with security hardening inside scoped files.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Service Builder).
- **Seniority bar:** Staff (Appendix B).
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Service Builder).
- **Seniority bar:** Staff (Appendix B). Records why strict annotations plus static analysis beat dynamic velocity (Mypy-clean codebases reject entire bug classes at CI, rejected untyped speed), why pickle stays banned on untrusted input (remote execution by deserialization, rejected convenience parsing), and why virtualenv isolation precedes every install.
- **Authority:** Tier-5 normative skill for `skills/backend/python-principles/`. Owns typing, async, and security guidance.
- **Must not define:** Frontend UI layout or client-side hydration routines.
- **Normative base:** `core/fellowship/frodo.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-4 (over-permissive execution), AP-14 (leaking secrets), AP-41 (unparameterized queries), AP-44 (phantom types), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                |
| --- | ---------------- | ------------------------------------------------------------------------------------ |
| 1   | Task             | Produce idiomatic, type-safe, secure Python across apps, scripts, and libraries.     |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.     |
| 3   | Output Format    | Implementation plan with typing, async, security, and gate notes.                    |
| 4   | Constraints      | Python 3.10 plus only. Ruff formatted. Zero em dashes. No dynamic execution.         |
| 5   | Input            | Feature spec, domain model, async needs, threat surface.                             |
| 6   | Context          | Prevents untyped sprawl, blocking event loops, and deserialization vulnerabilities.  |
| 7   | Audience         | Backend engineers shipping modern Python 3.10 codebases.                             |
| 8   | Success Criteria | Annotations complete; async clean; security floors met; plan approved before coding. |
| 9   | Examples         | See Section 10.                                                                      |

## 2. Trigger Matrix

| Trigger                        | Fire? | Notes                             |
| ------------------------------ | ----- | --------------------------------- |
| "Build this feature in Python" | YES   | Core trigger.                     |
| "Harden this Python service"   | YES   | Core trigger.                     |
| "/python-principles"           | YES   | Slash command trigger.            |
| "Build a React frontend"       | NO    | Out of scope for this skill.      |
| "Administer our servers"       | NO    | Out of scope; ops runbook needed. |

## 3. Execution Workflow

### Step 1: Lock Modern Standards

- **Action:** Target Python 3.10 plus with native union syntax and match statements. Standardize on `pyproject.toml` for metadata and tooling. Annotate every signature and enforce Mypy or Pyright clean.
- **Input:** Feature spec and domain model.
- **Stop Condition:** Halt when untyped public functions appear; require annotations.
- **Validation:** Typing audit complete with Ruff format clean.

### Step 2: Isolate Environments and Dependencies

- **Action:** Mandate virtualenvs via uv or Poetry, pin lockfiles deterministically, and audit installs against CVE feeds before merging.
- **Input:** Dependency list from user.
- **Stop Condition:** Halt on global installs or unpinned production deps.
- **Validation:** Lockfile reviewed with audit evidence.

### Step 3: Discipline Async and Security

- **Action:** Wrap resources in context managers, keep event loops non-blocking with worker offload, and timeout every network call. Ban eval, exec, pickle on untrusted input, and shell interpolation. Resolve paths against base directories and source secrets from environment only.
- **Input:** Async needs and threat surface.
- **Stop Condition:** Halt when any security floor stays unmet; mark as blocking.
- **Validation:** Security checklist reviewed per surface.

### Step 4: Handoff and Human Review

- **Action:** Present the plan and request approval before coding.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero code written by this skill.

## 4. Output Specification

```markdown
# Python Plan

- **Standards:** [Version with typing target]
- **Environment:** [Lockfile with audit notes]
- **Security:** [Floors per surface]
- **Async:** [Discipline notes]
```

## 5. Validation Gate

- [ ] Modern standards locked before logic.
- [ ] Dependencies pinned with audit.
- [ ] Security floors met per surface.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before coding.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Shipping untyped code with global installs.
- **Over-execution threshold:** Rewriting working systems unprompted.
- **Calibration default:** Strictness first; velocity follows.

## 7. Anti-Pattern Compliance

| Step | Prevents AP             | Mechanism                                       |
| ---- | ----------------------- | ----------------------------------------------- |
| 1    | AP-44 (phantom types)   | Requires annotations with static analysis.      |
| 2    | AP-26 (no scope)        | Isolates envs with pinned lockfiles.            |
| 3    | AP-4 (over-permissive)  | Bans dynamic execution and shell interpolation. |
| 4    | AP-45 (no human review) | Halts for approval before coding.               |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Service Builder role, role source, and seniority bar.
  - `1.0.0` - Legacy engineering principles baseline.

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

**Input:** "Build an async ingestion worker in Python with safe subprocess calls."
**Output:** Plan with typed service boundaries, worker-offloaded blocking I/O, argument-list subprocesses, and isolated test strategy.
