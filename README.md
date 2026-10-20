# LLM Lab

A reproducible, code-first lab for understanding how language models work—from tokenization and attention to pre-training, fine-tuning, evaluation, and efficiency.

The goal is not to train a production-scale LLM from scratch. It is to implement small, inspectable components, test their mathematical properties, run controlled experiments, and document what the evidence does and does not show.

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

See [the learning path](docs/learning-path.md) for module-level objectives and [the experiment protocol](docs/experiment-protocol.md) for reporting requirements.

## Repository layout

- `src/llm_lab/`: reusable, typed Python implementations.
- `tests/`: unit and numerical tests.
- `notebooks/`: optional explanatory notebooks; core logic should remain importable from `src`.
- `experiments/`: versioned configurations and runnable experiment entry points.
- `reports/`: concise, evidence-backed results and limitations.
- `docs/`: learning path, foundations, experiment protocol, and references.

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

The project builds on existing educational work rather than presenting established techniques as original. See [the annotated references](docs/references.md). Each experiment should cite the method, implementation, dataset, and evaluation setup it uses.

## Status

Initial repository scaffold. The first implementation is a small, tested cross-entropy loss and numerical gradient check; model components will be added incrementally.

## License

No license has been selected yet. Until a license is added, do not assume that others have permission to reuse, modify, or redistribute this repository's code.
