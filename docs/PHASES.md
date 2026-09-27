# DOMINO Phased Development Plan

Only one official phase is active at a time.

### Phase 0 — Repository Foundation
**Goal:** Establish maintainable engineering foundations.

Build:
- monorepo structure
- Python configuration
- Expo/TypeScript workspace
- strict type checking
- pytest
- Hypothesis
- ruff
- mypy
- GitHub Actions
- Docker Compose skeleton
- docs
- `AGENTS.md`

Do not implement business behavior.

Exit gate:
- Python imports work
- mobile type checks
- tests run
- lint/type checks pass
- CI exists
- docs exist
- `STATUS.md` is accurate

STOP.

---

### Phase 1 — Economic Compiler Kernel
**Goal:** Prove the core idea without database, API, mobile, AI, or real data.

Build:
- `EconomicVariable`
- typed values and units
- expression AST / IR
- equations
- `EconomicModel`
- immutable `ModelVersion`
- `Scenario`
- scenario changes
- `ScenarioRun`
- result and propagation trace
- reference validation
- dependency graph
- cycle detection
- topological ordering
- deterministic execution
- stable hashing

Initial operators:
- constant
- reference
- add
- subtract
- multiply
- divide

Synthetic model:
- `AcmeGPU`

Tests:
- arithmetic
- nested expressions
- bad references
- missing values
- cycles
- division by zero
- units
- scenario immutability
- determinism
- result hashes
- propagation
- property tests

Exit gate:
- full AcmeGPU scenario runs in Python
- deterministic
- no AI/database/API
- tests green
- spec docs updated

STOP.

---

### Phase 2 — Persistence Layer
**Goal:** Persist models without contaminating domain logic.

Add:
- PostgreSQL
- SQLAlchemy 2
- Alembic
- psycopg
- repository interfaces

Persist:
- entities
- economic models
- model versions
- variables
- equations
- scenarios
- runs
- results

Requirements:
- published versions immutable
- domain does not import SQLAlchemy
- clean migrations

Exit gate:
- clean DB bootstrap
- AcmeGPU persists and reloads
- execution identical after roundtrip
- immutability tested
- compiler tests remain database-independent

STOP.

---

### Phase 3 — HTTP API
**Goal:** Expose the engine through production-quality contracts.

Add FastAPI.

Initial endpoints:
- `GET /api/v1/entities`
- `GET /api/v1/entities/{id}`
- `GET /api/v1/entities/{id}/graph`
- `GET /api/v1/model-versions/{id}`
- `POST /api/v1/scenarios`
- `GET /api/v1/scenarios/{id}`
- `POST /api/v1/scenarios/{id}/run`
- `GET /api/v1/scenario-runs/{id}`

Requirements:
- Pydantic contracts
- structured errors
- OpenAPI
- API contract tests
- no raw ORM leakage

Exit gate:
- fresh DB seeded
- AcmeGPU loaded via HTTP
- scenario created and executed
- propagation returned
- OpenAPI valid
- integration tests green

STOP.

---

### Phase 4 — Mobile Foundation
**Goal:** First usable mobile client.

Add:
- Expo
- React Native
- TypeScript strict mode
- Expo Router
- TanStack Query
- Zustand
- Zod
- generated or strongly typed API client

Screens:
- Home
- Company List
- Company Detail
- Scenario Result

Flow:
```text
open app
→ AcmeGPU
→ run predefined scenario
→ see result
```

Exit gate:
- app launches
- backend connection works
- errors/loading states work
- scenario execution works
- mobile types/tests green

STOP.

---

### Phase 5 — Economic Graph
**Goal:** Build visual executable-company representation.

Add:
- Skia
- Reanimated

Support:
- bounded graph
- pan
- zoom
- node select
- edge select
- reset camera
- basic metadata panel

Target:
- 30–100 visible nodes

Exit gate:
- graph smooth on real device
- interactions reliable
- graph data contract tested

STOP.

---

### Phase 6 — Shock Lab
**Goal:** Create DOMINO's first magical interaction.

Flow:
```text
select variable
→ inspect baseline
→ set/increase/decrease
→ execute
→ animate propagation
→ compare baseline vs scenario
→ inspect why
```

Support initially:
- set
- percentage increase
- percentage decrease

Requirements:
- deterministic backend execution
- visual propagation order
- explicit deltas
- errors visible
- no AI calculation

**Major Product Kill Gate**

If the interaction is not compelling, do not hide it behind AI features.

Exit gate:
- new user can understand what changed, why, and by how much
- interaction feels meaningfully different from a finance chatbot

STOP.

---

### Phase 7 — Evidence Architecture
**Goal:** Tie relationships to provenance using manual fixtures first.

Add:
- `SourceDocument`
- `Evidence`
- `Claim`
- `Exposure`

Store precise evidence location where possible.

Mobile:
- evidence drawer
- assumption/type labels
- source metadata

Exit gate:
- major AcmeGPU relationships have inspectable provenance
- facts/assumptions are visibly distinct

STOP.

---

### Phase 8 — Real Document Ingestion
**Goal:** Create robust data ingestion before AI extraction.

Build worker process.

Jobs table:
- typed payload
- state
- attempts
- max attempts
- idempotency key
- timestamps
- last error

Start with:
- SEC EDGAR
- official IR documents

Pipeline:
```text
discover
→ download
→ hash
→ deduplicate
→ normalize
→ store
→ retrieve
```

Use S3-compatible object storage abstraction where appropriate.

Tests:
- idempotency
- retry
- duplicate ingestion
- source hashes
- parser fixtures
- locking
- failure states

Exit gate:
- selected semiconductor filings reproducibly enter DOMINO
- no LLM extraction yet

STOP.

---

### Phase 9 — Structured AI Extraction + Evals
**Goal:** Convert documents into candidate claims safely.

Build:
- provider abstraction
- structured-output schemas
- prompt versioning
- extraction records
- evidence spans
- entity resolution
- validation
- frozen human-reviewed eval dataset

Measure:
- precision
- coverage
- unsupported claim rate
- evidence-span correctness
- entity-resolution accuracy
- latency
- cost

No automatic model publication.

Exit gate:
- typed claims
- exact evidence
- invalid output rejected
- reproducible debugging metadata
- eval report exists

STOP.

---

### Phase 10 — First Real Company
**Goal:** One real evidence-backed executable model.

Choose a semiconductor company based on source quality.

Use:
- official sources
- reviewed claims
- human-curated assumptions
- deterministic equations

Clearly label:
- disclosed
- derived
- human assumption
- AI proposal

Exit gate:
- real company supports Explore → Change → Execute → Explain → Verify
- no unsupported precision
- important assumptions inspectable

STOP.

---

### Phase 11 — Semiconductor Economic Network
**Goal:** Expand to a bounded connected system.

Target:
- ~20–30 important entities

Possible areas:
- foundry
- packaging
- HBM
- memory
- GPU
- equipment
- server OEM
- hyperscaler

Requirements:
- cross-entity propagation
- bounded graph retrieval
- evidence on major edges
- explainable results

Exit gate:
- cross-company shock works end-to-end
- performance remains acceptable

STOP.

---

### Phase 12 — Time Machine
**Goal:** Point-in-time correct historical reconstruction.

Add:
- valid_from
- valid_to
- known_from
- known_to
- `as_of` queries

Aggressive leakage tests are mandatory.

Exit gate:
- future-known information cannot appear in historical views
- historical mode visible in UI

STOP.

---

### Phase 13 — Historical Calibration
**Goal:** Measure how useful the economic models are against history.

Add:
- `CalibrationRun`
- expected effect
- observed effect
- directional result
- magnitude error where measurable
- range coverage
- assumption sensitivity
- model coverage

Never call results "predictive accuracy" unless methodology supports it.

Exit gate:
- historical models replay
- error metrics persist
- calibration can inform new versions without rewriting old versions

STOP.

---

### Phase 14 — Thesis Monitoring
**Goal:** Create recurring value.

Users save:
- scenario
- assumption
- thesis
- watch target

New evidence classified as:
- supporting
- contradicting
- relevant but inconclusive
- unrelated

Do not present interpretation as objective investment truth.

Exit gate:
- user can save thesis, leave, return, and understand evidence changes

STOP.

---

### Phase 15 — Deployment & Review Console
**Goal:** Build the operational web surface an FDE would use to deploy and maintain DOMINO.

Use:
- Next.js
- React
- TypeScript

The console exists to operate the system, not as marketing UI.

Capabilities:
- ingestion job inspection
- document inspection
- claim review
- evidence review
- model-proposal review
- publish new model version
- eval dashboard
- calibration inspection
- deployment/environment configuration
- audit trail view

Requirements:
- reuse API contracts
- no duplicate economic logic in frontend
- explicit RBAC-ready boundaries
- critical workflows tested

FDE signal:
- full-stack web delivery
- human-in-the-loop AI workflow
- deployment operations
- repeatable customer/sector onboarding

Exit gate:
- operator can review and publish a model version without direct DB manipulation
- important actions are auditable

STOP.

---

### Phase 16 — Production Cloud + Infrastructure as Code
**Goal:** Deploy a reproducible production-like environment.

Use:
- Docker
- AWS
- Terraform
- GitHub Actions

Preferred simple AWS shape:
- containerized API
- containerized worker
- ECS/Fargate or equivalent
- RDS PostgreSQL
- S3
- ALB/API ingress
- IAM
- Secrets Manager
- CloudWatch and OpenTelemetry-compatible telemetry

Requirements:
- environment separation
- reproducible Terraform
- secrets not committed
- least-privilege IAM
- database migrations in deployment plan
- rollback/runbook
- CI builds and tests before deploy

Do not add Kubernetes in this phase.

Exit gate:
- environment can be reproduced from IaC
- deployment is documented
- CI/CD works
- application runs in cloud
- secrets and IAM reviewed

STOP.

---

### Phase 17 — Observability, Security & Reliability
**Goal:** Make the system operable under real failures.

Add:
- structured logs
- traces
- metrics
- correlation IDs
- OpenTelemetry
- error reporting
- health/readiness endpoints
- audit logs
- authentication
- authorization
- OIDC-compatible design
- rate limits
- timeout policies
- retry policies for idempotent same-operation retry only
- backup/restore procedure
- load tests
- incident runbook

Trace:
- API request
- scenario execution
- compiler
- worker jobs
- LLM extraction
- model publication
- integrations

No hidden fallbacks.

Exit gate:
- important failures observable
- load-test baseline documented
- authz tested
- restore procedure validated
- production debugging is realistic

STOP.

---

### Phase 18 — Integration & Agent Surface
**Goal:** Make DOMINO usable inside other systems, like an FDE-delivered platform.

Add only useful integrations.

Build:
- secure service-to-service API patterns
- webhook framework for explicit events
- audit logs
- idempotency
- integration adapter interface
- MCP server exposing selected read/scenario tools

Possible MCP tools:
- search_entity
- get_model
- get_evidence
- run_scenario
- inspect_scenario_result
- get_saved_thesis_changes

MCP must not expose model publication or privileged writes initially.

Requirements:
- auth
- rate limits
- strict schemas
- tool-level audit records
- integration tests

Exit gate:
- an external authorized client can call useful DOMINO capabilities without bypassing domain rules

STOP.

---

### Phase 19 — FDE Deployment Kit
**Goal:** Codify the deployment so the next environment/customer is easier than the first.

Build:
- typed environment/deployment config
- source adapter interface
- onboarding checklist
- data mapping template
- deployment readiness checks
- smoke tests
- runbook
- support/debugging checklist
- reusable Terraform modules
- repeatable seed/config process
- field feedback log template

Perform a second deployment-style exercise:
- new issuer set, dataset, or sandbox environment
- without editing core domain behavior

Measure:
- steps required
- manual interventions
- deployment time
- reusable components
- environment-specific code

FDE signal:
- field patterns are productized into reusable building blocks

Exit gate:
- second deployment is measurably cleaner than the first
- no customer/environment logic has leaked into core domain code

STOP.

---

### Phase 20 — Portable Kubernetes Deployment Profile
**Goal:** Demonstrate realistic customer-environment portability after the system is already production-capable.

Use:
- Kubernetes
- Helm
- kind for local CI/testing
- EKS-compatible manifests where useful

Package:
- API
- worker
- migrations/job
- config
- secrets references
- probes
- resource requests/limits
- autoscaling only if measured
- network/service configuration

Do not replace the simpler AWS deployment automatically.

This is a second deployment profile for environments where Kubernetes is required.

Requirements:
- Helm values separated from secrets
- readiness/liveness probes
- graceful shutdown
- documented upgrade path
- deployment smoke tests

Exit gate:
- same application can deploy to a clean local cluster using documented commands
- core application code did not change to support Kubernetes

STOP.

---

### Phase 21 — TestFlight
**Goal:** Real iPhone beta.

Configure:
- EAS development
- EAS preview
- EAS production

Test:
- install
- auth
- API reliability
- graph performance
- scenario UX
- evidence UX
- historical mode
- crash recovery

Observe users performing core loop without coaching.

Exit gate:
- stable TestFlight build
- major crashes fixed
- core interaction understandable
- critical performance issues resolved

STOP.

---

### Phase 22 — App Store Release
**Goal:** Public release.

Complete:
- App Store metadata
- screenshots
- privacy policy
- support page
- terms where appropriate
- onboarding
- accessibility review
- privacy disclosures
- release notes
- monitoring
- rollback/incident process

Measure:
- first-scenario completion
- scenarios per active user
- evidence inspection rate
- second-scenario rate
- thesis-save rate
- returning research users

STOP.

---

## Technology Trigger Appendix

These technologies are not banned forever.

They are gated.

### Add pgvector / semantic retrieval only when:
- exact/lexical retrieval baseline exists
- eval set exists
- semantic retrieval improves measured recall/precision
- Postgres-hosted pgvector is sufficient before considering another DB

### Add Redis only when:
- a measured caching, coordination, or rate-limit problem exists
- DB/in-process alternatives are inadequate

### Add Kafka only when:
- there are multiple independent consumers
- throughput/durability requirements exceed the job-table architecture
- replay/event semantics are real product requirements

### Add Spark/Databricks only when:
- data volume or compute demonstrates local/Postgres batch processing is inadequate
- distributed computation is measured, not imagined

### Add Neo4j only when:
- graph-query profiling demonstrates Postgres is inadequate
- query patterns justify the operational cost

### Add workflow orchestration platform only when:
- job DAG complexity
- long-running state
- retries
- backfills
- visibility
cannot be handled safely by the current worker design

