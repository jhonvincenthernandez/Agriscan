---
name: enterprise-business
description: Root router and software engineering lifecycle dispatcher for Tier-5 Enterprise AI Agent Skills.
department: workflow
ownerAgent: gandalf
triggerCommand: /enterprise-business
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-18
  - AP-26
  - AP-28
---

# Enterprise Business Router & Lifecycle Dispatcher

## 0. Identity

- **Role:** Master Planner. Owns enterprise request sequencing with approval gates across lifecycle stages.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Master Planner).
- **Seniority bar:** Staff (Appendix B). Records why staged routing beats monolithic handling (each stage owns its quality bar, rejected god-router implementations) and why routers never execute.
- **Authority:** Tier-5 normative root skill for `skills/workflow/enterprise-business/`.
- **Purpose:** Provide deterministic prompt analysis, phase classification, and skill dispatch across all seven software engineering lifecycle phases without duplicating skill logic or violating scope boundaries.
- **Normative base:** `core/fellowship/gandalf.md`, `rules/engineering/architecture-boundaries.md`, `references/anti-patterns.md`, and project context in `projects/<project-name>/context/`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-4 (over-permissive agent), AP-26 (scope boundary violation), AP-28 (uncontrolled loops), AP-44 (unlocked filesystem), and AP-45 (no human review).

---

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                                          |
| :-- | :--------------- | :------------------------------------------------------------------------------------------------------------- |
| 1   | Task             | Inspect incoming prompts, classify software engineering lifecycle phase, and dispatch to specialist skill file |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, or raw API.                             |
| 3   | Output Format    | Structured JSON routing decision containing selected phase, skill path, rationale, and preflight status.      |
| 4   | Constraints      | Zero code modifications inside router. Zero assumptions on ambiguous prompts. Deterministic phase routing.     |
| 5   | Input            | User feature request, bug report, architecture query, deployment task, or audit intent.                        |
| 6   | Context          | Prevents uncoordinated agent execution, scope creep, and chaotic prompt processing across enterprise domains.  |
| 7   | Audience         | Downstream fellowship agents, developers, and engineering leads.                                               |
| 8   | Success Criteria | Exactly one lifecycle phase matched or clarification requested; valid specialist skill path emitted.           |
| 9   | Examples         | See Section 10.                                                                                                |

---

## 2. Trigger Matrix

| User Intent / Trigger Pattern                                          | Targeted Lifecycle Phase         | Target Skill File Path                                                                 |
| :--------------------------------------------------------------------- | :------------------------------- | :------------------------------------------------------------------------------------- |
| Demand validation, customer problem analysis, product interrogation    | `01-think-and-spec`              | `skills/workflow/enterprise-business/01-think-and-spec/interrogate-product-demand/SKILL.md`       |
| Feature specification, acceptance criteria, task breakdown             | `01-think-and-spec`              | `skills/workflow/enterprise-business/01-think-and-spec/write-feature-spec/SKILL.md`             |
| Design system creation, UI component tokens, layout guidelines         | `02-architecture-and-design`     | `skills/workflow/enterprise-business/02-architecture-and-design/design-system-architecture/SKILL.md`   |
| Codebase mapping, dependency graph, architectural context              | `02-architecture-and-design`     | `skills/workflow/enterprise-business/02-architecture-and-design/map-codebase-context/SKILL.md`         |
| Model latency benchmarking, LLM evaluation, throughput scoring         | `03-engineering-execution`       | `skills/workflow/enterprise-business/03-engineering-execution/benchmark-model-performance/SKILL.md`    |
| Systematic root cause analysis, stack trace diagnosis, bug fixing      | `03-engineering-execution`       | `skills/workflow/enterprise-business/03-engineering-execution/execute-root-cause-debugging/SKILL.md`   |
| Code refactoring, debt reduction, pattern modernization                | `03-engineering-execution`       | `skills/workflow/enterprise-business/03-engineering-execution/refactor-clean-code/SKILL.md`            |
| Pre-merge code review, static analysis, quality gate verification      | `03-engineering-execution`       | `skills/workflow/enterprise-business/03-engineering-execution/review-code-quality/SKILL.md`            |
| Core feature implementation, module creation, system coding            | `03-engineering-execution`       | `skills/workflow/enterprise-business/03-engineering-execution/write-code-implementation/SKILL.md`      |
| OWASP audit, security vulnerability scanning, STRIDE threat modeling   | `04-quality-and-testing`         | `skills/workflow/enterprise-business/04-quality-and-testing/audit-security-vulnerabilities/SKILL.md`  |
| Automated unit test creation, integration testing, E2E test suites     | `04-quality-and-testing`         | `skills/workflow/enterprise-business/04-quality-and-testing/author-automated-tests/SKILL.md`          |
| WCAG 2.1 AA audit, screen reader testing, accessibility verification   | `04-quality-and-testing`         | `skills/workflow/enterprise-business/04-quality-and-testing/verify-accessibility-compliance/SKILL.md` |
| Environment configuration, secrets validation, environment drift       | `05-release-and-ops`             | `skills/workflow/enterprise-business/05-release-and-ops/manage-environment-config/SKILL.md`            |
| Production release deployment, version tagging, PR merging             | `05-release-and-ops`             | `skills/workflow/enterprise-business/05-release-and-ops/ship-production-release/SKILL.md`              |
| Incident triage, production outage response, rollback execution        | `05-release-and-ops`             | `skills/workflow/enterprise-business/05-release-and-ops/triage-incident-response/SKILL.md`             |
| Technical documentation, Diataxis framework guides, API reference      | `06-documentation-and-knowledge` | `skills/workflow/enterprise-business/06-documentation-and-knowledge/author-technical-documentation/SKILL.md` |
| Research synthesis, retrospective analysis, knowledge extraction       | `06-documentation-and-knowledge` | `skills/workflow/enterprise-business/06-documentation-and-knowledge/synthesize-research-findings/SKILL.md`   |
| Financial business metrics audit, unit economics, SaaS KPI analysis    | `07-business-and-growth`         | `skills/workflow/enterprise-business/07-business-and-growth/audit-financial-business-metrics/SKILL.md` |
| Growth marketing copy, positioning narrative, landing page copy        | `07-business-and-growth`         | `skills/workflow/enterprise-business/07-business-and-growth/author-growth-marketing-copy/SKILL.md`     |
| Pre-meeting research brief, prospect background                        | `business-skills`                | `skills/workflow/enterprise-business/business-skills/client-brief/SKILL.md`                            |
| Call transcript extraction, action items derivation                    | `business-skills`                | `skills/workflow/enterprise-business/business-skills/meeting-notes/SKILL.md`                           |
| Visual meeting dashboard, stakeholder map                              | `business-skills`                | `skills/workflow/enterprise-business/business-skills/meeting-visualizer/SKILL.md`                      |
| Deal leverage, contract negotiation preparation                        | `business-skills`                | `skills/workflow/enterprise-business/business-skills/negotiation/SKILL.md`                             |
| Multi-agent team alignment, persona orchestration                      | `business-skills`                | `skills/workflow/enterprise-business/business-skills/the-team/SKILL.md`                                |

---

## 3. Execution Workflow

```
+---------------------------------------------------------+
| Step 1: Analyze Request & Extract Intent               |
+----------------------------+----------------------------+
                             |
                             v
+---------------------------------------------------------+
| Step 2: Classify Phase & Select Target Skill            |
+----------------------------+----------------------------+
                             |
                             v
+---------------------------------------------------------+
| Step 3: Verify Pre-Flight Gates & Scope Boundaries       |
+----------------------------+----------------------------+
                             |
                             v
+---------------------------------------------------------+
| Step 4: Dispatch Execution & Return Handoff Plan        |
+---------------------------------------------------------+
```

### Step 1: Analyze Request & Extract Intent

- **Action:** Extract core action verbs, domain targets, and constraints from the incoming prompt.
- **Input:** User prompt and workspace environment.
- **Stop Condition:** Halt and ask user if request is completely empty or unintelligible.
- **Validation:** Primary domain and task intent isolated.

### Step 2: Classify Phase & Select Target Skill

- **Action:** Cross-reference extracted keywords against Trigger Matrix. Map request to exactly one primary lifecycle phase and select corresponding target file path.
- **Input:** Extracted domain keywords.
- **Stop Condition:** If request spans multiple phases ambiguously, trigger clarification question.
- **Validation:** Exactly one specialist skill selected.

### Step 3: Verify Pre-Flight Gates & Scope Boundaries

- **Action:** Confirm target skill file exists on disk. Verify that all required pre-flight artifacts are available.
- **Input:** Target skill path and repository state.
- **Stop Condition:** Halt if pre-requisite artifacts are missing.
- **Validation:** Preflight status verified.

### Step 4: Dispatch Execution & Return Handoff Plan

- **Action:** Emit structured dispatch payload. Direct executing agent to load normative instructions inside selected skill file.
- **Input:** Validated routing decision.
- **Stop Condition:** Complete handoff payload emitted.
- **Validation:** JSON schema satisfied.

---

## 4. Output Specification

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SkillRoutingDecision",
  "type": "object",
  "required": [
    "status",
    "selected_phase",
    "target_skill_path",
    "rationale",
    "preflight_checks_passed"
  ],
  "properties": {
    "status": {
      "type": "string",
      "enum": ["DISPATCHED", "CLARIFICATION_REQUIRED", "UNSUPPORTED_INTENT"]
    },
    "selected_phase": {
      "type": "string",
      "enum": [
        "01-think-and-spec",
        "02-architecture-and-design",
        "03-engineering-execution",
        "04-quality-and-testing",
        "05-release-and-ops",
        "06-documentation-and-knowledge",
        "07-business-and-growth",
        "business-skills"
      ]
    },
    "target_skill_path": {
      "type": "string"
    },
    "rationale": {
      "type": "string"
    },
    "preflight_checks_passed": {
      "type": "boolean"
    }
  }
}
```

---

## 5. Validation Gate

Before completing dispatch, the router MUST verify:

- [ ] Exactly one primary skill file is selected for execution.
- [ ] Target skill file path exists on disk under `skills/workflow/enterprise-business/`.
- [ ] No code edits or file modifications executed by the router itself.
- [ ] Ambiguous intents resolved prior to selection.

---

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Guessing user intent and dispatching to coding without checking specifications.
- **Over-execution threshold:** Modifying source files or executing the task directly inside the router.
- **Calibration default:** Router only dispatches; specialist skills execute.

---

## 7. Anti-Pattern Compliance

| Anti-Pattern | Description | Correct Action |
| :--- | :--- | :--- |
| AP-1 (Vague task) | Vague user intent passed downstream | Resolve intent via clarifying options before dispatch |
| AP-4 (Over-permissive agent) | Executing actions outside routing scope | Confine router strictly to JSON dispatch decision |
| AP-26 (Scope creep) | Attempting multiple phase actions simultaneously | Process lifecycle phases sequentially |
| AP-28 (No stop condition) | Looping indefinitely on ambiguous intent | Limit clarification to single question then halt |

---

## 8. Versioning & Changelog

- **v5.1.0** (2026-09-21): Standardized paths, added Tier-5 validation gate, full 9-dimension intent model, and fellowship agent ownership.
- **v5.0.0** (2026-08-30): Initial enterprise company-suite router release.

---

## 9. Portability Matrix

| Agent Runtime | Supported | Integration Mechanism |
| :--- | :--- | :--- |
| Claude Code | Yes | Direct slash command `/enterprise-business` |
| Cursor | Yes | `.cursorrules` skill path reference |
| Windsurf | Yes | `.windsurfrules` directive integration |
| Copilot Workspace | Yes | Custom agent instruction path |
| Kiro | Yes | `.kiro/skills` definition link |
| Cline | Yes | System prompt skill directive |
| Raw API | Yes | Model-agnostic execution |

---

## 10. Examples

### Example 1: Security Audit Dispatch

- **User Request:** "Run an OWASP security scan on our payment service."
- **Routing Decision:**
  - Selected Phase: `04-quality-and-testing`
  - Target Skill Path: `skills/workflow/enterprise-business/04-quality-and-testing/audit-security-vulnerabilities/SKILL.md`
  - Rationale: Request explicitly targets vulnerability auditing and threat analysis.

### Example 2: Ambiguous Request Resolution

- **User Request:** "Make this feature better."
- **Routing Decision:**
  - Status: `CLARIFICATION_REQUIRED`
  - Action: Prompt user with options:
    - A) Refactor codebase implementation (`03-engineering-execution/refactor-clean-code/SKILL.md`)
    - B) Audit code quality and bugs (`03-engineering-execution/review-code-quality/SKILL.md`)
    - C) Improve user experience and design (`02-architecture-and-design/design-system-architecture/SKILL.md`)
