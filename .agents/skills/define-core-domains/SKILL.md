---
name: define-core-domains
description: Act as Principal Systems Architect and Product Manager to translate a founder's initial brain dump into production-ready project core domain files within a project-scoped context directory (for example projects/<project-name>/context/core-domains/). Execute this skill when the user provides an unstructured project idea or asks to establish project foundation specs, PRD, architecture, schemas, and task breakdown.
department: workflow
ownerAgent: gandalf
triggerCommand: /define-core-domains
antiPatternsPrevented:
  - AP-1
  - AP-3
  - AP-6
  - AP-18
  - AP-26
  - AP-44
---

# Define Core Domains

## 0. Identity

- **Role:** Master Planner. Owns decomposition of raw ideas into sequenced domain specifications with approval gates.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Master Planner).
- **Seniority bar:** Staff (Appendix B). Records why interview-first grounding beats code-first speed (unbuilt wrong things cost more, rejected premature implementation) and why scoped domains precede architecture.
- **Authority:** Owns the project core domain foundation workflow. Populates structured domain files from native templates under `context/core-domains/`. Cannot mutate global rules or framework core outside the target project folder.
- **Must not define:** Direct implementation code; IDE loading adapters (`runtime/`); global rule configurations (`rules/`).
- **Normative base:** `core/fellowship/gandalf.md`, `rules/engineering/architecture-boundaries.md`, `references/anti-patterns.md`, and directory templates in `context/core-domains/`.
- **Anti-pattern gate:** No step may trigger AP-1 (vague task), AP-3 (no success criteria), AP-26 (no scope boundary), AP-28 (no stop condition), AP-44 (unlocked filesystem), or AP-45 (no human review trigger). Never write to `context/core-domains/` before ambiguity is destroyed.

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                                                                                            |
| --- | ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Task             | Convert a brain dump into structured domain specifications in `projects/<project-name>/context/core-domains/` using native Sauron core domain templates.         |
| 2   | Target Tool      | Any agent runtime reading markdown skills: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.                                                         |
| 3   | Output Format    | Clean markdown domain files generated in a dedicated project directory, written in Spartan voice. Summary in chat; never dump entire file texts into chat.       |
| 4   | Constraints      | Never write before the 3-round interview completes. Store files in a dedicated project folder (`projects/<project-name>/context/core-domains/`). No root sprawl. |
| 5   | Input            | User's initial idea or brain dump; project name; native templates from `context/core-domains/`.                                                                  |
| 6   | Context          | Prevents ambiguity-driven hallucination, scope creep, and unorganized project workspace sprawl (AP-1, AP-12, AP-26, AP-42).                                      |
| 7   | Audience         | The project creator/founder (approval gate) and downstream engineering fellowship agents building the application.                                               |
| 8   | Success Criteria | All ambiguity resolved via 3-round interview; project folder created; core domain files populated; user approves the summary.                                    |
| 9   | Examples         | See Section 10.                                                                                                                                                  |

## 2. Trigger Matrix

| Trigger                                                                 | Fire? | Notes                                                   |
| ----------------------------------------------------------------------- | ----- | ------------------------------------------------------- |
| "Here is my idea: [brain dump]"                                         | YES   | Core trigger.                                           |
| "Establish the project foundation / define core domains / PRD / schema" | YES   | Core trigger.                                           |
| "Turn this idea into a buildable project specification"                 | YES   | Core trigger.                                           |
| `/define-core-domains` or `/define-foundation`                          | YES   | Core trigger.                                           |
| Incremental feature work on an existing project                         | NO    | Route to feature planning / implementation skills.      |
| "Design the UI mockups / aesthetic tuning"                              | NO    | Route to `skills/frontend/design-engineering/SKILL.md`. |

## 3. Execution Workflow

### Step 1: Project Scope & Core Goal Extraction

- **Action:** Request or confirm the target project name (kebab-case, for example `my-project`). Extract the core objective from the user's initial brain dump. Restate the goal in one sentence and present it for confirmation.
- **Input:** User initial prompt and project name.
- **Stop Condition:** If no project name is provided or the objective is incoherent, stop and ask the user to clarify.
- **Validation:** Target project directory established (`projects/<project-name>/context/core-domains/`) and one-sentence goal confirmed.

### Step 2: The Grilling Phase (3-Round Interview)

- **Action:** Execute the rigorous 3-round interview before drafting any specifications:
  - **Round 1 (Goal and Scope):** Primary problem solved, target user persona, core features vs out-of-scope capabilities.
  - **Round 2 (Constraints & Stack):** Tech stack preferences, database requirements, performance non-negotiables, external third-party API dependencies.
  - **Round 3 (Boundaries & Metrics):** MVP vs V2 cutoff line, key metric definitions, release criteria, security and compliance constraints.
- **Input:** Confirmed project goal and stack notes.
- **Stop Condition:** If the user attempts to skip a round, refuse and complete the interview. If critical dimensions remain ambiguous, ask targeted follow-up questions.
- **Validation:** All 3 interview rounds completed with zero unresolved ambiguities.

### Step 3: Project Folder Creation & Domain File Generation

- **Action:** Ensure directory `projects/<project-name>/context/core-domains/` exists. Read corresponding templates from `context/core-domains/` and populate them with verified project facts:
  - **Core Foundation Tier (Mandatory):**
    - `product-requirements.md` - Target personas, MVP user stories, V2 scope boundaries, success metrics.
    - `system-architecture.md` - System topology, component boundaries, layer isolation, tech stack.
    - `database-schema.md` - Data models, entity relationships, fields, indexing constraints.
    - `task-backlog.md` - Numbered, single-line executable implementation tasks tracing directly to MVP stories.
    - `engineering-rules.md` - Non-negotiable technical invariants, testing thresholds, error handling standards.
    - `design-system.md` - Visual tokens, typography hierarchy, responsive breakpoints, component states.
    - `glossary.md` - Ubiquitous domain language, entity definitions, acronyms.
  - **Extended & Operations Tier (As applicable):**
    - `api-contracts.md`, `testing-strategy.md`, `security-policies.md`, `infrastructure-config.md`, `deployment-workflows.md`, etc.
- **Input:** Interview answers; templates from `context/core-domains/`.
- **Stop Condition:** If a required domain template is missing, report the missing template. If any task in `task-backlog.md` does not map to an MVP story in `product-requirements.md`, resolve the discrepancy.
- **Validation:** All files written cleanly inside `projects/<project-name>/context/core-domains/`. Root directory remains uncluttered.

### Step 4: Final Review & Approval

- **Action:** Present a concise summary of the generated project context files and request human approval. Output file paths and structural bullet points; do not flood chat with raw file dumps.
- **Input:** Generated files under `projects/<project-name>/context/core-domains/`.
- **Stop Condition:** If the user requests modifications, adjust the specific domain files and re-present.
- **Validation:** Human approval recorded before skill completes.

## 4. Output Specification

```markdown
# Core Domains Summary: [project-name]

Target Path: projects/[project-name]/context/core-domains/

## product-requirements.md

- MVP Stories: [count] | V2 Stories: [count] | Core Metrics: [list]

## system-architecture.md

- Stack: [frontend, backend, database] | Topology: [monolith/microservices/serverless]

## database-schema.md

- Entities: [count] | Primary relations: [summary]

## task-backlog.md

- Total Executable Tasks: [count] | Traced to MVP: 100%

## Additional Domain Files Generated:

- engineering-rules.md, design-system.md, glossary.md, [api-contracts.md...]
```

## 5. Validation Gate

Run before declaring completion:

- [ ] Dedicated project directory created (`projects/<project-name>/context/core-domains/`).
- [ ] 3-round interview completed without skipped rounds.
- [ ] All generated domain files populate native templates from `context/core-domains/`.
- [ ] Every line item in `task-backlog.md` traces to an MVP story in `product-requirements.md`.
- [ ] Zero uncontained file sprawl in repository root.
- [ ] User approval recorded.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Writing domain files before completing the 3 interview rounds, dumping files directly in the root without a project folder, or using generic unstructured markdown.
- **Over-execution threshold:** Generating application source code (`src/`) or UI components during the domain definition phase.
- **Calibration default:** Keep domain files strictly scoped within the target project's context directory.

## 7. Anti-Pattern Compliance

| Step             | Prevents AP                          | Mechanism                                                   |
| ---------------- | ------------------------------------ | ----------------------------------------------------------- |
| 1 (Scope)        | AP-1, AP-26 (vague / scope boundary) | Establishes explicit project name and folder containment.   |
| 2 (Grilling)     | AP-11, AP-12 (forgotten context)     | 3-round interview captures non-negotiables and boundaries.  |
| 3 (Generation)   | AP-42, AP-44 (no target / file leak) | Generates standardized templates in project-scoped context. |
| 4 (Final review) | AP-45 (no human review trigger)      | Human approval gate before proceeding.                      |

## 8. Versioning & Changelog

- **Version:** 3.0.0
- **Changelog:**
  - `3.0.0` (2026-09-21) - Renamed from `define-foundation` to `define-core-domains`. Upgraded to use 23 modular templates in `context/core-domains/`. Enforced project-scoped directory structure (`projects/<project-name>/context/core-domains/`) to eliminate workspace clutter.
  - `2.0.0` (2026-08-08) - Elevated to Tier 5 specification.

## 9. Portability Matrix

| Runtime              | Status   | Notes                          |
| -------------------- | -------- | ------------------------------ |
| Claude Code          | verified | Direct command integration.    |
| Cursor               | verified | Rules and prompt support.      |
| Copilot              | verified | Custom instructions.           |
| Windsurf             | verified | Directive integration.         |
| Kiro                 | verified | Skill runner handoff.          |
| Cline                | verified | Executed in current workspace. |
| Raw API (no tooling) | verified | Model-agnostic execution.      |

## 10. Examples

**Input:** "Turn this idea into core domains: a real-time multiplayer whiteboard app called colab-canvas."

**Output:** Creates `projects/colab-canvas/context/core-domains/` containing `product-requirements.md`, `system-architecture.md`, `database-schema.md`, `task-backlog.md`, `engineering-rules.md`, `design-system.md`, and `glossary.md` derived from `context/core-domains/` templates.
