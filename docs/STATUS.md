# DOMINO Status

## Current Phase
Phase 0 — Repository Foundation

## Phase State
COMPLETE

## Last Updated
2026-09-27

## Working System Summary
No business functionality exists. By design, Phase 0 contains no economic, persistence, API, or AI behavior.

What works:
- Python package `domino` installs from `backend/uv.lock` and imports.
- Backend quality gates: ruff lint (including blind-except / try-except-pass rules), ruff format, mypy strict, pytest + Hypothesis.
- Import-boundary enforcement for the planned layers (`backend/tests/architecture/`). The checker is tested and verified live against a violating probe module; each layer rule activates when its layer package is created.
- Expo SDK 57 shell app (`mobile/`) type checks under strict TypeScript and lints with zero warnings.
- `compose.yaml` defines PostgreSQL 17 with required variables (no defaults) and a healthcheck.
- GitHub Actions workflow with backend, mobile, and compose jobs.

## Current Architecture
Modular-monolith backend skeleton (`backend/src/domino`, no layer packages yet), standalone Expo client, local PostgreSQL via Compose. Layer rules and the dependency direction are documented in `docs/ARCHITECTURE.md` and enforced by tests.

## Completed In Current Phase
- Monorepo structure (ADR-0001)
- Python configuration: uv, uv_build, src layout, Python 3.12 (ADR-0002)
- Import-boundary checker + layer rules (ADR-0003)
- Expo/TypeScript workspace with strict type checking and ESLint (ADR-0004)
- pytest, Hypothesis (dev/ci profiles), ruff, mypy
- Docker Compose skeleton (ADR-0005)
- GitHub Actions CI (ADR-0006)
- Docs: `AGENTS.md`, `CLAUDE.md`, `README.md`, `docs/PRODUCT.md`, `docs/ARCHITECTURE.md`, `docs/ECONOMIC_MODEL_SPEC.md` (draft), `docs/PHASES.md`, `docs/DECISIONS.md`, `docs/STATUS.md`, `docs/EVALS.md`, `docs/PROMPTS.md`

## Remaining In Current Phase
- None in code. See "Current Risks" for the two checks that need an environment with Docker Hub / GitHub access.

## Exit Gate
- [x] Python imports work
- [x] Mobile type checks
- [x] Tests run
- [x] Lint/type checks pass
- [x] CI exists (validated with actionlint; not yet executed on GitHub — see Risks)
- [x] Docs exist
- [x] `STATUS.md` is accurate

## Tests
### Last Full Verification
Run from a clean copy of the repository (no `.venv`, no `node_modules`) on 2026-09-27, Linux, uv 0.12.19, Node 22.22.2.

Command: `cd backend && uv sync --locked && HYPOTHESIS_PROFILE=ci uv run pytest`
Result: 17 passed, 4 skipped. The skips are the four layer-boundary rules whose layer packages do not exist yet: `domino.engine` (Phase 1), `domino.domain` (Phase 1-2), `domino.application` (Phase 2-3), `domino.infrastructure` (Phase 2).

### Focused Tests
- `uv run pytest tests/architecture/test_import_boundaries.py` — 15 passed (checker behavior, including Hypothesis properties)
- Live probe: temporary `src/domino/engine/probe.py` with `from ..api import routes` → `test_layer_respects_dependency_direction[domino.engine]` failed as expected; probe removed
- `HYPOTHESIS_PROFILE=bogus uv run pytest` → fails at startup with `RuntimeError: Unknown HYPOTHESIS_PROFILE` (as designed)

## Type Checking
- `uv run mypy` — Success: no issues found in 7 source files
- `npm run typecheck` (`tsc --noEmit`) — pass
- Negative probe: `const first: number = xs[0]` → TS2322 (confirms `noUncheckedIndexedAccess` active)

## Lint
- `uv run ruff check .` — All checks passed
- `uv run ruff format --check .` — 8 files already formatted
- `npm run lint` (`eslint . --max-warnings=0`) — pass
- Negative probes: `except Exception: pass` → ruff `S110` + `BLE001`; empty `catch {}` → ESLint `no-empty`

## Build / Integration
- `docker compose config --quiet` with `.env` from `.env.example` — pass
- `docker compose config --quiet` without `.env` — fails with `required variable POSTGRES_PASSWORD is missing a value` (as designed)
- `actionlint .github/workflows/ci.yml` — pass; action inputs verified against `action.yml` of `actions/checkout@v7.0.1`, `actions/setup-node@v7.0.0`, `astral-sh/setup-uv@v10.2.0`
- `npm ci` from `mobile/package-lock.json` — pass (705 packages)

## Known Failures
- None.

## Known Limitations
- `npx expo-doctor`: 19/21 checks pass. The 2 failing checks (config schema, React Native Directory) require network access to Expo services that was unavailable in the verification environment; they are not project errors. Re-run locally.
- The import-boundary checker does not detect dynamic imports (`importlib.import_module`).
- `value or 0` unknown-to-zero coercion (`AGENTS.md` §17) is not lint-detectable; it remains a review item.
- The mobile app is a shell that renders a title. No navigation, API client, or tests (Phase 4).

## Deferred By Design
- Economic Compiler, domain model, AcmeGPU (Phase 1)
- SQLAlchemy, Alembic, schema, repositories (Phase 2)
- FastAPI and HTTP contracts (Phase 3)
- Expo Router, TanStack Query, Zustand, Zod, mobile test runner (Phase 4)
- Skia, Reanimated (Phase 5)
- Backend/worker Dockerfiles (added with the services they run)
- Terraform/AWS (Phase 16), Kubernetes/Helm (Phase 20)
- Repository license (owner decision)

## Current Risks
- **CI has not executed on GitHub.** The repository has no remote yet. The first push to GitHub is the first real CI run.
- **Compose database boot not executed.** Docker Hub was unreachable from the verification environment, so `docker compose up --wait` has not run. The CI `compose` job runs it; it can also be run locally.

## Next Allowed Action
1. Initialize git, push to GitHub, and confirm all three CI jobs are green.
2. Run `docker compose up --detach --wait` locally once.
3. `CONTINUE TO PHASE 1`
