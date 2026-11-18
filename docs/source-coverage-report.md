# Source-to-knowledge coverage report

The catalogue validator and the coverage report have deliberately different jobs:

- `site/tools/check_source_catalogue.py` checks structural validity and referential integrity. A broken ID or invalid controlled value is a validation failure.
- `site/tools/report_source_coverage.py` measures whether the catalogue forms a useful traceability chain. Gaps are review queues, not automatic failures.

## Run locally

From the repository root:

```bash
python site/tools/check_source_catalogue.py
python site/tools/report_source_coverage.py
python site/tools/report_source_coverage.py --format json --output /tmp/source-coverage.json
```

The report is deterministic for a fixed repository tree. It reads:

- `data/sources.yml` as the canonical source register;
- `data/extractions/*.yml`, associating records through each YAML `source_id` (never by filename);
- `data/concepts.yml` as the canonical concept inventory.

## What it measures

- source, extraction-record, extraction-item, and concept counts;
- scan and integration status distributions, separately and jointly;
- sources without an extraction, with an explicit queue for sources marked `integrated`;
- sources without a canonical concept link or a page destination;
- concepts with no linked source and concepts linked to only one source;
- unknown publication dates and licence statuses;
- extraction records whose `source_id` does not resolve to a canonical source;
- disagreement between a source's current scan status and its latest recorded scan event.

Page destinations are read from the canonical source record's `related.pages` field. Concept coverage combines source classification, source related concepts, and extraction-item classification. The report does not invent a destination field that is absent from the extraction schema.

## Interpretation rules

- **Missing extraction is not automatically a defect.** A source may be deferred, rejected, already covered, or useful only as a bibliography link. Review the integration status and record an explicit decision in the canonical data; do not create empty extraction files to make the metric look better.
- **One source per concept is a signal, not a quality verdict.** A primary paper or authoritative specification may be sufficient. Corroboration depends on the claim, domain, and evidence type.
- **Unknown dates and licences remain unknown.** The report exposes metadata debt; it does not infer dates, copyright status, or reuse permissions.
- **Contradictions and scientific corroboration remain human work.** The script cannot decide whether two claims genuinely conflict without comparing their definitions, scope, methods, data, and dates.
- **A page link is not proof of pedagogical integration.** The report measures traceability, not whether a page teaches the concept well or whether a learner can reconstruct it.

The report does not modify catalogue data, create concepts, assign tags, or alter learning routes. It complements the source-lineage architecture and the existing validator; it does not introduce a parallel registry.

## Related work

This tool supports issue [#1211](https://github.com/JM-Brun/llm-lab/issues/1211) and should be used alongside the source catalogue audit [PR #1210](https://github.com/JM-Brun/llm-lab/pull/1210). It does not replace the focused resource reviews or the bilingual pedagogical review workflow.
