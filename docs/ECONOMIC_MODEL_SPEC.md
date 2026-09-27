# Economic Model Specification

Status: **DRAFT — finalized in Phase 1.** This file consolidates the requirements from `AGENTS.md` (§2, §13, §24, §26–§30) that the Economic Compiler must satisfy. Anything marked *Open (Phase 1)* is intentionally undecided; Phase 1 resolves it and records the choice in `docs/DECISIONS.md`.

## 1. Purpose

The Economic Compiler turns a structured economic model plus a scenario into deterministic results with a full propagation trace. It is pure application code. It is not an LLM and never executes generated code.

**Inputs:** variables, equations, relationships, assumptions, baseline values, scenario overrides.

**Outputs:** calculated values, deltas vs. baseline, propagation paths, affected variables, uncertainty information, calculation traces, provenance references, a stable result hash.

## 2. Concepts

| Concept | Definition | Key invariant |
|---|---|---|
| `EconomicVariable` | A measurable or modeled economic quantity with an explicit unit | Unknown value stays unknown |
| `Equation` | Defines one target variable from an expression over other variables | May reference only declared variables |
| `EconomicModel` | Executable model of an entity or connected system | — |
| `ModelVersion` | Immutable snapshot of an `EconomicModel` | Published versions are never mutated; a change creates a new version |
| `Scenario` | A set of hypothetical changes to baseline values | — |
| `ScenarioRun` | Immutable execution of one `Scenario` against exactly one `ModelVersion` | Same model + baseline + scenario ⇒ identical result and hash |

## 3. Expression IR

Equations use a constrained, typed intermediate representation. Example:

```json
{
  "target": "revenue",
  "expression": {
    "op": "multiply",
    "args": [
      {"ref": "unit_volume"},
      {"ref": "average_selling_price"}
    ]
  }
}
```

### Operators

| Operator | Phase |
|---|---|
| `constant`, `reference`, `add`, `subtract`, `multiply`, `divide` | 1 |
| `min`, `max`, `clamp`, `percentage_change`, `weighted_average`, `piecewise`, `lag` | Only when a model requires them |

Operators are added one at a time with tests, never in bulk.

## 4. Compiler pipeline

```text
schema validation
→ reference validation
→ unit validation
→ dependency graph construction
→ cycle detection
→ topological ordering
→ execution plan
→ scenario overrides
→ deterministic execution
→ propagation trace
→ result hash
```

Each stage fails with a typed error; no stage substitutes a default to continue.

## 5. Units

Values carry explicit units, e.g. `USD`, `USD/unit`, `units`, `percentage`, `percentage_points`, `days`, `units/month`. Dimensionally invalid operations (e.g. `USD + units`) are rejected at compile time. A general symbolic math system is out of scope.

## 6. Uncertainty

Each value is classified as one of: `known`, `estimated`, `range`, `assumption`, `unknown`. Ranges are preserved through calculation rather than collapsed into a point estimate. No probability distributions are introduced without calibration (Phase 13).

## 7. Scenario changes

Phase 6 UI supports: `set`, `percentage increase`, `percentage decrease`. The engine representation of these is defined in Phase 1.

## 8. Explainability

A result exposes how it occurred, e.g.:

```text
HBM price +30%
│
├── memory cost +30%
├── GPU unit cost +7.4%
├── COGS +5.8%
└── gross margin -2.1pp
```

Each step eventually exposes equation, assumptions, evidence, uncertainty, and model version.

## 9. Invariants (to be enforced by tests in Phase 1)

- Equation cannot reference an unknown variable.
- Unsupported cycles are rejected.
- Unknown values never silently become zero.
- Division by zero is an explicit error.
- Published `ModelVersion` cannot be mutated.
- `ScenarioRun` references exactly one `ModelVersion`.
- Identical model + baseline + scenario produce identical results and identical hashes.

## 10. First model: `AcmeGPU` (synthetic)

Candidate variables: `memory_price`, `memory_cost_per_gpu`, `packaging_cost_per_gpu`, `wafer_cost_per_gpu`, `unit_cost`, `gpu_volume`, `gpu_asp`, `revenue`, `cogs`, `gross_profit`, `gross_margin`, `operating_expenses`, `operating_income`.

AcmeGPU is synthetic test/development data and must be labeled as such wherever it appears.

## 11. Open (Phase 1)

1. Numeric representation: `decimal.Decimal` with a fixed context vs. binary float; rounding rules for display vs. calculation.
2. Unit handling: Pint integration vs. a small closed unit algebra for the supported unit set.
3. Canonical serialization for hashing (key ordering, number formatting, hash algorithm).
4. Representation and arithmetic of `range` values through operators.
5. Semantics of `percentage` vs. `percentage_points` in scenario changes.
6. Whether any cycles are "supported" (e.g. lag-broken) or all cycles are rejected in Phase 1.
7. Whether dependency graphs use NetworkX or a local topological sort (the dependency is listed in the target stack; adoption must still be justified).
