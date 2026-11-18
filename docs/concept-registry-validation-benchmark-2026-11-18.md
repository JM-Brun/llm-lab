# Concept-registry validation benchmark

This benchmark is the first executable scale probe from the [scalability and capacity audit](scalability-capacity-audit-2026-11-18.md). It measures the existing concept validator without changing canonical registries or replacing the production validation path.

## Run

From the repository root, with the site-validation dependencies installed:

```bash
uv run --no-project --with-requirements docs/requirements-history-validation.txt \
  --python 3.12 python site/tools/benchmark_concept_registry.py
```

Use `--sizes 500 2000 10000`, `--repeats 5` (also the default), or `--output reports/benchmarks/concept-registry.json` to customize a run. The default sizes mirror the capacity scenarios in the audit. The script writes JSON to stdout and optionally to a file; generated measurements should be committed only when they are intentionally used as a dated baseline.

## GitHub Actions execution

The CI workflow exposes this benchmark as an opt-in job:
- From **Actions → CI → Run workflow**, set `run_concept_benchmark=true` to run it on the selected branch.
- A pull request whose title contains `[benchmark]` also opts in, and the job checks out that PR's head commit rather than the synthetic merge commit.

The job runs the documented 500 / 2,000 / 10,000 sizes with five repetitions. It publishes a job-summary table and a 90-day artifact containing the raw JSON and a separate execution-metadata JSON (checked-out SHA, workflow run/attempt, command, timestamps, duration, Python/PyYAML/uv versions, platform and runner architecture). No timing threshold is added to required CI.

## Fixture and measurement contract

- Start from the checked-in `data/concepts.yml` registry.
- Add valid bilingual synthetic concepts by cloning the shape of a real record, assigning stable benchmark-only IDs and definitions, and retaining valid domain/resource references.
- Connect added concepts in a single directed acyclic `part-of` chain. This exercises a long acyclic path without introducing an invalid cycle.
- Validate against the real published-page and domain ID sets.
- Measure fixture construction separately from `validate_registry`.
- Report median/min/max validation wall time and maximum `tracemalloc` peak across repetitions.
- Include the Git commit SHA when running in a Git worktree, interpreter/platform details, fixture dimensions, and explicit measurement boundaries.

The timed validation excludes YAML parsing, filesystem traversal, published-page discovery, process startup and Quarto rendering. It therefore isolates the in-memory concept-registry validator; it is not an end-to-end CI benchmark and cannot be compared directly with the source-catalogue validator or site build.

## First measured baseline — 2026-11-18

The first opt-in GitHub Actions run completed five repetitions at each size with zero validation errors.

| Concepts | Relations | Fixture build median | Validation median | Validation min–max | Peak validation memory |
|---:|---:|---:|---:|---:|---:|
| 500 | 522 | 0.004077 s | 0.049707 s | 0.049647–0.053422 s | 228,750 bytes |
| 2,000 | 2,022 | 0.015280 s | 0.206559 s | 0.205567–0.215764 s | 999,982 bytes |
| 10,000 | 10,022 | 0.083452 s | 1.083805 s | 1.076992–1.088022 s | 5,199,430 bytes |

The measured validation time grows by about 4.16× when the workload grows 4× (500 → 2,000), and by about 5.25× when it grows 5× (2,000 → 10,000). Peak memory grows by about 4.37× and 5.20× respectively. This is consistent with approximately linear scaling for this particular sparse chain; it is not evidence about other graph topologies or the full application pipeline.

**Run identity and environment**
- Measured commit: `38d0e69507525beb4c2679f206b4f03a9ba6988b`
- GitHub Actions run: `44321178540`, attempt 1; started 2026-11-18 14:09:34 UTC; benchmark command duration 9 seconds.
- Runner: GitHub-hosted Linux x64, `Linux-7.0.0-1019-azure-x86_64-with-glibc2.43`.
- CPython 3.12.16, PyYAML 6.0.3, uv 0.13.7.
- Repetitions: 5; all 15 validation calls returned zero errors.

The exact raw output and execution metadata are committed separately:
- `reports/benchmarks/concept-registry-validation-2026-11-18.json`
- `reports/benchmarks/concept-registry-validation-2026-11-18.metadata.json`
- `reports/benchmarks/concept-registry-validation-2026-11-18-run-2.json`
- `reports/benchmarks/concept-registry-validation-2026-11-18-run-2.metadata.json`

These files preserve the benchmark dimensions, baseline registry size (102 concepts / 125 relations), synthetic chain definition, timed/memory scopes, exact command, commit SHA and environment. The CI artifacts are retained for 90 days as additional copies.

### Second independent execution

A second run on the same hosted-runner image completed five repetitions at each size with zero validation errors:

| Concepts | Fixture build median | Validation median | Validation min–max | Peak validation memory |
|---:|---:|---:|---:|---:|
| 500 | 0.005927 s | 0.064100 s | 0.063751–0.093089 s | 228,750 bytes |
| 2,000 | 0.024934 s | 0.263519 s | 0.258465–0.309845 s | 999,982 bytes |
| 10,000 | 0.113342 s | 1.355029 s | 1.348475–1.363246 s | 5,199,430 bytes |

Run 2 used commit `aa62fe79411e157487a5ff2cbb9e8b1fb460bc87`, Actions run `44321450442`, started 2026-11-18 14:11:14 UTC and completed in 11 seconds. Python, PyYAML, uv and platform versions matched run 1.

Validation medians were 25–29% slower in run 2, while the measured peak memory was identical at all three sizes. The 500-concept run also had one noticeably slower repetition. This is evidence of timing noise between hosted-runner executions, not a change in algorithmic scaling. Both runs retain approximately linear growth across the tested chain sizes. Two runs are not enough to set a stable time budget; collect more comparable runs before introducing thresholds.

## Interpretation and limits

A successful run proves that the validator accepts the generated workload and provides a local timing/memory observation for that exact machine, interpreter, commit and fixture. It does not prove performance on other runners, browser graph usability, source/extraction scalability, or correctness of arbitrary graph semantics.

Record the commit SHA, machine/runner, Python version, repeat count and raw JSON when establishing a baseline. Compare growth ratios across sizes before setting budgets. Keep this benchmark opt-in initially; do not make noisy wall-clock thresholds a required CI gate until stable runner baselines and acceptable variance are known.

The fixture intentionally models one sparse chain. Follow-up workloads should add high-degree hubs, disconnected components, dense local neighborhoods, mixed relation types, duplicate IDs, dangling endpoints and invalid cycles. Those should be separate named shapes rather than silently changing this baseline.
