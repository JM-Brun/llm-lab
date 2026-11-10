# Knowledge tooling reliability audit

**Audit date:** 2026-11-05, against `codex/check-guided-route-freshness` at `61d4bdf` (local `origin/main` was `3b9f1ec`; GitHub was unreachable, so default-branch and open-PR state were not verified then).
**Port status, 2026-11-09:** four of the audit's changes were ported to `main` as separate PRs (see [Port status](#port-status)); the rest were not. Statements about code behaviour below describe the audited base unless stated otherwise.

**Confidence:** high for the source-level findings and the tests that exercised them; limited for the scientific correctness of individual extraction claims, learning outcomes, accessibility, and scalability under production-sized data, none of which these checks establish.

## Owners and traceability

Identifiers and relationships below are distinct even where a projection connects them. As of `main` at `942cae0`, `data/concepts.yml` uses schema version 2 and the other registries listed use version 1.

| Element | Canonical owner and contract | Consumers and checks |
|---|---|---|
| Source and extraction | `data/sources.yml`, `data/source-taxonomy.yml` and `data/extractions/*.yml`: source IDs and source-prefixed extraction item IDs; source-local pedagogical nodes use `src-` IDs. Extraction is a reviewed authoring workflow, not an automated ingestion implementation. | `site/tools/check_source_catalogue.py`; `tests/knowledge/test_source_pedagogical_model.py` and `test_source_taxonomy_contract.py`; CI source-catalogue step. |
| Domain | `data/domains.yml`: bilingual domain IDs; `concepts[].domains` is many-to-many. A page's primary `domain` is a separate classification. | `site/tools/check_concept_registry.py`; `site/tools/export_knowledge_graph.py`; `tests/knowledge/test_concept_registry.py`. |
| Concept and relation | `data/concepts.yml`: language-independent IDs, FR/EN labels and definitions, page associations and typed directional relations. The controlled vocabulary and symmetry rules are in `check_concept_registry.py`; prerequisite and generalization are checked for cycles. | Concept validator, map generator, JSON-LD exporter and their `tests/knowledge/` suites. A source-local instructional graph is not this canonical graph. |
| Resources and associations | `concepts[].resources` holds published page IDs. `data/resources.yml` separately owns first-class resource IDs, locations, lifecycle and many-to-many concept/page links; the supported kind is `implementation`. | `check_resource_registry.py`, `export_knowledge_graph.py`; `tests/knowledge/test_resource_registry.py` and `test_knowledge_graph_export.py`. |
| Curriculum and guided stages | `docs/learning-path.md` owns the narrative curriculum; `data/guided-route.yml` owns the bilingual machine-readable stages, objectives, core pages and optional links. Stage order is not a prerequisite DAG. | Route models and resolution in `site/tools/build_learning_map.py`; `tests/knowledge/test_learning_map.py` and `test_guided_route_freshness.py`. |
| Published pages | Page metadata in `site/**/*.qmd` owns page identity, navigation and hierarchy. `site/tools/page_index.py` indexes published pages for the validators, exporter and map generator; the full page validator `check_page_metadata.py` remains authoritative. | `tests/knowledge/test_page_index.py`, `test_page_metadata.py`. Page links, semantic edges and headings have different meanings. |
| Generated maps and export | `build_learning_map.py` generates localized page/concept JSON and route fragments; `export_knowledge_graph.py` generates JSON-LD. `artifact_writer.py` publishes them. | Map/export tests and the rendered-output checks in `.github/workflows/quarto.yml`. |

## Port status

| Audit finding | Result on `main` |
|---|---|
| PyYAML silently discarded repeated mapping keys, so an earlier source ID, schema version or page ID could vanish before validation. | **Ported:** [#792](https://github.com/JM-Brun/llm-lab/pull/792) adds `site/tools/strict_yaml.py` (safe loading, duplicate-key errors with both source locations, explicit overrides of merged defaults still valid) and uses it in the page, concept, resource and source validators, the map generator, the exporter and the page audit. History-pilot and computational-graph tooling were not converted. |
| Independent page scans disagreed: the concept and resource validators saw only `site/fr` and `site/en`, missing the root French home and the shared references page; the exporter skipped shared pages and built URLs from page IDs. | **Ported:** [#798](https://github.com/JM-Brun/llm-lab/pull/798) adds `site/tools/page_index.py` (one scan; rejects duplicate IDs, invalid status, malformed or duplicate tags and duplicate metadata keys; ignores files that only quote the page-map marker, such as generated includes). Exported URLs now follow source paths. The localized home-link discrepancy had already been fixed on `main`. |
| The French output could be written before an invalid English route or graph failed; a failed write could truncate an existing file. | **Ported:** [#799](https://github.com/JM-Brun/llm-lab/pull/799) adds `site/tools/artifact_writer.py` and renders all outputs before writing any. Replacement is per-file atomic, not a transaction: a later replacement failure can leave mixed versions, and the exception carries a note naming the failed target and how many files were already replaced. No locking or power-loss durability; symbolic-link targets and mode bits are preserved, but hard links, ownership, ACLs and extended attributes are not guaranteed. |
| Knowledge-pipeline tests shared a directory with rendered-site tests and the coverage boundary was undocumented. | **Ported:** [#801](https://github.com/JM-Brun/llm-lab/pull/801) moves them to `tests/knowledge/`. The coverage threshold still measures `llm_lab` only; `site/tools/README.md` documents running either suite alone. |
| An alternate extraction root raised a path exception; malformed source-local edge endpoints and several status values raised type errors; booleans were accepted as route order integers. | **Not ported.** Reported on the audited base; not re-checked on current `main`. |
| The localized concept projection silently omitted unresolved relations and page references; the standalone exporter silently omitted unresolved page associations. | **Not ported.** The exporter now reads pages through the shared index, but it does not newly validate domains, concepts and resources against it. Not re-checked on current `main`. |
| Recursive page-route and hierarchy validation failed on long chains (1,500-page fixture); invalid page relation types and malformed registry collections raised exceptions; boolean schema versions were accepted. | **Not ported.** Not re-checked on current `main`. |
| Repeated scans: one index scan took 0.071 s versus 0.212 s for three scans on 105 pages (best of five, one machine). | **Not ported** (the generator does not share one page snapshot across languages and the export). The measurement isolates repeated parsing; it is not an end-to-end benchmark or a claim about larger datasets. |

The full original work, including the unported items, is preserved in the local branch `backup/knowledge-tooling-wip` (not pushed).

## Remaining gaps

- Catalogue validation checks record structure and references, not whether a claim follows from a source. Source review, bilingual semantic quality and learner outcomes remain human evidence tasks.
- The registry has no first-class resource kind for figures, papers, experiments or datasets.
- mypy covers `src` and only `strict_yaml.py`, `page_index.py` and `artifact_writer.py` among the site tools; PyYAML has no installed type stubs.
- Malformed-input coverage is wider after the ported changes but not exhaustive; no fuzzing was done.
- The cycle check remains iterative and suitable for long chains in principle, but no runtime or memory scaling benchmark was performed.

## Validation

On the audited base, the full suite passed with 100% coverage of `llm_lab`, and the validators, map generator and exporter ran; a Quarto render of 105 pages and the rendered-map, JSON-LD, history and site-link checks passed. Interactive browser and accessibility review were not run.

For the ported PRs, each passed `ruff check`, `ruff format --check`, mypy on the touched modules and the site/knowledge tests (191 tests in #798, 198 in #799 and #801), the four validators, and the map and JSON-LD generators (whose output was byte-identical before and after #798 and #799). CI (`Python quality checks` and the Quarto render with browser audit) was green on each. The Quarto render was not run locally.
