---
name: prometheus-grafana
description: Operates Prometheus and Grafana with cardinality discipline, recording rules, SLO alerts, and dashboard standards. Excludes vendor APM administration.
department: devops
ownerAgent: boromir
triggerCommand: /prometheus-grafana
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-26
  - AP-28
---

# Prometheus Grafana

## 0. Identity

- **Role:** Telemetry Auditor. Owns metric completeness with cost-bounded cardinality.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Telemetry Auditor).
- **Seniority bar:** Staff (Appendix B). Records why recording rules beat repeated heavy queries (compute once, read many; rejected dashboard-driven load), why cardinality caps beat label freedom (unbounded labels bankrupt backends, rejected user-id labels), and why symptom alerts beat CPU pages.
- **Authority:** Tier-5 normative skill for `skills/devops/prometheus-grafana/`. Owns metrics and alerting guidance.
- **Must not define:** Vendor APM administration; pager rotation schedules.
- **Normative base:** `core/fellowship/boromir.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Produce metric pipelines with capped cardinality, precomputed rules, and actionable alerts.     |
| 2   | Target Tool      | Prometheus, Grafana, Alertmanager, Mimir, Thanos.                                              |
| 3   | Output Format    | Monitoring plan with metric catalog, rules, alerts, and dashboard notes.                       |
| 4   | Constraints      | Cardinality budgeted. Recording rules named conventionally. Zero em dashes. Alerts carry runbooks. |
| 5   | Input            | Service inventory, SLO targets, retention needs, incident history.                              |
| 6   | Context          | Prevents cardinality explosions, noisy pages, and unqueryable retention gaps.                   |
| 7   | Audience         | SREs and backend engineers operating metrics stacks.                                            |
| 8   | Success Criteria | Cardinality bounded; rules precompute; alerts actionable; plan approved.                        |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger                                      | Fire? | Notes                              |
| -------------------------------------------- | ----- | ---------------------------------- |
| "Fix our cardinality explosion"              | YES   | Core trigger.                      |
| "Make alerts actionable with runbooks"       | YES   | Core trigger.                      |
| "/prometheus-grafana"                        | YES   | Slash command trigger.             |
| "Administer our vendor APM"                  | NO    | Out of scope for this skill.       |
| "Set our pager rotation"                     | NO    | Out of scope for this skill.       |

## 3. Execution Workflow

### Step 1: Budget Cardinality First

- **Action:** Inventory series per metric, ban unbounded label values, drop unqueried exporter output, and set head-series alerts with ownership.
- **Input:** Metric inventory from user.
- **Stop Condition:** Halt on user-id labels; require removal.
- **Validation:** Cardinality budget recorded with alert threshold.

### Step 2: Precompute with Recording Rules

- **Action:** Move repeated heavy expressions into conventionally named recording rules. Separate recording design from alerting intent.
- **Input:** Dashboard and alert query inventory.
- **Stop Condition:** Halt when dashboards recompute shared expressions live; require rules.
- **Validation:** Rule catalog reviewed with naming audit.

### Step 3: Alert on Symptoms with Runbooks

- **Action:** Write rate-based alerts with pending periods, error-state handling, and runbook links. Route via Alertmanager with grouping and dedup. Size retention with remote-write or federation per need.
- **Input:** SLO targets and incident history.
- **Stop Condition:** Halt on alerts without runbooks or pending periods.
- **Validation:** Alert list reviewed with routing proof.

### Step 4: Handoff and Human Review

- **Action:** Present the monitoring plan and request approval before rollout.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero rollouts performed by this skill.

## 4. Output Specification

```markdown
# Monitoring Plan

- **Cardinality:** [Budget with head alert]
- **Rules:** [Recording catalog]
- **Alerts:** [Symptom rules with runbooks]
- **Retention:** [Local plus remote policy]
```

## 5. Validation Gate

- [ ] Cardinality budgeted with alert.
- [ ] Recording rules named conventionally.
- [ ] Alerts carry runbooks with pending.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before rollout.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Adding metrics without cardinality budget.
- **Over-execution threshold:** Reconfiguring production monitoring unprompted.
- **Calibration default:** Fewer, better metrics over exhaustive collection.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-1 (vague task)      | Requires metric inventory first.                    |
| 2    | AP-26 (no scope)       | Caps cardinality per metric.                        |
| 3    | AP-28 (no stop)        | Demands runbooks with pending.                      |
| 4    | AP-45 (no human review)| Halts for approval before rollout.                  |

## 8. Versioning & Changelog

- **Version:** 1.0.0
- **Changelog:**
  - `1.0.0` (2026-09-26) - Initial release covering metrics stack gap.

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

**Input:** "Our Prometheus OOMs monthly and pages fire on CPU blips."
**Output:** Plan with cardinality budget, recording rules, symptom alerts with runbooks, and remote-write retention.
