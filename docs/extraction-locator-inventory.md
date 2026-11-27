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
| `timestamp` | 14 | 14 timestamp-like values after range-aware classification |
| `chapter` | 11 | 11 timestamp-like values (single times and ranges) |
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

**Heuristic correction:** the first report classified timestamp ranges with en dashes or hyphens as `opaque-text`. The classifier is now range-aware and recognizes single timestamps, hyphen/en-dash/em-dash ranges, multiple ranges joined by `and`/`or`, and an optional `onward` suffix. Regression tests cover `05:41–10:22`, `00:01:00-03:21:46`, `00:00–03:02 and 12:59–14:55`, and `1:28:42–1:49:58 onward`. This changes only the report's descriptive bucket, not validation policy.

### Preliminary type contract matrix

The corpus supports a structural contract, but not one universal value grammar. The following matrix records the observed forms and the conservative rule for now.

| Type | Count | Representative historical value | Provisional interpretation / validation policy |
|---|---:|---|---|
| `section` | 354 | `§2.1–2.2 and §3.2, pp. 9905–9906`; `Definition, lines 19–24` | Broad textual anchor: headings, section numbers, page ranges and line references. Preserve opaque text; do not impose one grammar. |
| `page` | 18 | `https://huggingface.co/learn/llm-course/` | URL locator; all observed values are HTTP(S). Keep URL-shape monitoring report-only until compatibility is established. |
| `timestamp` | 14 | `05:41–10:22`; `00:00–03:02 and 12:59–14:55` | Video time range, possibly multiple segments or a trailing `onward` note; range-aware shape classification is covered by regression tests. |
| `chapter` | 11 | `00:01:00-03:21:46`; `01:20:32` | Video chapter/time anchor; both ranges and single timestamps occur. |
| `page-section` | 7 | `pp. 150–152, especially Eqs. (1)–(5)` | Combined page and section/equation anchor. |
| `heading` | 7 | `AI and Compression` | Descriptive heading text. |
| `figure` | 4 | `Fig. 1 caption`; `After 'Three different vectors…'` | Figure caption or nearby in-body anchor; not always a numbered figure. |
| `paragraph` | 4 | `Post body, paragraphs 2–3` | Paragraph/range anchor in article or post text. |
| `article` | 3 | `From Full to Hybrid Attention in LLMs` | Article title plus optional label for a subtopic. |
| `comment` | 3 | `Visible reply by @X_differentials on the mirrored post` | Comment/reply anchor; canonical source identity remains elsewhere in the source/evidence metadata. |
| `abstract` | 2 | `Benchmark description` | Abstract subheading/topic anchor. |
| `code` | 2 | `PositionalEncoding.__init__ and PositionalEncoding.forward` | Symbol/function anchor. |
| `external-source` | 2 | `Dao et al. 2022, abstract and IO analysis` | Descriptive pointer to an external source; the value need not itself be a URL. Canonical source identity must be resolved through source/evidence metadata. |
| `external-code` | 1 | `rasbt/LLMs-from-scratch/...ipynb; code cells 10, 11, 13 and 15` | Repository path and code-cell anchor. |

Common fields:
- `type`: required non-empty string under the current validator.
- `value`: required non-empty string under the observed corpus; the validator currently checks truthiness, not the Python type or a type-specific grammar.
- `label`: optional descriptive disambiguator. Present on 361/432 locators; absent on 71/432. Do not make it mandatory.
- Additional keys are not currently governed by a closed schema.

**Compatibility rule:** keep the mapping shape and required non-empty `type`/`value` as the structural contract. Treat unknown types, opaque text, mixed page/section anchors and additional keys as report-only until their semantics are reviewed. Do not promote locator presence into proof of source inspection or claim support.

### Reproducibility

Two raw snapshots are retained:
- Initial classifier output: `reports/source-audits/extraction-locator-inventory-2026-11-18.json` and `reports/source-audits/extraction-locator-inventory-2026-11-18.metadata.json`.
- Range-aware corrected output: `reports/source-audits/extraction-locator-inventory-2026-11-18-v2.json` and `reports/source-audits/extraction-locator-inventory-2026-11-18-v2.metadata.json`.

The corrected run used commit `a765ac6f5e0f8006831c1f870ae37454c15b1b63`, Actions run `44323092996`, attempt 1. It completed in 2 seconds on GitHub-hosted Linux x64 (`Linux-7.0.0-1016-aws-x86_64-with-glibc2.43`), CPython 3.12.16, PyYAML 6.0.3 and uv 0.13.7. The exact command, timestamps and all execution metadata are in the JSON metadata file. Artifact archive SHA-256: `005b8e406e5ee13b25d9a5259c9cd61a845c284d1f7b384ca3732d06c55f8ef7` (90-day GitHub Actions copy).

The two snapshots have identical structural counts (84 files, 432 items, zero malformed/missing/scalar/unsupported records). The corrected snapshot changes only the heuristic shape classification: all 14 timestamp locators and all 11 chapter locators are now timestamp-like.

This baseline establishes the observed corpus shape, not locator resolution, source inspection, claim support, independent corroboration or type-specific semantic validity.

## Next steps

1. Repeat the inventory after meaningful extraction-corpus changes and retain dated JSON plus execution metadata.
2. Continue type-specific semantic review, especially the broad `section` category and the descriptive `external-source`/`external-code` anchors.
3. Define a grammar only for types with stable, unambiguous usage; keep unknown/custom types report-only until classified.
4. Add compatibility fixtures before promoting malformed values to CI errors.
5. Keep locator syntax validation separate from source availability, claim support, and independent corroboration.


## Revalidation requested — 2026-11-19

The 2026-11-18 snapshot above (84 extraction files / 432 items) is historical and must not be presented as the current corpus state. A repository-tree inventory on 2026-11-19 found 96 extraction YAML filenames. That filename count does not establish the number of valid extraction records, items, or locators, and it does not establish that each declared `source_id` resolves.

A fresh full-corpus run of `site/tools/report_extraction_locator_inventory.py` is being requested through the opt-in CI inventory job. Its artifact and job summary—not this filename-level count—must supply the next current locator baseline. In parallel, the canonical `site/tools/check_source_catalogue.py` validation in CI must pass before claiming the 96-file corpus is structurally valid. Until those results are available, no current item or locator totals are asserted here.


### Verified current snapshot — 2026-11-19

The opt-in GitHub Actions inventory completed successfully on commit `0c856b92ebee9a069d405596c2e2d469aaf8d703` (workflow run `44531296011`). It parsed **96 files / 489 items** and reported:

- 0 YAML/record errors;
- 0 items without a locator, scalar locators, unsupported locator shapes, or non-mapping extraction records;
- 0 locator mappings missing required fields;
- 14 observed locator types: section 411, page 18, timestamp 14, chapter 11, heading 7, page-section 7, figure 4, paragraph 4, article 3, comment 3, abstract 2, code 2, external-source 2, external-code 1;
- 418 locator mappings with keys `label,type,value`; 71 with `type,value`.

The same workflow's canonical `site/tools/check_source_catalogue.py` step passed. That validator checks extraction source identity resolution, filename/source_id equality and duplicate extraction identities in addition to item structure. These results establish structural validity for this snapshot, not external locator resolution, source inspection completeness, evidential support, scientific correctness or independent corroboration. The earlier 84-file / 432-item snapshot is retained above as historical evidence.


## Current corpus revalidation — 2026-11-27

The 2026-11-19 baseline (96 extraction files / 489 items) is historical. The current-main catalogue and extraction-directory snapshot recorded in #1211 reports **177 source records and 137 extraction YAML files**. These raw counts do not establish valid extraction identities, item totals, locator quality, or destination/reference integrity.

A new full-corpus run is requested through the existing opt-in CI job. The run must capture:
- locator shape and required-field inventory;
- extraction destination and field inventory;
- exact commit SHA, workflow run/attempt, command, timestamp, runtime and platform metadata.

Do not turn this observational inventory into a new hard validation gate. Do not infer locator resolution, source inspection, claim support or scientific validity from the presence of a locator. The 2026-11-19 report remains historical until the new artifact is inspected.


### Verified current snapshot — 2026-11-27

The opt-in inventory completed successfully on commit `d9281aae7ebe5ad86cf97f10d2038d3f1e15de6a`, Actions run [`46071071663`](https://github.com/JM-Brun/llm-lab/actions/runs/46071071663), attempt 1. The raw artifact is `extraction-locator-inventory-d9281aae7ebe5ad86cf97f10d2038d3f1e15de6a` (90-day retention; archive SHA-256 `5b17fad9f0d3ca801d0e80289ba5556f30c6cbd33c21bbfb0f4adc977f491503`). The run took 3 seconds on Linux x64, CPython 3.12.16, PyYAML 6.0.3 and uv 0.13.7.

**Corrected corpus grain:** `data/extractions/` contains 136 `.yml` extraction records plus `README.md` (137 directory entries), not 137 extraction YAML files.

| Measure | Current value | Interpretation |
|---|---:|---|
| Source records | 177 | Canonical source catalogue records |
| Extraction files | 136 | One extraction record per file |
| Extraction items | 639 | All have mapping-shaped locators |
| Sources without extraction | 41 | Review/disposition queue, not automatically an error |
| Integrated sources without extraction | 18 | Must retain an explicit audit rationale; do not create empty extraction files |
| Sources without extraction with audit record | 41 | All 41 are represented in the source-coverage audit |
| Sources without extraction without audit record | 0 | No uncovered filename gap in this snapshot |
| Unknown extraction source IDs / filename mismatches | 0 / 0 | All extraction identities resolve structurally |
| Malformed records or items | 0 | Source-coverage validator passed |

**Locator-shape inventory:** 639 items; 0 without locators, scalar locators, unsupported locator shapes, malformed extraction records, missing required locator fields or YAML/record errors. The corpus has 17 observed locator types. Counts include `section` 540, `page` 28, `chapter` 11, `page-section` 8, `heading` 7, `figure` 6, `file` 5, `paragraph` 4, `article` 3, `comment` 3, `abstract` 2, `code` 2, `external-source` 2, `table` 2, `timestamp` 14, and the single-count types `code-symbol` and `external-code` (the complete exact distribution is in the artifact).

The dominant `section` type is semantically heterogeneous: 454 opaque text values, 45 section-like values, 25 line-reference-like values and 16 page-number-like values. The `page` type also mixes 18 HTTP URLs and 10 page-number-like values. This is the highest-value next semantic review; it is **not** a structural failure and does not justify a type-specific validator yet. Locator mappings contain `label,type,value` in 531 cases and `type,value` in 108 cases; `label` remains optional.

**Destination and field inventory:**
- `candidate_destinations.pages`: 521 records, 1,114 references, 104 unique page IDs, 0 invalid entries.
- `candidate_destinations.concepts`: 451 records, 505 references, 79 unique concept IDs, 0 invalid entries.
- `classification.concept_ids`: 475 records, 924 references, 94 unique concept IDs, 0 invalid entries.
- `source.related.pages`: 177 records, 750 references, 114 unique page IDs, 0 invalid entries.
- `source.related.concepts`: 176 records, 688 references; no unknown concept references.
- `mapped_concepts`: 46 records, 118 references, 26 unique values.
- `target_resources`: 46 records, 126 references, 26 unique values.
- Source-local pedagogical models contain 372 teaching-route steps; these are source-local reconstructions, not canonical learning-route memberships.
- `candidate_destinations.route_ids` is present in 198 mappings but contributes zero references. Treat this as an observed empty field, not a defect, until its intended contract is decided.

The destination inventory reports field presence, not field requiredness. For example, `classification`, `disposition_rationale`, `technical_assessment`, `pedagogical_assessment`, `mapped_concepts` and `target_resources` are not present on every item. Do not call these missing-data defects without checking item-kind and schema-version contracts. Likewise, `candidate_destinations` are editorial proposals, `mapped_concepts` and `target_resources` are legacy/authoring fields, and source-local teaching routes are not canonical route declarations.

The same CI run validated **6 domains, 125 concepts and 147 relations**. This establishes structural/reference integrity under current validators, not external locator resolution, source inspection completeness, claim support, scientific correctness or independent corroboration.

**Next actions:** review the 41 no-extraction audit decisions (especially the 18 integrated sources); inspect the semantic use of `section` and `page` before defining any grammar; keep the observed empty `route_ids` field report-only; do not add empty extraction files or promote locator presence into evidence of source inspection.


#### Cross-check against the canonical source-coverage report

The same CI run's `report_source_coverage.py` output adds context that the locator-shape report alone cannot provide:

| Measure | Count |
|---|---:|
| Canonical concepts | 125 |
| Sources without a concept link | 7 |
| Sources without a page destination | 8 |
| Concepts without a source | 12 |
| Concepts with exactly one source | 26 |
| Publication dates unknown | 47 |
| Licence status unknown | 155 |
| Extraction source references unknown | 0 |
| Concept references unknown | 0 |
| Scan-history/status mismatches | 0 |

Source status distribution: scan `discovered=1`, `inaccessible=2`, `partially-scanned=171`, `scanned=3`; integration `deferred=10`, `integrated=54`, `not-reviewed=2`, `partially-integrated=79`, `rejected=1`, `reviewed=31`. These are canonical metadata counts, not a judgment that 171 sources need full rescanning. Do not promote scan status without component-level evidence.

The 41 sources without extraction have this integration-status distribution: `integrated=18`, `reviewed=6`, `deferred=8`, `partially-integrated=7`, `not-reviewed=2`. Each has at least one `related.audit_records` reference (1–4 per source). This proves an audit reference exists, not that the rationale is complete or current. Prioritize the two `not-reviewed` sources and seven `partially-integrated` sources for a targeted decision check; retain the 18 integrated cases only when their no-extraction rationale is explicit.

Collection coverage in the same report is **69 explicit decisions**, **14 explicitly unassigned**, **108 without a decision**, and **55 total memberships**. This is included only as a cross-report diagnostic; collection identity and membership decisions remain exclusively owned by #1306. Do not reconcile or copy those decisions in this issue.

The 7 source/concept-link gaps, 8 page-destination gaps, 12 concepts without sources and 26 single-source concepts are graph-coverage review queues, not locator-shape errors. Coordinate their semantics with #416/#512; do not silently create links to improve counts. The 47 unknown publication dates and 155 unknown licence statuses remain unknown unless publisher/author/repository evidence supports a value.
