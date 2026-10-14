# Module Mapping Reference Guide

## Purpose

This guide maps project technology indicators, domains, and workspace profiles to matching Sauron capability suites, skills, and context templates.

---

## 1. Domain and Department Skill Mapping

| Project Category             | Technology Indicators                       | Recommended Sauron Department   | Key Skills to Provision                                                      | Context Templates Needed                                                 |
| ---------------------------- | ------------------------------------------- | ------------------------------- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| Full-Stack / Web App         | React, Next.js, Node.js, TypeScript, Vue    | `skills/frontend/` & `backend/` | `plan-feature`, `api-design`, `backend-patterns`, `react-modern-patterns`    | `projects/<project-name>/context/core-domains/` (or `engineering-loop/`) |
| Mobile Application           | React Native, Expo, iOS, Android            | `skills/frontend/`              | `mobile-react-native`, `react-native-best-practices`                         | `projects/<project-name>/context/core-domains/`                          |
| Design & UI Systems          | Tailwind, CSS Modules, Design Tokens, Figma | `skills/frontend/`              | `design-engineering`, `ui-snapshot-tokens`                                   | `design-system.md`, `design-tokens.md`                                   |
| Autonomous / Multi-Agent Dev | Long-running tasks, CLI agents, PR loops    | `skills/workflow/`              | `define-core-domains`, `engineering-loop`, `unified-memory-vault`, `caveman` | `projects/<project-name>/context/core-domains/`                          |
| Prompt & AI Engineering      | Model routing, system prompts, evaluation   | `skills/workflow/`              | `prompt-engineering/prompt-master-skill`, `define-enterprise-context`        | `projects/<project-name>/context/software-engineering/`                  |
| Enterprise & Business        | Workflows, enterprise architecture, SOC2    | `skills/workflow/`              | `define-enterprise-context`, `architecture-design`                           | `projects/<project-name>/context/software-engineering/`                  |
| Quality & Assurance          | Testing, TDD, fuzzing, load testing         | `skills/quality/`               | `tdd-workflow`, `e2e-testing`, `eval-harness`                                | `testing-strategy.md`, `quality-and-compliance/`                         |
| DevOps & Cloud               | Docker, Kubernetes, CI/CD, Terraform        | `skills/devops/`                | `ci-cd-pipeline-setup`, `cloud-run-service`, `bun-runtime`                   | `deployment/`, `infrastructure/`                                         |
| Security & Hardening         | Auth, OWASP, secrets, penetration testing   | `skills/security/`              | `security-auditor`, `security-review`, `vulnerability-scanner`               | `security/`                                                              |

---

## 2. Context Directory Provisioning Rules

All newly provisioned context templates belong strictly within project-scoped directories:

- **Standard Projects (Core):** `projects/<project-name>/context/core-domains/` derived from `context/core-domains/`.
- **Active Feature Loops:** `projects/<project-name>/context/engineering-loop/` derived from `context/engineering-loop/`.
- **Enterprise Multi-Domain Projects:** `projects/<project-name>/context/software-engineering/` derived from `context/software-engineering/`.

---

## 3. Tool-Specific Adaptation Guidelines

- **Claude Code:** Front-load intent, specify file bounds explicitly, use present-tense imperative instructions.
- **Cursor / Windsurf:** Define clear starting state, target state, explicit allowed/forbidden file paths.
- **Cline:** Enforce step validation, human review triggers before file writes, and clear stop conditions.
- **Reasoning Models:** Keep instructions short and direct. Do not add Chain of Thought scaffolding.

---

## 4. Adaptation to Existing (Brownfield) Projects

When applying Sauron to an existing codebase, follow these rules:

1. **Non-Destructive Audit:** Inspect existing `package.json`, build scripts, existing documentation, directory structures, and git commits. Never alter or overwrite existing application source code.
2. **Preserve Established Architecture:** Extract project patterns (such as folder structures, naming conventions, state management, database ORMs) and reflect them in the recommended context templates under `projects/<project-name>/context/`.
3. **Incremental Governance Setup:** Scaffold Sauron context files without deleting existing user documentation.
4. **Legacy Codebase Handling:** For repositories missing tests or strict type definitions, recommend `skills/quality/tdd-workflow` to establish test coverage before introducing large refactors.
