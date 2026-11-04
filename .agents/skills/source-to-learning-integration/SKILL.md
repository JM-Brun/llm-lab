---
name: source-to-learning-integration
description: Orchestrate the two-phase workflow that turns external sources into traceable structured knowledge and validated improvements to the LLM Lab knowledge graph and bilingual learning experience.
---

# Source-to-learning integration

## Mission

Coordinate two distinct phases with an explicit, persistent hand-off:

1. **Extraction** — inspect external sources and record their useful content as structured, evidence-linked data. Do not edit pedagogical pages or mutate the canonical knowledge graph.
2. **Integration** — review validated extraction records, decide what belongs in the knowledge graph and learning experience, then update canonical data, pages, assets, experiments, references, and navigation as justified.

The phases may run in separate sessions and PRs. Extraction is a durable research result, not a promise that every item will be published. Integration is a deliberate graph/editorial decision, not a mechanical copy of extraction notes.

## Specialist skills

- `source-extraction`: provenance, access and scan scope, structured claims/ideas/artifacts, confidence, source catalogue, extraction records and hand-off.
- `knowledge-and-learning-integration`: graph impact, concept/relation decisions, page mapping, content/assets/experiments, bilingual parity and validation.

Use this skill to orchestrate both. Run extraction first unless a complete, trustworthy record already exists. Run integration only against persistent, reviewable records. Do not repeat scans unnecessarily.

## Phase A — extraction

Input: URLs, documents, repositories, named sources, or a source set.

Output:
- stable source records in the canonical source catalogue;
- atomic extracted items with precise source locators;
- scan status and exact scope actually inspected;
- evidence kind, confidence, generality, assumptions, limitations and rights metadata;
- candidate concepts, relations, pages, visuals, experiments and teaching improvements;
- an extraction report with access limits and unresolved questions.

No page edits, published new pages, concept-registry mutations, or graph-projection changes in this phase. Candidate destinations and graph nodes/edges are proposals only.

## Phase B — integration

Input: reviewed extraction records and current repository state.

Output:
- accepted/deferred/rejected dispositions with rationale;
- canonical graph changes, or an explicit no-change decision;
- updates to existing pages or justified new pages;
- asset, experiment, implementation, reference, route and bilingual updates as needed;
- validation evidence and a before/after impact report.

A source can be fully scanned and catalogued without any page or graph change.

## Canonical architecture
## Classification contract

Use `docs/source-catalogue-schema.md` and `data/source-taxonomy.yml` for source/extraction classification. Reuse the six domains in `data/domains.yml`; assign one primary theme and optional secondary themes. Keep namespaced retrieval tags separate from canonical `concept_ids` and typed metadata. Do not introduce a generic `meta_tags` bag or treat tags as graph concepts. Apply the same distinction at extraction-item level, allowing a justified item-level refinement without rewriting its source classification.


Before creating or changing data structures, inspect:
- `docs/knowledge-graph-standards.md` and `docs/knowledge-graph-implementation-audit.md`;
- `data/concepts.yml`, `data/domains.yml`, `data/resources.yml`;
- `site/tools/export_knowledge_graph.py` and relevant validators/tests;
- source audits, `docs/references.md`, `docs/pedagogical-resource-library.md`, and `docs/visual-assets-register.md`.

Reuse existing stable IDs and graph semantics. The source catalogue is canonical in `data/sources.yml`, source classification in `data/source-taxonomy.yml`, and atomic extraction records in `data/extractions/`, governed by `docs/source-catalogue-schema.md`. Do not create a parallel catalogue, a second concept registry, a competing graph database, or manually maintained JSON-LD. Do not overload implementation-oriented `data/resources.yml`. Keep YAML as authoring data and JSON-LD as a generated projection.

Distinguish sources actually scanned from sources merely discovered, selected, linked, cited, inaccessible, superseded or rejected. A bibliography entry is not evidence of a scan.

## Global constraints

- Preserve existing useful knowledge; no silent deletion of caveats, examples, equations or links.
- Synthesize original explanations; do not concatenate articles or copy protected prose/figures.
- Separate general principles from model-, version-, task-, dataset- and hardware-specific findings.
- Evidence must support the exact claim; preserve uncertainty and disagreement.
- Bound analogies by stating both the mapping and where it breaks.
- Record figures, code, datasets and experiments with provenance, rights and reproducibility status.
- Create a page only for a distinct, durable learner question not adequately served by extending an existing page.
- Keep graph relations, pedagogical route, page navigation, source bibliography and learning-resource registry distinct but linked.
- Maintain substantive French/English parity for published changes.

## Completion report

Report the two phases separately:
1. sources examined, scan scope/status, extraction counts by type, provenance/rights gaps;
2. item dispositions, graph nodes/edges added or changed, pages/assets/experiments/references updated, and no-change decisions;
3. existing knowledge preserved or moved, FR/EN parity, validation results and unresolved follow-ups.

The workflow is complete only when persistent records and accepted integrations are traceable, validated and accurately reported.
