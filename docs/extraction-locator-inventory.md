# Extraction locator inventory

The source validator currently checks that an extraction locator has a type and value, but does not validate a grammar for each locator type. Before introducing type-specific hard errors, inventory the actual corpus.

## Run

```bash
uv run --no-project --with-requirements docs/requirements-history-validation.txt \
  --python 3.12 python site/tools/report_extraction_locator_inventory.py
```

Optionally save the deterministic JSON report:

```bash
uv run --no-project --with-requirements docs/requirements-history-validation.txt \
  --python 3.12 python site/tools/report_extraction_locator_inventory.py \
  --output reports/source-audits/extraction-locator-inventory.json
```

## GitHub Actions execution

The CI workflow exposes the full-corpus report as an opt-in job:
- From **Actions → CI → Run workflow**, set `run_locator_inventory=true`.
- A pull request whose title contains `[inventory]` also opts in and checks out that PR's head commit.

The job runs the command above against every `data/extractions/*.yml` file, prints a compact report to the job summary, and uploads a 90-day artifact containing the raw JSON plus separate execution metadata (exact SHA, run/attempt, command, timestamps, duration, Python/PyYAML/uv versions, platform and runner architecture). It does not add a new required-CI gate for locator shapes: only YAML or record-structure errors make the report command fail; scalar and unsupported locator shapes remain observational categories.

## What it reports

- Number of extraction files and items visited.
- Non-mapping extraction records, items with no locator, scalar-text locators, and unsupported locator shapes, separately.
- Coarse shape buckets and up to three record paths for unsupported non-mapping locator values.
- The legacy `items_without_locator_mapping` total (the sum of the preceding three categories); this is not a missing-evidence count.
- Mapping locators with missing/invalid required fields.
- Observed mapping locator type distribution, key-set shapes, and coarse value-shape buckets per type.
- Coarse value-shape buckets and up to three record paths for scalar locators.
- Up to three record paths per mapping type/shape for targeted human inspection.

Non-mapping extraction records are not counted as items with missing locators. The report deliberately does not print locator values, fetch URLs, resolve citations, infer that a source was inspected, or declare a grammar valid. Scalar text locators are preserved as an observed representation and are not automatically treated as invalid. Shape buckets are heuristics for triage, not semantic validation.

## Full-corpus baseline — 2026-11-18

The first official YAML-parsed inventory completed on GitHub Actions run `44322275805`, measured commit `452b30e9d14dcf0f9c5723ff91318b51a564b9af`.

| Measure | Result |
|---|---:|
| Extraction YAML files | 84 |
| Extraction items | 432 |
| Items without locator | 0 |
| Scalar `items[].locator` values | 0 |
| Unsupported locator shapes | 0 |
| Non-mapping extraction records | 0 |
| Mappings with missing/invalid required fields | 0 |
| YAML or record-structure errors | 0 |
| Locator key sets `type,value` | 71 |
| Locator key sets `label,type,value` | 361 |

All 432 extraction items have a mapping locator with a non-empty `type` and a non-empty `value` according to the current inventory checks. No locator values were printed in the report.

### Observed locator types

| Type | Count | Observed value forms |
|---|---:|---|
| `section` | 354 | 281 opaque text, 34 section-like, 25 line-reference-like, 14 page-number-like |
| `page` | 18 | 18 HTTP(S) URLs |
| `timestamp` | 14 | 14 opaque text under the current heuristic; examples are time ranges such as `05:41–10:22` |
| `chapter` | 11 | 8 opaque text, 3 timestamp-like |
| `page-section` | 7 | 7 opaque text |
| `heading` | 7 | 7 opaque text |
| `figure` | 4 | 4 opaque text |
| `paragraph` | 4 | 4 opaque text |
| `article` | 3 | 3 opaque text |
| `comment` | 3 | 3 opaque text |
| `abstract` | 2 | 2 opaque text |
| `code` | 2 | 2 opaque text |
| `external-source` | 2 | 2 opaque text |
| `external-code` | 1 | 1 opaque text |

The scalar-locator count of zero applies specifically to `items[].locator`. Historical descriptive strings in other fields, such as `pedagogical_model.source_graph.nodes[].locator`, are a separate contract and are not part of this inventory.

**Heuristic limitation found:** timestamp ranges with en dashes or hyphens are currently classified as `opaque-text` because the shape detector recognizes single timestamps but not ranges. Representative examples were inspected in `3blue1brown-cross-entropy-compression-intelligence-part-2-2026.yml` and the Karpathy chapter locators. This is a reporting-classification gap, not a malformed locator; a follow-up should extend the heuristic and add regression tests without changing validation policy.

### Reproducibility

- CPython 3.12.16, PyYAML 6.0.3, uv 0.13.7.
- GitHub-hosted Linux x64 runner: `Linux-7.0.0-1019-azure-x86_64-with-glibc2.43`.
- Exact command, commit SHA, workflow run/attempt, timestamps and duration are stored in `reports/source-audits/extraction-locator-inventory-2026-11-18.metadata.json`.
- Raw report: `reports/source-audits/extraction-locator-inventory-2026-11-18.json`.
- Inventory command duration: 4 seconds.
- Artifact archive SHA-256: `6ab381ad7fdceedd3f2ea25c75e5bcf7af70e3e37596b146b88b669767795e58` (90-day GitHub Actions copy).

This baseline establishes the observed corpus shape, not locator resolution, source inspection, claim support, independent corroboration or type-specific semantic validity.

## Next steps

1. Run against the complete checked-out corpus and retain the dated JSON artifact when useful.
2. Inspect representative examples for each locator type and scalar form; identify collisions (one type used for multiple incompatible forms).
3. Define a grammar only for types with stable, unambiguous usage; keep unknown/custom types report-only until classified.
4. Add type-specific unit fixtures, including legacy and partial records, before promoting malformed values to CI errors.
5. Keep locator syntax validation separate from source availability, claim support, and independent corroboration.
