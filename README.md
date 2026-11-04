# LLM Lab

LLM Lab is a bilingual, code-first learning project for understanding language models. It connects explanations and mathematical reasoning to small, inspectable implementations and reproducible experiments.

**[Explore LLM Lab in French](https://jm-brun.github.io/llm-lab/) · [Explore in English](https://jm-brun.github.io/llm-lab/en/)**

The NumPy reference implements inference with a small, randomly initialized decoder-only GPT. A complete tokenizer/corpus pipeline, training loop, and trained-model evaluation are still planned. See [project status](docs/project-status.md) for the evidence and limits behind each part.

## Run locally

You need Python 3.12 or later and [uv](https://docs.astral.sh/uv/). Core code runs on CPU.

```bash
uv sync --locked --dev
uv run --locked pytest
uv run --locked python experiments/decoding-distribution/run.py
```

The last command compares decoding distributions for fixed synthetic logits. Its [report](reports/decoding-distribution.md) explains the baseline, results, and limits; it does not measure language quality.

For optional deep-learning dependencies, run `uv sync --locked --dev --extra ml`. The committed [lockfile](uv.lock) records the resolved Python dependencies.

## Render the site

Install [Quarto](https://quarto.org/docs/get-started/) separately; CI uses version 1.11.9. From the repository root:

```bash
uv run --no-project --with-requirements docs/requirements-history-validation.txt --python 3.12 python scripts/render_history_pilot.py
quarto render site
```

The first command generates the bilingual timeline includes; the site is written to `site/_site/`.

## Contribute

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution modes, checks, and editorial conventions. The [learning path](docs/learning-path.md) defines the curriculum, and the [experiment protocol](docs/experiment-protocol.md) describes how to record evidence. Passing tests or a successful render does not by itself establish scientific correctness, learner understanding, or visual quality.

## License

Project-owned code is offered under MIT and project-owned prose under CC BY-SA 4.0. Third-party materials and images with unresolved provenance are excluded; see [LICENSE.md](LICENSE.md) and the [visual-assets register](docs/visual-assets-register.md).
