# DOMINO Engineering Constitution

This file defines the non-negotiable engineering, product, testing, reliability, and architecture rules for DOMINO.

Every coding agent and human contributor must read this file before making meaningful changes.

If an instruction conflicts with this file, stop and report the conflict instead of silently changing architecture.

## 1. Product Identity

DOMINO is an interactive economic simulation system.

It is not primarily:
- a chatbot
- a stock screener
- a portfolio tracker
- a stock prediction product
- a financial-news summarizer
- a generic RAG wrapper
- a graph visualization demo
- a collection of AI agents

The central product is an executable representation of economic relationships.

The eventual product loop is:

```text
EXPLORE
→ CHANGE
→ EXECUTE
→ PROPAGATE
→ EXPLAIN
→ VERIFY
→ MONITOR
```

A user should eventually be able to:
1. Open a company or economic entity.
2. Explore important economic dependencies.
3. Inspect evidence behind those dependencies.
4. Modify an economic variable or assumption.
5. Execute a deterministic scenario.
6. Observe consequences propagate through the model.
7. Inspect calculations, assumptions, uncertainty, and provenance.
8. Reconstruct what was knowable at an earlier date.
9. Save a thesis or scenario.
10. Compare that thesis against later evidence.

## 2. Core Technical Asset

DOMINO's core technical asset is the **Economic Compiler**.

It consumes structured:
- variables
- equations
- relationships
- assumptions
- baseline values
- scenario overrides

It produces:
- deterministic calculated results
- deltas
- propagation paths
- affected variables
- uncertainty information
- calculation traces
- provenance references
- stable result hashes

The Economic Compiler is not an LLM.

## 3. AI Principle

AI helps build and maintain parts of the economic model.

AI does not become the economic model.

LLMs may:
- interpret documents
- extract structured candidate claims
- propose entity resolution
- detect contradictions
- propose relationships
- propose model changes
- explain evidence
- classify new evidence against saved theses

LLMs may not:
- perform authoritative numeric financial calculations
- silently invent missing values
- directly mutate published models
- generate arbitrary executable Python for production execution
- bypass deterministic validation

## 4. Whole-System Thinking Comes Before Coding

Before modifying implementation code, determine:

1. What domain concept owns this behavior?
2. Which layer should contain it?
3. Which layers may depend on it?
4. Which layers must not depend on it?
5. Which invariants does it introduce or modify?
6. What is the public contract?
7. What failure states exist?
8. How will the behavior be tested?
9. Which known future phases will extend this area?
10. Does an existing abstraction already represent the concept?
11. Will this change create undesirable coupling?
12. Does this conflict with an ADR?

Never begin with:

> Where can I quickly put this code?

Begin with:

> What concept is this, who owns it, and what contract should represent it?

## 5. Abstraction First, But No Abstraction Theatre

DOMINO must not become a collection of one-off scripts.

It must also not become a speculative generic framework.

Create an abstraction when it:
- represents a real domain concept
- protects a stable system boundary
- centralizes an important invariant
- substantially improves testability
- separates infrastructure from domain behavior
- has multiple real implementations or a known near-term second implementation

Good examples:
- `EconomicModel`
- `ModelVersion`
- `EconomicVariable`
- `Scenario`
- `ScenarioRun`
- `Evidence`
- `Claim`
- `Exposure`
- `ModelRepository`
- `DocumentSource`
- `ExtractionProvider`

Bad examples without a concrete reason:
- `GenericManager`
- `UniversalProcessor`
- `BaseEverythingService`
- `CommonUtils`
- `FactoryFactory`

Every abstraction must answer:

> What stable concept or boundary does this represent?

If there is no good answer, do not create it.

## 6. Design For Known Evolution

Inspect relevant later phases before designing a boundary.

Do not implement future features early.

Instead:
- preserve extension points where requirements are known
- avoid schemas that make known future requirements impossible
- keep domain contracts stable
- document deliberate limitations

Plan for change.

Do not prebuild imaginary change.

## 7. Dependency Direction

Preferred conceptual dependency direction:

```text
Mobile / Web
    ↓
HTTP API
    ↓
Application layer
    ↓
Domain
    ↓
Economic Engine

Infrastructure adapters
    ↓
Domain interfaces
```

The domain and economic engine should not depend directly on:
- FastAPI
- SQLAlchemy
- PostgreSQL-specific APIs
- React
- React Native
- AWS SDKs
- LLM provider SDKs

when those can remain at system boundaries.

Frameworks are implementation details.

Economic rules are not.

## 8. Maintainability Is A Product Requirement

Code that works now but makes the system difficult to modify is incomplete.

Optimize for:
1. correctness
2. readability
3. maintainability
4. extensibility
5. testability
6. observability
7. explicit failure behavior
8. architectural consistency

Names must communicate domain meaning.

Avoid vague names like:
- `data`
- `obj`
- `thing`
- `manager`
- `processor`
- `helper`
- `util`
- `tmp`
- `res`

when a domain-specific name exists.

Functions should have one coherent responsibility.

Modules should have one coherent reason to change.

Do not artificially split every function into five-line fragments.

Optimize for comprehension, not line-count aesthetics.

## 9. Keep Side Effects At Boundaries

Core economic calculations should be pure where practical.

Do not make one function simultaneously:
- query PostgreSQL
- call an LLM
- perform economic calculation
- persist results
- send a notification

Prefer:

```text
load
↓
validate
↓
calculate
↓
persist
↓
publish
```

Pure calculations are easier to:
- test
- reproduce
- audit
- benchmark
- reason about

## 10. No Silent Fallbacks

DOMINO does not use silent fallbacks.

If an intended operation cannot be completed correctly, fail explicitly.

Forbidden examples:

```python
try:
    return primary_source()
except Exception:
    return []
```

```python
value = actual_value or 0
```

when zero carries economic meaning.

```python
try:
    return provider_a()
except Exception:
    return provider_b()
```

Automatic alternate-provider behavior is forbidden unless it becomes an explicitly approved product requirement with:
- architecture documentation
- typed semantics
- tests
- telemetry
- user-visible behavior where appropriate

Do not silently:
- use stale data
- use synthetic data
- substitute another provider
- return empty success
- fabricate defaults
- skip validation
- continue after corrupted state

Retries of the same idempotent operation are allowed when explicitly designed.

A retry is not a fallback.

If the operation still fails:
- return a typed failure
- log useful context
- preserve root cause
- do not claim success

## 11. No Exception Swallowing

Never write:

```python
except Exception:
    pass
```

Broad exceptions are acceptable only at a true boundary that must translate unexpected failures.

When translating:
- preserve cause
- add useful context
- use typed domain/application errors for expected failures
- preserve stack information for unexpected failures

## 12. No Placeholder Production Behavior

Never make production behavior look complete with:
- fake financial values
- dummy source data
- fake successful API responses
- TODO branches returning success
- placeholder calculations
- placeholder evidence presented as real
- mocked production integrations

Fixtures and synthetic data belong in tests and explicitly marked development environments.

If production functionality is unavailable, fail clearly.

## 13. Deterministic Economic Calculation

All authoritative scenario calculations execute in deterministic application code.

Never execute arbitrary generated Python.

Economic equations use a constrained typed intermediate representation.

Example:

```json
{
  "target": "revenue",
  "expression": {
    "op": "multiply",
    "args": [
      {"ref": "unit_volume"},
      {"ref": "average_selling_price"}
    ]
  }
}
```

Supported operators remain deliberately small and are added only when required.

## 14. Evidence First

DOMINO distinguishes:
- disclosed fact
- derived fact
- human assumption
- AI-proposed interpretation
- user scenario assumption

Do not silently collapse these categories.

Material relationships should eventually support exact provenance.

## 15. Immutable Published Models

Published `ModelVersion` records are immutable.

A model change creates a new version.

Never silently rewrite history.

## 16. Point-In-Time Correctness

Historical reconstruction must contain only information knowable at the requested date.

Future information must never leak backward.

Important claims should eventually distinguish:

- valid time: when the claim was true
- knowledge time: when the claim became knowable

## 17. Unknown Is Not Zero

Unknown or missing economic values remain unknown.

Never silently replace unknown with zero.

## 18. Avoid Fake Precision

If the evidence supports a range, preserve a range or sensitivity analysis.

Do not convert uncertain inputs into falsely precise decimals.

## 19. PostgreSQL First

PostgreSQL is the primary datastore.

Do not introduce another database without:
- a concrete requirement
- benchmark evidence
- an ADR
- explicit approval

This includes:
- Neo4j
- Redis
- a separate vector database

PostgreSQL capabilities should be evaluated first.

## 20. Modular Monolith First

Begin as a modular monolith.

Do not introduce microservices until a real requirement exists around:
- independent scaling
- fault isolation
- separate deployment lifecycle
- security isolation
- team ownership

## 21. No Infrastructure Theatre

Do not add infrastructure merely because it sounds senior.

Technologies requiring explicit justification include:
- Kafka
- Spark
- Kubernetes before its designated deployment phase
- service meshes
- distributed workflow engines
- multiple databases
- complex agent frameworks

Complexity must be earned.

## 22. Technology Adoption Gate

Before adding a major dependency or platform, document:

1. Product problem.
2. Current limitation.
3. Alternatives considered.
4. Why the existing stack is insufficient.
5. Operational cost introduced.
6. Testing impact.
7. Rollback/removal path.
8. Evidence that adoption is justified.

Record the decision in `docs/DECISIONS.md`.

## 23. Target Stack

### Mobile
- React Native
- Expo
- TypeScript
- Expo Router
- TanStack Query
- Zustand
- Reanimated
- Skia
- Zod

### Web deployment console
- Next.js
- React
- TypeScript
- TanStack Query
- Zod

Only add in its designated phase.

### Backend
- Python 3.12+
- FastAPI
- Pydantic v2
- SQLAlchemy 2
- Alembic
- psycopg
- PostgreSQL
- httpx
- Pint
- NetworkX

### Infrastructure
- Docker
- Docker Compose
- GitHub Actions
- AWS
- Terraform
- OpenTelemetry
- Kubernetes/Helm only in designated portable-deployment phase

## 24. Domain Model

Important concepts include:

### Entity
Economically meaningful object such as:
- Company
- Product
- Commodity
- Technology
- Facility
- Industry
- Geography

### SourceDocument
A specific source artifact.

### Evidence
An exact location inside a source.

### Claim
A structured assertion derived from evidence.

### Exposure
An economic dependency between variables.

### EconomicVariable
A measurable or modeled economic quantity.

### EconomicModel
Executable model of an entity or connected economic system.

### ModelVersion
Immutable snapshot of an EconomicModel.

### Equation
Defines how one variable is derived from others.

### Scenario
Defines hypothetical changes.

### ScenarioRun
Immutable execution of a Scenario against one ModelVersion.

### CalibrationRun
Historical evaluation comparing model output against subsequently observed outcomes.

## 25. Strong Contracts

Use explicit typed contracts at boundaries:
- API requests/responses
- repository interfaces
- economic expressions
- scenario definitions
- LLM structured outputs
- worker jobs
- integrations

Validate once at system boundaries where possible.

Inside validated domain code, rely on established invariants instead of repeated defensive clutter.

## 26. Domain Invariants

Important invariants should be represented in code and tests.

Examples:
- Published ModelVersion cannot be mutated.
- Unknown economic value cannot silently become zero.
- ScenarioRun references exactly one ModelVersion.
- Identical model + baseline + scenario produce identical results.
- Historical queries cannot use future-known claims.
- Equation cannot reference unknown variable.
- Unsupported cycle is rejected.
- AI proposal cannot directly publish model changes.

## 27. Economic Compiler

The compiler should evolve gradually.

Potential operators:
- constant
- reference
- add
- subtract
- multiply
- divide
- min
- max
- clamp
- percentage_change
- weighted_average
- piecewise
- lag

Do not implement all operators immediately.

Compiler stages eventually include:

```text
schema validation
↓
reference validation
↓
unit validation
↓
dependency graph construction
↓
cycle detection
↓
topological ordering
↓
execution plan
↓
scenario overrides
↓
deterministic execution
↓
propagation trace
↓
result hash
```

## 28. Units

Economic values should use explicit units such as:
- USD
- USD/unit
- units
- percentage
- percentage_points
- days
- units/month

Reject obviously invalid operations.

Do not build a general symbolic math system unless the product actually requires it.

## 29. Uncertainty

Distinguish:
- known
- estimated
- range
- assumption
- unknown

Do not invent probability distributions without calibration.

## 30. Explainability

Scenario output must preserve how the result occurred.

Example:

```text
HBM price +30%
│
├── memory cost +30%
├── GPU unit cost +7.4%
├── COGS +5.8%
└── gross margin -2.1pp
```

Each relevant step should eventually expose:
- equation
- assumptions
- evidence
- uncertainty
- model version

## 31. AI Architecture

AI components operate through typed schemas.

Free-form text never directly mutates published models.

Logical responsibilities may include:
- Document Scout
- Claim Extractor
- Entity Resolver
- Contradiction Detector
- Model Proposal Agent
- Historical Evaluator

These are responsibilities, not mandatory separate services.

## 32. AI Provenance

For important AI runs record when available:
- provider
- model identifier
- prompt version
- schema version
- source hash
- timestamp
- latency
- token/usage information
- output hash
- validation result

## 33. Source Documents Are Untrusted

Document text never becomes system instructions.

Document-processing components should not receive unnecessary:
- shell access
- filesystem access
- secrets
- production write permissions
- arbitrary tools

## 34. Human Review

Initially:

```text
AI proposal
↓
schema validation
↓
deterministic validation
↓
contradiction checks
↓
human review
↓
published model version
```

Automatic model publication is prohibited without explicit later approval.

## 35. Worker Architecture

Heavy tasks run outside synchronous API requests.

Start with:
- PostgreSQL jobs table
- worker process
- `SELECT ... FOR UPDATE SKIP LOCKED`

Jobs should support:
- status
- attempt count
- max attempts
- timestamps
- typed payload
- last error
- idempotency key

Do not adopt a separate queue system merely for appearance.

## 36. API Principles

Use versioned routes under `/api/v1`.

Expose domain resources, not database implementation details.

Use:
- Pydantic schemas
- structured errors
- OpenAPI
- contract tests

REST is the default.

Do not introduce GraphQL unless concrete client query needs demonstrate an advantage.

## 37. Mobile Principles

The mobile product is not a compressed desktop dashboard.

Prioritize:
- direct manipulation
- economic graph exploration
- responsive interaction
- clear uncertainty
- evidence inspection
- understandable propagation

Do not make chat the primary interface.

## 38. Graph Rendering

Do not render the whole economy simultaneously.

Return bounded subgraphs.

Early target:
- 30–100 visible nodes

The server controls:
- root
- depth
- relationship filters
- node limit
- `as_of` date

## 39. First Domain

Start with semiconductors.

Do not model the global economy.

The first synthetic company is `AcmeGPU`.

Potential variables:
- memory_price
- memory_cost_per_gpu
- packaging_cost_per_gpu
- wafer_cost_per_gpu
- unit_cost
- gpu_volume
- gpu_asp
- revenue
- cogs
- gross_profit
- gross_margin
- operating_expenses
- operating_income

## 40. Testing Is Continuous

Testing happens during implementation, not after implementation.

For each meaningful behavior:

```text
define behavior
↓
define invariants
↓
write/update focused test
↓
run and confirm expected failure where practical
↓
implement smallest correct behavior
↓
run focused test
↓
refactor
↓
run focused test again
```

Do not accumulate multiple untested features.

## 41. Red → Green → Refactor

Use this loop where practical:

### RED
Create or update a test demonstrating required behavior.

### GREEN
Implement the smallest correct solution.

### REFACTOR
Improve:
- names
- ownership
- duplication
- boundaries
- coupling

without changing behavior.

### GREEN
Run tests again.

## 42. Test Categories

For each feature consciously evaluate:
- happy path
- boundaries
- invalid input
- expected failures
- invariants
- regression case
- integration boundaries
- property-based opportunities

Not every category is mandatory for every feature, but the choice must be deliberate.

## 43. Test At The Right Layer

Economic logic:
- direct economic-engine tests

Persistence:
- repository/database integration tests

HTTP:
- API contract/integration tests

Worker:
- jobs-table + worker integration tests

AI:
- frozen eval datasets + structured-output tests

Mobile/web:
- critical interaction tests

Do not test domain behavior primarily through HTTP.

## 44. Deterministic Tests

Tests should not unnecessarily depend on:
- wall-clock time
- real internet
- unseeded randomness
- execution order
- shared mutable state

Inject or freeze time when relevant.

## 45. No Test Cheating

Never:
- delete legitimate failing tests to get green CI
- weaken assertions without justification
- skip failing tests to hide defects
- mock the exact behavior under test
- change expected results to match an unexplained regression

## 46. Every Bug Gets A Regression Test

Bug protocol:
1. reproduce
2. add failing regression test
3. confirm failure
4. fix root cause
5. confirm pass
6. run surrounding tests
7. inspect whether bug reveals architectural weakness

## 47. Test After Every Small Increment

After a small isolated change:
- run focused tests

After a coherent component:
- relevant unit tests
- relevant integration tests
- type checking
- linting

Before declaring a phase complete:
- full applicable suite
- build checks

Never claim a command passed unless it was actually run.

## 48. Refactor Continuously

Before declaring a feature complete inspect touched code for:
- duplication
- unclear names
- wrong ownership
- excessive coupling
- large mixed-responsibility functions
- leaky abstractions
- unnecessary dependencies
- hidden side effects

Make safe local refactors while tests are green.

## 49. Scalability Means Architectural Scalability First

First ask:

> Can the codebase grow without becoming impossible to change?

Design for growth in:
- companies
- variables
- model versions
- scenarios
- source types
- LLM providers
- extraction schemas
- integrations

Do not confuse scalability with premature distributed systems.

## 50. Performance Must Be Measured

Do not make code harder to understand based on imagined performance.

Measure:
- baseline
- bottleneck
- change
- result

Preserve correctness tests.

## 51. API-First Thinking

Before changing an API:
1. identify consumers
2. define domain resource
3. define contract
4. define normal behavior
5. define error behavior
6. consider evolution
7. write contract tests
8. implement

Do not expose database schema directly.

## 52. Database Changes Are Deliberate

Before schema changes consider:
- domain ownership
- constraints
- nullability
- uniqueness
- query patterns
- indexes
- migration path
- existing data
- historical requirements

Do not use JSONB as an escape hatch for stable relational concepts.

## 53. Security Basics

Never expose secrets in:
- source code
- logs
- mobile bundles
- test fixtures
- screenshots
- docs

Provider keys stay server-side.

Use least privilege.

## 54. Observability

Important operations should eventually emit structured telemetry.

Examples:
- scenario run
- compiler failure
- model publication
- ingestion job
- extraction run
- calibration run
- integration call

Use stable IDs for traceability.

## 55. FDE Deployment Mindset

DOMINO should be deployable into more than one environment without rewriting core domain logic.

Separate:
- domain
- application
- infrastructure
- environment configuration
- customer/deployment adapters

Repeated deployment work should be codified into:
- configuration
- adapters
- runbooks
- reusable modules
- automated checks

The Nth deployment should be easier than the first.

## 56. Customer/Deployment Configuration Is Not Hardcoded

Do not hardcode customer, company, sector, environment, or provider-specific behavior inside domain code.

Use:
- configuration
- typed adapter interfaces
- policy objects
- deployment manifests

where appropriate.

## 57. FDE Technology Rule

Technology is selected because the product/deployment requires it.

The project should demonstrate important FDE competencies, but never by contaminating the architecture with unused tools.

Examples:

### AWS + Terraform
Required because production infrastructure must be reproducible.

### Docker
Required for reproducible local/production runtime.

### Next.js
Required because human review, eval, and deployment operations benefit from a web console.

### OpenTelemetry
Required because FDEs must debug systems across boundaries.

### Kubernetes + Helm
Added later to prove a portable customer deployment profile after the core product is stable.

### MCP
Added later because DOMINO exposes useful economic tools to external AI systems.

These have product reasons.

## 58. Forbidden Scope Without Explicit Approval

Do not build early:
- Neo4j
- Kafka
- Spark
- Databricks
- Snowflake
- Redis
- Temporal
- Airflow
- separate vector database
- GraphQL
- brokerage integration
- real-money trading
- stock-price prediction
- personalized investment recommendations
- social feed
- chatbot-first UI
- 3D globe
- thousands of companies
- automatic AI model publication
- generated executable Python
- autonomous financial transactions

## 59. Product Kill Gates

The key early kill gate is after the Shock Lab.

By then a user must be able to:

```text
open AcmeGPU
↓
explore model
↓
change variable
↓
execute scenario
↓
watch propagation
↓
understand why
```

If this is not compelling, improve the core product before building expensive AI/data infrastructure.

## 60. Repository Source Of Truth

Read before significant work:
- `AGENTS.md`
- `docs/PRODUCT.md`
- `docs/ARCHITECTURE.md`
- `docs/ECONOMIC_MODEL_SPEC.md`
- `docs/PHASES.md`
- `docs/DECISIONS.md`
- `docs/STATUS.md`
- `docs/EVALS.md`

Repository documentation wins over conversational memory.

## 61. Phase Discipline

Only one official phase may be active at once.

At the beginning:
1. read repository source of truth
2. inspect existing code
3. identify current state
4. define scope
5. define acceptance criteria
6. define tests
7. identify risks

At the end:
1. run focused and phase-wide tests
2. run lint
3. run types
4. run integration/build checks
5. update docs
6. report changed files
7. report known limitations
8. report intentionally deferred work
9. STOP

Never automatically begin the next phase.

## 62. Definition Of Done

Work is not complete because code exists.

Applicable completion requirements include:
- implementation complete
- relevant tests pass
- regression coverage exists
- lint passes
- type checking passes
- integration tests pass
- build checks pass
- failure paths are explicit
- documentation updated
- architecture decisions recorded
- known limitations documented
- no hidden TODO behavior
- no fake success claims

## 63. Senior Engineer Review

Before completion ask:

- Is this the correct abstraction?
- Is responsibility in the right layer?
- Are dependency directions correct?
- Is domain logic duplicated?
- Are failures explicit?
- Did any fallback sneak in?
- Are there magic defaults?
- Is the code understandable?
- Is the change testable without excessive mocking?
- Will known future phases extend this cleanly?
- Did we add unnecessary flexibility?
- Did we under-design a stable boundary?
- Can another engineer understand this in six months?
- Does this code serve the product, not the resume?

Fix clear problems before declaring completion.
