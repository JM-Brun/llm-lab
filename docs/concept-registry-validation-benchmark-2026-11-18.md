# Concept-registry validation benchmark

This benchmark is the first executable scale probe from the [scalability and capacity audit](scalability-capacity-audit-2026-11-18.md). It measures the existing concept validator without changing canonical registries or replacing the production validation path.

## Run

From the repository root, with the site-validation dependencies installed:

```bash
uv run --no-project --with-requirements docs/requirements-history-validation.txt \
  --python 3.12 python site/tools/benchmark_concept_registry.py
```

Use `--sizes 500 2000 10000`, `--repeats 5` (also the default), or `--output reports/benchmarks/concept-registry.json` to customize a run. The default sizes mirror the capacity scenarios in the audit. The script writes JSON to stdout and optionally to a file; generated measurements should be committed only when they are intentionally used as a dated baseline.

## Fixture and measurement contract

- Start from the checked-in `data/concepts.yml` registry.
- Add valid bilingual synthetic concepts by cloning the shape of a real record, assigning stable benchmark-only IDs and definitions, and retaining valid domain/resource references.
- Connect added concepts in a single directed acyclic `part-of` chain. This exercises a long acyclic path without introducing an invalid cycle.
- Validate against the real published-page and domain ID sets.
- Measure fixture construction separately from `validate_registry`.
- Report median/min/max validation wall time and maximum `tracemalloc` peak across repetitions.
- Include the Git commit SHA when running in a Git worktree, interpreter/platform details, fixture dimensions, and explicit measurement boundaries.

The timed validation excludes YAML parsing, filesystem traversal, published-page discovery, process startup and Quarto rendering. It therefore isolates the in-memory concept-registry validator; it is not an end-to-end CI benchmark and cannot be compared directly with the source-catalogue validator or site build.

## Interpretation and limits

A successful run proves that the validator accepts the generated workload and provides a local timing/memory observation for that exact machine, interpreter, commit and fixture. It does not prove performance on other runners, browser graph usability, source/extraction scalability, or correctness of arbitrary graph semantics.

Record the commit SHA, machine/runner, Python version, repeat count and raw JSON when establishing a baseline. Compare growth ratios across sizes before setting budgets. Keep this benchmark opt-in initially; do not make noisy wall-clock thresholds a required CI gate until stable runner baselines and acceptable variance are known.

The fixture intentionally models one sparse chain. Follow-up workloads should add high-degree hubs, disconnected components, dense local neighborhoods, mixed relation types, duplicate IDs, dangling endpoints and invalid cycles. Those should be separate named shapes rather than silently changing this baseline.
