---
name: cloudflare-workers-edge
description: Builds Cloudflare Workers and edge services with routing, KV and D1 bindings, and cold-start discipline. Excludes origin server builds.
department: devops
ownerAgent: gimli
triggerCommand: /cloudflare-workers-edge
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-18
  - AP-26
  - AP-28
---

# Cloudflare Workers Edge

## 0. Identity

- **Role:** Release Engineer. Owns edge deployment packaging with binding contracts and cost guards.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Release Engineer).
- **Seniority bar:** Staff (Appendix B). Records why bindings beat REST calls from workers (zero hops and zero auth overhead, rejected in-worker API calls), why generated Env types beat hand-written ones (drift fails at compile time, rejected manual interfaces), and why queues own background work (request path stays thin, rejected fat handlers).
- **Authority:** Tier-5 normative skill for `skills/devops/cloudflare-workers-edge/`. Owns worker routing and binding guidance.
- **Must not define:** Origin application servers; DNS zone administration as default path.
- **Normative base:** `core/fellowship/gimli.md`, `rules/engineering/architecture-boundaries.md`, `references/anti-patterns.md`, and edge compute practice.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-18 (stale state), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Produce worker designs with routes, bindings, caching, and failure fallbacks.                  |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.                |
| 3   | Output Format    | Edge blueprint with routes, bindings, cache rules, and fallback paths.                         |
| 4   | Constraints      | CPU limits respected. Secrets in vault bindings. Zero em dashes. Origin fallback mandatory.    |
| 5   | Input            | Traffic shape, state needs, cache targets, secret list, latency budget.                         |
| 6   | Context          | Prevents edge logic that assumes node APIs or durable local state.                              |
| 7   | Audience         | Platform engineers shipping edge services.                                                      |
| 8   | Success Criteria | Routes bound; cache hit path defined; fallback proven on paper; blueprint approved.             |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger                                        | Fire? | Notes                              |
| -------------------------------------------- | ----- | ---------------------------------- |
| "Move our auth check to Cloudflare Workers"    | YES   | Core trigger.                      |
| "Fix cold starts and cache misses at edge"     | YES   | Core trigger.                      |
| "/cloudflare-workers-edge"                     | YES   | Slash command trigger.             |
| "Build our origin API server"                  | NO    | Out of scope for this skill.       |
| "Manage our DNS zones"                         | NO    | Out of scope by default.           |

## 3. Execution Workflow

### Step 1: Classify Edge versus Origin Work

- **Action:** Split request handling into edge-safe units and origin-only units with latency reasons per split. Bound Durable Object throughput per atom with SQLite backends.
- **Input:** Traffic shape and state needs.
- **Stop Condition:** Halt and ask when state requirements stay unclear.
- **Validation:** Split table complete before routing design.

### Step 2: Bind Routes, KV, and D1

- **Action:** Define route patterns, KV namespaces, D1 databases, and vault bindings. Generate Env types from configuration and test inside the workers runtime.
- **Input:** Split table from Step 1.
- **Stop Condition:** Halt when secrets target plain vars; require vault bindings.
- **Validation:** Binding table reviewed with secret scope.

### Step 3: Set Cache, Queues, and Fallback

- **Action:** Write cache rules per route, move retriable work to Queues and durable flows to Workflows, cap CPU per invocation, and define origin fallback with error pages.
- **Input:** Cache targets and latency budget.
- **Stop Condition:** Halt when a critical route lacks fallback; require one.
- **Validation:** Fallback paths rehearsed on paper.

### Step 4: Handoff and Human Review

- **Action:** Present the blueprint and request approval before deployment.
- **Input:** Completed blueprint.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero deploys performed.

## 4. Output Specification

```markdown
# Edge Blueprint

- **Split:** [Edge versus origin table]
- **Bindings:** [Routes, KV, D1, vault scope]
- **Cache:** [Rules with TTL per route]
- **Fallback:** [Origin and error paths]
```

## 5. Validation Gate

- [ ] Edge split justified per unit.
- [ ] Secrets bound to vault only.
- [ ] Every critical route carries fallback.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before deploy.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Routing traffic without cache and fallback rules.
- **Over-execution threshold:** Deploying workers to production zones unprompted.
- **Calibration default:** Cache aggressively; compute at edge sparingly.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-1 (vague task)      | Requires split table before routing.                |
| 2    | AP-44 (leaked secrets) | Forces vault bindings.                              |
| 3    | AP-28 (no stop)        | Demands fallback per critical route.                |
| 4    | AP-45 (no human review)| Halts for approval before deploy.                   |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Release Engineer role, role source, and seniority bar.
  - `1.0.0` (2026-09-26) - Initial release extending devops coverage.

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

**Input:** "Our edge auth worker times out and leaks staging keys."
**Output:** Blueprint with split auth check, vault-bound keys, cached JWKS route, and origin fallback.
