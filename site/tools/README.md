# Site tooling

These scripts generate and validate the Quarto site and its source data. They are maintenance tools, separate from the installable `llm_lab` learning package. The CI workflows run them from the repository root. Page, graph and history tools require `docs/requirements-history-validation.txt`; the embedding example also requires `docs/requirements-tokenizer-example.txt`. Knowledge-pipeline tests (registries, page index, map generation, JSON-LD export) are in `tests/knowledge/`; rendered-site, history and computational-graph tests are in `tests/site/`. Run either alone with `uv run pytest --no-cov -q tests/knowledge`; the coverage threshold applies only to `llm_lab`.


`project_index.py` provides the read-only canonical query projection. `project_coverage.py` builds a concept-centred coverage matrix from that projection; it is a library module, not a separate CLI or source of truth. Its tests are in `tests/knowledge/test_project_coverage.py`.
