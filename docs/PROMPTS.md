# DOMINO Prompt Library

Session prompts for coding agents. Source: DOMINO Complete Build Prompt Pack v1.0, sections 7–10.

These are the prompts you actually paste into Codex or Claude.

---

## PROMPT A — New Session Bootstrap

Use this at the beginning of a coding session.

```text
You are working on the DOMINO repository.

Before making any changes:

1. Read AGENTS.md.
2. Read docs/PRODUCT.md.
3. Read docs/ARCHITECTURE.md.
4. Read docs/ECONOMIC_MODEL_SPEC.md.
5. Read docs/PHASES.md.
6. Read docs/DECISIONS.md.
7. Read docs/STATUS.md.
8. Inspect the repository structure and the code relevant to the current phase.
9. Inspect recent tests relevant to the current phase.

Then report:

A. Current phase and its state.
B. What functionality actually exists right now.
C. Which exit criteria are already satisfied.
D. Which exit criteria remain.
E. Any inconsistency between code and documentation.
F. Any failing tests, lint, type checks, or builds that are already known.
G. The smallest sensible next implementation increment.

Do not modify code yet.

Do not propose a new architecture unless the current architecture has a concrete problem.

Do not advance phases.
```

---

## PROMPT B — Start / Continue A Phase

```text
CONTINUE TO PHASE <N>.

Follow AGENTS.md exactly.

Before editing code:

1. Verify the previous phase exit gate.
2. If it is not satisfied, finish the missing requirements before proceeding.
3. Restate the exact scope of Phase <N>.
4. Identify the domain concepts affected.
5. Identify the correct owning layers.
6. Identify relevant existing abstractions.
7. Inspect later phases only to avoid creating blocking architecture; do not implement future work.
8. Define acceptance criteria.
9. Define failure behavior.
10. Define the focused test plan.

Then break the phase into small coherent increments.

For each increment:

RED where practical:
- create/update the focused test
- run it and confirm the expected failure

GREEN:
- implement the smallest correct behavior
- run the focused test

REFACTOR:
- inspect naming, ownership, duplication, coupling, and side effects
- refactor while behavior is green
- rerun the test

After each coherent component:
- run relevant unit tests
- run relevant integration tests
- run type checking
- run linting

Never use silent fallbacks.
Never replace unknown values with defaults.
Never add placeholder production behavior.
Never weaken tests to get green.
Never introduce infrastructure or dependencies outside the phase without a documented necessity.

At the end of the phase:

1. Run the full applicable suite.
2. Run lint.
3. Run type checks.
4. Run build/integration checks.
5. Perform a senior-engineer review of all touched code.
6. Fix clear maintainability or architecture problems.
7. Update docs/STATUS.md.
8. Update docs/DECISIONS.md when decisions changed.
9. Update architecture/spec/API/eval docs where applicable.
10. Report actual commands and results.
11. Report files changed.
12. Report known limitations.
13. Report deferred work.
14. STOP.

Do not begin the next phase.
```

---

## PROMPT C — Implement One Small Feature

```text
Implement this DOMINO feature:

<FEATURE>

Do not start coding immediately.

First:

1. Read AGENTS.md and relevant project docs.
2. Inspect existing code and tests.
3. Explain what domain concept owns this behavior.
4. Explain which layer should implement it.
5. Identify the current contract and whether it must change.
6. Identify relevant invariants.
7. Identify failure modes.
8. Identify whether a new abstraction is truly required.
9. Check relevant future phases so the design does not create a known dead end.
10. Define the smallest useful tests.

Then implement in small increments.

For every meaningful behavior:
- add/update a focused test first where practical
- run it
- implement the smallest correct behavior
- run it again
- refactor
- rerun

No silent fallback.
No placeholder success.
No broad swallowed exceptions.
No duplicate business logic across layers.
No infrastructure changes unless required by the feature.
No speculative generic framework.

At completion:
- run focused tests
- run surrounding tests
- run type check
- run lint
- run integration tests if a boundary changed
- update relevant documentation
- report actual commands/results
- STOP
```

---

## PROMPT D — Bug Fix

```text
Fix this DOMINO bug:

<BUG DESCRIPTION>

Follow the bug-fix protocol.

1. Read AGENTS.md and relevant docs.
2. Reproduce the bug.
3. Identify the root cause, not just the visible symptom.
4. Identify the domain invariant or boundary that failed.
5. Add a regression test that demonstrates the bug.
6. Run it and confirm it fails for the expected reason.
7. Implement the smallest root-cause fix.
8. Run the regression test.
9. Run surrounding unit/integration tests.
10. Review whether this bug indicates:
   - wrong abstraction
   - duplicated logic
   - missing validation
   - hidden fallback
   - incorrect ownership
   - broken boundary
11. Refactor locally if required while tests remain green.
12. Run lint and type checks.
13. Update docs if semantics changed.

Do not:
- catch and hide the error
- default to another value
- add a fallback path
- weaken the regression test
- patch only the UI if the root problem is in the domain/backend

Finish with:
- root cause
- regression test
- fix
- commands actually run
- remaining risks

STOP.
```

---

## PROMPT E — Senior Code Review

Use this after another agent implements something.

```text
Review the current uncommitted/recent DOMINO changes as a strict senior staff engineer.

Do not modify code initially.

Read AGENTS.md and relevant architecture docs.

Review for:

ARCHITECTURE
- correct layer ownership
- dependency direction
- domain/framework separation
- inappropriate coupling
- duplicate business logic
- unnecessary abstractions
- missing abstractions
- known future-phase dead ends

CORRECTNESS
- domain invariants
- units
- unknown handling
- deterministic behavior
- mutation
- temporal correctness
- error semantics

FAILURE BEHAVIOR
- silent fallbacks
- swallowed exceptions
- fake defaults
- fake success
- stale/synthetic substitutions
- broad catches
- hidden retries

MAINTAINABILITY
- naming
- function/module responsibility
- readability
- excessive indirection
- magic values
- unnecessary generality
- dead code

TESTING
- tests for new behavior
- regression coverage
- boundaries
- invalid input
- failure paths
- property tests where appropriate
- excessive mocking
- tests coupled to implementation details

SECURITY
- secrets
- validation
- authorization boundaries
- unsafe document/LLM handling
- injection surfaces

FDE / OPERABILITY
- logging
- correlation
- deployment configuration
- environment-specific coupling
- debuggability

Return findings ordered by severity:

BLOCKER
HIGH
MEDIUM
LOW

For each finding include:
- exact file/location
- why it matters
- concrete fix

Then state whether you recommend:
APPROVE
APPROVE WITH FIXES
REQUEST CHANGES

Do not give a positive verdict merely because tests pass.
```

---

## PROMPT F — Apply Code Review Fixes

```text
Apply the accepted findings from the latest DOMINO code review.

For each finding:

1. Confirm the issue exists.
2. Add or update a test if the issue affects behavior.
3. Implement the smallest architectural/root-cause fix.
4. Run focused tests.
5. Refactor if needed.
6. Rerun tests.

Do not make unrelated changes.

Do not introduce fallbacks.

At the end run:
- relevant full tests
- type checks
- lint
- integration/build checks

Then provide a finding-by-finding resolution table.

STOP.
```

---

## PROMPT G — Architecture Review Before A Major Feature

```text
Perform an architecture review for this proposed DOMINO feature:

<FEATURE>

Do not write implementation code.

Read:
- AGENTS.md
- PRODUCT.md
- ARCHITECTURE.md
- ECONOMIC_MODEL_SPEC.md
- PHASES.md
- DECISIONS.md
- STATUS.md

Analyze:

1. Domain concept.
2. Ownership.
3. Required contract.
4. Data model impact.
5. API impact.
6. mobile/web impact.
7. worker impact.
8. AI impact.
9. infrastructure impact.
10. security impact.
11. observability impact.
12. failure behavior.
13. test strategy.
14. future extensibility.
15. migration/backward compatibility.
16. whether a new abstraction is justified.
17. whether a new dependency is justified.

Provide:
- recommended design
- dependency diagram in text
- alternatives considered
- risks
- explicit non-goals
- acceptance criteria
- proposed ADR if needed

Reject unnecessary infrastructure or generic frameworks.

STOP after the design review.
```

---

## PROMPT H — Test Audit

```text
Audit DOMINO's tests for the current phase.

Do not modify production code first.

Read AGENTS.md.

Map each phase requirement to test coverage.

Check for:
- happy paths
- boundaries
- invalid input
- failures
- invariants
- regression cases
- integration boundaries
- deterministic tests
- property tests
- historical leakage if applicable
- AI eval coverage if applicable
- worker idempotency if applicable
- API contract coverage if applicable

Identify:
1. behavior with no test
2. brittle implementation-detail tests
3. meaningless tests
4. over-mocked tests
5. nondeterministic tests
6. tests hiding failures
7. missing regression cases

Then add/fix tests in small increments.

Do not change production behavior merely to satisfy a badly designed test.

After changes run the full applicable test suite and report actual results.

STOP.
```

---

## PROMPT I — Refactor Without Feature Change

```text
Refactor this DOMINO area:

<SCOPE>

This is a behavior-preserving refactor.

Before changes:
1. Read AGENTS.md.
2. Run the current relevant tests and record baseline.
3. Identify concrete maintainability problems.
4. State the desired structural improvement.
5. Confirm public behavior/contracts should not change.

Refactor in small steps.

After every step:
- run focused tests

Do not:
- add unrelated features
- change API semantics
- change economic results
- weaken tests
- add speculative abstractions

At the end:
- run the same baseline suite
- run type checks
- run lint
- report structural improvement
- report whether any public behavior changed; expected answer should be "no"

STOP.
```

---

## PROMPT J — FDE Stack Alignment Audit

Use occasionally, not every session.

```text
Audit the DOMINO repository for Forward Deployed Engineer competency coverage.

Do NOT recommend adding tools merely because job listings mention them.

Evaluate whether the project currently demonstrates meaningful experience in:

- Python
- TypeScript
- React
- SQL/PostgreSQL
- APIs
- full-stack delivery
- data ingestion/pipelines
- AI/LLM systems
- structured outputs
- evals
- agent/tool integration
- Docker
- CI/CD
- cloud deployment
- AWS
- Terraform
- observability
- security/auth
- production debugging
- customer/environment configuration
- reusable deployment patterns
- Kubernetes portability
- MCP/integration surfaces

For every area classify:

STRONG
PARTIAL
PLANNED
UNJUSTIFIED

For PARTIAL:
identify the real product/deployment gap.

For PLANNED:
identify which phase already covers it.

For UNJUSTIFIED:
explain why we should not add it.

Only recommend a new technology if:
1. DOMINO has a real requirement,
2. existing stack is insufficient,
3. it improves product/deployment quality,
4. we can test and operate it,
5. the decision can be defended in an interview without saying "for my resume."

Finish with the 3 highest-value engineering gaps, not a shopping list of technologies.
```

---

## PROMPT K — AWS/Terraform Deployment Review

```text
Review DOMINO's cloud deployment as an FDE responsible for putting it into production.

Check:

- reproducible Terraform
- environment separation
- Docker image reproducibility
- immutable artifacts
- IAM least privilege
- secrets handling
- networking
- ingress
- database access
- migration strategy
- S3/object storage
- worker deployment
- health checks
- logs/metrics/traces
- backup/restore
- rollback
- cost-awareness
- CI/CD
- smoke tests
- failure visibility

Do not add managed services without a requirement.

Do not hide failure through fallback behavior.

Return:
- blockers
- reliability risks
- security risks
- operability gaps
- unnecessary complexity
- concrete remediation order
```

---

## PROMPT L — AI / Agent Safety & Evals Review

```text
Review DOMINO's AI extraction/agent components.

Focus on whether AI is constrained to the correct role.

Check:

- structured output schema
- source provenance
- prompt/version tracking
- evidence spans
- unsupported-claim rejection
- prompt injection handling
- tool permissions
- production write permissions
- model-publication boundary
- deterministic validators
- eval dataset quality
- precision
- coverage
- hallucination / unsupported claim rate
- entity-resolution accuracy
- latency
- cost
- regression evals
- failure states

AI must not:
- calculate authoritative scenario results
- execute generated Python
- silently invent missing values
- directly publish production models
- obtain unnecessary shell/filesystem access

Return findings and an eval plan.

STOP.
```

---

## PROMPT M — Multi-Agent Coordination: Architect + Implementer

Use when Codex and Claude are both working.

```text
You are one of multiple engineering agents working on DOMINO.

Your assigned role is:

<ARCHITECT | IMPLEMENTER | REVIEWER | TEST ENGINEER>

Read AGENTS.md and docs/STATUS.md first.

Rules:

1. Do not modify files outside your assigned ownership unless explicitly necessary.
2. Do not redesign another agent's active area silently.
3. Before coding, state:
   - files you expect to touch
   - contracts you depend on
   - contracts you may change
4. If a shared contract must change, stop and surface the required contract change before proceeding.
5. Keep changes small and independently testable.
6. Update tests with behavior changes.
7. Never weaken another agent's tests.
8. Do not create duplicate implementations because another branch/worktree is not visible.
9. Record handoff notes after completion.
10. Do not advance the project phase independently.

Your task:

<TASK>

At completion report:

- files changed
- public contracts changed
- tests added
- commands run
- assumptions made
- unresolved integration needs
- suggested handoff target

STOP.
```

---

## PROMPT N — Multi-Agent Handoff

```text
Create a precise engineering handoff for the next DOMINO agent.

Do not make new code changes.

Include:

## Current phase
## Task completed
## Exact behavior now working
## Files changed
## Public contracts changed
## Database/schema changes
## Tests added
## Commands run and results
## Known failures
## Known limitations
## Deferred work
## Architectural decisions
## Assumptions
## Integration points the next agent must preserve
## Next smallest task
## Files the next agent should read first

Update docs/STATUS.md so this handoff survives chat history.

STOP.
```

---

## PROMPT O — Deployment/Customer Adapter Design

```text
Design a new DOMINO deployment or source integration for:

<TARGET>

Act like a Forward Deployed Engineer embedded with the customer/environment.

Do not begin implementation first.

Discover and specify:

1. Desired workflow/outcome.
2. Existing systems.
3. Data sources.
4. Data ownership.
5. Data formats.
6. Update frequency.
7. Authentication.
8. Network constraints.
9. compliance/security constraints.
10. failure consequences.
11. user roles.
12. acceptance criteria.
13. observability needs.
14. deployment environment.
15. handoff/maintenance expectations.

Then map requirements to existing DOMINO abstractions.

Prefer:
- adapters
- configuration
- policies
- reusable modules

over:
- customer-specific `if` statements
- copied services
- forked product behavior

Identify what is:
- reusable core
- deployment-specific adapter
- deployment-specific configuration

Define tests and a rollout plan.

STOP before implementation unless explicitly told to proceed.
```

---

## PROMPT P — MCP / Integration Implementation

```text
Implement the approved DOMINO integration/MCP capability:

<CAPABILITY>

First inspect:
- domain service being exposed
- authorization requirements
- audit requirements
- schema
- existing HTTP contract

MCP/integration code must remain an adapter.

It must not duplicate economic logic.

For every exposed tool define:
- name
- input schema
- output schema
- permissions
- side effects
- errors
- rate limit expectations
- audit event
- test cases

No privileged model publication tools unless explicitly approved.

No shell/filesystem/network access beyond the adapter's defined requirement.

Write integration tests for every tool.

STOP after verified implementation.
```

---

## PROMPT Q — Production Incident / Debugging

```text
Investigate this DOMINO production-like failure:

<INCIDENT>

Do not make speculative fixes first.

1. Establish timeline.
2. Identify affected request/job/scenario IDs.
3. Inspect logs, traces, metrics, and relevant state.
4. Reproduce where possible.
5. Identify the failing boundary.
6. Distinguish symptom from root cause.
7. State impact.
8. State whether data integrity was affected.
9. Add a regression or integration test.
10. Fix root cause.
11. Verify in the smallest environment.
12. Run surrounding tests.
13. Identify observability gaps that slowed diagnosis.
14. Update runbook if needed.

No fallback behavior may be added as a shortcut.

Finish with:
- root cause
- impact
- repair
- prevention
- detection improvement
- tests
- commands/results

STOP.
```

---

## PROMPT R — Release Gate

```text
Perform a release gate review for DOMINO.

Do not add new features.

Verify:

PRODUCT
- core flow works
- no fake/synthetic production data
- errors are understandable
- uncertainty is explicit

BACKEND
- tests green
- migrations validated
- API contracts stable
- jobs healthy
- scenario determinism intact

AI
- evals meet documented thresholds
- no direct model publication
- evidence required
- injection controls intact

SECURITY
- secrets safe
- auth/authz correct
- least privilege
- rate limits
- audit logs

OPERATIONS
- logs
- metrics
- traces
- health endpoints
- backups
- rollback
- incident runbook

MOBILE/WEB
- build succeeds
- loading/error states
- critical flows
- accessibility checks
- no debug-only behavior

INFRA
- Terraform plan reviewed
- deployment reproducible
- smoke tests pass

Return:

BLOCKERS
NON-BLOCKING RISKS
VERIFIED CHECKS

Final verdict:
READY
NOT READY

Do not call it READY if any release blocker remains.
```

---

# 8. PHASE-SPECIFIC START COMMANDS

After the bootstrap prompt, use one of these.

## Phase 0
```text
CONTINUE TO PHASE 0.
Initialize only the repository foundation defined in docs/PHASES.md.
Do not implement DOMINO business logic.
```

## Phase 1
```text
CONTINUE TO PHASE 1.
Build only the Economic Compiler kernel and synthetic AcmeGPU model.
No database, HTTP API, mobile UI, AI, or external data.
```

## Phase 2
```text
CONTINUE TO PHASE 2.
Add persistence behind repository interfaces without coupling the Economic Compiler to SQLAlchemy.
```

## Phase 3
```text
CONTINUE TO PHASE 3.
Expose the existing application/domain behavior through typed FastAPI contracts.
Do not move economic logic into endpoint handlers.
```

## Phase 4
```text
CONTINUE TO PHASE 4.
Create the Expo mobile foundation and connect it to the existing API.
Do not build the advanced graph yet.
```

## Phase 5
```text
CONTINUE TO PHASE 5.
Implement the bounded interactive economic graph.
Do not introduce 3D or global-scale rendering.
```

## Phase 6
```text
CONTINUE TO PHASE 6.
Implement Shock Lab and the first complete Explore → Change → Execute → Explain interaction.
Treat this as a product kill gate.
```

## Phase 7
```text
CONTINUE TO PHASE 7.
Implement provenance/evidence architecture using controlled fixtures before any AI extraction.
```

## Phase 8
```text
CONTINUE TO PHASE 8.
Implement robust official-document ingestion and worker semantics.
No AI extraction yet.
```

## Phase 9
```text
CONTINUE TO PHASE 9.
Implement structured AI claim extraction and a real evaluation harness.
AI may propose; it may not publish models.
```

## Phase 10
```text
CONTINUE TO PHASE 10.
Construct the first real evidence-backed company model.
Preserve explicit distinctions between disclosed, derived, assumed, and AI-proposed information.
```

## Phase 11
```text
CONTINUE TO PHASE 11.
Expand into a tightly scoped semiconductor network and support cross-entity propagation.
```

## Phase 12
```text
CONTINUE TO PHASE 12.
Implement point-in-time Time Machine semantics with mandatory leakage tests.
```

## Phase 13
```text
CONTINUE TO PHASE 13.
Implement historical calibration and error measurement without overstating predictive claims.
```

## Phase 14
```text
CONTINUE TO PHASE 14.
Implement saved-thesis monitoring and evidence-change classification.
```

## Phase 15
```text
CONTINUE TO PHASE 15.
Build the Next.js deployment/review console for real operational workflows.
Do not duplicate domain logic in TypeScript.
```

## Phase 16
```text
CONTINUE TO PHASE 16.
Deploy DOMINO reproducibly to AWS using Docker, Terraform, and CI/CD.
Prefer the simplest production architecture that satisfies current requirements.
```

## Phase 17
```text
CONTINUE TO PHASE 17.
Add observability, authentication/authorization, reliability engineering, load testing, and incident readiness.
No silent fallback behavior.
```

## Phase 18
```text
CONTINUE TO PHASE 18.
Build secure integration adapters and the approved MCP surface without bypassing domain rules.
```

## Phase 19
```text
CONTINUE TO PHASE 19.
Productize deployment patterns into the FDE Deployment Kit and validate them on a second deployment-style environment.
```

## Phase 20
```text
CONTINUE TO PHASE 20.
Create a portable Kubernetes/Helm deployment profile without rewriting core application code.
```

## Phase 21
```text
CONTINUE TO PHASE 21.
Prepare and validate the real TestFlight beta.
No new product scope.
```

## Phase 22
```text
CONTINUE TO PHASE 22.
Prepare the App Store release and production release gate.
No unrelated feature development.
```

---

# 9. DAILY CODING PROMPT

If you want one short prompt to use most often, use this:

```text
Read AGENTS.md, docs/PHASES.md, docs/STATUS.md, docs/DECISIONS.md, and the relevant code/tests.

Work only on:

<TASK>

Think about the whole system before coding.

Identify:
- domain owner
- correct layer
- contract
- invariants
- failure behavior
- abstraction needed, if any
- known future extension pressure
- tests

Do not over-engineer, but do not write one-off code that bypasses the architecture.

No silent fallbacks.
No fake defaults.
No placeholder production success.
No swallowed exceptions.
No duplicated domain logic.

Implement in small testable increments:

test → implement → test → refactor → test

Run focused tests after every small behavior.

Before completion run:
- relevant full tests
- integration tests
- type checking
- lint
- build checks where applicable

Review the touched code as a senior engineer for:
- readability
- maintainability
- scalability of the architecture
- dependency direction
- coupling
- duplication
- failure semantics
- test quality

Update STATUS.md and other relevant docs.

Report actual commands/results and STOP.
```

---

# 10. INTERVIEW / FDE STORY MAP

The project should ultimately let you truthfully explain:

## Discovery / product
"I started from the workflow: users need to understand how economic assumptions propagate, not just read AI summaries."

## System design
"I separated source evidence, claims, model assumptions, deterministic equations, and user scenarios."

## Python
"The Economic Compiler, ingestion workers, calibration, and backend are Python."

## SQL / PostgreSQL
"Models, versioning, provenance, jobs, temporal claims, scenarios, and audit records are relational and queryable."

## TypeScript / React
"The operator/deployment console is Next.js/React/TypeScript."

## Mobile
"The end-user interaction is Expo/React Native."

## APIs
"Clients and integrations operate through versioned typed REST/OpenAPI contracts."

## AI
"LLMs extract evidence-backed candidate claims through structured output; they do not calculate or publish authoritative economic models."

## Evals
"Extraction has frozen human-reviewed eval sets measuring precision, coverage, evidence correctness, and unsupported claims."

## Data engineering
"Official filings move through idempotent discovery, ingestion, hashing, normalization, extraction, review, and publication."

## Cloud
"The system is containerized and deployed on AWS."

## Terraform
"The environment can be reproduced from IaC."

## CI/CD
"GitHub Actions runs tests/type/lint/build before deployment."

## Observability
"Requests, scenarios, jobs, LLM extraction, and publication are traceable through logs, metrics, and traces."

## Security
"Secrets are server-side; privileges are separated; publication and integration actions are audited."

## Kubernetes
"Once the main system was stable, I created a Helm-based portable customer deployment profile without changing domain code."

## MCP / agents
"DOMINO exposes selected validated economic capabilities as MCP tools, with auth, schemas, and audit logs."

## FDE pattern
"The second deployment reused adapters, configuration, Terraform modules, smoke tests, and runbooks instead of forking the product."

That is a much stronger FDE story than:

> "I used 20 technologies."

