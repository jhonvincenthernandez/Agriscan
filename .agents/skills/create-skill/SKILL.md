---
name: create-skill
description: Interactively interviews the user to extract full requirements and scaffolds a Tier-5 compliant SKILL.md. Execute when user asks to "create a skill", "build a skill", "author a new skill", or "make a skill". Do NOT execute for editing code or writing one-off prompts.
department: workflow
ownerAgent: gandalf
triggerCommand: /create-skill
antiPatternsPrevented:
  - AP-1
  - AP-3
  - AP-6
  - AP-26
  - AP-28
---

# Create Skill

## 0. Identity

- **Role:** Master Planner. Owns interview sequencing with approval gates before skill scaffolding.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Master Planner).
- **Seniority bar:** Staff (Appendix B). Records why three interview rounds beat one-shot generation (requirements surface progressively, rejected assumption-filled drafts) and why audit gates precede every write.
- **Authority:** Owns skill authoring within `sauron/skills/<department>/<skill-name>/SKILL.md`.
- **Must not define:** Application production code; global runtime config changes.
- **Normative base:** `core/fellowship/gandalf.md`, `rules/engineering/architecture-boundaries.md`, `references/anti-patterns.md`, and local `skills/workflow/create-skill/references/skill-interview-protocol.md`.
- **Anti-pattern gate:** Never write `SKILL.md` without user completing interview rounds (AP-1, AP-3). Never omit validation gates or stop conditions (AP-28).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                |
| --- | ---------------- | ------------------------------------------------------------------------------------ |
| 1   | Task             | Conduct 3-round interview and output production-ready Tier-5 `SKILL.md`.             |
| 2   | Target Tool      | All 17 Sauron supported runtimes.                                                    |
| 3   | Output Format    | Normalized `SKILL.md` with single-line YAML frontmatter and standard sections.       |
| 4   | Constraints      | Maximum 4 questions per round. Must wait for user reply. Writing rules enforced.     |
| 5   | Input            | User intent, skill concept, interview answers.                                       |
| 6   | Context          | Prevents informal, incomplete, or anti-pattern polluted skills.                      |
| 7   | Audience         | Agent spec maintainers and AI agent harness adopters.                                |
| 8   | Success Criteria | Clean frontmatter, passes audit compliance, zero banned words, valid trigger matrix. |
| 9   | Examples         | See Section 10.                                                                      |

## 2. Trigger Matrix

| Trigger                           | Fire? | Notes                                          |
| --------------------------------- | ----- | ---------------------------------------------- |
| "Create a skill", "Build a skill" | YES   | Initiates 3-round interview protocol.          |
| "Make a new skill for X"          | YES   | Extracts X as initial context, starts Round 1. |
| One-off ad-hoc prompt request     | NO    | Not a reusable skill.                          |
| Edit application code             | NO    | Out of scope; delegate to Frodo.               |

## 3. Execution Workflow

### Step 1: Parse Prompt & Launch Round 1

- **Action:** Parse incoming concept. Ask Round 1 questions (Purpose, Department, Owner Agent, Command).
- **Input:** User prompt.
- **Stop Condition:** Stop and wait for user answers.
- **Validation:** 4 numbered questions presented.

### Step 2: Ingest Round 1 & Launch Round 2

- **Action:** Ingest answers. Formulate Round 2 questions (Triggers, Anti-triggers, File boundaries).
- **Input:** Round 1 answers.
- **Stop Condition:** Stop and wait for user answers.
- **Validation:** Specific boundaries clarified.

### Step 3: Ingest Round 2 & Launch Round 3

- **Action:** Ingest answers. Formulate Round 3 questions (Execution steps, Gates, Anti-patterns, References).
- **Input:** Round 2 answers.
- **Stop Condition:** Stop and wait for user answers.
- **Validation:** Quality criteria defined.

### Step 4: Scaffold and Write SKILL.md

- **Action:** Synthesize answers into standard 10-section Tier-5 schema with clean frontmatter. Write file to `sauron/skills/<department>/<name>/SKILL.md`.
- **Input:** All 3 rounds of answers.
- **Stop Condition:** File written to disk.
- **Validation:** Passes `scripts/audit-compliance.js`.

## 4. Output Specification

Target path: `sauron/skills/<department>/<skill-slug>/SKILL.md`

Format:

```markdown
---
name: <slug>
description: <Single-line clean description>
department: <department>
ownerAgent: <fellowship-agent>
triggerCommand: /<slug>
antiPatternsPrevented:
  - AP-1
  - AP-6
---

# Title

...
```

## 5. Validation Gate

- [ ] All 3 rounds of interview completed.
- [ ] Frontmatter contains single-line description and valid YAML.
- [ ] Zero banned words from writing rules.
- [ ] Trigger Matrix contains affirmative and negative triggers.
- [ ] Output written to correct department folder.

## 6. Anti-Patterns Enforced

- **AP-1 (Vague task):** Disallows skill generation without concrete task definition.
- **AP-3 (No success criteria):** Enforces Section 5 validation checklist in every generated skill.
- **AP-26 (No scope boundary):** Mandates explicit forbidden files and actions in Section 0.
- **AP-28 (No stop condition):** Requires explicit stop condition on every execution step.
