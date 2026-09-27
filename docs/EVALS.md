# DOMINO Evaluations

Status: **no evaluations exist.** AI extraction begins in Phase 9. This file fixes the methodology requirements in advance so that Phase 9 cannot ship without them.

## Scope

Evaluations cover AI components only: claim extraction, evidence-span location, entity resolution, contradiction detection, and (Phase 14) evidence-vs-thesis classification. The Economic Compiler is verified by deterministic tests, not evals.

## Required before any AI component is used on real documents (Phase 9 exit gate)

1. A **frozen, human-reviewed eval dataset** of source passages with expected claims, versioned in the repository or in object storage with a content hash recorded here.
2. Structured-output schemas; any output failing schema validation counts as a failure, never as an empty success.
3. Recorded provenance for every eval run (`AGENTS.md` §32): provider, model identifier, prompt version, schema version, source hash, timestamp, latency, token usage, output hash, validation result.

## Metrics

| Metric | Definition (finalized in Phase 9) |
|---|---|
| Precision | Correct extracted claims / all extracted claims |
| Coverage | Expected claims extracted / all expected claims |
| Unsupported claim rate | Claims with no supporting evidence span / all extracted claims |
| Evidence-span correctness | Claims whose span actually supports the claim / claims with a span |
| Entity-resolution accuracy | Correctly resolved entity references / all entity references |
| Latency | p50 / p95 per document |
| Cost | Per document and per accepted claim |

## Rules

- Eval datasets are never edited to make a regression pass. A dataset change is a new dataset version with a recorded reason.
- Thresholds are documented here before they gate CI.
- Results are reported per dataset version, prompt version, and model identifier.
- "Predictive accuracy" language is not used for calibration results (Phase 13) unless methodology supports it.

## Eval runs

None.
