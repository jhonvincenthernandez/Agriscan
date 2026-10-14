---
name: codebase-knowledge-graph
description: AST-based dependency and relationship mapping for codebases. Generates graph.json, graph-report.md, and interactive graph.html. Enables high token efficiency architecture navigation.
department: architecture
ownerAgent: aragorn
triggerCommand: /codebase-graph
antiPatternsPrevented:
  - AP-16
  - AP-41
  - AP-46
  - AP-47
  - AP-51
---

# Codebase Knowledge Graph

## 0. Identity

- **Role:** Retrieval Architect. Owns index topology and query routing over AST dependency graphs for token-efficient navigation.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Retrieval Architect).
- **Seniority bar:** Staff (Appendix B).
- **Staff judgment:** Records why graph-index navigation beats full-file context dumps (deterministic fan-in and fan-out at fractions of the token cost, rejected whole-repo scans) and why god-node detection precedes refactoring.
- **Authority:** Tier-4 operational skill within `skills/architecture/codebase-knowledge-graph/` under System Architect supervision (`core/fellowship/aragorn.md`).
- **Must not define:** Runtime production business logic or database schemas.
- **Normative base:** `core/fellowship/aragorn.md`, `rules/engineering/architecture-boundaries.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-16 (context dumping full files instead of using graph index), AP-41 (no starting state), AP-46 (vague first turn on literal models), AP-47 (context rot on long sessions), and AP-51 (silent token drain).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                                  |
| --- | ---------------- | ------------------------------------------------------------------------------------------------------ |
| 1   | Task             | Parse repository AST symbols and imports to emit graph.json, graph-report.md, and graph.html.          |
| 2   | Target Tool      | Polyglot: TypeScript, JavaScript, Python, Go, Rust, Java, Kotlin, PHP, Ruby, C/C++, C#.                |
| 3   | Output Format    | `.sauron/graph/graph.json`, `.sauron/graph/graph-report.md`, `.sauron/graph/graph.html`.               |
| 4   | Constraints      | Strict lowercase kebab-case naming. Zero cloud dependencies. Deterministic local execution.            |
| 5   | Input            | Target project codebase path containing source files in any supported language.                        |
| 6   | Context          | Eliminates massive raw file reads during architecture audits, saving up to 70x tokens.                 |
| 7   | Audience         | Principal software architects, AI agents, code reviewers, and engineering teams.                       |
| 8   | Success Criteria | Graph extraction generates valid nodes, edges, cycle detection, and interactive visualizer in seconds. |
| 9   | Examples         | See Section 5.                                                                                         |

## 2. Trigger Matrix

| Trigger Condition                                            | Fire? | Action / Route                                                          |
| ------------------------------------------------------------ | ----- | ----------------------------------------------------------------------- |
| User or agent asks to understand repo architecture or layout | YES   | Run `sauron graph .` and query `.sauron/graph/graph-report.md`.         |
| Detecting circular dependencies or god files in workspace    | YES   | Inspect high-degree nodes and cycle list in `.sauron/graph/graph.json`. |
| User asks for visual dependency graph in browser             | YES   | Direct user to open `.sauron/graph/graph.html`.                         |
| Creating or refactoring business domain models               | NO    | Route to `skills/architecture/clean-architecture/`.                     |
| Standardizing REST/HTTP API contracts                        | NO    | Route to `skills/architecture/api-design/`.                             |

## 3. Core Architectural Directives

1. **Deterministic Extraction:** AST symbol identification (functions, classes, types, interfaces) and import resolution execute via local static analysis without running target source code.
2. **Strict Sauron Naming Standard:** All emitted artifacts strictly use lowercase kebab-case (`graph.json`, `graph-report.md`, `graph.html`). Uppercase snake_case or camelCase filenames are forbidden.
3. **Token Conservation Rule:** Agents must query `graph-report.md` or filter `graph.json` before reading multi-thousand-line source directories into active context.
4. **Architectural Guardrails:**
   - **God Nodes:** Any module with total degree (in-degree + out-degree) greater than 10 warrants architectural decomposition review.
   - **Circular Dependencies:** 0 cycles allowed in production core libraries.

## 4. Execution Workflow

### Step 1: Execute Graph Generation

Run the CLI command at the root of the target project:

```bash
node bin/sauron.mjs graph .
```

### Step 2: Agent Architecture Analysis

1. Read `.sauron/graph/graph-report.md` to identify top hub modules and check for circular dependencies.
2. Query `.sauron/graph/graph.json` to inspect symbols or link targets for any specific module.
3. Target only the relevant source files for inspection or modification.

### Step 3: Interactive Browser Visualization

To visually explore the node graph:

```bash
start .sauron/graph/graph.html
```

## 5. Artifact Standards

All generated artifacts adhere to:

| Artifact          | Purpose                                                   | Location                        |
| :---------------- | :-------------------------------------------------------- | :------------------------------ |
| `graph.json`      | Node/edge graph data with symbol counts and import links  | `.sauron/graph/graph.json`      |
| `graph-report.md` | Quantitative architecture analysis and circularity checks | `.sauron/graph/graph-report.md` |
| `graph.html`      | Interactive in-browser visual dependency exploration      | `.sauron/graph/graph.html`      |
