"""Test-suite configuration.

Hypothesis profiles (select with the HYPOTHESIS_PROFILE environment variable):

- ``dev`` (default): randomized exploration with the local example database.
- ``ci``: derandomized so CI runs are reproducible (AGENTS.md §44).
"""

import os

from hypothesis import HealthCheck, settings

settings.register_profile("dev", max_examples=100)
settings.register_profile(
    "ci",
    derandomize=True,
    database=None,
    max_examples=200,
    deadline=None,
    print_blob=True,
    suppress_health_check=[HealthCheck.too_slow],
)

_profile = os.environ.get("HYPOTHESIS_PROFILE", "dev")
if _profile not in {"dev", "ci"}:
    raise RuntimeError(f"Unknown HYPOTHESIS_PROFILE {_profile!r}; expected 'dev' or 'ci'.")
settings.load_profile(_profile)
