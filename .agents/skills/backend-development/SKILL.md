---
name: backend-development
description: Framework-agnostic backend engineering standards for layered architecture, repository-service patterns, query optimization, atomic transactions, cache-aside strategies, and structured logging.
department: backend
ownerAgent: frodo
triggerCommand: /backend-development
antiPatternsPrevented:
  - AP-1
  - AP-4
  - AP-18
  - AP-26
  - AP-28
---

# Backend Development Principles

## 0. Identity

- **Role:** Service Builder. Owns layered server implementation with data boundaries and resilient recovery inside scoped files.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Service Builder).
- **Seniority bar:** Staff (Appendix B). Records why layered boundaries beat fat-controller speed (testability compounds quarterly, rejected logic-in-route shortcuts) and why atomic transactions beat scattered writes.
- **Authority:** Normative tier-4 engineering specification for backend applications under `skills/backend/backend-development/`.
- **Must not define:** Frontend UI layout, styling tokens, or client-side hydration routines.
- **Normative base:** `core/fellowship/frodo.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.
- **Anti-pattern gate:** Enforces AP-1 (strict testable boundaries), AP-4 (zero unauthorized state alterations), and AP-18 (bounded queries).

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                                        |
| --- | ---------------- | ------------------------------------------------------------------------------------------------------------ |
| 1   | Task             | Architect, implement, and review production-grade server architectures and business logic layers.            |
| 2   | Target Tool      | Node.js, TypeScript, Express, Next.js API, PostgreSQL, Redis, Supabase, Docker.                              |
| 3   | Output Format    | Modular repository, service, and controller implementations with test-verified contracts.                    |
| 4   | Constraints      | Strict separation of concerns: Controller -> Service -> Repository. No direct SQL in route handlers.         |
| 5   | Input            | Product capability specifications, domain models, database schemas, performance targets.                     |
| 6   | Context          | Prevents monolithic controller sprawl, data corruption, database lock contention, and latency spikes.        |
| 7   | Audience         | Backend engineers, distributed systems developers, technical leads.                                          |
| 8   | Success Criteria | Clean layer isolation, sub-50ms p99 latency for read operations, 100 percent transaction rollbacks on error. |
| 9   | Examples         | See Section 5.                                                                                               |

## 2. Trigger Matrix

| Trigger Condition                                  | Fire? | Action / Route                                        |
| -------------------------------------------------- | ----- | ----------------------------------------------------- |
| Structuring server repository or service layers    | YES   | Apply repository-service-controller pattern.          |
| Preventing N+1 queries or optimizing data fetching | YES   | Implement batched joins or DataLoader abstractions.   |
| Adding cache-aside logic with Redis                | YES   | Use cache-aside pattern with explicit TTL expiration. |
| Implementing multi-table state mutations           | YES   | Wrap operations inside atomic database transactions.  |
| Designing public HTTP REST contracts               | NO    | Route to `skills/architecture/api-design/`.           |

## 3. Core Architectural Directives

1. **Strict Layer Separation:**
   - **Controllers:** Handle HTTP request parsing, header validation, and response status mapping. Contain zero business logic.
   - **Services:** Execute business rules, orchestration, permission checks, and domain events. Independent of HTTP transport.
   - **Repositories:** Own direct data storage interactions, SQL queries, and ORM abstractions.
2. **N+1 Query Elimination:** Banish single-record query loops. Use batched `WHERE IN (...)` queries, composite joins, or DataLoader patterns to guarantee constant O(1) query count across varying result set sizes.
3. **Cache-Aside Architecture:** Always check cache before querying primary storage. On a cache miss, load from storage, populate cache with a deterministic time-to-live (TTL), and return the payload. Handle cache degradation gracefully without crashing request lifecycles.
4. **Atomic Transaction Scope:** Multi-step writes that must succeed or fail together must execute within a transactional boundary. Explicitly handle rollback on any caught exception.
5. **Structured Logging:** Output logs as single-line JSON records containing ISO timestamps, log severity level, correlation ID, and sanitized payload details. Banish passwords, tokens, and personally identifiable information from logs.

## 4. Execution Workflow

### Step 1: Interface and Boundary Design

- **Action:** Declare TypeScript interfaces for the repository contract and service operations.
- **Stop Condition:** Halt if repository methods expose underlying database connection handles directly to callers.
- **Validation:** Clear boundary types defined for input data transfer objects and output entities.

### Step 2: Query Optimization & Transaction Setup

- **Action:** Formulate parameterized queries with index coverage. Wrap multi-table updates in an atomic block.
- **Stop Condition:** Halt if dynamic string concatenation is detected in SQL query strings.
- **Validation:** Database queries execute with zero unindexed table scans.

### Step 3: Resilient Service Layer Execution

- **Action:** Implement business logic with exponential backoff on transient upstream failures.
- **Validation:** Service emits typed domain errors with error chaining preserved via `Error.cause`.

## 5. Reference Implementation

### TypeScript (Layered Repository, Service, and Cache-Aside Pattern)

```typescript
import { Redis } from "ioredis";

export interface UserEntity {
  id: string;
  email: string;
  status: "ACTIVE" | "SUSPENDED";
  createdAt: Date;
}

export interface UserRepository {
  findById(id: string): Promise<UserEntity | null>;
  findByIds(ids: string[]): Promise<UserEntity[]>;
  updateStatus(id: string, status: UserEntity["status"]): Promise<void>;
}

export class CachedUserRepository implements UserRepository {
  constructor(
    private readonly primaryRepo: UserRepository,
    private readonly redis: Redis,
    private readonly ttlSeconds: number = 300,
  ) {}

  async findById(id: string): Promise<UserEntity | null> {
    const cacheKey = `user:${id}`;
    const cachedData = await this.redis.get(cacheKey);

    if (cachedData) {
      return JSON.parse(cachedData) as UserEntity;
    }

    const user = await this.primaryRepo.findById(id);
    if (user) {
      await this.redis.setex(cacheKey, this.ttlSeconds, JSON.stringify(user));
    }

    return user;
  }

  // Batch query to eliminate N+1 problem
  async findByIds(ids: string[]): Promise<UserEntity[]> {
    if (ids.length === 0) return [];
    return this.primaryRepo.findByIds(ids);
  }

  async updateStatus(id: string, status: UserEntity["status"]): Promise<void> {
    await this.primaryRepo.updateStatus(id, status);
    await this.redis.del(`user:${id}`);
  }
}

export class UserService {
  constructor(private readonly userRepo: UserRepository) {}

  async activateUser(userId: string): Promise<UserEntity> {
    const user = await this.userRepo.findById(userId);
    if (!user) {
      throw new Error(`User with ID ${userId} not found`);
    }

    if (user.status === "ACTIVE") {
      return user;
    }

    await this.userRepo.updateStatus(userId, "ACTIVE");
    return { ...user, status: "ACTIVE" };
  }
}
```

## 6. Validation Gate

Run before deploying backend services:

- [ ] Route controllers contain zero direct SQL or ORM queries.
- [ ] Every multi-table state mutation executes inside an atomic transaction.
- [ ] Database queries are parameterized; zero dynamic string concatenation exists in SQL.
- [ ] List queries enforce bounded limits and utilize batch fetching rather than N+1 queries.
- [ ] Cache keys follow deterministic naming conventions and include explicit TTL expiration.
- [ ] Log outputs are structured JSON records with sensitive personal data redacted.

## 7. Versioning & Portability Matrix

- **Version:** 2.0.0
- **Changelog:**
  - `2.0.0` (2026-09-20): Elevated to Sauron Tier-5 standard. Integrated layered architecture, N+1 query mitigation, and cache-aside patterns from ECC.

| Runtime / Harness | Status   | Notes                                 |
| ----------------- | -------- | ------------------------------------- |
| Claude Code       | verified | Fully compatible with execution loop. |
| Cursor            | verified | Tested with rule adapters.            |
| Windsurf          | verified | Fully supported.                      |
| Antigravity       | verified | Certified.                            |
