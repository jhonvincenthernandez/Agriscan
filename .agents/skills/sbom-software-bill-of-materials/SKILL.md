---
name: sbom-software-bill-of-materials
description: CycloneDX and SPDX software bill of materials generation, supply chain integrity, and automated CVE alerting.
department: security
ownerAgent: boromir
triggerCommand: /sbom-software-bill-of-materials
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-18
  - AP-26
  - AP-28
---

# SBOM Software Bill of Materials

## 0. Identity

- **Role:** Security Auditor. Owns supply-chain findings with signed inventory evidence.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Security Auditor).
- **Seniority bar:** Staff (Appendix B). Records why signed SBOMs beat manifest lists (cryptographic proof travels with artifacts, rejected trust-me inventories), why transitive capture beats direct-only scans (most risk hides transitively, rejected shallow audits), and why license gates ride the same pipeline.
- **Authority:** Tier-5 normative skill for `skills/security/sbom-software-bill-of-materials/`. Owns SBOM generation guidance.
- **Must not define:** Application layout or UX features.
- **Normative base:** `core/fellowship/boromir.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`, `rules/security/supply-chain-integrity.md`, `context/core-domains/dependency-governance.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague task), AP-18 (hidden transitive risk), AP-26 (no scope boundary), and AP-28 (no stop condition).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                          |
| --- | ---------------- | ---------------------------------------------------------------------------------------------- |
| 1   | Task             | Produce signed SBOMs per artifact with CVE mapping and license gates.                          |
| 2   | Target Tool      | Syft, Grype, CycloneDX CLI, Cosign, Trivy.                                                     |
| 3   | Output Format    | Signed CycloneDX or SPDX artifacts with vulnerability reports.                                 |
| 4   | Constraints      | SBOM per release artifact. Transitive capture mandatory. Zero em dashes. Signatures required.  |
| 5   | Input            | Lockfiles, binaries, container layers, release inventory.                                       |
| 6   | Context          | Prevents supply chain attacks, hidden CVEs, and license violations.                            |
| 7   | Audience         | Enterprise security officers, compliance auditors, and DevOps leads.                           |
| 8   | Success Criteria | Full transitive capture with valid signatures per artifact.                                     |
| 9   | Examples         | See Section 10.                                                                                 |

## 2. Trigger Matrix

| Trigger                                      | Fire? | Notes                              |
| -------------------------------------------- | ----- | ---------------------------------- |
| "Generate SBOMs for our release"             | YES   | Core trigger.                      |
| "Gate on CVE severity"                       | YES   | Core trigger.                      |
| "/sbom-software-bill-of-materials"           | YES   | Slash command trigger.             |
| "Design our UI layouts"                      | NO    | Out of scope for this skill.       |
| "Write application features"                 | NO    | Out of scope for this skill.       |

## 3. Execution Workflow

### Step 1: Inventory Transitive Trees

- **Action:** Enumerate direct plus transitive dependencies per artifact with hashes and license identifiers.
- **Input:** Lockfiles and binaries from user.
- **Stop Condition:** Halt when transitive trees stay partial.
- **Validation:** Inventory complete per artifact.

### Step 2: Sign and Map Vulnerabilities

- **Action:** Generate standard-format SBOMs, sign with transparency-logged signatures, and map hashes against vulnerability feeds with severity evidence.
- **Input:** Inventory from Step 1.
- **Stop Condition:** Halt on unsigned artifacts; require signatures.
- **Validation:** Signed SBOMs reviewed with CVE map.

### Step 3: Gate Licenses and Severity

- **Action:** Fail builds on high-severity CVEs and blocked licenses per policy buckets.
- **Input:** Policy definitions from user.
- **Stop Condition:** Halt when gates warn instead of fail.
- **Validation:** Gate log reviewed per release.

### Step 4: Handoff and Human Review

- **Action:** Present the SBOM pack and request approval for exceptions.
- **Input:** Completed pack.
- **Stop Condition:** Await user approval.
- **Validation:** Approval recorded; zero exceptions granted by this skill.

## 4. Output Specification

```markdown
# SBOM Pack

- **Inventory:** [Transitive trees]
- **Signatures:** [Proof per artifact]
- **Gates:** [CVE and license verdicts]
```

## 5. Validation Gate

- [ ] Transitive capture complete.
- [ ] Signatures valid per artifact.
- [ ] Gates fail on violations.
- [ ] Zero em dashes in deliverable.
- [ ] Human approval recorded for exceptions.

## 6. Anti-Triggers and Calibration

- **Under-execution threshold:** Auditing direct deps only.
- **Over-execution threshold:** Rewriting application code unprompted.
- **Calibration default:** Transitive always; signatures always.

## 7. Anti-Pattern Compliance

| Step | Prevents AP            | Mechanism                                           |
| ---- | ---------------------- | --------------------------------------------------- |
| 1    | AP-1 (vague task)      | Requires full inventory first.                      |
| 2    | AP-26 (no scope)       | Signs every artifact.                               |
| 3    | AP-28 (no stop)        | Gates releases on violations.                       |
| 4    | AP-45 (no human review)| Halts for exception approval.                       |

## 8. Versioning & Changelog

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-26) - Tier-5 conversion with Security Auditor role, role source, and seniority bar.
  - `1.0.0` - Legacy SBOM baseline.

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

**Input:** "Our release ships unknown transitive deps."
**Output:** Signed SBOM pack with CVE map and license gate verdicts.
