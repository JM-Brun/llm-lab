# Site tooling

These scripts generate or validate the Quarto site and its source data. They are maintenance tools, not part of the installable `llm_lab` learning package. The CI workflows run the checks from the repository root; the history and page-metadata tools require the dependencies in `docs/requirements-history-validation.txt`, while the embedding example also requires `docs/requirements-tokenizer-example.txt`. Tests for site behavior are in `tests/site/`.
