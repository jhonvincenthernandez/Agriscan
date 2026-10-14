---
name: git-reconciler
description: Reconciles merge conflicts with three-way analysis, lockfile regeneration, and test-gated commits. Excludes feature development inside merges.
department: devops
ownerAgent: samwise
triggerCommand: /git-reconciler
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-17
  - AP-18
  - AP-26
  - AP-52
---

# Git Reconciler

## 0. Identity

- **Role:** State Keeper. Owns repository state integrity through conflict resolution without contribution loss.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (State Keeper).
- **Seniority bar:** Staff (Appendix B). Records why intent synthesis beats side-picking (both branches may carry valid enhancements, rejected delete-theirs shortcuts), why lockfile regeneration beats manual resolution (deterministic graphs over hand edits, rejected hand-merged lockfiles), and why test gates precede every merge commit.
- **Authority:** Tier-5 normative skill for `skills/devops/git-reconciler/`. Owns reconciliation protocol.
- **Must not define:** Feature development inside merge commits.
- **Normative base:** `core/fellowship/samwise.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-17 (skipping tests), AP-18 (non-atomic commits), and AP-52 (fake fixes).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Resolve conflicts preserving both sides intent with verified merge commits.                    |
| 2   | Target Tool      | Git, npm, pnpm, uv, type checkers, test runners.                                               |
| 3   | Output Format    | Resolution report with synthesis notes and verification evidence.                              |
| 4   | Constraints      | Tests green before commit. Lockfiles regenerated. Zero em dashes.                              |
| 5   | Input            | Conflicted files, branch intents, lockfile types, test commands.                               |
| 6   | Context          | Prevents lost contributions and silent regressions from rushed resolutions.                     |
| 7   | Audience         | Engineers merging concurrent branch work.                                                       |
| 8   | Success Criteria | Zero markers remain; tests pass; merge commit atomic.                                          |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger                                      | Fire? | Notes                              |
| -------------------------------------------- | ----- | ---------------------------------- |
| "Resolve these merge conflicts"              | YES   | Core trigger.                      |
| "Fix our conflicted lockfile"                | YES   | Core trigger.                      |
| "/git-reconciler"                            | YES   | Slash command trigger.             |
| "Add features inside the merge"              | NO    | Out of scope; separate commits.    |
| "Rewrite branch history"                     | NO    | Out of scope without approval.     |

## 3. Execution Workflow

### Step 1: Analyze Three-Way Diffs

- **Action:** Parse ours, base, and theirs markers. Identify original intent per side relative to the common ancestor.
- **Input:** Conflicted files and branch context.
- **Stop Condition:** Halt when intent stays unreadable; ask owning authors.
- **Validation:** Intent notes recorded per conflict hunk.

### Step 2: Synthesize Without Loss

- **Action:** Merge non-conflicting enhancements from both sides. Regenerate lockfiles deterministically instead of hand-editing.
- **Input:** Intent notes from Step 1.
- **Stop Condition:** Halt before deleting teammate code; require synthesis.
- **Validation:** Both sides represented or explicitly superseded with reason.

### Step 3: Verify Before Commit

- **Action:** Scan for lingering markers, run type checks and full test suites, then stage and commit atomically.
- **Input:** Resolved working tree.
- **Stop Condition:** Halt on any marker or red test; require clean state.
- **Validation:** Zero markers with green suite evidenced.

### Step 4: Handoff and Human Review

- **Action:** Present the resolution report and request approval before pushing.
- **Input:** Completed resolution.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero pushes performed by this skill.

## 4. Output Specification

```markdown
# Reconciliation Report

- **Conflicts:** [Hunks with synthesis notes]
- **Lockfiles:** [Regeneration evidence]
- **Verification:** [Type and test results]
```

## 5. Validation Gate

- [ ] Intent recorded per hunk.
- [ ] Lockfiles regenerated, never hand-merged.
- [ ] Zero markers with green tests.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before push.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Committing resolutions without tests.
- **Over-execution threshold:** Adding features inside merge commits.
- **Calibration default:** Preserve both sides; delete with written reason only.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-1 (vague task)      | Requires intent notes per hunk.                     |
| 2    | AP-52 (fake fix)       | Bans teammate-code deletion.                        |
| 3    | AP-17 (skipping tests) | Gates commits on green suites.                      |
| 4    | AP-45 (no human review)| Halts for approval before push.                     |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with State Keeper role, role source, and seniority bar.
  - `1.0.0` - Legacy reconciliation baseline.

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

**Input:** "Main and feature conflict on configs plus lockfile."
**Output:** Resolution report with synthesized configs, regenerated lockfile, and green verification evidence.
