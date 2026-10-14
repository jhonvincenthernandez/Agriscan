---
name: graphql-federation-patterns
description: Distributed GraphQL schema federation, Apollo Federation subgraph composition, entity resolution, and @key directives.
department: backend
ownerAgent: aragorn
triggerCommand: /graphql-federation-patterns
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-18
  - AP-26
---

# GraphQL Federation Patterns

## 0. Identity

- **Role:** API Designer. Owns federated contract composition with entity boundaries and resolution rules.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (API Designer).
- **Seniority bar:** Staff (Appendix B). Records why subgraph boundaries beat monolith gateways (independent evolution per team, rejected coupled supergraphs) and why entity resolution contracts precede query convenience.
- **Authority:** Normative engineering standard for federated GraphQL architectures under `skills/backend/graphql-federation-patterns/`.
- **Must not define:** Direct database table schemas or client-side query hooks.
- **Normative base:** `core/fellowship/frodo.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Blocks AP-1, AP-4, AP-18, AP-26, and AP-28.

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                                   |
| --- | ---------------- | ------------------------------------------------------------------------------------------------------- |
| 1   | Task             | Define, validate, and orchestrate federated subgraphs into a unified supergraph schema.                 |
| 2   | Target Tool      | Apollo Router, Rover CLI, Node.js GraphQL servers, and federated gateway runtimes.                      |
| 3   | Output Format    | Validated GraphQL Schema Definition Language (SDL) files with Apollo Federation v2 directives.          |
| 4   | Constraints      | Prohibit monolithic schema stitching. All shared entities must declare explicit `@key` directives.      |
| 5   | Input            | Subgraph schema definitions, entity relationships, and service routing boundaries.                      |
| 6   | Context          | Prevents broken distributed joins, supergraph composition errors, and runaway query fan-outs.           |
| 7   | Audience         | Backend engineers, distributed systems architects, and API platform teams.                              |
| 8   | Success Criteria | Clean Rover supergraph composition, hermetic entity resolvers, zero cross-subgraph query amplification. |
| 9   | Examples         | See Section 5.                                                                                          |

## 2. Trigger Matrix

| Trigger                                                    | Fire? | Notes                                 |
| ---------------------------------------------------------- | ----- | ------------------------------------- |
| Composing multi-service GraphQL subgraphs into supergraph  | YES   | Core architectural trigger.           |
| Defining cross-service entity relations with `@key`        | YES   | Entity resolution guidance.           |
| Resolving N+1 query waterfalls across federated boundaries | YES   | Dataloader batching pattern.          |
| Writing single standalone monolithic GraphQL schema        | NO    | Route to standard backend API design. |

## 3. Architectural Directives

1. **Explicit Entity Ownership:** Every federated entity must declare a single authoritative owning subgraph. Owning subgraphs define base fields; consuming subgraphs extend fields using `@key(fields: "id")`.
2. **Deterministic Entity Resolvers:** Implement `__resolveReference` using batched dataloaders to prevent N+1 remote RPC roundtrips during gateway query execution.
3. **Hermetic Subgraph Contracts:** Never allow a subgraph to invoke another subgraph directly via HTTP. All cross-domain queries must route exclusively through the federated gateway.
4. **Contract Evolution & Deprecation:** Deprecate fields with `@deprecated(reason: "...")` before schema retirement. Verify backward compatibility using schema check pipelines.

## 4. Execution Workflow

### Step 1: Subgraph Boundary Definition

- **Action:** Isolate domain ownership boundaries. Determine which service owns core entity fields versus projected extensions.
- **Validation:** No entity fields duplicated across subgraphs without explicit `@shareable` directives.

### Step 2: Supergraph Composition Audit

- **Action:** Run Rover composition validation against all subgraph schemas.
- **Validation:** Rover outputs zero schema composition or naming collisions.

### Step 3: Dataloader Reference Resolution

- **Action:** Implement batched entity reference resolvers to guarantee single-pass database fetching.
- **Validation:** Gateway query plan indicates parallel execution branches without nested loops.

## 5. Reference Implementation

```graphql
extend schema
  @link(
    url: "https://specs.apollo.dev/federation/v2.0"
    import: ["@key", "@shareable", "@external"]
  )

type User @key(fields: "id") {
  id: ID!
  email: String! @shareable
  profile: Profile
}

extend type Order @key(fields: "id") {
  id: ID!
  customerId: ID!
  customer: User
}
```

```typescript
// Subgraph Entity Reference Resolver with DataLoader
export const userReferenceResolver = {
  __resolveReference: async (reference: { id: string }, { dataLoaders }) => {
    return dataLoaders.userById.load(reference.id);
  },
};
```
