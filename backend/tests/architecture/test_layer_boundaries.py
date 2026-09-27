"""Enforce DOMINO's dependency direction on the real source tree (AGENTS.md §7).

Layers that do not exist yet are reported as skipped with the phase that
creates them; once a layer package exists its rule is enforced.
"""

from pathlib import Path

import pytest

from tests.architecture.import_boundaries import LayerRule, find_violations

SRC_ROOT = Path(__file__).resolve().parents[2] / "src"

# Frameworks and SDKs that belong at system boundaries, never in the core.
FRAMEWORKS = (
    "fastapi",
    "starlette",
    "uvicorn",
    "sqlalchemy",
    "alembic",
    "psycopg",
    "psycopg2",
    "asyncpg",
    "httpx",
    "requests",
    "boto3",
    "botocore",
    "aioboto3",
    "openai",
    "anthropic",
    "google.genai",
    "litellm",
)

LAYER_RULES = (
    LayerRule(
        layer="domino.engine",
        forbidden=(
            *FRAMEWORKS,
            "domino.domain",
            "domino.application",
            "domino.infrastructure",
            "domino.api",
        ),
    ),
    LayerRule(
        layer="domino.domain",
        forbidden=(*FRAMEWORKS, "domino.application", "domino.infrastructure", "domino.api"),
    ),
    LayerRule(
        layer="domino.application",
        forbidden=(*FRAMEWORKS, "domino.infrastructure", "domino.api"),
    ),
    LayerRule(layer="domino.infrastructure", forbidden=("domino.api",)),
)

INTRODUCED_IN = {
    "domino.engine": "Phase 1",
    "domino.domain": "Phase 1-2",
    "domino.application": "Phase 2-3",
    "domino.infrastructure": "Phase 2",
}


def test_every_rule_has_a_documented_introduction_phase() -> None:
    assert {rule.layer for rule in LAYER_RULES} == set(INTRODUCED_IN)


def test_src_root_contains_the_domino_package() -> None:
    assert (SRC_ROOT / "domino" / "__init__.py").is_file()


@pytest.mark.parametrize("rule", LAYER_RULES, ids=lambda rule: rule.layer)
def test_layer_respects_dependency_direction(rule: LayerRule) -> None:
    layer_dir = SRC_ROOT.joinpath(*rule.layer.split("."))
    if not layer_dir.exists():
        pytest.skip(f"{rule.layer} not created yet (introduced in {INTRODUCED_IN[rule.layer]})")

    violations = find_violations(rule, package_root=SRC_ROOT)

    assert violations == [], "\n".join(str(v) for v in violations)
