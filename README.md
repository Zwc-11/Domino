# DOMINO

An interactive economic simulation system: companies and economic systems modeled as executable, evidence-backed variables and equations. Change an assumption, execute a deterministic scenario, and inspect how the consequences propagate and why.

Current state: see [`docs/STATUS.md`](docs/STATUS.md). Rules for all contributors and coding agents: [`AGENTS.md`](AGENTS.md).

## Repository

| Path | Contents |
|---|---|
| `backend/` | Python 3.12 package `domino` (uv) |
| `mobile/` | Expo / React Native / TypeScript client |
| `docs/` | Product, architecture, spec, phases, decisions, status, evals, agent prompts |
| `compose.yaml` | Local PostgreSQL |
| `.github/workflows/ci.yml` | CI |

## Prerequisites

- [uv](https://docs.astral.sh/uv/) ≥ 0.12 (installs Python 3.12 automatically)
- Node.js 22 (see `mobile/.nvmrc`)
- Docker with Compose v2 (for the local database)

## Setup

```bash
# Backend
cd backend
uv sync

# Mobile
cd ../mobile
npm ci

# Local database (from repository root)
cd ..
cp .env.example .env        # PowerShell: Copy-Item .env.example .env
docker compose up --detach --wait
```

## Verification (what CI runs)

```bash
# backend/
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest

# mobile/
npm run typecheck
npm run lint
# or both: npm run check

# repository root
docker compose config --quiet
```

## Working on DOMINO

Work proceeds one phase at a time (`docs/PHASES.md`). Session prompts for coding agents are in `docs/PROMPTS.md`; start each session with Prompt A (bootstrap), then `CONTINUE TO PHASE <N>`.
