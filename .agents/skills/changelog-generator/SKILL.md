---
name: changelog-generator
description: Drafts release changelogs from conventional commits with breaking-change callouts and migration notes. Excludes tag pushes.
department: workflow
ownerAgent: samwise
triggerCommand: /changelog-generator
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-18
  - AP-26
  - AP-28
---

# Changelog Generator

## 0. Identity

- **Role:** Release Scribe. Owns changelog drafts traced to commits with migration notes.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Release Scribe).
- **Seniority bar:** Staff (Appendix B). Records why generated notes beat hand-written archaeology (history never forgets, rejected release-week digs), why breaking changes lead every surface (migration urgency, rejected buried breakage), and why hosted pages serve users while repo files serve engineers.
- **Authority:** Tier-5 normative skill for `skills/workflow/changelog-generator/`. Owns draft notes and grouping.
- **Must not define:** Tag creation or pushes; version number decisions.
- **Normative base:** `core/fellowship/samwise.md`, `rules/engineering/architecture-boundaries.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-18 (stale history), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Draft grouped changelogs with highlights, breaking changes, and migration notes per release.   |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.                |
| 3   | Output Format    | Changelog draft with sections, links, and upgrade notes.                                       |
| 4   | Constraints      | Commits are the source of truth. Breaking changes called out first. Zero em dashes.            |
| 5   | Input            | Commit range, prior tag, grouping rules, audience notes.                                        |
| 6   | Context          | Prevents empty releases and surprise breaking changes buried in notes.                          |
| 7   | Audience         | Maintainers publishing user-facing releases.                                                    |
| 8   | Success Criteria | Notes group cleanly; breaking changes lead; draft approved before publish.                      |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger                                          | Fire? | Notes                              |
| ------------------------------------------------ | ----- | ---------------------------------- |
| "Draft changelog for this release"               | YES   | Core trigger.                      |
| "Summarize breaking changes since v2"            | YES   | Core trigger.                      |
| "/changelog-generator"                           | YES   | Slash command trigger.             |
| "Tag and push the release now"                   | NO    | Out of scope; release flow owns it.|
| "Decide our next version number"                 | NO    | Owner decision, not this skill.    |

## 3. Execution Workflow

### Step 1: Collect Commit Range

- **Action:** Gather commits since the prior tag with conventional type parsing and linked PR references.
- **Input:** Range and prior tag.
- **Stop Condition:** Halt and ask when the range boundary stays ambiguous.
- **Validation:** Commit list complete before drafting.

### Step 2: Group and Highlight

- **Action:** Group by features, fixes, performance, and chores. Elevate user-facing highlights and breaking changes with migration notes to the lead.
- **Input:** Parsed commits from Step 1.
- **Stop Condition:** Halt when grouping hides a breaking change; promote it.
- **Validation:** Breaking changes lead the draft with migration notes.

### Step 3: Draft Notes with Links

- **Action:** Write concise entries with commit and PR links plus upgrade steps where behavior changes. Split engineer and customer views where audiences differ.
- **Input:** Grouped commits from Step 2.
- **Stop Condition:** Halt when an entry lacks verifiable source; drop or mark it.
- **Validation:** Every entry traces to a commit.

### Step 4: Handoff and Human Review

- **Action:** Present the draft and request approval before publishing.
- **Input:** Completed draft.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero tags pushed by this skill.

## 4. Output Specification

```markdown
# Changelog Draft

- **Highlights:** [Top user-facing changes]
- **Breaking:** [Changes with migration notes]
- **Sections:** [Grouped entries with links]
```

## 5. Validation Gate

- [ ] Range boundary explicit before drafting.
- [ ] Breaking changes lead with migration notes.
- [ ] Every entry traces to a commit.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before publish.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Publishing notes without commit traceability.
- **Over-execution threshold:** Tagging or pushing releases unprompted.
- **Calibration default:** Short entries with links beat long prose.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-1 (vague task)      | Requires explicit range boundary.                   |
| 2    | AP-26 (no scope)       | Promotes breaking changes to lead.                  |
| 3    | AP-18 (stale state)    | Traces entries to commits.                          |
| 4    | AP-45 (no human review)| Halts for approval before publish.                  |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Release Scribe role, role source, and seniority bar.
  - `1.0.0` (2026-09-26) - Initial release for release notes flow.

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

**Input:** "Draft notes for v1.3.0 from commits since v1.2.0."
**Output:** Draft with highlights, breaking section with migration steps, and linked entries.
