# 23 Enterprise Software Engineering Context Domains

This normative reference details the 23 software engineering context domains and 45 specification templates located under `context/software-engineering/`.

Managed by `skills/workflow/define-enterprise-context/`. All output context files must be provisioned inside `projects/<project-name>/context/software-engineering/`.

---

## 1. Core Architecture & System Foundation (Domains 1–4)

1. **System Architecture (`architecture/`)**
   - `component-topology.md`: Component boundary contracts, microservice / modular monolith topology.
   - `data-flow-and-runtime.md`: Synchronous vs asynchronous runtime flow, message propagation, edge delivery.
   - `system-architecture.md`: High-level system design, system context, primary external dependencies.
2. **Backend Services (`backend/`)**
   - `api-design-and-contracts.md`: REST, GraphQL, gRPC protocols, error envelopes (RFC 7807), rate limiting.
   - `service-boundaries-and-logic.md`: Domain logic isolation, dependency injection, domain services.
3. **Database & Persistence (`database/`)**
   - `schema-and-data-models.md`: Primary entities, relations, indexing, partitioning strategy.
   - `data-lifecycle-and-integrity.md`: ACID/BASE isolation, transactional boundaries, retention, archiving.
4. **Architecture Decisions (`decisions/`)**
   - `architecture-decision-records.md`: ADR framework (MADR standard), decision status, options evaluated.

---

## 2. Infrastructure, Platform & Delivery (Domains 5–9)

5. **Release & Deployment (`deployment/`)**
   - `environment-configuration.md`: Dev/Staging/Prod environment boundaries, 12-Factor config rules.
   - `release-and-deployment-process.md`: Blue/green, canary, progressive delivery, automated rollback conditions.
6. **Deployment Platform (`deployment-platform/`)**
   - `platform-hosting-and-compute.md`: Compute runtime (Kubernetes, ECS, Serverless, Cloud Run, Bare Metal).
7. **Development Setup (`development/`)**
   - `local-setup-and-tooling.md`: Local dev environment bootstrap, containerized dependencies, dev seeds.
   - `workflow-and-testing-standards.md`: Branching strategy, git conventions, local commit hooks.
8. **Cloud Infrastructure (`infrastructure/`)**
   - `infrastructure-architecture.md`: Cloud topology, VPC, subnet isolation, IaC definitions (Terraform/OpenTofu).
   - `networking-and-storage.md`: Ingress, DNS, TLS termination, object storage, block volumes.
9. **Developer Experience (`developer-experience/`)**
   - `internal-developer-portal.md`: Developer onboarding, tooling catalog, runbook links.
   - `monorepo-and-tooling-architecture.md`: Workspace packages, build caching, task pipelines (Turborepo/Nx).

---

## 3. Governance, Security, Quality & Resilience (Domains 10–14)

10. **Security & Auth (`security/`)**
    - `auth-and-data-protection.md`: AuthN/AuthZ, JWT/OIDC, session management, encryption at rest and in transit.
    - `security-and-threat-model.md`: OWASP Top 10 mitigations, STRIDE threat model, zero-trust perimeter.
11. **Governance & Policy (`governance-and-policy/`)**
    - `code-ownership-and-review-policies.md`: CODEOWNERS rules, mandatory reviewers, approval gates.
    - `license-and-dependency-governance.md`: Allowed OSS licenses (MIT/Apache), forbidden licenses (GPL/AGPL).
12. **Quality & Compliance (`quality-and-compliance/`)**
    - `code-quality-and-static-analysis.md`: Linter rules, SonarQube / SAST thresholds, coverage requirements.
    - `regulatory-and-audit-compliance.md`: SOC2, HIPAA, GDPR, ISO 27001 data sovereignty compliance.
13. **Disaster Recovery (`disaster-recovery/`)**
    - `backup-and-business-continuity.md`: Snapshot schedules, cross-region replication, backup testing.
    - `rto-rpo-and-failover-spec.md`: Recovery Time Objective (RTO), Recovery Point Objective (RPO), failover drill playbooks.
14. **Cost & FinOps (`cost-and-finops/`)**
    - `capacity-planning-and-budgets.md`: Scaling limits, compute sizing, cost runaway guardrails.
    - `cloud-cost-and-resource-tagging.md`: Cost allocation tags, cost center attribution, waste reduction.

---

## 4. Extended Capabilities, Data, AI & Operations (Domains 15–23)

15. **Data Engineering (`data-engineering/`)**
    - `data-warehousing-and-analytics.md`: Warehouse schema, OLAP models (Snowflake, BigQuery, ClickHouse).
    - `pipeline-and-etl-architecture.md`: Batch and streaming ingestion pipelines, schema registry, backfills.
16. **AI & Machine Learning (`ai-and-ml/`)**
    - `model-serving-and-llm-gateways.md`: LLM model routing, latency budgets, fallbacks, token spend telemetry.
    - `vector-storage-and-rag-pipelines.md`: Vector database indexing, embedding models, retrieval pipelines.
17. **Third-Party Integrations (`integrations/`)**
    - `event-bus-and-external-services.md`: Kafka, RabbitMQ, SQS message contracts, dead letter queues.
    - `third-party-apis-and-webhooks.md`: Webhook ingestion, signature verification, idempotent delivery.
18. **Observability (`observability/`)**
    - `incident-and-health-monitoring.md`: PagerDuty alert definitions, SLOs/SLAs, health checks, runbooks.
    - `telemetry-and-signals.md`: OpenTelemetry spans, Prometheus metrics, structured JSON logging.
19. **Performance & CDN (`performance/`)**
    - `caching-and-cdn-strategy.md`: Redis / memory cache hierarchies, CDN cache-control headers, invalidation.
    - `load-testing-and-benchmarking.md`: k6 / Locust load test scenarios, p95/p99 latency thresholds.
20. **Frontend Architecture (`frontend/`)**
    - `state-and-client-performance.md`: Client cache, hydration, Web Vitals (LCP, INP, CLS).
    - `ui-and-component-architecture.md`: Component hierarchy, design tokens, micro-frontends / design system.
21. **Mobile Architecture (`mobile/`)**
    - `mobile-app-architecture.md`: Native / React Native / Flutter topology, navigation, device hardware access.
    - `offline-sync-and-push-services.md`: Local persistence (SQLite/Watermelon), push notification pipelines.
22. **Product Roadmap (`roadmap/`)**
    - `roadmap-and-tech-debt.md`: Milestone phases, feature horizons, tech debt tracking, deprecation schedules.
23. **Test Strategy (`testing/`)**
    - `test-strategy-and-suites.md`: Test pyramid distribution, E2E vs integration boundaries, CI test runners.
    - `test-data-and-environments.md`: Synthetic test seed generation, ephemeral environments, fixture mocking.

---

## 5. Dynamic Enterprise Expansion Protocol

The 45 specification templates in `context/software-engineering/` define the **foundational baseline taxonomy**. Because complex enterprise architectures regularly demand domain-specific depth, `define-enterprise-context` dynamically discovers and generates additional specialized specification files under the appropriate domain directory whenever requirements emerge during the grilling interview:

### Common Enterprise Expansion Examples:

- **`architecture/`:**
  - `c4-model-component-level3.md` (Deep C4 component diagrams)
  - `multi-tenant-isolation-strategy.md` (SaaS data/tenant isolation)
  - `event-driven-domain-events.md` (Event sourcing / CQRS design)
- **`security/`:**
  - `rbac-abac-permission-matrix.md` (Fine-grained authorization grid)
  - `secrets-rotation-lifecycle.md` (Vault / KMS key rotation policy)
  - `zero-trust-network-perimeter.md` (mTLS service-to-service rules)
  - `incident-containment-playbook.md` (Breach containment workflows)
- **`backend/`:**
  - `grpc-protobuf-contracts.md` (gRPC service and message definitions)
  - `rate-limiting-and-throttling-policies.md` (Token bucket / leaky bucket specs)
  - `webhook-idempotency-and-delivery.md` (Retry schedules and deduplication)
- **`database/`:**
  - `sharding-and-partitioning-strategy.md` (Horizontal sharding rules)
  - `zero-downtime-migration-rules.md` (Expand/contract database migrations)
  - `data-masking-and-pii-governance.md` (PII column masking in lower envs)
- **`disaster-recovery/` & `cost-and-finops/`:**
  - `multi-region-active-active-failover.md` (Cross-region replication & DNS failover)
  - `unit-economics-and-cost-allocation.md` (Cost per tenant / per transaction model)

---

## 6. Domain Audit & Health Rubric

When auditing an existing enterprise codebase:

- **HEALTHY:** File exists in `projects/<project-name>/context/software-engineering/`, contains verified facts, has 0 unresolved placeholders, and aligns with current production architecture.
- **EXPANDED:** File exists as an enterprise addition beyond baseline 45 templates, strictly housed under its parent domain folder, adhering to standard markdown structure.
- **DRIFTED:** File exists but contains stale data contradicting actual implementation or unresolved `[PLACEHOLDER]` text.
- **MISSING:** Domain document or folder is absent from the project context directory.
