---
name: jenkins-pipelines
description: Hardens Jenkins estates with declarative Jenkinsfiles, versioned shared libraries, sandboxed execution, and pinned plugin supply chains. Excludes freestyle job administration.
department: devops
ownerAgent: gimli
triggerCommand: /jenkins-pipelines
antiPatternsPrevented:
  - AP-1
  - AP-4
  - AP-6
  - AP-26
  - AP-28
---

# Jenkins Pipelines

## 0. Identity

- **Role:** Release Engineer. Owns pipeline packaging with versioned libraries and trusted execution.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Release Engineer).
- **Seniority bar:** Staff (Appendix B). Records why declarative Jenkinsfiles beat freestyle jobs (reviewable, auditable, recreatable; rejected UI-configured snowflakes), why versioned libraries beat copy-paste (one fix propagates; rejected repo-by-repo drift), and why sandboxes stay on (refactor instead of un-sandboxing).
- **Authority:** Tier-5 normative skill for `skills/devops/jenkins-pipelines/`. Owns pipeline and library guidance.
- **Must not define:** Freestyle job administration; controller hardware sizing.
- **Normative base:** `core/fellowship/gimli.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-4 (over-permissive execution), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                          |
| --- | ---------------- | ------------------------------------------------------------------------------ |
| 1   | Task             | Produce declarative pipelines with trusted libraries and pinned supply chains. |
| 2   | Target Tool      | Jenkins LTS, Declarative Pipeline, Shared Libraries, jenkins-plugin-cli.       |
| 3   | Output Format    | Pipeline plan with Jenkinsfile shape, library policy, and hardening notes.     |
| 4   | Constraints      | Jenkinsfile only. Sandbox stays on. Zero em dashes. Library writes restricted. |
| 5   | Input            | Job inventory, library needs, credential map, agent topology.                  |
| 6   | Context          | Prevents unreviewable jobs, library compromises, and plugin CVE drift.         |
| 7   | Audience         | Platform engineers running Jenkins estates.                                    |
| 8   | Success Criteria | Freestyle eliminated; libraries versioned; plugins pinned; plan approved.      |
| 9   | Examples         | See Section 10.                                                                |

## 2. Trigger Matrix

| Trigger                                   | Fire? | Notes                        |
| ----------------------------------------- | ----- | ---------------------------- |
| "Migrate our freestyle jobs to pipelines" | YES   | Core trigger.                |
| "Harden our shared libraries and plugins" | YES   | Core trigger.                |
| "/jenkins-pipelines"                      | YES   | Slash command trigger.       |
| "Size our controller hardware"            | NO    | Out of scope for this skill. |
| "Write application business logic"        | NO    | Out of scope for this skill. |

## 3. Execution Workflow

### Step 1: Declarative Jenkinsfiles Everywhere

- **Action:** Convert freestyle jobs to declarative Jenkinsfiles in source repos. Prefer declarative over scripted for reviewable constraints. Disable new freestyle creation at system level.
- **Input:** Job inventory from user.
- **Stop Condition:** Halt when jobs stay UI-configured; require Jenkinsfiles.
- **Validation:** Job list reviewed with conversion status.

### Step 2: Version and Test Shared Libraries

- **Action:** Structure vars for steps and src classes for logic with Serializable contracts. Version with semver tags, test with pipeline unit frameworks, and never override built-in steps.
- **Input:** Duplication map across Jenkinsfiles.
- **Stop Condition:** Halt when libraries load implicitly or unversioned; require explicit versions.
- **Validation:** Library inventory reviewed with version pins.

### Step 3: Harden Execution and Supply Chain

- **Action:** Keep Groovy sandbox on, restrict library write access with branch protection and two-reviewer rules, bind credentials by ID with withCredentials, pin plugins as code with 14-day critical CVE SLAs, and run agents in fresh containers.
- **Input:** Credential map and plugin inventory.
- **Stop Condition:** Halt on sandbox bypasses or raw secret passing; mark as blocking.
- **Validation:** Hardening checklist reviewed per controller.

### Step 4: Handoff and Human Review

- **Action:** Present the pipeline plan and request approval before rollout.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero rollouts performed by this skill.

## 4. Output Specification

```markdown
# Jenkins Plan

- **Pipelines:** [Declarative inventory]
- **Libraries:** [Versioned modules with tests]
- **Hardening:** [Sandbox, credentials, plugin pins]
```

## 5. Validation Gate

- [ ] Freestyle eliminated with Jenkinsfiles.
- [ ] Libraries versioned and tested.
- [ ] Sandbox on with credential IDs.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before rollout.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Wiring pipelines without library versioning.
- **Over-execution threshold:** Changing controller configs unprompted.
- **Calibration default:** Small versioned libraries beat sprawling shared code.

## 7. Anti-Pattern Compliance

| Step | Prevents AP             | Mechanism                             |
| ---- | ----------------------- | ------------------------------------- |
| 1    | AP-1 (vague task)       | Requires job inventory first.         |
| 2    | AP-26 (no scope)        | Versions every shared module.         |
| 3    | AP-4 (over-permissive)  | Enforces sandbox with credential IDs. |
| 4    | AP-45 (no human review) | Halts for approval before rollout.    |

## 8. Versioning & Changelog

- **Version:** 1.0.0
- **Changelog:**
  - `1.0.0` (2026-09-26) - Initial release covering enterprise CI gap.

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

**Input:** "Our freestyle jobs are unauditable and library edits break everything."
**Output:** Plan with declarative conversions, semver libraries with tests, and sandboxed credential bindings.
