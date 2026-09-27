# Architecture Decision Log

## ADR-0001 — Monorepo layout

### Status
Accepted

### Date
2026-09-27

### Context
DOMINO has a Python backend and a React Native client now, and a web console, Terraform, and Helm later. Contracts (OpenAPI) must stay consistent across them.

### Decision
Single repository with top-level `backend/`, `mobile/`, `docs/`, and root-level `compose.yaml` and CI. Later phases add `web/` (Phase 15), `infra/` (Phase 16), and `deploy/helm/` (Phase 20). No JavaScript workspace tooling (npm/pnpm workspaces, Turborepo) at root: `mobile/` is a standalone npm package with its own lockfile.

### Alternatives Considered
1. Separate repositories per client/service — breaks atomic contract changes, adds CI overhead.
2. npm/pnpm workspaces from day one — no second TypeScript package exists to share code with.

### Why
One source of truth for docs and contracts; each package keeps its native toolchain.

### Consequences
Positive:
- Atomic changes across API contract and clients.
- Per-package tooling stays idiomatic (`uv`, `npm`).

Negative:
- CI must scope jobs by package directory.

### Revisit Trigger
Phase 15 introduces `web/`. If `mobile/` and `web/` need shared TypeScript (generated API client, Zod schemas), adopt a workspace tool then, via ADR.

---

## ADR-0002 — Python toolchain: uv, uv_build, src layout, ruff, mypy strict, pytest + Hypothesis

### Status
Accepted

### Date
2026-09-27

### Context
The backend needs reproducible environments, a lockfile, fast lint/format, strict typing, and property-based testing (`AGENTS.md` §40–§47).

### Decision
- `uv` 0.12 for environments, locking (`uv.lock`), and running tools; CI pins uv `0.12.19` and uses `uv sync --locked`.
- `uv_build` as build backend; package at `backend/src/domino` (src layout).
- Python `>=3.12`; `.python-version` pins 3.12 for local and CI.
- `ruff` for lint + format. Rule set includes `BLE` (blind except), `S110`/`S112` (try-except-pass/continue), and `TRY`, so the no-swallowed-exceptions rule (`AGENTS.md` §11) is machine-enforced.
- `mypy --strict` with `warn_unreachable` and extra error codes (`ignore-without-code`, `redundant-expr`, `truthy-bool`, `possibly-undefined`).
- `pytest` with warnings-as-errors, strict markers/config, strict xfail; `Hypothesis` with a derandomized `ci` profile.

### Alternatives Considered
1. Poetry — slower resolver; separate lock format; no advantage for this project.
2. pip-tools + venv — more manual steps; weaker Windows ergonomics.
3. Hatchling backend — works equally; `uv_build` removes a dependency and matches the tool already required.
4. pyright instead of mypy — mypy is the stack listed in `AGENTS.md` §23/§Quality.

### Why
Single fast tool for the whole Python lifecycle; strictness settings turn several constitution rules into CI failures instead of review comments.

### Consequences
Positive:
- Reproducible environments on Windows, macOS, Linux, and CI from one lockfile.
- Lint catches swallowed and blind exceptions automatically.

Negative:
- Contributors must install uv.
- `value or 0`-style unknown-to-zero coercion (`AGENTS.md` §17) is not lint-detectable; it remains a review item.

### Revisit Trigger
uv or uv_build introduces a breaking change that blocks a phase, or the ruff rule set produces recurring false positives that require `noqa` more than rarely.

---

## ADR-0003 — Layer package names and mechanical import-boundary enforcement

### Status
Accepted

### Date
2026-09-27

### Context
`AGENTS.md` §7 defines dependency direction (engine ← domain ← application ← API; infrastructure implements domain interfaces). Written rules drift unless checked.

### Decision
Layer packages are `domino.engine`, `domino.domain`, `domino.application`, `domino.infrastructure`, `domino.api`, each created in its phase (not pre-created empty). A ~130-line AST-based checker in `backend/tests/architecture/` enforces per-layer forbidden-import rules (table in `docs/ARCHITECTURE.md`). It resolves relative imports and checks `from x import y` names as potential submodules. Missing layers are reported as skipped tests naming their introduction phase; a rule pointing at a missing layer inside the checker API raises instead of passing.

### Alternatives Considered
1. `import-linter` — mature, declarative contracts; adds a dependency and configuration language for a rule set that is currently five lines.
2. Documentation only — not enforced.
3. Pre-creating empty layer packages — speculative structure; violates "do not implement future features early".

### Why
Zero dependencies, fully tested (including Hypothesis properties for prefix matching), and the rules sit next to the tests that use them.

### Consequences
Positive:
- A framework import in the engine fails CI the moment the engine exists.

Negative:
- Dynamic imports (`importlib.import_module`) are not detected.
- The framework list must be extended when a new boundary dependency is added.

### Revisit Trigger
Rules require layered contracts, independence contracts between sibling modules, or exceptions lists — then migrate to `import-linter`.

---

## ADR-0004 — Mobile workspace: Expo SDK 57, strict TypeScript, ESLint; tests deferred to Phase 4

### Status
Accepted

### Date
2026-09-27

### Context
Phase 0 requires an Expo/TypeScript workspace that type checks. The target stack lists Expo, TypeScript strict mode, Expo Router, TanStack Query, Zustand, Zod, Reanimated, Skia — each assigned to later phases.

### Decision
- Scaffold from `create-expo-app` `blank-typescript`: Expo `~57.0.25`, React Native `0.86.3`, React `19.2.3`, TypeScript `~6.0.3` (versions as pinned by the SDK template).
- `tsconfig.json` extends `expo/tsconfig.base` with `strict`, `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, `noImplicitOverride`, `noImplicitReturns`, `noFallthroughCasesInSwitch`, `noUnused*`, `noPropertyAccessFromIndexSignature`.
- ESLint 9 flat config with `eslint-config-expo` plus `no-empty` (including empty catch), `eqeqeq`, `no-console` (warn/error allowed). Lint runs with `--max-warnings=0`.
- Node 22 (`mobile/.nvmrc`).
- No Expo Router, state, query, or validation libraries yet (Phase 4). No mobile test runner yet: there is no behavior to test, and adding `jest-expo` now would produce only placeholder tests.

### Alternatives Considered
1. Bare React Native CLI — loses EAS/managed workflow needed for Phase 21 TestFlight.
2. Installing the full Phase 4–5 library set now — dependencies without behavior; version drift before use.
3. TypeScript 7 (native compiler) — not the version the Expo SDK 57 template pins; revisit when Expo adopts it.

### Why
Smallest workspace that satisfies the Phase 0 exit gate and gives strict type checking from the first line of real code.

### Consequences
Positive:
- Strict flags catch unchecked index access and optional-property misuse from the start.

Negative:
- `exactOptionalPropertyTypes` can conflict with some third-party typings; if it does, the resolution is recorded in a new ADR rather than silently disabling it.

### Revisit Trigger
Phase 4 adds Expo Router and a test runner (`jest-expo` + React Native Testing Library) together with the first real screens.

---

## ADR-0005 — Local services: Docker Compose with PostgreSQL 17 only, required variables without defaults

### Status
Accepted

### Date
2026-09-27

### Context
Phase 0 requires a Docker Compose skeleton. PostgreSQL is the primary datastore (`AGENTS.md` §19); schema work begins in Phase 2.

### Decision
`compose.yaml` defines one service, `postgres:17`, bound to `127.0.0.1`, with a named volume and a `pg_isready` healthcheck. Every variable uses `${VAR:?message}` so a missing `.env` fails immediately instead of falling back to defaults (`AGENTS.md` §10). `.env.example` holds local-only development values; `.env` is git-ignored. API and worker containers are added in their phases.

### Alternatives Considered
1. Empty compose file — satisfies "skeleton" literally but verifies nothing.
2. Include API/worker containers now — no code to run.
3. PostgreSQL 18 — newer; 17 chosen as the conservative major with the broadest managed-service support at the time of Phase 16 planning.

### Why
Gives Phase 2 a ready, health-checked database and exercises the no-silent-defaults rule in configuration.

### Consequences
Positive:
- Phase 2 integration tests have a local target.

Negative:
- Contributors need Docker to run the database locally.

### Revisit Trigger
Phase 16 selects the RDS engine version; local major version must match production.

---

## ADR-0006 — CI: GitHub Actions with backend, mobile, and compose jobs

### Status
Accepted

### Date
2026-09-27

### Context
`AGENTS.md` §47 and the Phase 0 exit gate require CI that runs tests, lint, and type checks.

### Decision
`.github/workflows/ci.yml` runs on pushes to `main` and all pull requests, with `contents: read` permissions and per-ref concurrency cancellation:
- **backend:** `uv sync --locked`, `ruff check`, `ruff format --check`, `mypy`, `pytest` with `HYPOTHESIS_PROFILE=ci`.
- **mobile:** `npm ci`, `npm run typecheck`, `npm run lint`.
- **compose:** `docker compose config`, `docker compose up --wait` (healthcheck-gated), teardown.

Action versions: `actions/checkout@v7`, `actions/setup-node@v7`, `astral-sh/setup-uv@v10`. The workflow is validated with `actionlint`.

### Alternatives Considered
1. Single job running everything — slower feedback, coupled failures.
2. Path-filtered jobs — premature at current size; risks skipping checks on cross-cutting changes.

### Why
Fast, parallel, independently failing checks per package, each using the lockfile.

### Consequences
Positive:
- Every PR proves lockfiles install, lint/types pass, tests pass, and the database boots.

Negative:
- Compose job pulls `postgres:17` on every run.

### Revisit Trigger
CI time exceeds ~10 minutes, or Phase 16 adds build/deploy stages (then split into CI and CD workflows).
