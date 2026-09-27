"""Static import-boundary checker for DOMINO's layered architecture.

Enforces AGENTS.md §7 (dependency direction) mechanically: each layer package
declares module prefixes it must never import. The checker parses source with
``ast`` and never imports the code under inspection.

Both ``import x`` and ``from x import y`` are checked. For ``from`` imports the
imported names are also checked as potential submodules, so ``from .. import api``
inside ``domino.engine`` is reported as an import of ``domino.api``.
"""

import ast
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class LayerRule:
    """A layer package and the module prefixes it must not import."""

    layer: str
    forbidden: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ImportedModule:
    """One import statement's target module, resolved to an absolute name.

    ``names`` holds the names of a ``from`` import (empty for ``import x``).
    """

    module: str
    names: tuple[str, ...]
    line: int

    def candidates(self) -> Iterator[str]:
        """Every absolute module name this statement may import."""
        yield self.module
        for name in self.names:
            if name != "*":
                yield f"{self.module}.{name}"


@dataclass(frozen=True, slots=True)
class Violation:
    path: Path
    line: int
    imported: str
    forbidden_prefix: str

    def __str__(self) -> str:
        return (
            f"{self.path}:{self.line}: imports {self.imported!r} "
            f"(forbidden: {self.forbidden_prefix!r})"
        )


def is_within(module: str, prefix: str) -> bool:
    """True if ``module`` is ``prefix`` or one of its submodules."""
    return module == prefix or module.startswith(prefix + ".")


def _module_name(path: Path, package_root: Path) -> str:
    parts = path.relative_to(package_root).with_suffix("").parts
    if parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts)


def _resolve_relative(node: ast.ImportFrom, path: Path, package_root: Path) -> str:
    module_name = _module_name(path, package_root)
    # The package that relative imports are resolved against.
    package_parts = module_name.split(".")
    if path.name != "__init__.py":
        package_parts = package_parts[:-1]

    levels_up = node.level - 1
    if levels_up >= len(package_parts):
        raise ValueError(
            f"{path}:{node.lineno}: relative import of level {node.level} "
            "reaches beyond the package root"
        )
    base_parts = package_parts[: len(package_parts) - levels_up]
    if node.module:
        base_parts = [*base_parts, *node.module.split(".")]
    return ".".join(base_parts)


def imported_modules(path: Path, *, package_root: Path) -> list[ImportedModule]:
    """Return the absolute import targets of the module at ``path``.

    ``package_root`` is the directory containing the top-level package
    (the ``src`` directory), used to resolve relative imports.
    """
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    found: list[ImportedModule] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found.extend(ImportedModule(alias.name, (), node.lineno) for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.level == 0:
                # The grammar guarantees a module name for absolute ``from`` imports.
                assert node.module is not None
                module = node.module
            else:
                module = _resolve_relative(node, path, package_root)
            names = tuple(alias.name for alias in node.names)
            found.append(ImportedModule(module, names, node.lineno))
    return sorted(found, key=lambda imp: imp.line)


def find_violations(rule: LayerRule, *, package_root: Path) -> list[Violation]:
    """Return every import inside ``rule.layer`` that matches a forbidden prefix.

    Raises ``FileNotFoundError`` if the layer package does not exist, so a
    misconfigured rule can never pass by scanning nothing.
    """
    layer_dir = package_root.joinpath(*rule.layer.split("."))
    if not (layer_dir / "__init__.py").is_file():
        raise FileNotFoundError(f"Layer package {rule.layer!r} not found at {layer_dir}")

    violations: list[Violation] = []
    for path in sorted(layer_dir.rglob("*.py")):
        for imported in imported_modules(path, package_root=package_root):
            for prefix in rule.forbidden:
                match = next(
                    (name for name in imported.candidates() if is_within(name, prefix)),
                    None,
                )
                if match is not None:
                    violations.append(Violation(path, imported.line, match, prefix))
    return violations
