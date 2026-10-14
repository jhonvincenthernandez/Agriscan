---
name: embedding-drift-monitor
description: Detects embedding distribution and retrieval quality drift with re-index triggers and rollback notes. Excludes model retraining.
department: ai-engineering
ownerAgent: merry
triggerCommand: /embedding-drift-monitor
antiPatternsPrevented:
  - AP-1
  - AP-3
  - AP-6
  - AP-26
  - AP-28
---

# Embedding Drift Monitor

## 0. Identity

- **Role:** Quality Gatekeeper. Owns pass and fail verdicts on embedding health with threshold evidence.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Quality Gatekeeper).
- **Seniority bar:** Staff (Appendix B). Records why golden recall beats traffic dashboards (traffic looks healthy until users leave, rejected vanity monitoring), and why versioned baselines beat floating comparisons.
- **Authority:** Tier-5 normative skill for `skills/ai-engineering/embedding-drift-monitor/`. Owns drift signals and re-index policy.
- **Must not define:** Embedding model retraining; production index rebuilds.
- **Normative base:** `core/fellowship/merry.md`, `rules/engineering/architecture-boundaries.md`, `references/anti-patterns.md`, and retrieval operations practice.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-3 (no success criteria), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Define drift signals, thresholds, and re-index triggers for embedding pipelines.               |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.                |
| 3   | Output Format    | Monitor plan with signals, thresholds, alert routing, and re-index runbook.                    |
| 4   | Constraints      | Baseline window mandatory. Thresholds explicit per signal. Zero em dashes.                     |
| 5   | Input            | Embedding model, corpus cadence, golden query set, quality floor.                               |
| 6   | Context          | Prevents silent relevance decay after content shifts or model swaps.                            |
| 7   | Audience         | AI engineers owning retrieval quality in production.                                            |
| 8   | Success Criteria | Signals fire on injected drift; re-index path rehearsed; plan approved.                         |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger                                              | Fire? | Notes                              |
| ---------------------------------------------------- | ----- | ---------------------------------- |
| "Monitor our embeddings for drift"                   | YES   | Core trigger.                      |
| "Alert us when retrieval quality decays"             | YES   | Core trigger.                      |
| "/embedding-drift-monitor"                           | YES   | Slash command trigger.             |
| "Retrain our embedding model"                        | NO    | Out of scope for this skill.       |
| "Rebuild the production index now"                   | NO    | Out of scope; needs approval gate. |

## 3. Execution Workflow

### Step 1: Lock Baseline and Golden Set

- **Action:** Freeze a baseline embedding snapshot with a versioned golden query set carrying relevance labels. Pin exact model versions per index.
- **Input:** Current index and judged queries.
- **Stop Condition:** Halt and ask when golden labels are missing.
- **Validation:** Baseline and golden set versioned before monitoring.

### Step 2: Define Drift Signals

- **Action:** Set distribution signals (centroid movement, spread per domain) plus golden recall tracking with per-signal numeric thresholds and check cadence. Correlate signals with deploy markers.
- **Input:** Baseline from Step 1 and quality floor.
- **Stop Condition:** Halt when thresholds stay vague; require numbers.
- **Validation:** Signals recorded with thresholds and cadence.

### Step 3: Wire Alerts and Re-index Path

- **Action:** Route alerts to named owners, define re-index triggers with rollback snapshots taken before each run, and require post-migration golden verification.
- **Input:** On-call roster and index snapshot policy.
- **Stop Condition:** Halt when rollback snapshot is missing; require one.
- **Validation:** Runbook covers alert, trigger, re-index, and rollback.

### Step 4: Handoff and Human Review

- **Action:** Present the monitor plan and request approval before enabling.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero monitors enabled by this skill.

## 4. Output Specification

```markdown
# Drift Monitor Plan

- **Baseline:** [Snapshot with golden set version]
- **Signals:** [Thresholds with cadence]
- **Alerts:** [Routing with owners]
- **Re-index:** [Trigger with rollback notes]
```

## 5. Validation Gate

- [ ] Baseline versioned before monitoring.
- [ ] Thresholds explicit per signal.
- [ ] Alerts routed with owners.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before enabling.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Watching dashboards without golden recall tracking.
- **Over-execution threshold:** Rebuilding indexes or swapping models unprompted.
- **Calibration default:** Alert on golden recall first; distribution signals second.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-3 (no success)      | Versions baseline with golden labels.               |
| 2    | AP-26 (no scope)       | Bounds signals with thresholds.                     |
| 3    | AP-28 (no stop)        | Demands rollback snapshot.                          |
| 4    | AP-45 (no human review)| Halts for approval before enabling.                 |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Quality Gatekeeper role, role source, and seniority bar.
  - `1.0.0` (2026-09-26) - Initial release guarding retrieval quality.

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

**Input:** "Retrieval got worse after our docs migration and nobody alerted."
**Output:** Monitor plan with golden recall threshold, owner routing, and re-index trigger with rollback snapshot.
