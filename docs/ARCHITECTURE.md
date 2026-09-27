# DOMINO Architecture

Status: Phase 0. Describes the enforced repository structure and the target layering. Components listed as "planned" do not exist yet; see `docs/STATUS.md` for what works.

## Repository layout

```text
DOMINO/
├── AGENTS.md                  Engineering constitution (governs all work)
├── CLAUDE.md                  Imports AGENTS.md for Claude Code
├── README.md                  Setup and verification commands
├── compose.yaml               Local services (PostgreSQL)
├── .env.example               Local-only variables for compose.yaml
├── .github/workflows/ci.yml   CI: backend, mobile, compose jobs
├── docs/
│   ├── PRODUCT.md             Product intent and non-goals
│   ├── ARCHITECTURE.md        This file
│   ├── ECONOMIC_MODEL_SPEC.md Economic Compiler specification (draft until Phase 1)
│   ├── PHASES.md              Phased plan; one active phase at a time
│   ├── DECISIONS.md           Architecture decision records
│   ├── STATUS.md              Current, verified state
│   ├── EVALS.md               AI evaluation methodology (from Phase 9)
│   └── PROMPTS.md             Session prompts for coding agents
├── backend/                   Python 3.12 package `domino` (uv-managed)
│   ├── pyproject.toml         Dependencies + ruff/mypy/pytest configuration
│   ├── uv.lock
│   ├── src/domino/            Layer packages live here (see below)
│   └── tests/
│       ├── conftest.py        Hypothesis profiles (dev / ci)
│       └── architecture/      Import-boundary checker + layer rules
└── mobile/                    Expo / React Native / TypeScript (strict)
```

Planned top-level additions, each only in its phase: `web/` (Next.js console, Phase 15), `infra/` (Terraform, Phase 16), `deploy/helm/` (Phase 20).

## Layers and dependency direction

```text
mobile/  web/            (clients; talk to the API only)
    │
    ▼
domino.api               HTTP boundary: FastAPI routes, Pydantic contracts   (Phase 3)
    │
    ▼
domino.application       use cases, orchestration, transaction boundaries    (Phase 2–3)
    │
    ▼
domino.domain            domain concepts, invariants, repository interfaces  (Phase 1–2)
    │
    ▼
domino.engine            Economic Compiler: pure, deterministic              (Phase 1)

domino.infrastructure ──implements──▶ domain interfaces                     (Phase 2)
```

### Enforced import rules

`backend/tests/architecture/test_layer_boundaries.py` parses every module in each layer (via `ast`; nothing is imported) and fails on a forbidden import. A layer package that does not exist yet is reported as a skipped test naming the phase that introduces it.

| Layer | Must not import |
|---|---|
| `domino.engine` | frameworks/SDKs¹, `domino.domain`, `domino.application`, `domino.infrastructure`, `domino.api` |
| `domino.domain` | frameworks/SDKs¹, `domino.application`, `domino.infrastructure`, `domino.api` |
| `domino.application` | frameworks/SDKs¹, `domino.infrastructure`, `domino.api` |
| `domino.infrastructure` | `domino.api` |
| `domino.api` | (composition root; may import inward layers) |

¹ `fastapi`, `starlette`, `uvicorn`, `sqlalchemy`, `alembic`, `psycopg`, `psycopg2`, `asyncpg`, `httpx`, `requests`, `boto3`, `botocore`, `aioboto3`, `openai`, `anthropic`, `google.genai`, `litellm`.

Adding a framework to the backend requires adding it to this list if it must stay at the boundary. Changing a rule requires an ADR.

## Side-effect ordering

Every use case follows `load → validate → calculate → persist → publish` (`AGENTS.md` §9). The engine performs only `calculate`.

## Runtime components

| Component | State | Phase |
|---|---|---|
| PostgreSQL (local, via compose) | Service defined; no schema | 0 (service), 2 (schema) |
| Economic Compiler | Planned | 1 |
| Repositories + migrations | Planned | 2 |
| HTTP API (`/api/v1`) | Planned | 3 |
| Mobile client | Shell app only | 0 (shell), 4 (screens) |
| Worker (Postgres jobs table, `FOR UPDATE SKIP LOCKED`) | Planned | 8 |
| Object storage (S3-compatible) | Planned | 8 |
| AI extraction providers | Planned | 9 |
| Web console | Planned | 15 |
| AWS (ECS/Fargate, RDS, S3) via Terraform | Planned | 16 |

## Datastores

PostgreSQL is the only datastore (`AGENTS.md` §19). Any other store requires the Technology Adoption Gate (`AGENTS.md` §22) and an ADR.

## Quality gates

| Area | Tool | Command (from package directory) |
|---|---|---|
| Python lint | ruff (incl. `BLE`, `S110`, `S112`, `TRY`) | `uv run ruff check .` |
| Python format | ruff format | `uv run ruff format --check .` |
| Python types | mypy `strict` + `warn_unreachable` | `uv run mypy` |
| Python tests | pytest + Hypothesis | `uv run pytest` |
| Mobile types | tsc (strict, `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`) | `npm run typecheck` |
| Mobile lint | ESLint flat config (`eslint-config-expo`, `no-empty` incl. catch) | `npm run lint` |
| Compose | `docker compose config` + boot with healthcheck | CI `compose` job |

Pytest runs with `filterwarnings = error`, `--strict-markers`, `--strict-config`, and `xfail_strict`. CI sets `HYPOTHESIS_PROFILE=ci` (derandomized, no example database).
