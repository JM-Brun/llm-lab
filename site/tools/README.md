# Site tooling

These scripts generate and validate the Quarto site and its source data. They are maintenance tools, separate from the installable `llm_lab` learning package. The CI workflows run them from the repository root. Page, graph and history tools require `docs/requirements-history-validation.txt`; the embedding example also requires `docs/requirements-tokenizer-example.txt`. Knowledge-pipeline tests (registries, page index, map generation, JSON-LD export) are in `tests/knowledge/`; rendered-site, history and computational-graph tests are in `tests/site/`. Run either alone with `uv run pytest --no-cov -q tests/knowledge`; the coverage threshold applies only to `llm_lab`.


`project_index.py` provides the read-only canonical query projection. `project_coverage.py` builds a concept-centred coverage matrix and flags missing associations for uniquely paired published FR/EN counterparts. `report_project_index.py` summarizes these results without writing files. From the repository root:

```bash
uv run python site/tools/report_project_index.py
uv run python site/tools/report_project_index.py --format json --language fr --destination understand
```

Filters affect the page selection. Whole-project counts and findings describe the full read model. JSON includes the source commit, modified-input flag, count units, exclusions and evidence paths. See the [metric registry](../../docs/project-metric-registry.md) for definitions.
