# Test and CI performance — remaining work

**Status:** active optimization track; the first low-risk changes in [PR #1636](https://github.com/JM-Brun/llm-lab/pull/1636) merged on 2026-11-25. Repeated timing and follow-up profiling remain open.  
**Last measured:** 2026-11-25.  
**Scope:** contributor feedback time, Python test runtime, GitHub Actions overhead and the integrity of the validation gates.

This document is the focused execution plan for test/CI latency. It complements, rather than replaces, the broader [scalability and capacity audit](scalability-capacity-audit-2026-11-18.md), which covers the knowledge-management data model and corpus growth.

## 1. Evidence and current baseline

Two GitHub Actions runs on 2026-11-25 provide an initial before/after observation:

| Run | Change | Tests | Result | Test duration | Coverage |
|---|---|---:|---|---:|---:|
| [#45599115842](https://github.com/JM-Brun/llm-lab/actions/runs/45599115842) | Before PR #1636 | 832 + 1 skipped | Pass | 181.45 s | 98.27% |
| [#45600157356](https://github.com/JM-Brun/llm-lab/actions/runs/45600157356) | PR #1636, cached extraction corpus | 832 + 1 skipped | Pass | 93.85 s | 98.27% |

Both runs used **pytest-xdist 3.8.0, two workers and `--dist loadscope`**. Parallel execution was already enabled before this work; it is not the explanation for the observed difference. The wall-clock difference is approximately 48%, but this is a single pair of hosted-runner observations, not yet a controlled performance claim. Repeat measurements before attributing the full gain to any one change.

The test suite and coverage gate were preserved. The run on the PR branch reported 832 passed, one skipped, and 98.27% coverage.

### Slow-test observations

The `--durations=20` output identifies recurring full-repository integration work:

| Test or operation | Before | PR run |
|---|---:|---:|
| Understand-boundaries pilot, FR | 10.24 s | 5.74 s |
| Understand-boundaries pilot, EN | 10.17 s | 5.65 s |
| Cross-graph query CLI | 8.04 s | 4.65 s |
| Revision-coverage inventory, real repository | 7.12 s | 3.76 s |
| Source taxonomy contract | 6.30 s | 3.82 s |
| Extraction-history reconciliation, individual tests | about 6.1–6.65 s each | slowest one 3.64 s |

The extraction-history test module called `_corpus()` independently from several tests. Each call loaded the global source catalogue, concept registry and all extraction YAML files. PR #1636 adds process-local caching for those immutable inputs. The test module only reads the returned structures; if future tests need to mutate them, they must use copies or isolated fixtures rather than mutate shared cached objects.

The other duration changes are useful signals, but should not be treated as proven effects of the extraction cache: hosted-runner variance, worker scheduling and concurrent load can affect individual timings.

### Existing CI architecture — do not duplicate it

- The Python CI already runs formatting, lint, mypy and domain checks in one job, and the complete pytest suite in a parallel job.
- The test job already installs pinned `pytest-xdist==3.8.0` and runs `uv run pytest -n 2 --dist loadscope --durations=20`.
- Domain checks are conditionally run based on changed paths; formatting, lint and type checks remain general checks.
- The Quarto workflow already has incremental-render and published-site-cache paths, plus a daily scheduled audit.
- The Quarto job uses a Playwright container. In PR #1636's docs/tests-only run, container initialization alone took about 23 seconds before the scope detector skipped the render and browser steps.

Do not add one workflow per concept, test file or validator. Keep a small number of coherent workflows and make their jobs/steps conditional where that can be done safely.

## 2. Work remaining — prioritized

### P0 — first optimization delivered; measurement remains open

[PR #1636](https://github.com/JM-Brun/llm-lab/pull/1636) merged on 2026-11-25. It caches the immutable YAML corpus within extraction-history tests and removes the full pytest suite from the pre-commit hook. The full suite and coverage gate remain required. The implementation and review gate are complete; do not keep the PR-validation checklist open.

The cached corpus is read-only by contract. If a future test needs mutation, copy the relevant record at the mutation boundary rather than mutating shared dictionaries or nested lists.

**Remaining measurement:** repeat the full suite several times on comparable runners and report median/range, test count, coverage, worker/scheduling configuration and job setup time. The current two-run comparison is one observation pair, not a controlled estimate of causal improvement.

### P1 — remove repeated expensive setup in repository-level tests

4. **Profile the remaining slow tests.**
   - Start with `test_understand_boundaries_pilot.py`, `test_cross_graph_query.py`, `test_revision_coverage_inventory.py`, `test_source_taxonomy_contract.py` and `test_map_artifacts_freshness.py`.
   - Separate setup time, function-call time, filesystem/YAML reads, page discovery, graph/index construction and subprocess/CLI startup.
   - Use the existing `--durations=20` output as a first signal; add targeted timing only where it identifies a concrete cost.
5. **Reuse immutable project indexes where the same build is repeated.**
   - Inspect repeated `ProjectIndex.build(...)`, page-index loads, registry reads and route preparation across tests.
   - Where the same root and options are used in one test process, consider a session- or module-scoped pytest fixture.
   - Keep different index options (notably evidence-enabled versus default) distinct.
   - Do not share mutable state between tests; test isolation takes precedence over caching.
6. **Avoid rebuilding language-independent inputs in bilingual parameterized tests.**
   - In the Understand-boundaries pilot, identify the common route document, concept registry and published-page index separately from language-specific projections.
   - Load common inputs once per worker/module and keep FR/EN assertions independent.
   - Preserve both language checks; do not collapse bilingual coverage into one representative language.
7. **Keep one real CLI integration check, but test most behavior below the CLI boundary.**
   - For cross-graph query, retain at least one test of argument parsing/output serialization.
   - Exercise query semantics and edge cases directly through the Python API.
   - Avoid repeatedly loading the same repository index merely to test output formatting.
8. **Review generated-artifact freshness tests.**
   - Determine whether bilingual map and route projections can share a single validated input model during one test.
   - Keep independent checks for FR/EN outputs and stale committed artifacts.
   - Do not replace deterministic regeneration checks with snapshots that cannot detect stale source data.

**Exit gate:** each optimization has a before/after measurement, preserves full-repository behavior and bilingual coverage, and does not introduce shared mutable fixtures or brittle mocks.

### P1 — avoid unnecessary GitHub Actions startup

9. **Skip the Playwright container for PRs that cannot affect the site.**
   - Current Quarto job-level container initialization costs about 23 seconds even when its first scope check subsequently skips all rendering and browser work.
   - Evaluate a lightweight, non-container scope job followed by a conditionally-created render/browser job.
   - Preserve full render for shared inputs, configuration changes, page additions/deletions/renames and uncertain scope.
   - Preserve the daily scheduled audit and explicit manual full-audit path.
   - Avoid duplicating the changed-file detection logic in multiple places; extract a single reusable scope script/job contract.
10. **Audit job-level concurrency and cancellation.**
    - Keep cancellation of superseded PR runs.
    - Confirm that pushes to `main`, scheduled audits and manual dispatches cannot cancel a required validation unexpectedly.
    - Keep the Python quality and test jobs parallel; they are already independent.
11. **Measure dependency setup before changing it.**
    - The test workflow installs the project environment, site-test dependencies and pytest-xdist separately.
    - Check cache hit rates and actual install time first.
    - Consider moving CI-only dependencies into a clearly named optional/dependency group only if that improves lockfile reproducibility without burdening ordinary users.
    - Do not disable dependency locking or add broad caches that can conceal stale environments.

**Exit gate:** docs-only and Python-only PRs avoid browser-container startup when safe; site-affecting PRs still receive the same render, link, visual and browser checks.

### P2 — tune test scheduling and developer feedback

12. **Benchmark xdist worker counts and scheduling.**
    - Compare 1, 2 and (if runner CPU/memory allows) 4 workers.
    - Compare `loadscope` with an alternative such as `worksteal` only after measuring worker imbalance.
    - Watch memory, startup overhead and test flakiness; more workers are not automatically faster.
    - Keep the worker count explicit and documented once selected.
13. **Introduce a clear local test ladder.**
    - Document commands for fast unit tests, focused integration tests and the complete suite.
    - Keep the full suite as the CI integration gate.
    - The pre-commit hook should remain limited to fast, relevant checks; do not reintroduce the entire 800+ test suite there.
14. **Make slow-test regressions visible.**
    - Retain `--durations=20`.
    - Consider storing machine-readable timing summaries or a lightweight benchmark artifact only if it can be compared reliably across runs.
    - Alert on material regressions rather than enforcing fragile per-test millisecond thresholds on shared hosted runners.

**Exit gate:** a contributor can choose a fast feedback command without weakening the required PR checks; CI timing changes can be compared over time.

### P3 — revisit only when measurements justify it

15. **Incremental domain validation.**
    - The broader scalability audit already identifies full-corpus YAML and page scans as a future cost.
    - First measure the validators individually and map their input dependencies.
    - Then add changed-file/affected-neighborhood validation as an additional fast path, retaining a full-corpus integrity gate.
16. **Persistent build caches or generated indexes.**
    - Consider only if repeated in-process reuse and job-level caching are insufficient.
    - Define cache keys, invalidation, determinism and stale-cache failure behavior before implementation.
    - Do not introduce a database, graph server or a second canonical registry to solve a measured test-runtime issue.
17. **Coverage overhead.**
    - Measure coverage instrumentation separately.
    - Do not remove coverage from required CI or lower the threshold to improve a timing number.
    - A local fast command may omit coverage; the required full CI run must retain it.

## 3. Measurement protocol

For every proposed optimization:

1. Use the same commit except for the isolated change, the same Python version, dependency lock, runner class and worker configuration.
2. Run at least three comparable measurements where practical; report median and range.
3. Record:
   - number of collected/passed/skipped tests;
   - coverage percentage and threshold;
   - pytest wall time and slowest 20 tests;
   - job wall time and setup/install time;
   - worker count and distribution strategy;
   - whether the run was warm/cold with respect to dependency and site caches.
4. Compare correctness gates as well as speed. A faster run that skipped relevant checks is not an improvement.
5. Keep the complete test suite and full-corpus validators as the correctness reference.

Do not set a hard numeric runtime target until the repeated baseline is available. The first objective is to make the feedback loop measurably faster without losing diagnostic quality or repository-wide guarantees.

## 4. Current implementation and decisions

| Item | State |
|---|---|
| Cache immutable YAML corpus in extraction-history tests | Merged in [PR #1636](https://github.com/JM-Brun/llm-lab/pull/1636) on 2026-11-25 |
| Remove full pytest suite from pre-commit | Merged in [PR #1636](https://github.com/JM-Brun/llm-lab/pull/1636) on 2026-11-25 |
| pytest-xdist with two workers | Already present before this work; do not count as a new optimization |
| Full pytest suite and 90% coverage threshold | Retained |
| Quarto incremental rendering/site cache | Already present; optimize only the unnecessary container startup |
| Repeated measurements and slow-test profile | Remaining |
| Shared project-index/page fixtures | Candidate; profile before implementation |
| Conditional Quarto job startup | Candidate; preserve scheduled/manual audits |
| Worker/scheduling benchmark | Remaining |

## 5. Relationship to other project documents

- [Scalability and capacity audit](scalability-capacity-audit-2026-11-18.md): corpus growth, YAML parsing, validators and generated projections.
- [Source lineage architecture](source-lineage-architecture.md): future distributed source records and migration gates.
- [Experiment protocol](experiment-protocol.md): reproducibility and reporting principles.
- [Roadmap](roadmap.md): wider learning and project priorities.

This document owns the focused test/CI latency backlog; it does not authorize weakening any scientific, editorial, provenance or full-corpus validation rule.
