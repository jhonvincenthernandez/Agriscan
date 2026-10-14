---
name: architecture-decision-records
description: Architecture Decision Record (ADR) standards for capturing technical decisions, architectural trade-offs, consequences, and acceptance criteria in version-controlled markdown.
department: architecture
ownerAgent: gandalf
triggerCommand: /architecture-decision-records
antiPatternsPrevented:
  - AP-1
  - AP-4
  - AP-9
  - AP-18
  - AP-26
  - AP-28
---

# Architecture Decision Records (ADR)

## 0. Identity

- **Role:** Decision Records Keeper. Owns architecture decision log completeness with consequences and acceptance criteria per record.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Decision Records Keeper).
- **Seniority bar:** Staff (Appendix B).
- **Staff judgment:** Records why ADRs beat wiki pages (versioned, reviewable, indexed) and why rejected alternatives stay in the record (future readers need the losing reasons, not just the winner).
- **Authority:** Normative tier-4 standard for architectural decisions across repositories under `skills/architecture/architecture-decision-records/`.
- **Must not define:** Application UI components, specific CSS styling rules, or transient ticket tracking.
- **Normative base:** `core/fellowship/aragorn.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1 (vague architectural scope), AP-9 (unverified assumptions), and AP-28 (unbounded design drift).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                                    |
| --- | ---------------- | -------------------------------------------------------------------------------------------------------- |
| 1   | Task             | Formulate, review, update, and index version-controlled Architecture Decision Records.                   |
| 2   | Target Tool      | Git, Markdown, Node.js ADR indexing scripts, repository architecture directories.                        |
| 3   | Output Format    | Standardized markdown ADR files with YAML frontmatter and automated index tables.                        |
| 4   | Constraints      | One architectural decision per record. Mandatory alternatives analysis. No retroactive fictionalization. |
| 5   | Input            | High-impact technical proposals, system refactoring demands, technology evaluations.                     |
| 6   | Context          | Prevents institutional memory loss, recurring debates, and architectural drift.                          |
| 7   | Audience         | Principal engineers, technical leads, software architects, future contributors.                          |
| 8   | Success Criteria | 100 percent of major technical choices recorded with clear rationale, tradeoffs, and rollback plans.     |
| 9   | Examples         | See Section 5.                                                                                           |

## 2. Trigger Matrix

| Trigger Condition                                                   | Fire? | Action / Route                                     |
| ------------------------------------------------------------------- | ----- | -------------------------------------------------- |
| Evaluating new database engines, frameworks, or messaging platforms | YES   | Author proposed ADR with alternatives analysis.    |
| Changing service boundary structures or communication protocols     | YES   | Draft ADR; initiate mandatory 3-day review window. |
| Minor bug fix or localized internal code refactoring                | NO    | Reject ADR; document via pull request description. |
| Defining public HTTP REST interface contracts                       | NO    | Route to `skills/architecture/api-design/`.        |

## 3. Core Architectural Directives

1. **Storage and File Naming:** All ADR files must reside under `docs/architecture/adr/`. Files must follow the date-stamped naming convention: `YYYYMMDD-kebab-case-description.md` (for example `20260920-use-postgres-for-ledger.md`).
2. **Deterministic Lifecycle States:** Every record must declare one of four unambiguous statuses:
   - `proposed`: Open for team review and benchmarking. Zero code changes committed.
   - `accepted`: Decision formally ratified. Implementation authorized.
   - `deprecated`: Replaced or phased out. Migration directives documented.
   - `superseded`: Replaced by a subsequent ADR. Must reference the replacement file link.
3. **Mandatory Alternatives Evaluation:** An ADR must evaluate at least two viable alternatives against the chosen path. Document concrete trade-offs, not subjective preferences.
4. **Honest Consequence Ledger:** Document both positive benefits and negative compromises. Include ongoing maintenance overhead, failure modes, and rollback strategies.
5. **Automated Indexing:** Maintain `docs/architecture/adr/README.md` using an automated generator script that parses YAML frontmatter to prevent stale catalogs.

## 4. Execution Workflow

### Step 1: Context & Problem Formulation

- **Action:** Document the business problem, current state bottlenecks, and operational constraints.
- **Stop Condition:** Halt if the scope encompasses multiple disjointed architectural choices. Split into separate records.
- **Validation:** Clear problem statement articulated in two sentences or fewer.

### Step 2: Options and Trade-Off Evaluation

- **Action:** Compare candidate options across performance, operational complexity, licensing, and team familiarity.
- **Validation:** Rationale explains why dismissed alternatives were rejected.

### Step 3: Consequence and Rollback Documentation

- **Action:** Enumerate positive capabilities, negative technical debt, and step-by-step rollback procedures.
- **Validation:** Rollback plan specifies how to reverse the decision if production metrics degrade.

## 5. Reference Implementation

### Standard Architecture Decision Record Markdown Template

```markdown
---
id: "001"
title: "Adopt PostgreSQL Partitioning for Transaction Ledger"
date: "2026-09-20"
status: "accepted"
author: "Gandalf (Chief Systems Architect)"
tags: ["database", "postgres", "partitioning", "scale"]
supersedes: ""
supersededBy: ""
---

# ADR 001: Adopt PostgreSQL Partitioning for Transaction Ledger

## 1. Context

- **Problem:** The transaction ledger table exceeds 50 million records, causing sequential vacuum stalls and p99 query latency spikes exceeding 450 milliseconds on monthly range queries.
- **Current State:** Single monolithic table with composite B-Tree indexes.
- **Constraints:** Must maintain zero application downtime during migration. Maximum allowed p99 query latency is 25 milliseconds.

## 2. Decision

- **Chosen Path:** Implement declarative range partitioning on `created_at` broken down by calendar month, with a default fallback partition.
- **Options Evaluated:**
  1. _MongoDB Sharded Cluster:_ Rejected due to operational complexity and lack of native multi-document relational constraints.
  2. _TimescaleDB Extension:_ Rejected due to vendor lock-in concerns and non-standard cloud managed database support.
  3. _PostgreSQL Declarative Range Partitioning:_ Selected for native engine support, predictable partition pruning, and seamless ORM compatibility.

## 3. Consequences

- **Positive:**
  - Partition pruning reduces monthly query scan volume by over 90 percent.
  - Vacuum operations isolate to individual active monthly partitions.
- **Negative:**
  - Global unique constraints across partitions require composite primary keys including `created_at`.
  - Monthly partition generation requires automated cron provisioning.
- **Rollback Plan:** If query planning regression occurs, restore from snapshot to monolithic unpartitioned table using the dual-write sync queue.
```

### Automated ADR Catalog Generator Script (Node.js)

```javascript
import fs from "node:fs";
import path from "node:path";

export function generateAdrCatalog(adrDir, outputPath) {
  const files = fs
    .readdirSync(adrDir)
    .filter((file) => file.endsWith(".md") && file !== "README.md");

  const entries = files
    .map((file) => {
      const raw = fs.readFileSync(path.join(adrDir, file), "utf8");
      const idMatch = raw.match(/id:\s*"([^"]+)"/);
      const titleMatch = raw.match(/title:\s*"([^"]+)"/);
      const statusMatch = raw.match(/status:\s*"([^"]+)"/);
      const dateMatch = raw.match(/date:\s*"([^"]+)"/);

      return {
        file,
        id: idMatch ? idMatch[1] : "N/A",
        title: titleMatch ? titleMatch[1] : file,
        status: statusMatch ? statusMatch[1] : "unknown",
        date: dateMatch ? dateMatch[1] : "unknown",
      };
    })
    .sort((a, b) => a.id.localeCompare(b.id, undefined, { numeric: true }));

  let markdown = "# Architecture Decision Records Catalog\n\n";
  markdown += "| ID | Title | Status | Date | Document |\n";
  markdown += "|---|---|---|---|---|\n";

  for (const entry of entries) {
    markdown += `| ${entry.id} | ${entry.title} | **${entry.status}** | ${entry.date} | [${entry.file}](./${entry.file}) |\n`;
  }

  fs.writeFileSync(outputPath, markdown, "utf8");
}
```

## 6. Validation Gate

Run before accepting an ADR:

- [ ] ADR is committed under `docs/architecture/adr/` with date-stamped filename.
- [ ] YAML frontmatter contains valid `id`, `title`, `date`, `status`, and `author`.
- [ ] At least two alternatives are explicitly analyzed and dismissed with technical rationale.
- [ ] Negative trade-offs and maintenance liabilities are honestly disclosed.
- [ ] Concrete rollback plan or criteria for reversal is documented.
- [ ] Catalog index file reflects the newly proposed or accepted record.

## 7. Versioning & Portability Matrix

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-20): Elevated to Sauron Tier-5 specification with automated catalog generation tooling.

| Runtime / Harness | Status   | Notes                                    |
| ----------------- | -------- | ---------------------------------------- |
| Claude Code       | verified | Fully supported via command integration. |
| Cursor            | verified | Compatible with editor rule context.     |
| Windsurf          | verified | Fully functional.                        |
| Antigravity       | verified | Certified.                               |
