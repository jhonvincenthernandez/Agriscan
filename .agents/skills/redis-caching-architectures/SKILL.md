---
name: redis-caching-architectures
description: Multi-tier Redis caching strategies, invalidation stampede mitigation, probabilistic early expiration, and write-through patterns.
department: backend
ownerAgent: frodo
triggerCommand: /redis-caching-architectures
antiPatternsPrevented:
  - AP-1
  - AP-6
  - AP-18
  - AP-26
---

# Redis Caching Architectures

## 0. Identity

- **Role:** Service Builder. Owns in-memory caching implementation with topology and invalidation discipline inside scoped files.
- **Role source:** Appendix A of `skills/_template/skill-name/SKILL.md` (Service Builder).
- **Seniority bar:** Staff (Appendix B). Records why invalidation protocols beat TTL-only hope (stale reads corrupt decisions, rejected time-only expiry) and why topology choice precedes client tuning.
- **Authority:** Normative specification under `skills/backend/redis-caching-architectures/`.
- **Must not define:** Source-of-truth relational database constraints.
- **Normative base:** `core/fellowship/frodo.md`, `rules/engineering/architecture-boundaries.md`, `rules/common/code-style-standards.md`, `references/anti-patterns.md`.

## 1. Intent (9 Dimensions)

| #   | Dimension        | Value                                                                                   |
| --- | ---------------- | --------------------------------------------------------------------------------------- |
| 1   | Task             | Implement resilient caching topologies and stampede prevention mechanisms.              |
| 2   | Target Tool      | Redis Cluster, Redis Sentinel, DragonflyDB, Node.js/Go backend services.                |
| 3   | Output Format    | Cache client wrappers, Lua scripts, and TTL calculation algorithms.                     |
| 4   | Constraints      | Ban unkeyed caches and unbounded TTLs. Always employ jitter on expiration.              |
| 5   | Input            | Query volume metrics, latency profiles, and cache hit-ratio telemetry.                  |
| 6   | Context          | Eliminates thundering herd problems, cache penetration, and stale read inconsistencies. |
| 7   | Audience         | Systems architects and senior backend engineers.                                        |
| 8   | Success Criteria | 95%+ cache hit ratio, bounded memory utilization, sub-2ms cache response times.         |
| 9   | Examples         | See Section 5.                                                                          |

## 2. Trigger Matrix

| Trigger                                               | Fire? | Notes                                 |
| ----------------------------------------------------- | ----- | ------------------------------------- |
| Scaling high-read endpoints with in-memory caching    | YES   | Cache-aside or write-through pattern. |
| Preventing database crashes during cache expiration   | YES   | Cache stampede mitigation.            |
| Designing distributed session stores or rate limiters | YES   | Redis atomic commands.                |
| Designing primary persistent storage schemas          | NO    | Route to database principles.         |

## 3. Core Directives

1. **XFetch Probabilistic Early Recomputation:** Recompute cached assets before hard expiration:
   `readTime - (delta * beta * ln(random())) > expiry`
2. **Distributed Mutex Locking (Redlock):** On complete cache miss for expensive queries, acquire an ephemeral distributed lock before querying disk.
3. **Bloom Filter Screening:** Pass incoming requests through a Bloom filter to reject guaranteed non-existent keys before touching databases.
4. **Jittered Expirations:** Add random variance (+/- 15%) to TTL values to avoid synchronized bulk expirations.

## 4. Execution Workflow

### Step 1: Cache Pattern Selection

- **Action:** Evaluate consistency trade-offs between Cache-Aside, Write-Through, and Write-Behind.
- **Validation:** Strong consistency requirements choose Cache-Aside with transaction-bound invalidation.

### Step 2: Serialization & Memory Budget

- **Action:** Enforce binary (MessagePack/Protobuf) or compressed JSON to limit RAM footprint.
- **Validation:** Memory limit policy set to `volatile-lru` or `allkeys-lru`.

## 5. Code Example

```typescript
export async function getWithProbabilisticRefresh<T>(
  redis: RedisClient,
  key: string,
  fetchFn: () => Promise<T>,
  ttlSeconds: number,
  beta = 1.0,
): Promise<T> {
  const record = await redis.get(key);
  if (record) {
    const { value, computeTimeMs, expiresAt } = JSON.parse(record);
    const now = Date.now();
    const shouldRefresh =
      now - computeTimeMs * beta * Math.log(Math.random()) > expiresAt;
    if (!shouldRefresh) return value;
  }
  const start = Date.now();
  const fresh = await fetchFn();
  const computeTimeMs = Date.now() - start;
  await redis.set(
    key,
    JSON.stringify({
      value: fresh,
      computeTimeMs,
      expiresAt: Date.now() + ttlSeconds * 1000,
    }),
    "EX",
    ttlSeconds + 60,
  );
  return fresh;
}
```
