"""Tests for the import-boundary checker itself."""

from pathlib import Path

import pytest
from hypothesis import given
from hypothesis import strategies as st

from tests.architecture.import_boundaries import (
    LayerRule,
    find_violations,
    imported_modules,
    is_within,
)

_identifier = st.from_regex(r"[a-z][a-z0-9_]{0,11}", fullmatch=True)
_dotted = st.lists(_identifier, min_size=1, max_size=4).map(".".join)


def _write(root: Path, relative: str, source: str) -> Path:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(source, encoding="utf-8")
    return path


# ------------------------------------------------------------------ is_within


@given(prefix=_dotted, suffix=_dotted)
def test_submodule_is_within_prefix(prefix: str, suffix: str) -> None:
    assert is_within(f"{prefix}.{suffix}", prefix)


@given(prefix=_dotted)
def test_module_is_within_itself(prefix: str) -> None:
    assert is_within(prefix, prefix)


@given(prefix=_dotted, tail=_identifier)
def test_sibling_sharing_a_name_prefix_is_not_within(prefix: str, tail: str) -> None:
    # "fastapi_utils" must not be treated as part of "fastapi".
    assert not is_within(f"{prefix}{tail}", prefix)


# ------------------------------------------------------------ imported_modules


def test_collects_absolute_imports(tmp_path: Path) -> None:
    module = _write(
        tmp_path,
        "domino/engine/compiler.py",
        "import fastapi\nimport os.path as p\nfrom sqlalchemy.orm import Session\n",
    )
    found = {imp.module for imp in imported_modules(module, package_root=tmp_path)}
    assert found == {"fastapi", "os.path", "sqlalchemy.orm"}


def test_resolves_relative_imports_against_the_module_package(tmp_path: Path) -> None:
    module = _write(
        tmp_path,
        "domino/engine/compiler.py",
        "from . import graph\nfrom .graph import order\nfrom ..api import routes\n",
    )
    found = {imp.module for imp in imported_modules(module, package_root=tmp_path)}
    assert found == {"domino.engine", "domino.engine.graph", "domino.api"}


def test_resolves_relative_imports_inside_package_init(tmp_path: Path) -> None:
    module = _write(tmp_path, "domino/engine/__init__.py", "from .compiler import compile_model\n")
    found = {imp.module for imp in imported_modules(module, package_root=tmp_path)}
    assert found == {"domino.engine.compiler"}


def test_relative_import_beyond_package_root_is_an_error(tmp_path: Path) -> None:
    module = _write(tmp_path, "domino/x.py", "from ... import nowhere\n")
    with pytest.raises(ValueError, match="beyond the package root"):
        imported_modules(module, package_root=tmp_path)


def test_records_line_numbers(tmp_path: Path) -> None:
    module = _write(tmp_path, "domino/engine/a.py", "import os\n\nimport fastapi\n")
    lines = {imp.module: imp.line for imp in imported_modules(module, package_root=tmp_path)}
    assert lines == {"os": 1, "fastapi": 3}


# ------------------------------------------------------------- find_violations

_ENGINE_RULE = LayerRule(layer="domino.engine", forbidden=("fastapi", "domino.api"))


def test_reports_forbidden_framework_import(tmp_path: Path) -> None:
    _write(tmp_path, "domino/engine/__init__.py", "")
    _write(tmp_path, "domino/engine/compiler.py", "import os\nfrom fastapi import APIRouter\n")

    violations = find_violations(_ENGINE_RULE, package_root=tmp_path)

    assert [(v.imported, v.forbidden_prefix, v.line) for v in violations] == [
        ("fastapi", "fastapi", 2)
    ]
    assert violations[0].path.name == "compiler.py"


def test_reports_forbidden_relative_import_of_outer_layer(tmp_path: Path) -> None:
    _write(tmp_path, "domino/engine/__init__.py", "")
    _write(tmp_path, "domino/engine/compiler.py", "from ..api.routes import router\n")

    violations = find_violations(_ENGINE_RULE, package_root=tmp_path)

    assert [v.imported for v in violations] == ["domino.api.routes"]


def test_reports_outer_layer_imported_as_a_name_from_its_parent(tmp_path: Path) -> None:
    # `from .. import api` names the forbidden subpackage only in the imported names.
    _write(tmp_path, "domino/engine/__init__.py", "")
    _write(tmp_path, "domino/engine/compiler.py", "from .. import api\nfrom domino import api\n")

    violations = find_violations(_ENGINE_RULE, package_root=tmp_path)

    assert [(v.imported, v.line) for v in violations] == [("domino.api", 1), ("domino.api", 2)]


def test_scans_nested_subpackages(tmp_path: Path) -> None:
    _write(tmp_path, "domino/engine/__init__.py", "")
    _write(tmp_path, "domino/engine/ir/__init__.py", "")
    _write(tmp_path, "domino/engine/ir/nodes.py", "import fastapi.routing\n")

    violations = find_violations(_ENGINE_RULE, package_root=tmp_path)

    assert [v.imported for v in violations] == ["fastapi.routing"]


def test_clean_layer_has_no_violations(tmp_path: Path) -> None:
    _write(tmp_path, "domino/engine/__init__.py", "")
    _write(tmp_path, "domino/engine/compiler.py", "import math\nfrom . import graph\n")

    assert find_violations(_ENGINE_RULE, package_root=tmp_path) == []


def test_missing_layer_is_an_error_not_an_empty_result(tmp_path: Path) -> None:
    # No silent success: checking a layer that does not exist must fail loudly.
    with pytest.raises(FileNotFoundError, match=r"domino\.engine"):
        find_violations(_ENGINE_RULE, package_root=tmp_path)


def test_syntax_error_in_scanned_module_propagates(tmp_path: Path) -> None:
    _write(tmp_path, "domino/engine/__init__.py", "")
    _write(tmp_path, "domino/engine/broken.py", "def (:\n")

    with pytest.raises(SyntaxError):
        find_violations(_ENGINE_RULE, package_root=tmp_path)
