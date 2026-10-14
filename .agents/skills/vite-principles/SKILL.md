---
name: vite-principles
description: Vite 6.x architecture rules covering Environment API, plugin ordering, alias hygiene, SSR hydration, monorepo optimization, and security hardening.
department: frontend
ownerAgent: gimli
triggerCommand: /vite-principles
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-26
  - AP-28
---

# Vite Principles

## 0. Identity

- **Role:** Release Engineer. Owns build packaging with deterministic bundling and hardened dev servers.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Release Engineer).
- **Seniority bar:** Staff (Appendix B). Records why explicit targets beat implicit defaults (reproducible output, rejected mystery builds), why pure transforms beat stateful plugins (cacheable pipelines, rejected side-effect hooks), and why server guards beat leaked secrets.
- **Authority:** Tier-5 normative skill for `skills/frontend/vite-principles/`. Owns bundler and config guidance.
- **Must not define:** Application business logic or backend APIs.
- **Normative base:** `core/fellowship/gimli.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Produce Vite configs with isolated environments, ordered plugins, and hardened servers.        |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.                |
| 3   | Output Format    | Config plan with environments, plugins, aliases, and security notes.                           |
| 4   | Constraints      | Targets explicit. Transforms pure. Zero em dashes. Secrets server-only.                        |
| 5   | Input            | Target runtimes, plugin inventory, monorepo layout, security needs.                             |
| 6   | Context          | Prevents mystery builds, plugin races, and secret leaks into bundles.                           |
| 7   | Audience         | Frontend engineers configuring Vite builds.                                                     |
| 8   | Success Criteria | Config deterministic; plugins ordered; plan approved before coding.                             |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger                                      | Fire? | Notes                              |
| -------------------------------------------- | ----- | ---------------------------------- |
| "Configure our Vite build"                   | YES   | Core trigger.                      |
| "Fix slow builds and leaking secrets"        | YES   | Core trigger.                      |
| "/vite-principles"                           | YES   | Slash command trigger.             |
| "Write application business logic"           | NO    | Out of scope for this skill.       |
| "Bundle with another tool"                   | NO    | Out of scope; Vite only.           |

## 3. Execution Workflow

### Step 1: Isolate Environments Explicitly

- **Action:** Declare build targets and per-environment resolve, plugin, and dev configs with aligned TypeScript module resolution. Check runtime context via environment APIs, never process sniffing.
- **Input:** Target runtimes from user.
- **Stop Condition:** Halt on implicit targets or legacy SSR overrides.
- **Validation:** Environment map reviewed with target audit.

### Step 2: Order Plugins Purely

- **Action:** Declare hook enforcement with phase restrictions, keep transforms pure and idempotent, scope dev middleware correctly, and namespace virtual modules safely.
- **Input:** Plugin inventory from Step 1.
- **Stop Condition:** Halt on stateful transforms or unscoped middleware.
- **Validation:** Plugin review complete with ordering proof.

### Step 3: Guard Assets and Secrets

- **Action:** Mirror aliases in TypeScript config, ban root wildcards, stream SSR responses correctly, split vendor chunks without cycles, enforce strict file access with prefixed env vars, and hide production sourcemaps.
- **Input:** Monorepo layout and security needs.
- **Stop Condition:** Halt on client-referenced secrets or unguarded file access.
- **Validation:** Asset and secret audit complete.

### Step 4: Handoff and Human Review

- **Action:** Present the plan and request approval before coding.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero code written by this skill.

## 4. Output Specification

```markdown
# Vite Plan

- **Environments:** [Isolated configs]
- **Plugins:** [Ordered pure hooks]
- **Assets:** [Guarded pipeline notes]
```

## 5. Validation Gate

- [ ] Targets explicit per environment.
- [ ] Plugins ordered and pure.
- [ ] Secrets guarded from bundles.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before coding.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Shipping configs without target audit.
- **Over-execution threshold:** Rewriting app logic unprompted.
- **Calibration default:** Explicit everything; implicit nothing.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-1 (vague task)      | Requires environment map first.                     |
| 2    | AP-26 (no scope)       | Orders plugins explicitly.                          |
| 3    | AP-28 (no stop)        | Guards assets and secrets.                          |
| 4    | AP-45 (no human review)| Halts for approval before coding.                   |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Release Engineer role, role source, and seniority bar.
  - `1.0.0` - Legacy bundler baseline.

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

**Input:** "Our Vite build is slow and secrets leak into bundles."
**Output:** Plan with isolated environments, ordered pure plugins, and guarded assets with hidden sourcemaps.
