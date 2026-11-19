# Extraction destination and field inventory

This is a read-only compatibility report for the historical extraction corpus. It complements, but does not replace, `report_source_coverage.py` and `check_source_catalogue.py`.

## Run

```bash
uv run --no-project --with-requirements docs/requirements-history-validation.txt \
  --python 3.12 python site/tools/report_extraction_destination_inventory.py
```

For machine-readable output:

```bash
uv run --no-project --with-requirements docs/requirements-history-validation.txt \
  --python 3.12 python site/tools/report_extraction_destination_inventory.py \
  --format json --output extraction-destination-inventory.json
```

The opt-in `[inventory]` CI job runs the report against the complete extraction corpus and uploads its JSON alongside the locator inventory.

## Baseline — 2026-11-19

Measured against the repository data snapshot used by PR #1369:

| Measure | Count |
|---|---:|
| Sources | 139 |
| Extraction files | 96 |
| Atomic extraction items | 489 |
| Items with `candidate_destinations` | 385 |
| Unknown extraction source IDs | 0 |
| Filename / `source_id` mismatches | 0 |
| Malformed records or items | 0 |
| Source-local teaching-route steps | 294 |

### Extraction-record field presence

| Field | Extraction records |
|---|---:|
| `schema_version`, `source_id`, `items` | 96 each |
| `pedagogical_model` | 59 |
| `scan` | 36 |
| `canonical_mapping` | 28 |
| `integration_decision` | 1 |
| `pedagogical_limits` | 1 |
| `pedagogical_strengths` | 1 |
| `supplementary_audit` | 1 |

The top-level `scan` field is present in 36 historical extraction records even though the authoring guide says scan history is source-owned and new extraction-level scan blocks should not be created. Preserve and report this legacy presence; do not infer that it is authoritative or promote its absence/presence to a new validation rule without inspecting the 36 records. `canonical_mapping` is an optional editorial proposal field, not a second canonical source of links.

### Item-field presence

| Field | Items |
|---|---:|
| `evidence`, `id`, `kind`, `locator`, `summary` | 489 each |
| `disposition` | 460 |
| `disposition_rationale` | 341 |
| `classification` | 373 |
| `candidate_destinations` | 385 |
| `pedagogical_assessment` | 116 |
| `technical_assessment` | 132 |
| `pedagogical_profile` | 42 |
| `mapped_concepts` | 39 |
| `target_resources` | 39 |
| `verification` | 7 |
| `provenance` | 3 |

The report also retains a complete field-presence map, including fields not listed in this summary. Absence is not itself a validation failure.

### Destination and relation counts

| Owner / field | Records with field | References | Unique IDs |
|---|---:|---:|---:|
| Source `related.pages` | 139 | 622 | 106 |
| Source `related.concepts` | 139 | 464 | 84 |
| Source `classification.concept_ids` | 139 | 454 | 82 |
| Item `candidate_destinations.pages` | 385 | 840 | 96 |
| Item `candidate_destinations.concepts` | 325 | 374 | 64 |
| Item `candidate_destinations.route_ids` | 143 | 0 | 0 |
| Item `classification.concept_ids` | 342 | 582 | 69 |
| Legacy item `mapped_concepts` | 39 | 105 | 26 |
| Legacy item `target_resources` | 39 | 100 | 22 |
| Pedagogical-model `comparison.canonical_routes` | 51 | 142 | 37 |

No explicit non-empty canonical route-ID destination is recorded. The `candidate_destinations.route_ids` key is present on 143 items, but all 143 lists are empty; `candidate_destinations.routes` and `target_routes` are absent. The 294 `pedagogical_model.teaching_route` steps are source-local instructional sequences, not canonical destination routes.

A separate `pedagogical_model.comparison.canonical_routes` field occurs in 51 instructional source models (142 entries, 37 distinct strings). Its values mix route labels, prose descriptions, page-metadata references and file paths such as `data/guided-route.yml` and `docs/learning-path.md`. These are useful review annotations, but they are not a normalized route-ID vocabulary and must not be counted as 142 integrated route links.

The legacy `target_resources` field contains bilingual page-like IDs (for example, `fr/...` and `en/...`). It is counted separately rather than silently renamed or merged with `candidate_destinations.pages`; its name should not be confused with the stable non-page resource IDs in `data/resources.yml`.

### Compatibility findings

- All 96 extraction records resolve to a known source; filenames match their declared `source_id`.
- Source-level `related.pages`, `related.concepts`, and source/item classification concept references contain no unresolved IDs in this snapshot.
- Candidate page destinations are distinct from already-recorded source page associations. Candidate destinations remain proposals, even when their page IDs resolve.
- Three candidate concept IDs are not present in the canonical concept registry: `context-window`, `log-probability`, and `weighted-aggregation`. They are report-only exceptions, not validator errors:
  - `context-window`: `hesam-sheikh-llm-study-roadmap-2024:hallucination-causality-qualification` (clarify).
  - `log-probability`: `marek-ryabinin-score-centering-off-policy-rl-2026:topk-and-compute` (integrate-by-reference).
  - `weighted-aggregation`: `codefinity-qkv-building-blocks:quiz-pooling`, `codefinity-qkv-building-blocks:quiz-context` (integrate-by-reference), and `mbrenndoerfer-qkv-attention-mechanism:convex-hull` (integrate).
  Review each proposal before mapping it to an existing concept, creating a concept through the normal review process, or removing the proposal.
- No explicit route destination field is used. Do not interpret source-local teaching sequences or the legacy `target_resources` field as proof of a canonical route integration.

## Interpretation rules

1. `related.pages` and `related.concepts` are source-owned associations.
2. `classification.concept_ids` are classifications, not destination proposals.
3. `candidate_destinations` records editorial proposals, not completed integration.
4. `mapped_concepts` and `target_resources` are retained as separate historical fields pending an explicit migration decision.
5. `pedagogical_model.teaching_route` is local to the source's instructional reconstruction.
6. Missing optional fields and unknown proposal IDs are diagnostics; this report does not change validator severity.
7. A resolvable ID does not prove that the source supports the destination or that the proposed integration is pedagogically appropriate.

The inventory does not alter source records, extraction records, taxonomy, canonical registries, or validator behavior.
