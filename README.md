# LLM Lab

A reproducible, code-first lab for understanding how language models work—from tokenization and attention to pre-training, fine-tuning, evaluation, and efficiency.

The goal is not to train a production-scale LLM from scratch. It is to implement small, inspectable components, test their mathematical properties, run controlled experiments, and document what the evidence does and does not show.

## Quick start

Requirements: Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync --dev
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy src
```

Install the optional deep-learning dependencies when a module needs them:

```bash
uv sync --dev --extra ml
```

Install the Git hooks once per clone:

```bash
uv run pre-commit install
uv run pre-commit run --all-files
```

The first `uv sync` creates or updates `uv.lock`; commit that file so collaborators and CI can reproduce the resolved environment.

## Learn through the Quarto site

The project includes a bilingual Quarto website organized around LLM-specific explanations.

- **French introduction:** [`site/index.qmd`](site/index.qmd)
- **English introduction:** [`site/en/index.qmd`](site/en/index.qmd)
- **Roadmap and priorities:** [`docs/roadmap.md`](docs/roadmap.md)

Generate the bilingual history fragments, then render the site locally with the [Quarto CLI](https://quarto.org/docs/get-started/):

```bash
uv run --no-project --with-requirements docs/requirements-history-validation.txt python site/tools/render_history_pilot.py
quarto render site
```

The generator writes fragments under `site/includes/`; the rendered site is written to `site/_site/`. The Quarto CLI is a separate system dependency; it is not installed by `uv`.

## Repository layout

- `src/llm_lab/foundations/`: tested numerical reference components for the learning path. These are not a complete LLM.
- `src/llm_lab/minimal/`: reserved for the smallest end-to-end teaching model and its training and generation code; the model is not implemented yet.
- `src/llm_lab/advanced/`: reserved for learning-path extensions and experiments beyond that minimal build.
- `tests/unit/`: numerical tests for learning-path code; `tests/site/`: tests for site behavior and tooling.
- `notebooks/`: optional explanatory notebooks; core logic should remain importable from `src`.
- `experiments/`: versioned configurations and runnable experiment entry points.
- `reports/`: concise, evidence-backed results and limitations.
- `docs/`: learning path, mathematical foundations, experiment protocol, annotated references, and roadmap.
- `site/`: Quarto website sources in French and English; `site/tools/` contains site generation and validation scripts, separate from the installable learning package.

The minimal build should be understandable and runnable without importing advanced extensions or site tooling. Advanced learning code may build on the minimal model; site tooling belongs under `site/tools/` and is not part of the `llm_lab` package. Shared numerical reference components remain in `foundations/` until a real implementation establishes what it needs.

## Learning path

The path is deliberately incremental. Modules can be revisited when tests or experiments expose gaps.

| Stage | Focus | Evidence to produce |
| --- | --- | --- |
| 0 | Mathematical and numerical foundations | Loss and gradients checked against finite differences |
| 1 | Text data and tokenization | Tested encode/decode, special tokens, and input-target windows |
| 2 | Attention and Transformer blocks | Shape, causal-mask, and gradient tests |
| 3 | A small GPT and pre-training loop | Training/validation curves and reproducible generation |
| 4 | Reference implementation and pretrained weights | Numerical comparisons and a documented discrepancy analysis |
| 5 | Supervised fine-tuning (SFT) | Fixed evaluation set and before/after error analysis |
| 6 | LoRA, quantization, and memory trade-offs | Quality, memory, latency, and cost comparisons |
| 7 | Preference optimization | Controlled experiment distinguishing SFT from preference learning |
| 8 | Evaluation, efficiency, and robustness | Baselines, ablations, uncertainty, limitations, and failure analysis |

See [the learning path](docs/learning-path.md), [the roadmap](docs/roadmap.md), and [the experiment protocol](docs/experiment-protocol.md) for details.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution modes, acceptance criteria, and editorial conventions. Core exercises should run on CPU with small inputs; record device, software versions, runtime, and peak memory for performance claims.

## Status

Current scope: a bilingual Quarto learning site, tested NumPy attention and cross-entropy reference components, and automated Python/Quarto checks. A complete Transformer and training loop remain planned; see [`docs/roadmap.md`](docs/roadmap.md) for verified status, priorities, and completion criteria. Passing CI verifies configured checks, not research claims or visual quality.

## License

Code is released under the [MIT License](LICENSE.md). Content (Quarto pages, documentation, and illustrations) is released under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). See [LICENSE.md](LICENSE.md) for full details.
