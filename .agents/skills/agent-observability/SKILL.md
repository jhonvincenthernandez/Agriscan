---
name: agent-observability
description: Traces agent turns, tool calls, token spend, and failures into per-developer dashboards with privacy-safe capture policy. Excludes model provider billing disputes.
department: ai-engineering
ownerAgent: boromir
triggerCommand: /agent-observability
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-26
  - AP-28
  - AP-45
---

# Agent Observability

## 0. Identity

- **Role:** Telemetry Auditor. Owns trace completeness and privacy-safe capture across agent fleets.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Telemetry Auditor).
- **Seniority bar:** Staff (Appendix B). Records why metadata-first capture beats full-content capture (most diagnoses need counts and spans, rejected secret-hoarding defaults), and why gateway enforcement beats hook telemetry for compliance proof.
- **Authority:** Tier-5 normative skill for `skills/ai-engineering/agent-observability/`. Owns trace schema and capture policy.
- **Must not define:** Model provider billing records; raw secret storage in traces.
- **Normative base:** `core/fellowship/boromir.md`, `rules/engineering/architecture-boundaries.md`, `references/anti-patterns.md`, and batch research on coding-agent tracing.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-26 (no scope boundary), AP-44 (unlocked data), and AP-45 (no human review trigger).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                    |
| --- | ---------------- | ---------------------------------------------------------------------------------------- |
| 1   | Task             | Define trace capture, cost dashboards, and failure replay for agent fleets.              |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.         |
| 3   | Output Format    | Observability plan with event schema, dashboards, alerts, and privacy rules.             |
| 4   | Constraints      | Metadata-first capture by default. Secrets redacted before export. Zero em dashes.       |
| 5   | Input            | Agent inventory, cost questions, failure pain points, privacy constraints.               |
| 6   | Context          | Prevents blind agent rollouts where spend and destructive actions stay invisible.        |
| 7   | Audience         | Platform leads and security auditors governing agent fleets.                             |
| 8   | Success Criteria | Dashboards answer cost per developer; failed sessions replay; privacy policy signed off. |
| 9   | Examples         | See Section 10.                                                                          |

## 2. Trigger Matrix

| Trigger                                            | Fire? | Notes                             |
| -------------------------------------------------- | ----- | --------------------------------- |
| "Track what our agents cost per developer"         | YES   | Core trigger.                     |
| "Replay failed agent sessions with tool timelines" | YES   | Core trigger.                     |
| "/agent-observability"                             | YES   | Slash command trigger.            |
| "Dispute our model provider invoice"               | NO    | Out of scope for this skill.      |
| "Store raw prompts with secrets in traces"         | NO    | Refused; violates capture policy. |

## 3. Execution Workflow

### Step 1: Define Cost and Failure Questions

- **Action:** Record the exact questions dashboards must answer: spend per developer, tool failure rate, and abandonment triggers with recent incident examples.
- **Input:** Stakeholder questions and recent incident examples.
- **Stop Condition:** Halt and ask when no concrete question exists.
- **Validation:** Question list recorded with dashboard mapping.

### Step 2: Specify Trace Schema and Hooks

- **Action:** Define turn, generation, tool span, token, skill tag, and status fields plus hook installation per agent. Tag turns with invoked skills for skill-level cost analysis.
- **Input:** Agent inventory from Step 1.
- **Stop Condition:** Halt when an agent lacks hook support; mark it as telemetry-only gap.
- **Validation:** Schema covers all agents or gaps are explicit.

### Step 3: Set Privacy and Alert Policy

- **Action:** Set metadata-only default, secret redaction rules, retention windows with deletion schedules, and threshold alerts for spend and failure spikes.
- **Input:** Privacy constraints from security lead.
- **Stop Condition:** Halt without sign-off on prompt capture; default stays metadata-only.
- **Validation:** Policy document signed off before any capture starts.

### Step 4: Handoff and Human Review

- **Action:** Present the observability plan with sample dashboards and request approval before enabling capture.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero capture enabled by this skill.

## 4. Output Specification

```markdown
# Observability Plan

- **Events:** [Schema fields per agent]
- **Dashboards:** [Cost, tool use, failure views]
- **Alerts:** [Thresholds with owners]
- **Privacy:** [Capture policy with sign-off]
```

## 5. Validation Gate

- [ ] Dashboard questions defined with mappings.
- [ ] Trace schema covers agents or gaps explicit.
- [ ] Privacy policy signed off with metadata default.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before capture.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Enabling trace capture without a privacy policy.
- **Over-execution threshold:** Storing raw secrets or full prompt dumps by default.
- **Calibration default:** Capture metadata first; expand to content only with sign-off.

## 7. Anti-Pattern Compliance

| Step | Prevents AP             | Mechanism                                   |
| ---- | ----------------------- | ------------------------------------------- |
| 1    | AP-1 (vague task)       | Requires concrete dashboard questions.      |
| 2    | AP-26 (no scope)        | Bounds schema per agent with explicit gaps. |
| 3    | AP-44 (unlocked data)   | Enforces redaction and retention policy.    |
| 4    | AP-45 (no human review) | Halts for approval before capture.          |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Telemetry Auditor role, role source, and seniority bar.
  - `1.0.0` (2026-09-26) - Initial release from AI engineering batch research.

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

**Input:** "Our team spend on agents tripled and nobody knows which workflow burns tokens."
**Output:** Observability plan with per-developer cost dashboard, tool failure view, and metadata-only capture policy.
