# DOMINO backend

Python package `domino`. See the repository-root `README.md` for setup and `docs/ARCHITECTURE.md` for layer boundaries.

```bash
uv sync                      # create .venv from uv.lock
uv run pytest                # tests
uv run ruff check .          # lint
uv run ruff format --check . # formatting
uv run mypy                  # strict type checking
```
