# Contributing

This is a learning and experimentation repository. Prefer small, testable changes that make the reasoning, implementation, and evidence inspectable. The Wiki is the canonical home for general mathematical and machine-learning concepts; LLM Lab owns the LLM-specific learning path and its demonstrations.

## Contribution modes

Choose the mode that matches the change and identify it in the PR.

1. **Concept teaching page or synthesis** — explain an LLM-specific concept, connect it to prerequisites, cite sources, state assumptions and limits, and include counterexamples where they clarify likely misconceptions. Link to canonical Wiki definitions for general concepts instead of duplicating them.
2. **French/English parity and navigation** — improve translations, glossary, cross-links, learning sequence, accessibility, or site structure. Keep substantive claims, caveats, examples, and references equivalent in both languages; do not translate a claim into a stronger one.
3. **Reference implementation and numerical tests** — add or revise reusable code under `src/llm_lab`, with typed interfaces and tests for shapes, masks, gradients, numerical edge cases, or known values. Notebooks may explain the code but must not be its only implementation.
4. **Controlled experiment and evaluation** — define a hypothesis, baseline, data provenance, configuration, seed, split strategy, metrics, compute budget, and limitations. Preserve runnable entry points/configuration and report negative or inconclusive results as well as positive ones.
5. **Critical review or correction** — challenge a claim, implementation, illustration, or interpretation with a source, counterexample, reproducible check, or explicit uncertainty. Separate a documented source claim from the project's own analysis.
6. **Figures and external references** — add or revise visual material with source/author attribution and a checked licence. Prefer embedding from an authorized original source to copying external assets; record provenance in the reference page.
7. **Build, dependencies, and developer tooling** — update Quarto, Python packaging, CI, linting, or reproducibility tooling. Explain material dependency changes and keep the core exercises runnable on CPU with small inputs.

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
quarto render site
```

Run the relevant checks for the changed surface and state clearly if a tool or optional dependency is unavailable. Review the rendered page, including the other language version for bilingual changes.

## Engineering and research conventions

- Put reusable code in `src/llm_lab`; notebooks are explanatory, not the sole home of core logic.
- Keep functions focused, typed, and small enough to reason about; document tensor shapes and numerical conventions.
- For numerical implementations, test known values and/or finite differences.
- For model or training changes, document hypothesis, baseline, data provenance, split/deduplication policy, configuration, seed, hardware, metrics, costs, and limitations.
- Keep experiments reproducible; do not commit secrets, raw datasets, model weights, or large generated outputs.
- Pin dependencies through `pyproject.toml` constraints and the committed `uv.lock`.
- Explain deviations from upstream implementations and cite the source.
- Separate verified, planned, illustrative, and experimentally observed results. Passing CI verifies configured checks, not scientific claims or visual quality.
- No license has been selected yet; do not imply that others have permission to reuse or redistribute code or content.
