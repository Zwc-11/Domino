"""DOMINO: an interactive economic simulation system.

Layer packages (created in their designated phases, see docs/ARCHITECTURE.md):

- ``domino.engine``          Economic Compiler (Phase 1)
- ``domino.domain``          domain model and repository interfaces
- ``domino.application``     use cases / orchestration
- ``domino.infrastructure``  persistence, providers, external adapters
- ``domino.api``             HTTP boundary (Phase 3)

Allowed import directions are enforced by ``tests/architecture``.
"""
