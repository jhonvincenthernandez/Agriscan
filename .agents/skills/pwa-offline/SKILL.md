---
name: pwa-offline
description: PWA rules covering installability manifests, service worker lifecycles, per-class cache strategies, update UX, and offline testing. Excludes native app builds.
department: frontend
ownerAgent: legolas
triggerCommand: /pwa-offline
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-26
  - AP-28
---

# PWA Offline

## 0. Identity

- **Role:** Interface Builder. Owns installable composition with offline-first resilience.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Interface Builder).
- **Seniority bar:** Staff (Appendix B). Records why per-class cache strategies beat one-strategy caching (freshness needs differ, rejected blanket cache-first), why prompt updates beat forced activation (mixed chunks break sessions, rejected skipWaiting defaults), and why precache shells stay lean (install speed decides retention, rejected precache-everything).
- **Authority:** Tier-5 normative skill for `skills/frontend/pwa-offline/`. Owns manifest and worker guidance.
- **Must not define:** Native app builds or app store releases.
- **Normative base:** `core/fellowship/legolas.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                            |
| --- | ---------------- | -------------------------------------------------------------------------------- |
| 1   | Task             | Produce installable apps with offline resilience and safe update flows.          |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API. |
| 3   | Output Format    | PWA plan with manifest, worker, cache, and test notes.                           |
| 4   | Constraints      | HTTPS only. Scoped caches. Zero em dashes. Prompt updates for installed apps.    |
| 5   | Input            | App type, offline needs, install targets, device matrix.                         |
| 6   | Context          | Prevents uninstallable apps, stale sessions, and offline dead ends.              |
| 7   | Audience         | Frontend engineers shipping installable web apps.                                |
| 8   | Success Criteria | Installable verified; offline covered; plan approved before coding.              |
| 9   | Examples         | See Section 10.                                                                  |

## 2. Trigger Matrix

| Trigger                                | Fire? | Notes                          |
| -------------------------------------- | ----- | ------------------------------ |
| "Make our app installable and offline" | YES   | Core trigger.                  |
| "Fix stale sessions after deploys"     | YES   | Core trigger.                  |
| "/pwa-offline"                         | YES   | Slash command trigger.         |
| "Build native iOS and Android apps"    | NO    | Out of scope for this skill.   |
| "Run our push notification server"     | NO    | Out of scope; backend owns it. |

## 3. Execution Workflow

### Step 1: Declare Installability

- **Action:** Ship complete manifests with icons, screenshots, shortcuts, and identity fields. Serve over HTTPS with correct MIME types and no-cache worker headers.
- **Input:** Install targets from user.
- **Stop Condition:** Halt when manifest requirements stay unmet.
- **Validation:** Installability checklist verified per platform.

### Step 2: Assign Cache Strategies

- **Action:** Map hashed assets to cache-first, documents to network-first, API lists to stale-while-revalidate, and transactions plus analytics to network-only with sync queues.
- **Input:** Offline needs per route.
- **Stop Condition:** Halt when one strategy covers all classes; require mapping.
- **Validation:** Strategy table reviewed per request class.

### Step 3: Update Safely and Test Offline

- **Action:** Prompt installed apps before activation, scope runtime caches to own domains, precache shells leanly, and verify with DevTools offline plus Playwright offline suites including iOS Safari passes.
- **Input:** Device matrix from user.
- **Stop Condition:** Halt when updates force-activate on long sessions.
- **Validation:** Offline test evidence recorded per platform.

### Step 4: Handoff and Human Review

- **Action:** Present the plan and request approval before coding.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero code written by this skill.

## 4. Output Specification

```markdown
# PWA Plan

- **Manifest:** [Installability checklist]
- **Cache:** [Strategy per class]
- **Updates:** [Prompt flow with tests]
```

## 5. Validation Gate

- [ ] Installability verified per platform.
- [ ] Strategies mapped per class.
- [ ] Offline tested with evidence.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before coding.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Shipping workers without strategy mapping.
- **Over-execution threshold:** Building native apps unprompted.
- **Calibration default:** Strategy per class; never global.

## 7. Anti-Pattern Compliance

| Step | Prevents AP             | Mechanism                                |
| ---- | ----------------------- | ---------------------------------------- |
| 1    | AP-1 (vague task)       | Requires installability checklist first. |
| 2    | AP-26 (no scope)        | Maps strategies per class.               |
| 3    | AP-28 (no stop)         | Tests offline with evidence.             |
| 4    | AP-45 (no human review) | Halts for approval before coding.        |

## 8. Versioning & Changelog

- **Version:** 1.0.0
- **Changelog:**
  - `1.0.0` (2026-09-26) - Initial release closing the PWA gap.

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

**Input:** "Our app must work offline on warehouse tablets."
**Output:** Plan with install manifest, per-class cache map, prompt updates, and offline test evidence.
