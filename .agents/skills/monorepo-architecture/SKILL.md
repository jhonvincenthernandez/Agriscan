---
name: monorepo-architecture
description: Monorepo design rules covering workspace boundaries, ownership mapping, affected builds, and versioning strategies. Excludes VCS hosting administration.
department: architecture
ownerAgent: aragorn
triggerCommand: /monorepo-architecture
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-26
  - AP-28
---

# Monorepo Architecture

## 0. Identity

- **Role:** System Architect. Owns repository shape with ownership boundaries and scalable builds.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (System Architect).
- **Seniority bar:** Staff (Appendix B). Records why affected-builds beat build-everything (CI minutes compound daily, rejected full-repo runs), why ownership files beat tribal knowledge (CODEOWNERS routes reviews automatically, rejected hallway routing), and why independent versioning beats lockstep releases.
- **Authority:** Tier-5 normative skill for `skills/architecture/monorepo-architecture/`. Owns workspace design guidance.
- **Must not define:** VCS hosting administration or migration execution.
- **Normative base:** `core/fellowship/aragorn.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                   |
| --- | ---------------- | --------------------------------------------------------------------------------------- |
| 1   | Task             | Produce monorepo layouts with ownership, affected builds, and versioning policy.        |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.        |
| 3   | Output Format    | Workspace blueprint with boundaries, build graph, and release notes.                    |
| 4   | Constraints      | Ownership explicit per path. Builds affected-only. Zero em dashes. Versioning declared. |
| 5   | Input            | Package inventory, team map, build times, release cadence.                              |
| 6   | Context          | Prevents unbuildable monoliths and ownerless directories.                               |
| 7   | Audience         | Architects consolidating repositories.                                                  |
| 8   | Success Criteria | Boundaries owned; builds scoped; plan approved.                                         |
| 9   | Examples         | See Section 10.                                                                         |

## 2. Trigger Matrix

| Trigger                                 | Fire? | Notes                                    |
| --------------------------------------- | ----- | ---------------------------------------- |
| "Consolidate our repos into a monorepo" | YES   | Core trigger.                            |
| "Fix 40-minute full-repo builds"        | YES   | Core trigger.                            |
| "/monorepo-architecture"                | YES   | Slash command trigger.                   |
| "Host our git servers"                  | NO    | Out of scope for this skill.             |
| "Migrate history this weekend"          | NO    | Out of scope; migration runbook owns it. |

## 3. Execution Workflow

### Step 1: Bound Workspaces by Team

- **Action:** Partition packages by owning team with CODEOWNERS coverage and public API surfaces per boundary.
- **Input:** Team map from user.
- **Stop Condition:** Halt on ownerless directories; require owners.
- **Validation:** Boundary map reviewed with owners.

### Step 2: Scope Builds to Affected

- **Action:** Wire dependency-graph-aware builds with remote caching so only changed packages and dependents rebuild and retest.
- **Input:** Build times from Step 1.
- **Stop Condition:** Halt when CI builds everything unconditionally.
- **Validation:** Build graph reviewed with timing evidence.

### Step 3: Version and Release Independently

- **Action:** Choose lockstep versus independent versioning per release line with changelog generation per package.
- **Input:** Release cadence from user.
- **Stop Condition:** Halt when versioning stays implicit.
- **Validation:** Release policy reviewed per line.

### Step 4: Handoff and Human Review

- **Action:** Present the workspace blueprint and request approval before migration.
- **Input:** Completed blueprint.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero migrations performed by this skill.

## 4. Output Specification

```markdown
# Workspace Blueprint

- **Boundaries:** [Team-owned map]
- **Builds:** [Affected graph with cache]
- **Releases:** [Versioning policy]
```

## 5. Validation Gate

- [ ] Boundaries owned per path.
- [ ] Builds affected-only with evidence.
- [ ] Versioning declared per line.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before migration.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Merging repos without ownership maps.
- **Over-execution threshold:** Migrating history unprompted.
- **Calibration default:** Boundaries first; tooling second.

## 7. Anti-Pattern Compliance

| Step | Prevents AP             | Mechanism                            |
| ---- | ----------------------- | ------------------------------------ |
| 1    | AP-1 (vague task)       | Requires team map first.             |
| 2    | AP-26 (no scope)        | Scopes builds per change.            |
| 3    | AP-28 (no stop)         | Declares versioning policy.          |
| 4    | AP-45 (no human review) | Halts for approval before migration. |

## 8. Versioning & Changelog

- **Version:** 1.0.0
- **Changelog:**
  - `1.0.0` (2026-09-26) - Initial release closing the workspace-design gap.

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

**Input:** "Twelve repos share copy-pasted code and CI takes an hour."
**Output:** Blueprint with team boundaries, affected builds, and independent release lines.
