---
name: unified-memory-vault
description: Cross-agent context sharing, inspectable handoff contracts, and portable memory persistence across multiple AI harnesses with scoped vaults and fail-closed isolation.
department: workflow
ownerAgent: samwise
triggerCommand: /unified-memory-vault
antiPatternsPrevented:
  - AP-1
  - AP-4
  - AP-18
  - AP-26
  - AP-28
  - AP-53
---

# Unified Memory Vault

## 0. Identity

- **Role:** State Keeper. Owns durable session state with scoped, secret-free persistence.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (State Keeper).
- **Seniority bar:** Staff (Appendix B). Records why tiered vaults beat single stores (project, team, and user scopes separate cleanly, rejected flat memory dumps), why recall stays evidence (verification precedes decisions, rejected memory-as-truth), and why secrets never enter vaults.
- **Authority:** Tier-5 normative skill for cross-session and cross-harness memory under `skills/workflow/unified-memory-vault/`.
- **Must not define:** Application database migrations or business rules.
- **Normative base:** `core/fellowship/samwise.md`, `core/fellowship/frodo.md`, `rules/engineering/architecture-boundaries.md`, and `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-26 (leaking secrets in context) and AP-53 (treating recalled memory as unquestioned fact).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Store, search, recall, and hand off structured agent context across sessions.                  |
| 2   | Target Tool      | Sauron Fellowship agents, Claude Code, Codex, Cursor, Windsurf, Antigravity.                    |
| 3   | Output Format    | Markdown documents adhering to portable vault schemas with metadata frontmatter.                |
| 4   | Constraints      | Banish passwords and tokens. Scopes must fail-closed. Recalled text is evidence, not certainty. |
| 5   | Input            | Task summaries, verified test outcomes, architecture decisions, unresolved questions.           |
| 6   | Context          | Prevents context loss between handoffs, repetitive re-discovery, and contradictory actions.    |
| 7   | Audience         | Autonomous agents, pair programming engineers, multi-agent coordinators.                        |
| 8   | Success Criteria | 100 percent verifiable handoff packages; zero secret leaks; fail-closed gitignore protection.   |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger Condition                                        | Fire? | Action / Route                                        |
| -------------------------------------------------------- | ----- | ----------------------------------------------------- |
| Handing off task state to another agent or session       | YES   | Generate structured handoff markdown in vault.        |
| Resuming multi-phase project and searching prior choices | YES   | Execute scoped search across project and team vaults. |
| Storing transient debug logs or oversized process traces | NO    | Reject; store only distilled, high-signal findings.   |
| Managing application database migrations                 | NO    | Route to `skills/database/database-migration/`.       |

## 3. Execution Workflow

### Step 1: Recall Before Acting

- **Action:** Query project then team vaults for prior decisions, timestamp observations, and verify claims against current files and tests.
- **Input:** Task topic from user.
- **Stop Condition:** Halt on unreadable vaults or missing permissions; repair first.
- **Validation:** Findings synthesized with timestamps; secrets absent.

### Step 2: Scope Writes Correctly

- **Action:** Store project-local state in repo vaults, shared knowledge in team vaults after review, and operator specifics in user vaults. Never persist hypotheses as facts.
- **Input:** Session outputs from Step 1.
- **Stop Condition:** Halt when unverified claims present as confirmed.
- **Validation:** Vault writes scoped with frontmatter metadata.

### Step 3: Hand Off with Contracts

- **Action:** Author handoff packages stating objective, progress, executed commands, modified files, blockers, and the single next step.
- **Input:** Session completion state.
- **Stop Condition:** Halt on missing next actions or file paths.
- **Validation:** Handoff includes explicit next actions.

### Step 4: Handoff and Human Review

- **Action:** Present vault writes for team-scope review and request approval where required.
- **Input:** Completed vault updates.
- **Stop Condition:** Await user approval on team scope.
- **Validation:** Approval recorded; secrets verified absent.

## 4. Output Specification

```markdown
# Vault Update

- **Recall:** [Synthesized findings]
- **Writes:** [Scoped documents]
- **Handoff:** [Contract package]
```

## 5. Validation Gate

- [ ] Recall verified against current state.
- [ ] Writes scoped per tier.
- [ ] Zero secrets persisted.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded for team scope.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Acting without vault recall.
- **Over-execution threshold:** Persisting unverified claims as facts.
- **Calibration default:** Distilled findings only; traces stay out.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-53 (blind trust)    | Verifies recall against files.                      |
| 2    | AP-26 (leaked secrets) | Bans credentials per tier.                          |
| 3    | AP-1 (vague task)      | Contracts handoffs explicitly.                      |
| 4    | AP-45 (no human review)| Gates team scope on approval.                       |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with State Keeper role, role source, and seniority bar.
  - `1.0.0` - Legacy vault baseline.

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

**Input:** "Resume the auth migration from last session."
**Output:** Recalled decisions with timestamps, verified current state, and contracted next step.
