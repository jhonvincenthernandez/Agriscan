---
name: feature-flags
description: Feature flag architecture covering dynamic configuration management, trunk-based development enablement, ring rollouts, kill switches, and flag deprecation lifecycles.
department: architecture
ownerAgent: aragorn
triggerCommand: /feature-flags
antiPatternsPrevented:
  - AP-1
  - AP-4
  - AP-18
  - AP-26
  - AP-28
---

# Feature Flags & Progressive Delivery

## 0. Identity

- **Role:** System Architect. Owns rollout system shape: toggle architecture, ring deployments, and flag retirement lifecycle.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (System Architect).
- **Seniority bar:** Staff (Appendix B).
- **Staff judgment:** Records why trunk-based flags beat long-lived branches (integration pain surfaces daily, rejected branch-per-feature isolation) and why retirement sweeps are scheduled at flag creation, not discovered as dead code years later.
- **Authority:** Normative tier-4 standard for runtime configuration and feature flags under `skills/architecture/feature-flags/`.
- **Must not define:** Application authentication credentials or cloud infrastructure provisioning.
- **Normative base:** `core/fellowship/aragorn.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1 (unbounded toggle proliferation), AP-4 (unverified flag overrides), and AP-28 (unbounded dead code accumulation).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                                  |
| --- | ---------------- | ------------------------------------------------------------------------------------------------------ |
| 1   | Task             | Architect, evaluate, and clean up feature flags and progressive rollout configurations.                |
| 2   | Target Tool      | OpenFeature SDK, LaunchDarkly, Unleash, Flipt, TypeScript, Go, Python.                                 |
| 3   | Output Format    | In-memory evaluation adapters, typed toggle definitions, and flag retirement pull requests.            |
| 4   | Constraints      | Mandatory in-memory cached evaluation. Fail-safe defaults. Maximum 60-day lifecycle for release flags. |
| 5   | Input            | Release roadmaps, risk profiles, user tenant identifiers, progressive deployment plans.                |
| 6   | Context          | Prevents massive merge conflicts, release deployment blockers, and production incident blast radiuses. |
| 7   | Audience         | Release engineers, backend developers, frontend architects, product operations leads.                  |
| 8   | Success Criteria | Sub-millisecond flag evaluation latency; zero production downtime during feature toggling.             |
| 9   | Examples         | See Section 5.                                                                                         |

## 2. Trigger Matrix

| Trigger Condition                                       | Fire? | Action / Route                                                         |
| ------------------------------------------------------- | ----- | ---------------------------------------------------------------------- |
| Implementing trunk-based development with dark launches | YES   | Wrap incomplete capabilities in release flags with false defaults.     |
| Setting up canary rollouts or tenant ring deployments   | YES   | Configure percentage-based or tenant-matched evaluation rules.         |
| Flag reaches 100 percent rollout for over 30 days       | YES   | Schedule immediate technical debt cleanup and remove dead branch code. |
| Defining application role-based access control (RBAC)   | NO    | Route to security authorization frameworks.                            |

## 3. Core Architectural Directives

1. **Flag Classification Taxonomy:**
   - **Release Flags:** Short-lived (under 30 to 60 days). Enable continuous integration and trunk-based development.
   - **Ops Flags (Kill Switches):** Long-lived. Degrade non-critical features instantly during infrastructure incidents.
   - **Experimentation Flags:** Medium-lived. Power randomized A/B multivariate trials with telemetry tracking.
   - **Permission Flags:** Long-lived. Control customer plan entitlements and premium feature access.
2. **In-Memory Evaluation Performance:** Flag checks must never make synchronous external HTTP calls in request paths. Evaluations must execute in memory against locally synchronized or cached flag rules.
3. **Fail-Safe Defaults:** Every flag evaluation must specify an explicit fallback value. If the flag provider is unreachable, the system must fall back to the proven baseline state without throwing exceptions.
4. **Ring Deployment Discipline:** Deploy features progressively: Ring 0 (internal staff) -> Ring 1 (1 percent canary) -> Ring 2 (10 percent) -> Ring 3 (50 percent) -> Ring 4 (100 percent general availability).

## 4. Execution Workflow

### Step 1: Flag Definition and Default Allocation

- **Action:** Declare the feature flag in a centralized typed configuration registry with an explicit default state.
- **Validation:** Flag name uses domain prefixing (for example `release_v2_checkout_flow`).

### Step 2: Boundary Wrapping

- **Action:** Encapsulate new feature paths behind the flag check at the entry controller or route level. Avoid scattering flag checks into deep domain logic.
- **Validation:** Baseline fallback executes when flag evaluates to false.

### Step 3: Progressive Rollout and Telemetry Monitoring

- **Action:** Incrementally expand rollout rings while monitoring error rates and latency metrics.
- **Validation:** Instant kill switch restores baseline if error rate spikes.

## 5. Reference Implementation

### TypeScript (OpenFeature In-Memory Evaluation Pattern)

```typescript
import {
  OpenFeature,
  Client,
  EvaluationContext,
} from "@openfeature/server-sdk";

export class FeatureFlagService {
  private client: Client;

  constructor() {
    this.client = OpenFeature.getClient("app-feature-service");
  }

  async isFeatureEnabled(
    flagKey: string,
    context: EvaluationContext,
    defaultValue: boolean = false,
  ): Promise<boolean> {
    try {
      return await this.client.getBooleanValue(flagKey, defaultValue, context);
    } catch (error) {
      // In-memory fallback prevents request disruption
      return defaultValue;
    }
  }

  // Ring deployment evaluation using tenant ID hashing
  isUserInCanaryRing(userId: string, rolloutPercentage: number): boolean {
    let hash = 0;
    for (let i = 0; i < userId.length; i++) {
      hash = (hash << 5) - hash + userId.charCodeAt(i);
      hash |= 0;
    }
    const normalizedScore = Math.abs(hash) % 100;
    return normalizedScore < rolloutPercentage;
  }
}
```

## 6. Validation Gate

Run before shipping code containing feature flags:

- [ ] Flag is registered in centralized typed configuration registry.
- [ ] Safe default fallback value is explicitly defined.
- [ ] Flag evaluations execute entirely in memory with zero blocking network calls.
- [ ] Flag conditionals are isolated to boundary layers, not scattered in domain entities.
- [ ] Expiration date and owner are assigned to release flags.

## 7. Versioning & Portability Matrix

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-20): Elevated to Sauron Tier-5 specification with OpenFeature reference patterns.

| Runtime / Harness | Status   | Notes                                    |
| ----------------- | -------- | ---------------------------------------- |
| Claude Code       | verified | Fully supported via command integration. |
| Cursor            | verified | Compatible with editor rule context.     |
| Windsurf          | verified | Fully functional.                        |
| Antigravity       | verified | Certified.                               |
