# Site tooling

These scripts generate and validate the Quarto site and its source data. They are maintenance tools, separate from the installable `llm_lab` learning package. The CI workflows run them from the repository root. Page, graph and history tools require `docs/requirements-history-validation.txt`; the embedding example also requires `docs/requirements-tokenizer-example.txt`. Knowledge-pipeline tests (registries, page index, map generation, JSON-LD export) are in `tests/knowledge/`; rendered-site, history and computational-graph tests are in `tests/site/`. Run either alone with `uv run pytest --no-cov -q tests/knowledge`; the coverage threshold applies only to `llm_lab`.


`project_index.py` provides the read-only canonical query projection. `project_coverage.py` builds a concept-centred coverage matrix and flags missing associations for uniquely paired published FR/EN counterparts. `report_project_index.py` summarizes these results without writing files. From the repository root:

```bash
uv run python site/tools/report_project_index.py
uv run python site/tools/report_project_index.py --format json --language fr --destination understand
```

Filters affect the page selection. Whole-project counts and findings describe the full read model. JSON includes the source commit, modified-input flag, count units, exclusions and evidence paths. See the [metric registry](../../docs/project-metric-registry.md) for definitions.


## Cross-graph evidence queries

`ProjectIndex.build(root, include_evidence=True)` opts into a read-only projection of the existing source catalogue, extraction items, computational graph and guided-route conceptual focus. The default `ProjectIndex.build(root)` remains unchanged and does not load the larger extraction corpus.

From the repository root, query one or more canonical concept IDs:

```bash
uv run python site/tools/cross_graph_query.py \
  --concept scaled-dot-product-attention \
  --concept predictive-compression \
  --concept v-information \
  --concept mutual-information \
  --concept joint-embedding-predictive-architecture
```

The JSON result contains typed `paths` and explicit `gaps`:

- Source-evidence paths require an item-level mapping (`mapped_concepts` or `classification.concept_ids`) and retain the extraction locator, confidence, assumptions, limitations, item disposition, and source scan/integration status.
- Source-catalogue concept associations without an item-level mapping are reported as gaps, not promoted to evidence paths. Candidate destinations are also reported as gaps and never traversed as accepted relations.
- Computation paths distinguish page-mediated links through `concepts[].resources` and `computational_graph.nodes[].resources` from stage-mediated `guided-route` conceptual-focus associations. Neither is represented as a direct canonical concept-to-node edge.
- Practice paths require an authored page-map `related` edge to a page tagged `destination: practice`. Non-page resources remain distinct from source extractions and computational nodes.

The projection is derived from existing registries and YAML files; it introduces no second graph or source of truth.
