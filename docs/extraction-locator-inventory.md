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
- Non-mapping extraction records, items with no locator, scalar-text locators, and unsupported locator shapes, separately.
- Coarse shape buckets and up to three record paths for unsupported non-mapping locator values.
- The legacy `items_without_locator_mapping` total (the sum of the preceding three categories); this is not a missing-evidence count.
- Mapping locators with missing/invalid required fields.
- Observed mapping locator type distribution, key-set shapes, and coarse value-shape buckets per type.
- Coarse value-shape buckets and up to three record paths for scalar locators.
- Up to three record paths per mapping type/shape for targeted human inspection.

Non-mapping extraction records are not counted as items with missing locators. The report deliberately does not print locator values, fetch URLs, resolve citations, infer that a source was inspected, or declare a grammar valid. Scalar text locators are preserved as an observed representation and are not automatically treated as invalid. Shape buckets are heuristics for triage, not semantic validation.

## Next steps

1. Run against the complete checked-out corpus and retain the dated JSON artifact when useful.
2. Inspect representative examples for each locator type and scalar form; identify collisions (one type used for multiple incompatible forms).
3. Define a grammar only for types with stable, unambiguous usage; keep unknown/custom types report-only until classified.
4. Add type-specific unit fixtures, including legacy and partial records, before promoting malformed values to CI errors.
5. Keep locator syntax validation separate from source availability, claim support, and independent corroboration.
