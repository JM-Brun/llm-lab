# Contributing

This is a learning repository: prefer small, testable changes that make the reasoning and evidence inspectable.

## Local setup

Install Python 3.12 and uv, then run:

```bash
uv sync --dev
uv run pre-commit install
uv run pre-commit run --all-files
```

Commit `uv.lock` whenever dependency metadata changes. Use `uv lock --check` to check that the lockfile matches `pyproject.toml`, and use `uv sync --locked --dev` to reproduce the locked environment.

## Before opening a pull request

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy src
uv run pytest
```

For numerical implementations, include tests against known values and/or finite differences. For model or training changes, document the hypothesis, baseline, data provenance, configuration, seed, hardware, metrics, and limitations.

## Engineering conventions

- Put reusable code in `src/llm_lab`; notebooks are explanatory, not the sole home of core logic.
- Keep functions focused, typed, and small enough to reason about.
- Prefer explicit tensor-shape documentation and deterministic tests.
- Do not commit secrets, raw datasets, model weights, or large experiment outputs.
- Pin dependencies through `pyproject.toml` constraints and the committed `uv.lock`.
- Explain deviations from upstream implementations and cite the source.
