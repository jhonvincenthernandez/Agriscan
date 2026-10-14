---
name: define-enterprise-context
description: Execute a deep multi-phase enterprise interview to scaffold, populate, and maintain the 23 Enterprise Software Engineering Context domains (45 specification templates) into projects/<project-name>/context/software-engineering/. Run when establishing enterprise-grade agentic context, auditing documentation drift, or initializing production infrastructure and architectural specifications.
department: workflow
ownerAgent: gandalf
triggerCommand: /define-enterprise-context
antiPatternsPrevented:
  - AP-1
  - AP-3
  - AP-6
  - AP-11
  - AP-18
  - AP-26
  - AP-44
  - AP-45
---

# Define Enterprise Context

## 0. Identity

- **Role:** Master Planner. Owns enterprise discovery sequencing with approval gates before production hardening specs.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Master Planner).
- **Seniority bar:** Staff (Appendix B). Records why interview depth beats template filling (missed domains become incidents, rejected checkbox coverage) and why hardening follows discovery, never precedes it.
- **Authority:** Owns the enterprise context generation and audit lifecycle. Scaffolds verified templates from `context/software-engineering/` into `projects/<project-name>/context/software-engineering/`. Cannot mutate global framework rules or commit uncontained files to repository root.
- **Must not define:** Direct application feature code; global framework core files.
- **Normative base:** `core/fellowship/gandalf.md`, `core/fellowship/aragorn.md`, `rules/engineering/architecture-boundaries.md`, `references/anti-patterns.md`, and native templates in `context/software-engineering/`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-3 (no success criteria), AP-11 (forgotten context), AP-26 (no scope boundary), AP-44 (unlocked filesystem), and AP-45 (no human review trigger). Never write files to disk before the multi-phase deep interview protocol is executed and confirmed.

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                                                                               |
| --- | ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Task             | Conduct deep architectural interview, discover enterprise stack, and scaffold the 23 software engineering domains into project context.             |
| 2   | Target Tool      | Any agent runtime reading markdown skills: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.                                            |
| 3   | Output Format    | Structured project-scoped context tree (`projects/<project-name>/context/software-engineering/`) and executive audit summary in chat.               |
| 4   | Constraints      | Execute deep interview protocol via references. Require explicit confirmation before writing files. Zero root directory pollution.                  |
| 5   | Input            | User architectural requirements; codebase manifests; native templates from `context/software-engineering/`.                                         |
| 6   | Context          | Eliminates agent hallucination, architectural drift, security blindspots, and lack of domain governance in enterprise systems (AP-1, AP-26, AP-44). |
| 7   | Audience         | Enterprise architects, engineering leads, founders, and downstream fellowship agents building complex systems.                                      |
| 8   | Success Criteria | Multi-phase interview completed; 23 domain directories scaffolded with verified facts; user approval recorded.                                      |
| 9   | Examples         | See Section 10.                                                                                                                                     |

## 2. Trigger Matrix

| Trigger                                                                            | Fire? | Notes                                                    |
| ---------------------------------------------------------------------------------- | ----- | -------------------------------------------------------- |
| "Define enterprise context / scaffold enterprise architecture / setup 23 domains"  | YES   | Core trigger.                                            |
| "Bootstrap enterprise project context / audit documentation drift across 45 specs" | YES   | Core trigger.                                            |
| `/define-enterprise-context` or `/scaffold-enterprise-context`                     | YES   | Core trigger.                                            |
| Basic MVP brain dump for a simple app                                              | NO    | Route to `skills/workflow/define-core-domains/SKILL.md`. |
| Feature planning on an already scaffolded codebase                                 | NO    | Route to `skills/workflow/engineering-loop/SKILL.md`.    |

## 3. Execution Workflow

### Step 1: Project Scope & Repository Audit

- **Action:** Request or confirm the target project name (`projects/<project-name>/`). For existing (brownfield) repositories, inspect manifests (`package.json`, `Cargo.toml`, `go.mod`, `pyproject.toml`) and directory layout to detect existing stack components.
- **Input:** Target project name and workspace files.
- **Stop Condition:** If project name cannot be determined, halt and ask the user.
- **Validation:** Target directory established (`projects/<project-name>/context/software-engineering/`).

### Step 2: Enterprise Deep Interview Protocol

- **Action:** Execute the structured 4-phase interview per `skills/workflow/define-enterprise-context/references/interview-protocol.md`:
  - **Phase 1:** Project Identity & Core Architecture Tier (`architecture/`, `backend/`, `database/`, `decisions/`).
  - **Phase 2:** Platform, Cloud & Infrastructure Tier (`infrastructure/`, `deployment/`, `deployment-platform/`, `development/`, `developer-experience/`).
  - **Phase 3:** Security, Governance & Resilience Tier (`security/`, `governance-and-policy/`, `quality-and-compliance/`, `disaster-recovery/`, `cost-and-finops/`).
  - **Phase 4:** Extended Operations, AI & Data Tier (`data-engineering/`, `ai-and-ml/`, `integrations/`, `observability/`, `performance/`, `frontend/`, `mobile/`, `roadmap/`, `testing/`).
- **Input:** User responses to phase interview questions.
- **Stop Condition:** Do not skip phases. If answers are ambiguous, ask targeted follow-up questions before advancing.
- **Validation:** All relevant enterprise tiers clarified and confirmed.

### Step 3: Synthesis & Scaffolding Blueprint Gate

- **Action:** Present an executive blueprint summarizing the confirmed architecture, stack selections, and list of domain folders to be provisioned. Request explicit user approval.
- **Input:** Gathered facts from Step 2.
- **Stop Condition:** Halt and wait for user confirmation before writing or modifying any context files.
- **Validation:** Explicit human review recorded (AP-45 compliance).

### Step 4: Template Provisioning & Dynamic Expansion

- **Action:** Ensure `projects/<project-name>/context/software-engineering/` directory structure exists. Read native specification templates from `context/software-engineering/` and populate verified facts:
  - Inject confirmed architecture decisions, topology diagrams, models, and SLAs.
  - Strictly preserve `[PLACEHOLDER: ...]` markers for any open or undecided details.
  - **Dynamic Enterprise Expansion:** If the grilling interview surfaced specialized enterprise requirements (for example, multi-tenant isolation, fine-grained RBAC/ABAC matrices, gRPC contracts, horizontal sharding, or multi-region failover), dynamically generate and populate those specialized specification files under the corresponding domain directory per `references/context-domains.md` §5.
- **Input:** Approved blueprint, native baseline templates from `context/software-engineering/`, and confirmed enterprise expansion specs.
- **Stop Condition:** Stop if attempting to write outside `projects/<project-name>/context/`.
- **Validation:** All selected domain folders, baseline specs, and dynamic enterprise expansion files written cleanly inside the project directory.

### Step 5: Verification & Handoff Summary

- **Action:** Present the completion summary detailing scaffolded domain folders, total baseline specs, dynamic enterprise expansion specs created, remaining placeholders to populate, and recommended fellowship agents to proceed with development.
- **Input:** Provisioned directory state.
- **Stop Condition:** Output summary and await developer commands.
- **Validation:** Output matches Section 4 specification.

## 4. Output Specification

```markdown
# Enterprise Context Summary: [project-name]

Target Path: projects/[project-name]/context/software-engineering/
Audited Domains: 23 Total | Baseline Specs: [N]/45 | Enterprise Expanded Specs: [N]

## Provisioned Domain Folders:

- architecture/ ([system-architecture.md, component-topology.md, data-flow-and-runtime.md, + dynamic expansion specs])
- backend/ ([api-design-and-contracts.md, service-boundaries-and-logic.md, + dynamic expansion specs])
- database/ ([schema-and-data-models.md, data-lifecycle-and-integrity.md, + dynamic expansion specs])
- security/ ([auth-and-data-protection.md, security-and-threat-model.md, + dynamic expansion specs])
- [Additional provisioned domain directories...]

## Enterprise Expansion Specifications Generated:

- [domain]/[custom-enterprise-spec].md: [Purpose and architecture role]

## Locked Architectural Invariants:

- Topology: [e.g., Event-Driven Modular Monolith]
- Compute Runtime: [e.g., AWS EKS / Kubernetes]
- Recovery Targets: RTO: [< 1h] | RPO: [< 5m]

## Remaining Placeholders:

- [domain/spec.md]: [PLACEHOLDER details requiring further team sign-off]
```

## 5. Validation Gate

- [ ] Project-scoped directory established (`projects/<project-name>/context/software-engineering/`).
- [ ] 4-phase interview protocol from `skills/workflow/define-enterprise-context/references/interview-protocol.md` completed.
- [ ] Explicit user approval received prior to writing context files.
- [ ] All 23 domain directories utilize native templates from `context/software-engineering/`.
- [ ] Undecided facts retain exact `[PLACEHOLDER: ...]` syntax without fabricated data.
- [ ] Zero uncontained context sprawl in repository root.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Writing context files without conducting the deep interview protocol, or writing flat files in the root.
- **Over-execution threshold:** Generating application source code (`src/`), database migration scripts, or IaC terraform files during context definition.
- **Calibration default:** Keep all enterprise specifications contained within the target project's context directory.

## 7. Anti-Pattern Compliance

| Step | Prevents AP                 | Mechanism                                                                |
| ---- | --------------------------- | ------------------------------------------------------------------------ |
| 1    | AP-1 (vague task)           | Establishes explicit project name and repository audit baseline.         |
| 2    | AP-11 (forgotten context)   | Deep 4-phase interview captures non-negotiables across all 23 domains.   |
| 3    | AP-45 (no human review)     | Halts for explicit user approval before provisioning files.              |
| 4    | AP-44 (unlocked filesystem) | Gates file creation inside `projects/<project-name>/` only.              |
| 4    | AP-42 (no target state)     | Preserves `[PLACEHOLDER]` markers instead of inventing fake assumptions. |

## 8. Versioning & Changelog

- **Version:** 3.0.0
- **Changelog:**
  - `3.0.0` (2026-09-21) - Rebranded and upgraded to `define-enterprise-context`. Aligned with 23 enterprise domain folders and 45 specification templates from `context/software-engineering/`. Added external `skills/workflow/define-enterprise-context/references/interview-protocol.md` and project-scoped folder containment.
  - `2.0.0` (2026-08-31) - Initial enterprise skill release.

## 9. Portability Matrix

| Runtime     | Status   | Notes                                 |
| ----------- | -------- | ------------------------------------- |
| Claude Code | verified | Direct slash command execution.       |
| Cursor      | verified | Custom instructions & rules support.  |
| Copilot     | verified | Enterprise workspace context builder. |
| Windsurf    | verified | Cascade flow integration.             |
| Kiro        | verified | Steering model execution.             |
| Cline       | verified | Task step-by-step scaffolding flow.   |
| Raw API     | verified | Model-agnostic context domain engine. |

## 10. Examples

**Input:** "/define-enterprise-context for a multi-tenant fintech banking API called apex-pay."
**Output:** Agent triggers Phase 1 of `skills/workflow/define-enterprise-context/references/interview-protocol.md`, collects security, compliance (SOC2/PCI-DSS), database, and compute requirements, receives confirmation, and provisions the 23 domain directories in `projects/apex-pay/context/software-engineering/`.
