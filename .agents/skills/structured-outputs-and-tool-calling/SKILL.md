---
name: structured-outputs-and-tool-calling
description: Enforces JSON schema contracts, function calling discipline, and guardrails so agents emit parseable outputs and safe tool calls. Excludes model selection.
department: ai-engineering
ownerAgent: legolas
triggerCommand: /structured-outputs-and-tool-calling
antiPatternsPrevented:
  - AP-1
  - AP-4
  - AP-6
  - AP-26
  - AP-28
---

# Structured Outputs and Tool Calling

## 0. Identity

- **Role:** Contract Enforcer. Owns schema validity and call-policy compliance for agent outputs and actions.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Contract Enforcer).
- **Seniority bar:** Staff (Appendix B). Records why strict schemas beat regex hope (parse failures surface at the boundary, rejected free-text contracts), and why deny-by-default beats allow-by-default for mutations.
- **Authority:** Tier-5 normative skill for `skills/ai-engineering/structured-outputs-and-tool-calling/`. Owns schema contracts and call policy.
- **Must not define:** Model provider choice; business logic inside tools.
- **Normative base:** `core/fellowship/legolas.md`, `rules/engineering/architecture-boundaries.md`, `references/anti-patterns.md`, and 2026 function calling practice.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-4 (over-permissive agent), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                       |
| --- | ---------------- | ------------------------------------------------------------------------------------------- |
| 1   | Task             | Specify output schemas, tool contracts, idempotency keys, and guardrails for agent actions. |
| 2   | Target Tool      | Any agent runtime: Claude Code, Cursor, Copilot, Windsurf, Kiro, Cline, raw API.            |
| 3   | Output Format    | Contract pack with schemas, tool manifests, retry policy, and refusal rules.                |
| 4   | Constraints      | Every side effect carries an idempotency key. Timeouts mandatory. Zero em dashes.           |
| 5   | Input            | Tool inventory, output consumers, mutating versus read-only classification.                 |
| 6   | Context          | Prevents unparseable outputs and unsafe fire-and-forget tool calls in production agents.    |
| 7   | Audience         | AI engineers wiring agents to real systems.                                                 |
| 8   | Success Criteria | All outputs validate; all mutating calls gated; contract pack approved before wiring.       |
| 9   | Examples         | See Section 10.                                                                             |

## 2. Trigger Matrix

| Trigger                                           | Fire? | Notes                              |
| ------------------------------------------------- | ----- | ---------------------------------- |
| "Force our agent to return valid JSON every time" | YES   | Core trigger.                      |
| "Add guardrails and idempotency to agent tools"   | YES   | Core trigger.                      |
| "/structured-outputs-and-tool-calling"            | YES   | Slash command trigger.             |
| "Pick the cheapest model for our agent"           | NO    | Out of scope for this skill.       |
| "Design the full agent graph topology"            | NO    | Route to `langgraph-orchestrator`. |

## 3. Execution Workflow

### Step 1: Classify Tools and Outputs

- **Action:** List every tool with mutating versus read-only label, timeout, retry policy, and output consumer. Version output schemas so consumers pin contracts.
- **Input:** Tool inventory and downstream consumers.
- **Stop Condition:** Halt and ask when a mutating tool lacks an owner.
- **Validation:** Classification table complete with owners.

### Step 2: Write Schema Contracts

- **Action:** Author strict JSON schemas per output with required fields, enums, refusal shape, and single-repair path for invalid output.
- **Input:** Consumer requirements from Step 1.
- **Stop Condition:** Halt when consumers accept free text; require schema sign-off.
- **Validation:** Schemas reject malformed samples in dry-run validation.

### Step 3: Gate Mutating Calls

- **Action:** Attach idempotency keys, 30-second timeout caps with backoff, approval interrupts, and prompt-injection delimiters separating user input from system instructions. Hash PII before logging.
- **Input:** Mutating tool list from Step 1.
- **Stop Condition:** Halt when a side effect lacks an idempotency key; mark as finding.
- **Validation:** Every mutating call carries key, timeout, and gate.

### Step 4: Handoff and Human Review

- **Action:** Present the contract pack with validation evidence and request approval before wiring.
- **Input:** Completed contract pack.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero tools wired by this skill.

## 4. Output Specification

```markdown
# Contract Pack

- **Schemas:** [Output schemas with refusal shape]
- **Tools:** [Manifest with mutating flags and timeouts]
- **Gates:** [Idempotency, approval, and delimiter rules]
- **Validation:** [Dry-run evidence]
```

## 5. Validation Gate

- [ ] Every tool classified with owner.
- [ ] Schemas reject malformed samples.
- [ ] Every side effect carries idempotency key and timeout.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before wiring.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Accepting free-text outputs where consumers need parseable data.
- **Over-execution threshold:** Wiring tools to production systems without approval.
- **Calibration default:** Deny mutating calls by default; allowlist explicitly.

## 7. Anti-Pattern Compliance

| Step | Prevents AP             | Mechanism                                    |
| ---- | ----------------------- | -------------------------------------------- |
| 1    | AP-1 (vague task)       | Requires tool classification with owners.    |
| 2    | AP-26 (no scope)        | Bounds outputs with strict schemas.          |
| 3    | AP-4 (over-permissive)  | Gates side effects with keys and interrupts. |
| 4    | AP-45 (no human review) | Halts for approval before wiring.            |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Contract Enforcer role, role source, and seniority bar.
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

**Input:** "Our agent sometimes returns broken JSON and double-charges refunds."
**Output:** Contract pack with strict refund schema, idempotency key on charge tool, 30 second timeout, and approval interrupt.
