# Contributing

This is a learning and experimentation repository. Prefer small, testable changes that make the reasoning, implementation, and evidence inspectable. Follow the shared [reader-experience and editorial method](docs/reader-experience-and-editorial-method.md): the site is a navigable learning graph with progressive depth, not a mandatory linear book. The Wiki is the canonical home for reusable, domain-general concepts; LLM Lab is a separate public, bilingual learning site whose explanations must be complete without access to the private Wiki. The repositories have different purposes, not a shared runtime or reading dependency. Reusing a concept in both is intentional when LLM Lab needs to teach it to explain language models. Public readers must never need a Wiki URL, private definition, or private file to understand a page or render the site. Cite accessible public sources and include all definitions, assumptions, derivations, examples, caveats, and exercises needed by the LLM Lab learning experience—even when that creates deliberate overlap with the Wiki.

## Contribution modes

Choose the mode that matches the change and identify it in the PR.

1. **Concept teaching page or synthesis** — first identify the reader question and page type. Lead with the high-level purpose and mental model, then offer optional depth through meaningful links. Explain an LLM-specific concept, connect it to essential (not merely related) prerequisites, cite sources, state assumptions and limits, and include counterexamples where they clarify likely misconceptions. Do not put private Wiki URLs or concept IDs in public lesson content. If maintainers need cross-repository traceability, record it in the private `career-knowledge` repository; it must never be a reader or build dependency. Teach enough of the general mathematics locally for the page to stand alone; include the derivations and worked examples required by the LLM learning objective. Focus the selection, notation, examples, counterexamples, and interpretation on LLMs. It is acceptable—and sometimes necessary—to repeat a definition or derivation also present in the Wiki. Do not shorten or remove material solely to eliminate overlap.
2. **French/English parity and navigation** — improve translations, glossary, cross-links, learning sequence, accessibility, or site structure. Keep substantive claims, caveats, examples, and references equivalent in both languages; do not translate a claim into a stronger one.
3. **Reference implementation and numerical tests** — add or revise reusable code under `src/llm_lab`, with typed interfaces and tests for shapes, masks, gradients, numerical edge cases, or known values. Notebooks may explain the code but must not be its only implementation.
4. **Controlled experiment and evaluation** — define a hypothesis, baseline, data provenance, configuration, seed, split strategy, metrics, compute budget, and limitations. Preserve runnable entry points/configuration and report negative or inconclusive results as well as positive ones.
5. **Critical review or correction** — challenge a claim, implementation, illustration, or interpretation with a source, counterexample, reproducible check, or explicit uncertainty. Separate a documented source claim from the project's own analysis.
6. **Figures and external references** — add or revise visual material with source/author attribution and a checked licence. Prefer embedding from an authorized original source to copying external assets; record provenance in the reference page.
7. **Build, dependencies, and developer tooling** — update Quarto, Python packaging, CI, linting, or reproducibility tooling. Explain material dependency changes and keep the core exercises runnable on CPU with small inputs.

## Pedagogical resource discovery

Use the curated [Pedagogical Resource Library](docs/pedagogical-resource-library.md) when creating or substantially revising a concept, overview, mathematical explanation, or learning sequence. It includes visual explainers, animations, interactive tools, science communication, and primary/official references.

Actively look for ideas on how to explain the topic—not just sources that mention it. Consider whether an original diagram, figure, animation, interactive experiment, analogy, or step-by-step visual sequence would make the mechanism clearer. Compare sources when the concept is important or easily misunderstood; identify what each source simplifies or omits, then produce an original synthesis with consistent notation, worked examples, counterexamples, and limitations. Use primary papers and official documentation to verify technical claims; popularity or visual polish is not evidence.

This is a quality prompt, not a requirement to add a figure to every page or to cite a fixed number of resources. A visual should answer a concrete learner question and remain useful alongside the text. Do not copy prose, exercises, code, diagrams, or animations without a clear legal basis. Check the specific licence and attribution requirements, record provenance in `site/references.qmd`, and provide captions and alt text. A publicly accessible asset is not automatically reusable.

For substantial revisions, use the library's [repeatable improvement loop](docs/pedagogical-resource-library.md#a-repeatable-improvement-loop). Record the learner problem, source roles, design decision, limitations, checks actually run, and remaining work in docs/page-audit-inventory.md or the PR description. Start with a small number of complementary sources rather than collecting links indefinitely. A decision to retain an existing explanation or not add a visual is acceptable when supported by the learner need and evidence. Do not report source inspection as rendered review, and do not report planned validation as completed.


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
