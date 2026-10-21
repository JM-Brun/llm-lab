# LLM Lab

A reproducible, code-first lab for understanding how language models work—from tokenization and attention to pre-training, fine-tuning, evaluation, and efficiency.

The goal is not to train a production-scale LLM from scratch. It is to implement small, inspectable components, test their mathematical properties, run controlled experiments, and document what the evidence does and does not show.

## Learn through the Quarto site

The project includes a bilingual Quarto website organized into three layers: overview pages that connect concepts, dedicated concept pages that explain one idea in depth, and implementation/tests referenced when they exist. Pages explicitly distinguish verified code from planned work.

- French introduction: `site/index.qmd`
- English introduction: `site/en/index.qmd`
- Transformer overview: `site/fr/transformer.qmd` and `site/en/transformer.qmd` (high-level synthesis, not a detailed concept chapter)
- Dedicated attention concepts: Q/K/V, scaled dot-product attention, and causal masking, each with French and English pages under `site/fr/` and `site/en/`
- Entropy, uncertainty, and compression: `site/fr/entropy.qmd` and `site/en/entropy.qmd`
- Cross-entropy and KL divergence: `site/fr/cross-entropy.qmd` and `site/en/cross-entropy.qmd`
- Critical notes on cosine similarity: `site/fr/cosine-similarity.qmd` and `site/en/cosine-similarity.qmd`
- Critical notes on embedding linearity: `site/fr/linearite-embeddings.qmd` and `site/en/embedding-linearity.qmd`
- Visual references and image provenance: `site/references.qmd`
- Prioritized roadmap and acceptance criteria: [`docs/roadmap.md`](docs/roadmap.md)

The site uses carefully attributed illustrations embedded from their original source when suitable. It does not mirror or redistribute external image files. An accessible URL is not a licence: check reuse terms before copying or modifying a figure. The site can be rendered locally with the [Quarto CLI](https://quarto.org/docs/get-started/).

```bash
quarto render site
```

The rendered site is written to `site/_site/`. The Quarto CLI is a separate system dependency; it is not installed by `uv`.

## Learning principles

- **Understand before scaling:** start with small tensors, toy corpora, and small models.
- **Verify implementations:** test shapes, masks, gradients, and numerical behavior.
- **Measure rather than assume:** record baselines, seeds, compute costs, limitations, and failure cases.
- **Keep experiments reproducible:** version code, configuration, data provenance, and evaluation procedures.
- **Separate teaching from performance:** readable reference implementations first; optimized kernels and libraries as comparisons.
- **Use public, appropriately licensed data:** document provenance and avoid committing datasets, model weights, credentials, or generated artifacts.

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

See [the learning path](docs/learning-path.md) for module-level objectives, the [roadmap](docs/roadmap.md) for priorities and acceptance criteria, and the [experiment protocol](docs/experiment-protocol.md) for reporting requirements.

## Repository layout

- `src/llm_lab/`: reusable, typed Python implementations.
- `tests/`: unit and numerical tests.
- `notebooks/`: optional explanatory notebooks; core logic should remain importable from `src`.
- `experiments/`: versioned configurations and runnable experiment entry points.
- `reports/`: concise, evidence-backed results and limitations.
- `docs/`: learning path, mathematical foundations, experiment protocol, annotated references, and roadmap.
- `site/`: Quarto website sources in French and English.

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

## Hardware policy

Core exercises should run on CPU with small inputs. Later experiments may offer PyTorch CPU/MPS/CUDA or MLX alternatives where appropriate. No module should require a large GPU just to understand the concept. Record device, software versions, runtime, and peak memory for performance claims.

## Research and references

The project builds on existing educational work rather than presenting established techniques as original. See [the annotated references](docs/references.md) and [the Quarto figure provenance page](site/references.qmd). Each experiment should cite the method, implementation, dataset, and evaluation setup it uses.

## Status

Current scope: a bilingual Quarto learning site, a tested NumPy cross-entropy implementation, and automated Python/Quarto checks. Transformer and training modules remain planned; see [`docs/roadmap.md`](docs/roadmap.md) for verified status, priorities, and completion criteria. Passing CI verifies configured checks, not research claims or visual quality.

## License

No license has been selected yet. Until a license is added, do not assume that others have permission to reuse, modify, or redistribute this repository's code.
