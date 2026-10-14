# Enterprise Context Deep Interview Protocol (Grill-Me Pattern)

## Role / Authority

- **Role:** Deep requirements extraction and architectural grilling protocol modeled after Matt Pocock's `grill-me` pattern and `build-spec-interviewer`.
- **Authority:** Enforces an unskippable, structured multi-round interrogation before scaffolding any of the 23 enterprise domains (45 specification templates) in `context/software-engineering/`.
- **Target Output Directory:** `projects/<project-name>/context/software-engineering/`

---

## 1. Core Grilling Rules (Matt Pocock Grill-Me Standard)

1. **Never build or write first:** Zero template files or folders are touched before the interview finishes and explicit user approval is given.
2. **Batch 4–6 questions per round:** Group questions logically into 2–3 iterative rounds. Do not fire 20 questions in one dump.
3. **Number every single question:** Every question must have an explicit index (e.g. `1.`, `2.`, `3.`) so the user can easily answer by number or inline.
4. **Every question must be able to change the build:** Never ask fluffy, philosophical, or redundant questions. If the user already answered or it's obvious from manifests, do not ask it.
5. **Drill down based on answers:** Round 2 and Round 3 must directly probe edge cases, tradeoffs, and failure modes arising from Round 1 responses.
6. **Refuse full skips:** If the user says "just build it / skip questions", refuse per anti-pattern AP-1/AP-45. Compress immediately to the **Top 3 Most Critical Architectural Questions** and require explicit answers before proceeding.
7. **Isolate Guesses under Assumptions:** Any unconfirmed detail must be tagged explicitly as `[PLACEHOLDER: ...]` or listed under an `Assumptions` block.

---

## 2. Round 1: Enterprise Foundations & Architecture (4–6 Questions)

**Target Domains:** `architecture/`, `backend/`, `database/`, `decisions/`

1. **System Identity & Topology:**
   - What is the project name (`kebab-case`) and core enterprise mission? Is it a Modular Monolith, Microservices, Event-Driven, or Serverless system?
2. **Component Boundaries & Communication:**
   - What are the primary service boundaries (e.g. Auth, Billing, Core Domain), and what is the inter-service protocol (REST, gRPC, GraphQL, Kafka/Event Bus)?
3. **Persistence & Consistency Guarantees:**
   - Which primary operational databases will be used (PostgreSQL, MySQL, DynamoDB, MongoDB), and what are the transactional boundaries (Strict ACID vs Eventual Consistency)?
4. **Caching & Hot Data Strategy:**
   - Is there a distributed cache (Redis/Memcached) or CDN edge caching required, and what is the invalidation strategy?
5. **Non-Negotiable ADR Constraints:**
   - Are there any fixed architectural invariants or locked ADR decisions that must never be violated?

---

## 3. Round 2: Platform, Cloud, Security & Compliance (4–6 Questions)

**Target Domains:** `infrastructure/`, `deployment/`, `deployment-platform/`, `security/`, `governance-and-policy/`, `quality-and-compliance/`, `disaster-recovery/`

1. **Cloud & Compute Infrastructure:**
   - Which cloud provider (AWS, GCP, Azure, Hybrid) and compute engine (Kubernetes/EKS, ECS, Serverless, Bare Metal) are targeted?
2. **Infrastructure as Code & Network Isolation:**
   - What IaC tooling is mandated (Terraform, OpenTofu, CDK), and what VPC/subnet or service mesh constraints exist?
3. **CI/CD & Progressive Delivery:**
   - What deployment workflow is required (Blue/Green, Canary, Rolling), and what automated rollback conditions apply?
4. **Auth & Identity Governance:**
   - What is the identity model (OAuth2/OIDC, JWT, Okta, Auth0, Keycloak) and authorization mechanism (RBAC vs ABAC)?
5. **Regulatory Compliance & Recovery Objectives (RTO/RPO):**
   - Which compliance frameworks apply (SOC2, HIPAA, GDPR, PCI-DSS)? What are the exact RTO (Recovery Time) and RPO (Recovery Point) targets?

---

## 4. Round 3: Extended Capabilities, AI, Data & Operations (4–6 Questions)

**Target Domains:** `data-engineering/`, `ai-and-ml/`, `integrations/`, `observability/`, `cost-and-finops/`, `testing/`, `frontend/`, `mobile/`

1. **Data Engineering & Analytics Warehouse:**
   - Are there OLAP data warehouses (Snowflake, BigQuery, ClickHouse) or ETL pipelines (dbt, Airflow, Spark) in scope?
2. **AI / LLM Gateways (if applicable):**
   - Does the architecture feature LLM integration, model gateways (LiteLLM, LangChain), or Vector RAG pipelines (Pinecone, Qdrant, pgvector)?
3. **Observability, Tracing & Alerting:**
   - What are the OpenTelemetry, Prometheus, Datadog metrics/tracing expectations, and incident escalation channels (PagerDuty, Slack)?
4. **Testing Strategy & Coverage Thresholds:**
   - What is the testing pyramid distribution (Unit vs Integration vs E2E), and what are the mandatory coverage/assertion thresholds?
5. **Cost & FinOps Guardrails:**
   - Are there monthly cloud budget limits, mandatory resource tagging taxonomies, or auto-scaling ceilings?

---

## 5. Build Spec Synthesis & Confirmation Gate

After completing the rounds, compile an **Enterprise Context Blueprint** with the exact structure below and halt for approval:

```markdown
# Enterprise Context Blueprint: [project-name]

- **Target Directory:** projects/[project-name]/context/software-engineering/
- **Topology:** [Modular Monolith | Microservices | Event-Driven | Serverless]
- **Target Runtime:** [Compute / Cloud / DB]
- **SLAs / Targets:** RTO: [target] | RPO: [target] | Compliance: [frameworks]

## 23 Domains & Specs to Provision:

- architecture/ (component-topology.md, data-flow-and-runtime.md, system-architecture.md)
- backend/ (api-design-and-contracts.md, service-boundaries-and-logic.md)
- database/ (schema-and-data-models.md, data-lifecycle-and-integrity.md)
- security/ (auth-and-data-protection.md, security-and-threat-model.md)
- [List of all 23 domains to be provisioned]

## Locked Decisions:

- [Key architectural decisions confirmed in interview]

## Assumptions & Unresolved Placeholders:

- [Any items not explicitly answered, marked to retain [PLACEHOLDER] format]
```

**STOP CONDITION:** Halt execution. Never scaffold files into `projects/<project-name>/context/software-engineering/` until the user confirms the blueprint with explicit approval.
