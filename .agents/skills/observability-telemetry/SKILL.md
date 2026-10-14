---
name: observability-telemetry
description: Instruments structured logging, distributed tracing, RED and USE metrics, OTel collection, SLO alerts, and PII scrubbing. Excludes vendor dashboards and pager rosters.
department: devops
ownerAgent: boromir
triggerCommand: /observability-telemetry
antiPatternsPrevented:
  - AP-1
  - AP-4
  - AP-26
  - AP-28
  - AP-44
---

# Observability Telemetry

## 0. Identity

- **Role:** Telemetry Auditor. Owns signal completeness with privacy-safe capture across services.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Telemetry Auditor).
- **Seniority bar:** Staff (Appendix B). Records why symptom-based SLO alerts beat CPU-blip pages (customer impact pages, rejected infrastructure noise), why cardinality caps beat label freedom (unbounded labels bankrupt backends, rejected user-id labels), and why scrubbed streams beat raw logs.
- **Authority:** Tier-5 normative skill for `skills/devops/observability-telemetry/`. Owns instrumentation guidance.
- **Must not define:** Third-party vendor APM dashboard visual layouts or incident pager rotation schedules.
- **Normative base:** `core/fellowship/boromir.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-4 (unscrubbed PII), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Produce instrumentation plans with logs, traces, metrics, alerts, and scrubbing.               |
| 2   | Target Tool      | OpenTelemetry, Prometheus, structured loggers, alert managers.                                 |
| 3   | Output Format    | Observability plan with signal specs, SLO alerts, and scrub rules.                             |
| 4   | Constraints      | JSON logs with trace ids. Cardinality capped. Zero em dashes. PII scrubbed.                    |
| 5   | Input            | Service inventory, SLO targets, compliance needs, incident history.                             |
| 6   | Context          | Prevents blind services, alert fatigue, and PII-laden telemetry.                                |
| 7   | Audience         | SREs and backend engineers instrumenting services.                                              |
| 8   | Success Criteria | Signals complete; alerts actionable; scrub verified; plan approved.                             |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger                                      | Fire? | Notes                              |
| -------------------------------------------- | ----- | ---------------------------------- |
| "Instrument our services end to end"         | YES   | Core trigger.                      |
| "Fix alert fatigue and noisy pages"          | YES   | Core trigger.                      |
| "/observability-telemetry"                   | YES   | Slash command trigger.             |
| "Design our vendor dashboards"               | NO    | Out of scope for this skill.       |
| "Set our pager rotation"                     | NO    | Out of scope for this skill.       |

## 3. Execution Workflow

### Step 1: Structure Logs and Traces

- **Action:** Emit JSON logs with envelope fields plus trace ids, propagate W3C context across HTTP and queues, and annotate spans with bounded domain attributes.
- **Input:** Service inventory from user.
- **Stop Condition:** Halt when trace continuity breaks at queue boundaries.
- **Validation:** Sample traces reviewed end to end.

### Step 2: Instrument Metrics with Caps

- **Action:** Apply RED for request services and USE for resources with standard counter, gauge, and histogram types. Cap cardinality by banning unbounded label values.
- **Input:** SLO targets from user.
- **Stop Condition:** Halt on user-id or raw-URL labels; require removal.
- **Validation:** Metric catalog reviewed with cardinality audit.

### Step 3: Alert on Symptoms and Scrub Streams

- **Action:** Page on SLO burn with runbook links, ticket the rest, and scrub PII and credentials at framework level before emission.
- **Input:** Incident history and compliance needs.
- **Stop Condition:** Halt when alerts lack runbooks or streams carry PII.
- **Validation:** Alert list reviewed with scrub verification.

### Step 4: Handoff and Human Review

- **Action:** Present the plan and request approval before wiring.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero wiring performed by this skill.

## 4. Output Specification

```markdown
# Observability Plan

- **Logs:** [JSON envelope with trace ids]
- **Metrics:** [RED and USE catalog]
- **Alerts:** [SLO pages with runbooks]
- **Scrub:** [PII rules verified]
```

## 5. Validation Gate

- [ ] Traces continuous across boundaries.
- [ ] Cardinality capped per metric.
- [ ] Alerts carry runbook links.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before wiring.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Shipping services without trace ids.
- **Over-execution threshold:** Wiring collectors unprompted.
- **Calibration default:** Symptom alerts first; infra signals second.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-1 (vague task)      | Requires service inventory first.                   |
| 2    | AP-26 (no scope)       | Caps cardinality per metric.                        |
| 3    | AP-44 (leaked secrets) | Scrubs PII before emission.                         |
| 4    | AP-45 (no human review)| Halts for approval before wiring.                   |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Telemetry Auditor role, role source, and seniority bar.
  - `1.0.0` - Legacy observability baseline.

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

**Input:** "Our pages fire on CPU blips and logs carry emails."
**Output:** Plan with SLO burn alerts, cardinality-capped metrics, and framework-level PII scrubbing.
