---
name: performance-principles
description: Governs latency budgets, asset optimization, backend throughput, multi-tier caching, memory hygiene, and horizontal scalability. Excludes design tokens and billing budgets.
department: devops
ownerAgent: legolas
triggerCommand: /performance-principles
antiPatternsPrevented:
  - AP-1
  - AP-4
  - AP-26
  - AP-28
---

# Performance Principles

## 0. Identity

- **Role:** Diagnostic Analyst. Owns performance failure classification with budget evidence.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Diagnostic Analyst).
- **Seniority bar:** Staff (Appendix B). Records why budgets precede optimization (unbudgeted tuning optimizes noise, rejected vibes-based speedups), why measured profiles beat guessed hotspots, and why horizontal statelessness beats vertical hope.
- **Authority:** Tier-5 normative skill for `skills/devops/performance-principles/`. Owns performance guidance.
- **Must not define:** UI visual design tokens or infrastructure billing budgets.
- **Normative base:** `core/fellowship/legolas.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Produce performance plans with budgets, asset rules, backend tactics, and scale notes.         |
| 2   | Target Tool      | Profilers, flamegraphs, CDNs, Redis, load balancers, CI perf gates.                            |
| 3   | Output Format    | Performance plan with budgets, tactics per layer, and gate notes.                              |
| 4   | Constraints      | Budgets numeric per surface. Profiles before fixes. Zero em dashes.                            |
| 5   | Input            | Latency complaints, traffic shape, asset inventory, scaling targets.                            |
| 6   | Context          | Prevents premature optimization and unmeasured scaling spend.                                   |
| 7   | Audience         | Full-stack engineers owning responsiveness and throughput.                                      |
| 8   | Success Criteria | Budgets set; tactics evidenced; gates wired; plan approved.                                     |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger                                      | Fire? | Notes                              |
| -------------------------------------------- | ----- | ---------------------------------- |
| "Our pages and APIs are slow"                | YES   | Core trigger.                      |
| "Set performance budgets with CI gates"      | YES   | Core trigger.                      |
| "/performance-principles"                    | YES   | Slash command trigger.             |
| "Design our color tokens"                    | NO    | Out of scope for this skill.       |
| "Set our cloud billing budget"               | NO    | Out of scope for this skill.       |

## 3. Execution Workflow

### Step 1: Budget Every Surface

- **Action:** Set p95 under 200ms and p99 under 500ms for APIs plus LCP, INP, and CLS targets for pages. Wire CI regression flags before tuning anything.
- **Input:** Latency complaints and traffic shape.
- **Stop Condition:** Halt when budgets stay verbal; require numbers.
- **Validation:** Budget table recorded with gate wiring.

### Step 2: Slim Assets and Backends

- **Action:** Split bundles with dynamic imports, serve modern image formats with reserved space, push static assets behind immutable CDN caching, offload slow work to queues, batch database calls, and cap payloads with pagination plus compression.
- **Input:** Asset inventory from Step 1.
- **Stop Condition:** Halt when payloads stay unbounded; require caps.
- **Validation:** Asset and backend tactics reviewed per surface.

### Step 3: Cache, Free Memory, and Scale Out

- **Action:** Layer caches with explicit TTLs plus event invalidation and stampede guards. Release resources explicitly, stream large sets, and profile under load. Scale stateless services horizontally behind throttled gateways with breakers.
- **Input:** Scaling targets from user.
- **Stop Condition:** Halt when caches lack invalidation or growth stays unbounded.
- **Validation:** Cache, memory, and scale notes reviewed per tier.

### Step 4: Handoff and Human Review

- **Action:** Present the plan and request approval before implementation.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero changes made by this skill.

## 4. Output Specification

```markdown
# Performance Plan

- **Budgets:** [Numeric targets with gates]
- **Assets:** [Slimming tactics per surface]
- **Scale:** [Cache, memory, and horizontal notes]
```

## 5. Validation Gate

- [ ] Budgets numeric before tactics.
- [ ] Profiles evidence hotspots.
- [ ] Caches carry invalidation rules.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before implementation.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Tuning without budgets or profiles.
- **Over-execution threshold:** Rewriting systems for unmeasured gains.
- **Calibration default:** Measure first; budget second; tune third.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-1 (vague task)      | Requires numeric budgets first.                     |
| 2    | AP-26 (no scope)       | Caps payloads per surface.                          |
| 3    | AP-28 (no stop)        | Demands invalidation and scale notes.               |
| 4    | AP-45 (no human review)| Halts for approval before implementation.           |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Diagnostic Analyst role, role source, and seniority bar.
  - `1.0.0` - Legacy performance baseline.

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

**Input:** "Checkout p99 tripled after launch and images shift layout."
**Output:** Plan with 200ms budgets, split bundles with reserved space, batched queries, and TTL caches with invalidation.
