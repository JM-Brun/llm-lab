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
| Item `classification.concept_ids` | 342 | 582 | 69 |
| Legacy item `mapped_concepts` | 39 | 105 | 26 |
| Legacy item `target_resources` | 39 | 100 | 22 |

No explicit canonical `routes`, `target_routes`, or `candidate_destinations.routes` fields occur in this snapshot. The 294 `pedagogical_model.teaching_route` steps are source-local instructional sequences, not canonical destination routes.

The legacy `target_resources` field contains bilingual page-like IDs (for example, `fr/...` and `en/...`). It is counted separately rather than silently renamed or merged with `candidate_destinations.pages`.

### Compatibility findings

- All 96 extraction records resolve to a known source; filenames match their declared `source_id`.
- Source-level `related.pages`, `related.concepts`, and source/item classification concept references contain no unresolved IDs in this snapshot.
- Candidate page destinations are distinct from already-recorded source page associations. Candidate destinations remain proposals, even when their page IDs resolve.
- Three candidate concept IDs are not present in the canonical concept registry: `context-window`, `log-probability`, and `weighted-aggregation`. They are report-only exceptions, not validator errors. Review their exact item occurrences before deciding whether to map them to existing concepts, create concepts through the normal review process, or remove the proposals.
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
