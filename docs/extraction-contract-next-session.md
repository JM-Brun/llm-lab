# Extraction contract audit — session handoff

**Last updated:** 2026-11-19  
**Repository:** `JM-Brun/llm-lab`  
**Working branch:** `audit/extraction-destination-inventory`  
**Pull request:** [#1369 — Add extraction destination and field inventory](https://github.com/JM-Brun/llm-lab/pull/1369)  
**Recorded PR head before this handoff commit:** `4facb34d2db3705775849f1bddb568c13891b1d2`

This document is the continuation point for future sessions. It distinguishes completed work, measured facts, pending verification and safe next actions.

## 1. Executive status

- The technical decision recorded for #1365 remains: its three controls were accepted. The next step is measured compatibility review, not immediate validator tightening.
- PR #1369 is open, non-draft and not merged. It adds a read-only full-corpus inventory, focused tests, opt-in CI reporting and documentation.
- No canonical source, concept, page, resource or route record was changed by this work. No validator rule was changed.
- On the recorded PR head, Python quality/domain checks, the full test suite, the inventory job and secret scanning were reported successful. The Quarto full-site/browser audit was still running at the last observed check. Re-check current checks on the current PR head before relying on this status.
- All counts below are a 2026-11-19 snapshot; rerun the report after any corpus change.

## 2. Work completed

### 2.1 Inventory tooling and tests

Added:
- `site/tools/report_extraction_destination_inventory.py`: read-only inventory of extraction/source correspondence, top-level and item-level field presence, value shapes, nested field presence, destination references, unresolved candidate concepts and route annotations.
- `tests/test_extraction_destination_inventory.py`: focused regression tests for representative shapes, reference accounting and exception cases.

CI:
- Added opt-in `[inventory]` workflow input in `.github/workflows/ci.yml`.
- The inventory job runs against the complete corpus, publishes a Markdown summary and uploads JSON.
- This is an inventory/reporting job, not a new hard validation gate.

Documentation:
- `docs/extraction-destination-inventory.md`: measured baseline, counts, field shapes, exceptions, interpretation and reproducible commands.
- `docs/source-contract-validation-matrix.md`: corpus-backed compatibility evidence and provisional compatibility decisions.
- This handoff: remaining work and session start checklist.

Run locally:

```bash
uv run --no-project --with-requirements docs/requirements-history-validation.txt \
  --python 3.12 python site/tools/report_extraction_destination_inventory.py
```

JSON output:

```bash
uv run --no-project --with-requirements docs/requirements-history-validation.txt \
  --python 3.12 python site/tools/report_extraction_destination_inventory.py \
  --format json --output extraction-destination-inventory.json
```

## 3. Measured corpus baseline (2026-11-19)

| Measure | Count |
|---|---:|
| Source records | 139 |
| Extraction files | 96 |
| Atomic extraction items | 489 |
| Items with `candidate_destinations` | 385 |
| Unknown extraction source IDs | 0 |
| Filename / `source_id` mismatches | 0 |
| Malformed extraction records or items | 0 |
| Source-local `teaching_route` steps | 294 |

### 3.1 Destination and reference counts

| Owner / field | Records with field | References | Unique values |
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

Source/item classification references and legacy `mapped_concepts` resolve in this snapshot. Candidate destinations remain proposals, not evidence of completed integration.

### 3.2 Optional and historical fields

At extraction-record level: `pedagogical_model` occurs in 59 records, `scan` in 36, and `canonical_mapping` in 28. `integration_decision`, `pedagogical_limits`, `pedagogical_strengths` and `supplementary_audit` each occur once.

- All 36 historical extraction-level `scan` values are mappings with ten nested keys. Authoring guidance says scan history is source-owned; preserve and report legacy extraction-level blocks during compatibility review. Do not confuse them with source `scan_history`.
- All 28 `canonical_mapping` values are mappings. Their nested fields are editorial proposals, not a second canonical registry or proof of integration.
- All 59 `pedagogical_model` values are mappings. Each contains `reconstruction`, `source_graph`, `learning_outcomes`, `assumed_prerequisites`, `teaching_route` and `comparison`. Strengths, limits and other branches are conditional.

At item level, `id`, `kind`, `summary`, `locator` and `evidence` occur in all 489 items. Optional examples: `disposition` 460; `disposition_rationale` 341; `classification` 373; `candidate_destinations` 385; `pedagogical_assessment` 116; `technical_assessment` 132; `pedagogical_profile` 42; `mapped_concepts` and `target_resources` 39 each; `verification` 7; `provenance` 3.

### 3.3 Route semantics

- `candidate_destinations.route_ids` occurs on 143 items, but every observed list is empty.
- `candidate_destinations.routes` and `target_routes` are absent.
- `pedagogical_model.comparison.canonical_routes` has 142 annotations across 51 models and 37 distinct strings. They mix route labels, prose, page metadata descriptions and file paths; they are not normalized route IDs.
- The 294 `pedagogical_model.teaching_route` steps are source-local instructional sequences, not canonical site routes.
- Legacy `target_resources` contains bilingual page-like identifiers. Do not infer that these are IDs in `data/resources.yml`.

### 3.4 Unresolved candidate concept references

Three IDs used in candidate concept proposals are absent from the canonical concept registry:

| Candidate ID | Exact item(s) | Existing editorial signal |
|---|---|---|
| `context-window` | `hesam-sheikh-llm-study-roadmap-2024:hallucination-causality-qualification` | clarify |
| `log-probability` | `marek-ryabinin-score-centering-off-policy-rl-2026:topk-and-compute` | integrate-by-reference |
| `weighted-aggregation` | `codefinity-qkv-building-blocks:quiz-pooling`; `codefinity-qkv-building-blocks:quiz-context`; `mbrenndoerfer-qkv-attention-mechanism:convex-hull` | integrate-by-reference / integrate |

These are report-only exceptions, not current validator errors. Inspect item evidence and existing concept definitions before deciding whether to map to an existing concept, create a concept through the normal review process, or reject/remove the proposal. Check near-synonyms and granularity; do not create all three automatically.

## 4. Work remaining — ordered plan

### Step 1 — Reconcile PR #1369 and exact checks

1. Fetch current PR metadata and current head SHA; do not assume the recorded SHA remains current.
2. Inspect every required workflow/job on that exact SHA, including Quarto full render and browser audit.
3. If a check failed, inspect logs, fix only the demonstrated issue and rerun on the new head.
4. Review the diff for accidental changes, especially CI wiring, report scope, generated artifacts and documentation claims.
5. Keep the PR unmerged until required checks are green and review is complete. Never describe Quarto as passed while pending.

### Step 2 — Review the three unresolved concept proposals

For each exact item above:
1. Read the complete extraction item: locator, evidence, summary, classification and context.
2. Inspect the source record and existing concept definitions for semantic overlap, granularity and bilingual coverage.
3. Record a reasoned decision: map to an existing concept, create through the normal concept process, or reject/remove the proposal.
4. Only then update canonical concepts or extraction proposals; add tests and refresh inventory counts.

Do not bulk-create the three IDs or decide from string similarity alone.

### Step 3 — Inspect historical `scan` and `canonical_mapping`

1. List all 36 files with extraction-level `scan`; compare each block with source-level `scan_history`.
2. Identify duplicated, unique, stale and richer fields, preserving provenance, rights and retrieval details.
3. Inspect all 28 `canonical_mapping` blocks. Classify proposals as pending, superseded, partially integrated or demonstrably integrated using canonical records/history, not field names.
4. Decide whether to preserve, migrate with traceability or deprecate. No deletion or bulk move before an explicit migration plan and tests.
5. Record findings and exceptions in the compatibility matrix.

### Step 4 — Complete compatibility matrix and discriminating tests

Map every proposed rule to observed presence and shape, valid historical examples, malformed/ambiguous examples, unknown-reference semantics, intended severity and migration implications.

Add focused fixtures for:
- absent optional fields and null/empty/wrong-type values;
- valid, invalid and unknown references;
- unknown candidate-only concepts (must remain distinct from canonical links);
- historical `scan` and `canonical_mapping` shapes;
- pedagogical-model variants and conditional branches.

Add non-regression assertions so absent optional fields and unknown proposal IDs do not accidentally become hard errors.

### Step 5 — Change validator only where evidence supports a safe rule

- Require only genuinely mandatory fields and stable invariants.
- Validate a supplied optional value without requiring the field to exist.
- Distinguish canonical references from candidate proposals and editorial annotations.
- Do not promote unknown candidate concept IDs to hard errors without an approved semantic policy.
- Preserve legacy fields during the agreed compatibility window.
- Update validator documentation and tests in the same change.

### Step 6 — Re-run complete validation and publish a fresh baseline

Run source catalogue/extraction validation, Python quality/type checks, full tests, opt-in inventory, Quarto full render and browser audit on the exact final commit. After any data migration, rerun the inventory and update counts, exceptions, matrix and this handoff. Record final SHA and workflow run IDs.

## 5. Explicit safety boundaries

- Do not create duplicate concepts, pages, resources or routes just to make proposals resolve.
- Do not treat `candidate_destinations` as completed integration.
- Do not equate `comparison.canonical_routes` or `teaching_route` with canonical route IDs.
- Do not merge `mapped_concepts` into classifications or `target_resources` into page/resource destinations without item-level review.
- Do not delete or silently rewrite historical `scan` / `canonical_mapping` blocks.
- Do not make unknown proposal IDs or missing optional fields hard validation failures by default.
- Do not change validator behavior before the compatibility matrix and discriminating tests are complete.

## 6. Start-of-session checklist

- [ ] Read this handoff and `docs/extraction-destination-inventory.md`.
- [ ] Check whether PR #1369 is still open and fetch its current head SHA.
- [ ] Check Quarto and all required CI results on that exact SHA.
- [ ] Start with the three unresolved candidate concept occurrences; avoid broad refactoring.
- [ ] Update this handoff and the compatibility matrix as decisions are made.

**Recommended next action:** verify the final Quarto/browser result for PR #1369, then perform the item-level review of the three unresolved candidate concept proposals.
