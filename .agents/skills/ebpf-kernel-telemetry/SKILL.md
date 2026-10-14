---
name: ebpf-kernel-telemetry
description: Deploys verifier-safe eBPF probes with ring-buffer streaming and CO-RE portability for sub-1-percent-overhead kernel telemetry. Excludes userspace application logic.
department: devops
ownerAgent: legolas
triggerCommand: /ebpf-kernel-telemetry
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-18
  - AP-26
  - AP-28
---

# eBPF Kernel Telemetry

## 0. Identity

- **Role:** Diagnostic Analyst. Owns kernel-level failure classification with verifier-safe evidence.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Diagnostic Analyst).
- **Seniority bar:** Staff (Appendix B). Records why ring buffers beat perf arrays (lossless high-frequency streaming, rejected legacy event arrays), why bounded loops beat clever ones (verifier acceptance is non-negotiable, rejected unbounded iteration), and why CO-RE beats per-kernel builds.
- **Authority:** Tier-5 normative skill for `skills/devops/ebpf-kernel-telemetry/`. Owns probe design and loader guidance.
- **Must not define:** Application UI display components.
- **Normative base:** `core/fellowship/legolas.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-18 (unbounded probe overhead), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Deploy safe eBPF probes that stream kernel telemetry under 1 percent CPU overhead.              |
| 2   | Target Tool      | Linux BPF, Cilium, Tetragon, bpftrace, BCC, libbpf.                                            |
| 3   | Output Format    | Probe plan with programs, maps, loader notes, and overhead budget.                             |
| 4   | Constraints      | Verifier must accept every program. Zero allocations in probe context. Zero em dashes.         |
| 5   | Input            | Profiling targets, latency questions, audit requirements, kernel versions.                      |
| 6   | Context          | Prevents blind production systems where kernel behavior stays invisible.                        |
| 7   | Audience         | SREs, kernel engineers, and performance teams.                                                  |
| 8   | Success Criteria | Verifier passes on target kernels; overhead under 1 percent; plan approved.                     |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger                                      | Fire? | Notes                              |
| -------------------------------------------- | ----- | ---------------------------------- |
| "Trace syscalls with sub-1-percent overhead" | YES   | Core trigger.                      |
| "Profile socket latency in production"       | YES   | Core trigger.                      |
| "/ebpf-kernel-telemetry"                     | YES   | Slash command trigger.             |
| "Build our application UI"                   | NO    | Out of scope for this skill.       |
| "Debug userspace business logic"             | NO    | Out of scope; use app tracers.     |

## 3. Execution Workflow

### Step 1: Scope Probes to Questions

- **Action:** Map each profiling question to minimal hook points with bounded loops and validated pointers.
- **Input:** Profiling targets and kernel versions.
- **Stop Condition:** Halt when hooks stay unscoped; require explicit attach points.
- **Validation:** Hook list reviewed with verifier constraints.

### Step 2: Stream via Ring Buffers

- **Action:** Design ring-buffer maps sized to event rates with CO-RE compilation for portable bytecode across kernels.
- **Input:** Event volume estimates from Step 1.
- **Stop Condition:** Halt when buffer sizing lacks rate math; require numbers.
- **Validation:** Map design reviewed with drop policy.

### Step 3: Load and Budget Overhead

- **Action:** Pair probes with Go or Rust loaders exporting OpenTelemetry metrics. Measure overhead against the 1 percent budget before sign-off.
- **Input:** Loader inventory and overhead budget.
- **Stop Condition:** Halt when overhead exceeds budget; require probe reduction.
- **Validation:** Overhead evidence recorded per probe.

### Step 4: Handoff and Human Review

- **Action:** Present the probe plan and request approval before loading.
- **Input:** Completed plan.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero probes loaded by this skill.

## 4. Output Specification

```markdown
# eBPF Probe Plan

- **Hooks:** [Attach points with bounds]
- **Maps:** [Ring buffers with sizing]
- **Loaders:** [Userspace exporters]
- **Overhead:** [Budget evidence]
```

## 5. Validation Gate

- [ ] Hooks scoped with verifier constraints.
- [ ] Buffers sized with rate math.
- [ ] Overhead under 1 percent evidenced.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded before loading.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Loading probes without verifier evidence.
- **Over-execution threshold:** Tracing production kernels unprompted.
- **Calibration default:** Fewest hooks answering the question.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-1 (vague task)      | Requires hook map first.                            |
| 2    | AP-26 (no scope)       | Sizes buffers with rate math.                       |
| 3    | AP-28 (no stop)        | Enforces overhead budget.                           |
| 4    | AP-45 (no human review)| Halts for approval before loading.                  |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Diagnostic Analyst role, role source, and seniority bar.
  - `1.0.0` - Legacy telemetry baseline.

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

**Input:** "Our p99 latency spikes with no userspace explanation."
**Output:** Probe plan with syscall latency hooks, ring-buffer streaming, and sub-1-percent overhead evidence.
