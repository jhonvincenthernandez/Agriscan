---
name: skill-name
description: "A clear, trigger-optimized sentence describing what this skill does, its department, and explicit exclusions."
department: architecture
ownerAgent: gandalf
triggerCommand: /command-name
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-18
  - AP-26
  - AP-28
---

# [Skill Title]

## 0. Identity

- **Role:** [Defines the skill's explicit operational role and job title]
- **Authority:** [Normative tier level and exact ownership boundaries within Sauron]
- **Must not define:** [Clear boundaries of what this skill does not own; cross-references to other skills/rules]
- **Normative base:** `core/fellowship/[ownerAgent].md`, `rules/engineering/architecture-boundaries.md`, `references/anti-patterns.md`, and applicable project context in `projects/<project-name>/context/`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-3 (no success criteria), AP-26 (no scope boundary), AP-28 (no stop condition), AP-44 (unlocked filesystem), and AP-45 (no human review trigger).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                  |
| --- | ---------------- | -------------------------------------------------------------------------------------- |
| 1   | Task             | [Explicit, measurable task statement]                                                  |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.       |
| 3   | Output Format    | [Structured deliverable format: Markdown, code diff, JSON, or chat summary]            |
| 4   | Constraints      | [Hard constraints: file bounds, tone, no em dashes, no banned words, zero root sprawl] |
| 5   | Input            | [Required inputs and files]                                                            |
| 6   | Context          | [Anti-patterns prevented and architectural context]                                    |
| 7   | Audience         | [Requesting developer, team leads, downstream fellowship agents]                       |
| 8   | Success Criteria | [Binary, testable verification conditions]                                             |
| 9   | Examples         | See Section 10.                                                                        |

## 2. Trigger Matrix

| Trigger                         | Fire? | Notes                                        |
| ------------------------------- | ----- | -------------------------------------------- |
| "[Exact user prompt trigger 1]" | YES   | Core trigger.                                |
| "[Exact user prompt trigger 2]" | YES   | Core trigger.                                |
| "/[command-name]"               | YES   | Slash command trigger.                       |
| "[Out of scope scenario 1]"     | NO    | Route to `skills/[department]/[other-skill]` |
| "[Out of scope scenario 2]"     | NO    | Out of scope.                                |

## 3. Execution Workflow

### Step 1: Input Validation & Context Discovery

- **Action:** Inspect inputs, verify parameters, and load required context without whole-repo scanning.
- **Input:** User prompt and workspace files.
- **Stop Condition:** Halt and ask user if required inputs are missing or ambiguous.
- **Validation:** Baseline parameters verified before execution begins.

### Step 2: Core Processing & Verification

- **Action:** Execute the specialized skill transformation or analysis.
- **Input:** Validated parameters and loaded context.
- **Stop Condition:** Halt if unexpected state or failure is detected.
- **Validation:** Step deliverables satisfy functional invariants.

### Step 3: Synthesis & Verification Gate

- **Action:** Check deliverable against Section 5 Validation Gate before presenting to user.
- **Input:** Generated artifact.
- **Stop Condition:** If validation checks fail, correct before proceeding.
- **Validation:** All criteria pass.

### Step 4: Handoff & Human Review

- **Action:** Present output summary and request explicit user review where required.
- **Input:** Final verified deliverable.
- **Stop Condition:** Await user command or next action.
- **Validation:** Human approval recorded.

## 4. Output Specification

```markdown
# [Deliverable Title]

- **Target:** [Path or scope]
- **Status:** [Status]
- **Summary:** [Dense, technical summary without conversational filler]
```

## 5. Validation Gate

- [ ] All inputs validated before execution.
- [ ] No uncontained files written outside project-scoped directories (`projects/<project-name>/`).
- [ ] Zero em dashes, banned words, or conversational padding in deliverables.
- [ ] Deliverable conforms strictly to Section 4 format.
- [ ] Explicit user confirmation recorded prior to destructive modifications.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Providing vague, unverified advice without inspecting code or context.
- **Over-execution threshold:** Modifying files outside the declared scope or executing tasks owned by other departments.
- **Calibration default:** Keep changes tightly scoped, deterministic, and traceable to explicit user requests.

## 7. Anti-Pattern Compliance

| Step | Prevents AP                | Mechanism                                                   |
| ---- | -------------------------- | ----------------------------------------------------------- |
| 1    | AP-1 (vague task verb)     | Enforces parameter validation and explicit context loading. |
| 2    | AP-26 (no scope boundary)  | Isolates execution to declared target domain.               |
| 3    | AP-3 (no success criteria) | Enforces deterministic validation gate checks.              |
| 4    | AP-45 (no human review)    | Halts for user confirmation prior to marking task complete. |

## 8. Versioning & Changelog

- **Version:** 1.0.0
- **Changelog:**
  - `1.0.0` (2026-09-21) - Initial enterprise Tier-5 standard release for Sauron.

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

**Input:** "[Sample user prompt]"
**Output:** [Concrete sample output demonstrating proper agent execution]

## Appendix A: Role Catalog (Normative)

Contributors select exactly one role verbatim from this catalog for Section 0.
A role states responsibility, boundary, and handoff in one line, following subagent design practice: name what the skill owns and name what it hands to neighbors. Never invent titles outside this list. Pair each role with its mapped ownerAgent.

### Architect family (ownerAgent: aragorn)

| Role title              | Remit                                                               | Must not define           |
| ----------------------- | ------------------------------------------------------------------- | ------------------------- |
| System Architect        | Owns system shape: components, boundaries, and recorded trade-offs. | Implementation code.      |
| API Designer            | Owns service contracts and versioning policy.                       | Backend business logic.   |
| Data Modeler            | Owns schema shapes and relationship rules.                          | Database administration.  |
| Retrieval Architect     | Owns index topology and query routing.                              | Embedding model training. |
| Decision Records Keeper | Owns architecture decision log completeness.                        | Product roadmap choices.  |

### Builder family (ownerAgent: frodo, gimli; Interface Builder also pairs with legolas for frontend construction)

| Role title        | Remit                                              | Must not define               |
| ----------------- | -------------------------------------------------- | ----------------------------- |
| Service Builder   | Owns service implementation within scoped files.   | Infrastructure provisioning.  |
| Interface Builder | Owns screen composition and interaction wiring.    | Backend APIs.                 |
| Mobile Builder    | Owns cross-platform screens and channel contracts. | Store release administration. |
| Pipeline Builder  | Owns staged data or delivery pipeline topology.    | Production traffic routing.   |
| Release Engineer  | Owns packaging, versioning, and rollback paths.    | Cluster administration.       |

### Precision family (ownerAgent: legolas)

| Role title         | Remit                                            | Must not define            |
| ------------------ | ------------------------------------------------ | -------------------------- |
| Syntax Reviewer    | Owns static correctness and style conformance.   | Feature design.            |
| Contract Enforcer  | Owns schema validity and call-policy compliance. | Tool business logic.       |
| Relevance Tuner    | Owns ranking quality measured on judged sets.    | Answer generation prompts. |
| Diagnostic Analyst | Owns failure classification with evidence spans. | Live system repairs.       |
| Output Optimizer   | Owns token budgets and compression levels with measured savings. | Model selection. |

### Quality family (ownerAgent: merry)

| Role title         | Remit                                                | Must not define      |
| ------------------ | ---------------------------------------------------- | -------------------- |
| Quality Gatekeeper | Owns pass and fail verdicts with threshold evidence. | Pipeline redesign.   |
| Eval Runner        | Owns metric collection and regression proof.         | Production rollouts. |
| Test Strategist    | Owns coverage plans matched to risk areas.           | Application code.    |

### Security family (ownerAgent: boromir)

| Role title        | Remit                                                | Must not define           |
| ----------------- | ---------------------------------------------------- | ------------------------- |
| Security Auditor  | Owns vulnerability findings with severity and proof. | Live exploitation.        |
| Compliance Mapper | Owns control-to-criterion traceability.              | Auditor opinions.         |
| Telemetry Auditor | Owns trace completeness and privacy-safe capture.    | Provider billing records. |

### Planning family (ownerAgent: gandalf)

| Role title           | Remit                                                | Must not define          |
| -------------------- | ---------------------------------------------------- | ------------------------ |
| Master Planner       | Owns decomposition, sequencing, and approval gates.  | Implementation code.     |
| Graph Designer       | Owns agent topology with checkpoints and interrupts. | Model provider choice.   |
| Context Steward      | Owns window budgets, maps, and compaction policy.    | Prompt wording style.    |
| Research Synthesizer | Owns multi-source intelligence with cited deltas.    | Production code changes. |
| Content Strategist   | Owns staged content lifecycles with audience-mapped outputs. | Product strategy. |

### State family (ownerAgent: samwise)

| Role title     | Remit                                             | Must not define         |
| -------------- | ------------------------------------------------- | ----------------------- |
| State Keeper   | Owns session state, commits, and handoff records. | Feature implementation. |
| Release Scribe | Owns changelog drafts traced to commits.          | Tag pushes.             |
| Docs Gardener  | Owns doc-to-code freshness with evidence.         | Feature code changes.   |
| Import Scout   | Owns migration previews with backup notice.       | Blind bulk rewrites.    |

### Chaos family (ownerAgent: pippin)

| Role title        | Remit                                               | Must not define            |
| ----------------- | --------------------------------------------------- | -------------------------- |
| Edge Prober       | Owns boundary and fuzz findings with reproductions. | Production traffic.        |
| Integration Scout | Owns external surface discovery and summaries.      | Credential-bearing writes. |
| MCP Specialist    | Owns MCP server inspection and resource mapping.    | Server administration.     |

### Catalog rules

- One skill carries exactly one catalog role. Splits mean two skills.
- Write the Role line as `**Role:** [Title]. [Remit adapted to the skill].`
- The Must-not-define column seeds the Section 0 boundary line.
- New titles require a template amendment. Propose the title, remit, and ownerAgent mapping first.

## Appendix B: Seniority Ladder (Informative)

Titles signal scope and autonomy, not just years. Contributors use this ladder to calibrate how deep a skill should reason. Skill files carry no seniority label; seniority shows in scope, trade-off records, and boundary discipline.

### Individual contributor track

| Level                         | Scope                                                                             | Autonomy marker                            |
| ----------------------------- | --------------------------------------------------------------------------------- | ------------------------------------------ |
| Junior (IC1-IC2)              | Executes scoped tasks with guidance.                                              | Needs task breakdowns from others.         |
| Mid-level (IC3)               | Owns features independently end to end.                                           | Ships without supervision inside a domain. |
| Senior (IC4)                  | Owns systems, mentors juniors, decides architecture inside a domain.              | Others seek their review on domain calls.  |
| Staff (IC5)                   | Multi-team impact through Tech Lead, Architect, Solver, or Right Hand archetypes. | Sets direction others execute.             |
| Principal (IC6)               | Organization-wide technical strategy across domains.                              | Decisions bind multiple teams.             |
| Distinguished / Fellow (IC7+) | Industry-level influence on practice and standards.                               | Work cited outside the company.            |

### Management track (for context, never skill roles)

Engineering Manager, Director, VP Engineering, CTO. Skills never take management titles because skills own technical remit, never people or org decisions.

### Ladder-to-skill mapping

- Principle skills (Tier-3 style) encode Senior judgment: concrete versioned rules a senior applies without deliberation.
- Orchestration skills (Tier-5 planning, multi-agent, governance) encode Staff judgment: recorded trade-offs, rejected alternatives, and cross-team boundaries.
- A skill that only lists steps without trade-off reasoning reads Junior. A skill that records why alternatives lost reads Staff. Write toward the higher bar.
