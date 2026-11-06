# Site tooling

These scripts generate and validate the Quarto site and its source data. They are maintenance tools, separate from the installable `llm_lab` learning package. The CI workflows run them from the repository root. Page, graph and history tools require `docs/requirements-history-validation.txt`; the embedding example also requires `docs/requirements-tokenizer-example.txt`. Site behavior and tooling tests are in `tests/site/`.

- `render_computational_graph.py` renders selected bilingual Mermaid fragments from `data/computational-graph.yml`; run it before rendering the Quarto site.
