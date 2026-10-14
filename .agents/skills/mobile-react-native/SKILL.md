---
name: mobile-react-native
description: Root router for the Mobile (React Native & Expo) module, routing UI styling, project scaffolding, Tailwind setup, and production best practice requests to specialist sub-skills.
department: frontend
ownerAgent: aragorn
triggerCommand: /mobile-react-native
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-18
---

# Mobile (React Native & Expo) Router

## 0. Identity

- **Role:** System Architect. Owns module routing shape with explicit dispatch maps to specialist sub-skills.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (System Architect).
- **Seniority bar:** Staff (Appendix B). Records why explicit routing tables beat implicit dispatch (every request resolves deterministically, rejected fuzzy matching) and why routers never execute (separation keeps dispatch auditable, rejected god-router implementations).
- **Authority:** Tier-5 normative root skill for `skills/frontend/mobile-react-native/`.
- **Must not define:** Direct component code, scaffolding execution, or tool configuration; delegates to sub-skills.
- **Normative base:** `core/fellowship/aragorn.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`, `context/core-domains/design-system.md`.

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                                         |
| --- | ---------------- | ------------------------------------------------------------------------------------------------------------- |
| 1   | Task             | Classify mobile React Native and Expo requests and dispatch to target sub-skills.                             |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.                              |
| 3   | Output Format    | Structured routing decision and handoff to target mobile sub-skill.                                           |
| 4   | Constraints      | Router executes no mobile development tasks directly.                                                         |
| 5   | Input            | User request related to Expo screens, app architecture, Tailwind setup, or React Native performance/worklets. |
| 6   | Context          | Prevents style rule conflicts and architectural degradation in mobile codebases.                              |
| 7   | Audience         | Mobile developers and autonomous engineering agents.                                                          |
| 8   | Success Criteria | Request routed cleanly to target mobile sub-skill.                                                            |
| 9   | Examples         | See Section 10.                                                                                               |

## 2. Trigger Matrix

| Sub-Skill                   | Trigger                                                                              | Target Skill File Path                                                     |
| --------------------------- | ------------------------------------------------------------------------------------ | -------------------------------------------------------------------------- |
| Expo Native UI              | Build screens, components, and HIG native controls using inline styles (no Tailwind) | `skills/frontend/mobile-react-native/expo-native-ui/SKILL.md`              |
| Expo Project Structure      | Scaffold feature-based modular folder structure for new Expo Router apps             | `skills/frontend/mobile-react-native/expo-project-structure/SKILL.md`      |
| Expo Tailwind Setup         | Configure Tailwind v4, PostCSS, and NativeWind v5 universal styling repository setup | `skills/frontend/mobile-react-native/expo-tailwind-setup/SKILL.md`         |
| React Native Best Practices | Production performance, New Architecture, animations, worklets, gestures, or JSI     | `skills/frontend/mobile-react-native/react-native-best-practices/SKILL.md` |

## 3. Execution Workflow

### Step 1: Analyze Request

- **Action:** Classify user request into UI building, project scaffolding, Tailwind setup, or production best practices.
- **Input:** User prompt text and project context.
- **Stop Condition:** Ask user if target domain is ambiguous.
- **Validation:** Matches Trigger Matrix.

### Step 2: Resolve Target

- **Action:** Select target sub-skill path under `skills/frontend/mobile-react-native/`.
- **Input:** Trigger Matrix.
- **Stop Condition:** Decline execution if request is out of scope.
- **Validation:** Target SKILL.md exists on disk.

### Step 3: Handoff

- **Action:** Delegate control to target SKILL.md.
- **Input:** Resolved target path.
- **Stop Condition:** Handoff control.
- **Validation:** Sub-skill executes.

## 4. Output Specification

```json
{
  "module": "mobile-react-native",
  "target_skill": "skills/mobile-react-native/expo-native-ui/SKILL.md"
}
```

## 5. Validation Gate

- [ ] Intent mapped to target mobile sub-skill.
- [ ] Target file exists on disk.
- [ ] Router executes no component or configuration logic directly.

## 6. Anti-Triggers

- **Under-execution:** Writing React Native code without checking for New Architecture worklet rules.
- **Over-execution:** Running a full project scaffolding router for a single button color change.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                             |
| ---- | ---------------------- | ----------------------------------------------------- |
| 1    | AP-1 (vague task)      | Demands domain classification before handoff.         |
| 3    | AP-4 (over-permissive) | Module root router delegates execution to sub-skills. |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` - Root router created for `skills/mobile-react-native/`.

## 9. Portability Matrix

| Runtime     | Status   | Notes                         |
| ----------- | -------- | ----------------------------- |
| Claude Code | verified | Mobile root dispatcher.       |
| Cursor      | verified | Mobile rules routing.         |
| Copilot     | verified | Custom instructions.          |
| Windsurf    | verified | Directive routing.            |
| Kiro        | verified | Skill runner handoff.         |
| Cline       | verified | System prompt loading.        |
| Raw API     | verified | Model-agnostic mobile router. |

## 10. Examples

**Input:** "Create an Expo Router setup for a new app."
**Output:** Target `skills/frontend/mobile-react-native/expo-project-structure/SKILL.md`.
