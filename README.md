# LLM Lab

LLM Lab is a bilingual, code-first learning and experimentation project for people who want to understand how language models work, build their components, and investigate their behavior. It connects intuition, mathematics, readable implementations, tests, and controlled experiments—from text and tokenization through attention and generation, with training, adaptation, evaluation, and efficiency as longer-term goals.

The aim is to learn from small, inspectable models and evidence, not to train a production-scale LLM from scratch.

**[Explore LLM Lab in French](https://jm-brun.github.io/llm-lab/) · [Explore in English](https://jm-brun.github.io/llm-lab/en/)**

## How the lab is designed

- **Understand before scaling.** Follow inference through a small model before studying how its parameters learn. The guided build, pretrained-model adaptation, and cross-cutting evaluation have distinct dependencies; advanced mathematics is available when needed, not a blanket prerequisite.
- **Learn at different depths.** The site connects conceptual explanations, a guided build, optional deep dives, exercises, and experiments. It supports non-linear navigation and progressive disclosure while keeping necessary definitions and caveats visible.
- **Test the mathematics and code.** Use worked examples, explicit shapes and conventions, numerical edge cases, invariants, gradients, and reference comparisons where appropriate. Readable teaching implementations take priority over optimized kernels.
- **Measure and challenge claims.** Define questions and baselines; record data provenance, configurations, seeds, metrics, compute costs, and limitations. Use counterexamples and failure analysis, and distinguish an illustration, a passing test, and an experimental result.
- **Keep the public material complete and bilingual.** French and English should preserve the same claims and qualifications. The public lab must stand on its own even when general concepts are also developed in a separate private knowledge base; no private repository is a reading or build dependency.
- **Respect provenance and reuse.** Cite the work that supports a claim, check rights for code, data, and figures, and avoid committing secrets, raw datasets, or model weights.

See [the learning path](docs/learning-path.md) for the authoritative module-level objectives and evidence gates, the [content-section map](docs/content-section-mapping.md) for destination boundaries and page ownership, the [roadmap](docs/roadmap.md) for priorities and acceptance criteria, and the [experiment protocol](docs/experiment-protocol.md) for reporting requirements. The interactive learning route and exploratory graphs are reader-facing projections; their source ownership and maintenance are indexed in [information architecture](docs/information-architecture.md).

## Inspiration and sources

Sebastian Raschka's [*Build a Large Language Model (From Scratch)*](https://github.com/rasbt/LLMs-from-scratch) provides a major implementation and scope reference, not a mandatory table of contents. The lab also draws on visual explanations such as [Jay Alammar's Illustrated GPT-2](https://jalammar.github.io/illustrated-gpt2/) and the practical perspective of the [Hugging Face LLM Course](https://huggingface.co/learn/llm-course/). The [annotated references](docs/references.md) describe these and other sources, their roles, and reuse boundaries; primary papers and official documentation remain important for checking technical claims.

## Current state

The NumPy reference implements inference with a small, randomly initialized decoder-only GPT, plus loss, training-window, and decoding helpers. Its output demonstrates generation mechanics, not learned language quality. A complete tokenizer/corpus pipeline, training loop, and trained-model evaluation are still planned. See [project status](docs/project-status.md) for evidence and limitations.

## Run locally

You need Python 3.12 or later and [uv](https://docs.astral.sh/uv/). Core exercises use small inputs and run on CPU.

```bash
uv sync --locked --dev
uv run --locked pytest
uv run --locked python experiments/decoding-distribution/run.py
```

The last command compares decoding distributions for fixed synthetic logits. Its [report](reports/decoding-distribution.md) explains the baseline, results, and limits; it does not measure language quality.

The core implementation uses NumPy. The lockfile records the resolved Python dependencies; optional PyTorch support can be installed with `uv sync --locked --dev --extra ml`. Reusable code lives in `src/llm_lab/`, tests in `tests/`, and experiment definitions and evidence in `experiments/` and `reports/`. Notebooks are explanatory rather than the sole home of reusable logic.

## Render the site

Install [Quarto](https://quarto.org/docs/get-started/) separately; CI uses version 1.11.9. From the repository root:

```bash
uv run --no-project --with-requirements docs/requirements-history-validation.txt --python 3.12 python site/tools/build_learning_map.py
uv run --no-project --with-requirements docs/requirements-history-validation.txt --python 3.12 python site/tools/render_history_pilot.py
quarto render site
```

The first command validates the canonical page/concept metadata and generates the bilingual learning-map data and guided-route Markdown partials. The route is maintained in [`data/guided-route.yml`](data/guided-route.yml); the generated partials are tracked because Quarto expands their includes before project pre-render hooks run. The second command generates the bilingual history timeline includes. The site is written to `site/_site/`.

## Contribute

**Architecture and maintenance entry point:** [Information architecture and metadata governance](docs/information-architecture.md). It is the index for the canonical sources, their ownership boundaries, the generated projections, and the maintenance workflow. Use the [contributor guide](CONTRIBUTING.md) for the practical change workflow; detailed rules remain in their owning documents.

- Ownership, cross-document references, and update rules: [information architecture](docs/information-architecture.md). The map above is an index; the linked documents remain authoritative for their own subject.

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution modes, setup, Git hooks, and checks. The toolchain uses pytest for tests, Ruff for linting and formatting, mypy for type checking, pre-commit hooks, and GitHub Actions for Python and site checks. Passing these checks or rendering the site does not by itself establish scientific correctness, learner understanding, or visual quality.

The [roadmap](docs/roadmap.md) records priorities; the [information architecture](docs/information-architecture.md) indexes the metadata, page composition, and audit contracts. Site sources are in `site/`; project guidance and research notes are in `docs/`.

## License

Project code is released under the MIT License. CC BY-SA 4.0 applies only to original project-authored prose in Quarto pages and documentation; it excludes all visual assets whose rights are not established. Third-party materials retain their own terms. See [LICENSE.md](LICENSE.md), [licensing scope](docs/licensing-scope.md), and the [visual asset register](docs/visual-assets-register.md).
