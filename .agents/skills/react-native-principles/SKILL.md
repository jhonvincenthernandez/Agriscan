---
name: react-native-principles
description: Normative foundation for React Native and Expo apps covering architecture posture, platform boundaries, rendering discipline, list and image policies, storage security, and accessibility mapping.
department: frontend
ownerAgent: legolas
triggerCommand: /react-native-principles
antiPatternsPrevented:
  - AP-1
  - AP-4
  - AP-6
  - AP-26
  - AP-28
---

# React Native Principles

## 0. Identity

- **Role:** Interface Builder. Owns native screen composition with platform boundary discipline.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Interface Builder).
- **Seniority bar:** Staff (Appendix B). Records why Expo-first beats hand-edited natives (config plugins survive upgrades, rejected Gradle surgery), why FlashList beats FlatList past one screen (recycling over mounting, rejected ScrollView dumps), and why secure-store beats AsyncStorage for secrets.
- **Authority:** Tier-5 normative skill for `skills/frontend/react-native-principles/`. Owns mobile UI guidance.
- **Must not define:** Backend APIs; app store release administration.
- **Normative base:** `core/fellowship/legolas.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-4 (over-permissive natives), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Produce React Native screens with platform-correct primitives and performant lists.             |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.                |
| 3   | Output Format    | Screen plan with architecture, platform, list, and security notes.                             |
| 4   | Constraints      | Expo first. No web APIs. Zero em dashes. Secrets in secure store.                              |
| 5   | Input            | Screen specs, list inventory, secret inventory, a11y targets.                                   |
| 6   | Context          | Prevents web-habit ports, janky lists, and plaintext secret storage.                            |
| 7   | Audience         | Mobile engineers shipping React Native and Expo apps.                                           |
| 8   | Success Criteria | Primitives native; lists recycled; plan approved before coding.                                 |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger                                      | Fire? | Notes                              |
| -------------------------------------------- | ----- | ---------------------------------- |
| "Build this screen in React Native"          | YES   | Core trigger.                      |
| "Fix janky lists and secret storage"         | YES   | Core trigger.                      |
| "/react-native-principles"                   | YES   | Slash command trigger.             |
| "Build a web React app instead"              | NO    | Route to `react-principles`.       |
| "Publish to app stores"                      | NO    | Release flow owns it.              |

## 3. Execution Workflow

### Step 1: Posture the Architecture

- **Action:** Target current Expo SDK with New Architecture, strict TypeScript API imports, Hermes runtime, Expo Router navigation, and modern DevTools debugging.
- **Input:** Screen specs and SDK inventory.
- **Stop Condition:** Halt on legacy architecture targets or hand-edited natives with plugin alternatives.
- **Validation:** Posture checklist reviewed per app.

### Step 2: Respect Platform Boundaries

- **Action:** Ban web APIs in favor of Platform selections and file splits, compose from core primitives with module-scoped stylesheets, and consume safe areas dynamically.
- **Input:** Component inventory from Step 1.
- **Stop Condition:** Halt on window or document usage; require native equivalents.
- **Validation:** Boundary audit complete per screen.

### Step 3: Lists, Media, and Secrets

- **Action:** Default long lists to FlashList with estimated sizes, serve images via expo-image with dimensions, run animations off-thread, store secrets in secure enclaves, and map accessibility roles with Maestro-tested flows.
- **Input:** List, media, and secret inventories.
- **Stop Condition:** Halt on ScrollView dumps or AsyncStorage secrets.
- **Validation:** Performance and security review complete.

### Step 4: Handoff and Human Review

- **Action:** Present the plan and request approval before coding.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero code written by this skill.

## 4. Output Specification

```markdown
# React Native Plan

- **Architecture:** [Posture checklist]
- **Platform:** [Boundary audit]
- **Performance:** [List and media notes]
- **Security:** [Secret storage map]
```

## 5. Validation Gate

- [ ] Architecture current per SDK.
- [ ] Boundaries native per screen.
- [ ] Secrets in secure enclaves.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before coding.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Porting web habits without boundary audit.
- **Over-execution threshold:** Publishing store releases unprompted.
- **Calibration default:** Expo managed first; eject with receipts.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-1 (vague task)      | Requires posture checklist first.                   |
| 2    | AP-26 (no scope)       | Enforces platform boundaries.                       |
| 3    | AP-4 (over-permissive) | Vaults secrets in enclaves.                         |
| 4    | AP-45 (no human review)| Halts for approval before coding.                   |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Interface Builder role, role source, and seniority bar.
  - `1.0.0` - Legacy mobile baseline.

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

**Input:** "Our RN feed janks and tokens sit in AsyncStorage."
**Output:** Plan with FlashList recycling, off-thread animations, and secure-enclave secret migration.
