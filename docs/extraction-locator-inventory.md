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

## What it reports

- Number of extraction files and items visited.
- Items with no locator separately from scalar/non-mapping locators.
- Non-mapping locator value shapes and representative record paths, without exposing locator values.
- Malformed extraction records and mapping locators with missing/invalid required fields.
- Observed mapping locator type distribution, key-set shapes and coarse value-shape buckets.
- Up to three record paths per shape for targeted human inspection.

A scalar locator is **not** silently counted as absent. It is reported as a present, non-mapping locator requiring a separate contract decision. The inventory does not assume scalar values are valid or invalid for every locator type.

The report deliberately does not print locator values, fetch URLs, resolve citations, infer that a source was inspected, or declare a grammar valid. Its shape buckets are heuristics for triage, not semantic validation.

## Next steps

1. Run against the complete checked-out corpus and retain the dated JSON artifact when useful.
2. Inspect representative examples for each locator type and scalar shape; identify collisions (one type used for multiple incompatible forms).
3. Decide whether scalar forms are supported legacy syntax, malformed records, or type-specific forms before migrating or rejecting them.
4. Define a grammar only for types with stable, unambiguous usage; keep unknown/custom types report-only until classified.
5. Add type-specific unit fixtures, including legacy, scalar and partial records, before promoting malformed values to CI errors.
6. Keep locator syntax validation separate from source availability, claim support, and independent corroboration.
