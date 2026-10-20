# Learning path

This plan is a sequence of evidence-producing modules, not a promise of mastery after a fixed number of hours. Each module is complete only when its implementation, tests, experiment notes, and limitations are available.

## Module 0 — Mathematical and numerical foundations

**Learn:** vectors and matrices, logits and probabilities, log-sum-exp intuition, cross-entropy, derivatives, the chain rule, gradient descent, numerical stability.

**Build:** a small NumPy loss implementation and a finite-difference gradient check.

**Exit criteria:** explain tensor shapes and the loss reduction; pass tests for edge cases; show analytical gradients agree with numerical estimates within a justified tolerance.

## Module 1 — Text data and tokenization

**Learn:** Unicode, normalization, vocabulary construction, byte-pair encoding (BPE), special tokens, padding, truncation, sliding windows, next-token targets.

**Build:** a small tokenizer or a clearly scoped educational tokenizer adapter, plus a deterministic dataset/window builder.

**Exit criteria:** round-trip tests where applicable, explicit special-token behavior, no accidental train/validation overlap, and documented limitations versus production tokenizers.

## Module 2 — Attention and Transformer blocks

**Learn:** embeddings, positional information, queries/keys/values, scaled dot-product attention, causal masks, multi-head attention, residual connections, normalization, feed-forward blocks.

**Build:** small, composable PyTorch modules with explicit tensor shapes and tests.

**Exit criteria:** causal masking prevents future-token influence; forward and backward passes are finite; shape and gradient tests cover important boundary cases.

## Module 3 — Small GPT and pre-training

**Learn:** autoregressive objective, batching, optimizer, learning-rate schedule, gradient clipping, validation loss, perplexity, checkpointing, text generation.

**Build:** a tiny GPT trained on a small, documented corpus.

**Exit criteria:** deterministic configuration and seed, separate train/validation data, saved training curves, a generation example, and honest discussion of model/data limitations.

## Module 4 — Reference comparison

**Learn:** parameter naming, initialization, tokenizer compatibility, checkpoint loading, numerical tolerances, optimized attention.

**Build:** compare selected outputs with a trusted reference implementation where architecture and preprocessing match.

**Exit criteria:** documented matching conditions, numerical comparison, and an explanation of any discrepancies. Do not claim equivalence when tokenization or architecture differs.

## Module 5 — Supervised fine-tuning (SFT)

**Learn:** instruction formats, target masking, sequence packing, data quality, overfitting, catastrophic forgetting, evaluation-set design.

**Build:** a small SFT run with a fixed, held-out evaluation set and a baseline.

**Exit criteria:** training and evaluation examples are separated before learned preprocessing or selection; report regressions and examples, not only aggregate scores.

## Module 6 — LoRA, quantization, and memory

**Learn:** low-rank updates, rank/alpha/dropout, adapter targeting, quantization, activation and optimizer memory, throughput and latency.

**Build:** compare a baseline with an adapter-based fine-tune under a measured resource budget.

**Exit criteria:** record model, tokenizer, data, configuration, device, peak memory, runtime, quality, and trade-offs. Distinguish LoRA from quantization and QLoRA.

## Module 7 — Preference optimization

**Learn:** preference pairs, reward modeling concepts, DPO objective, SFT versus preference optimization, preference-data bias.

**Build:** a small controlled experiment or a fully specified simulation if hardware/data make training inappropriate.

**Exit criteria:** explain the objective, establish a baseline, and examine regressions and preference-data limitations.

## Module 8 — Evaluation, efficiency, and robustness

**Learn:** task-specific metrics, calibration where relevant, confidence intervals, repeated runs, ablations, contamination, leakage, distribution shift, prompt sensitivity, safety and failure analysis.

**Build:** an evaluation harness with versioned tasks and machine-readable outputs.

**Exit criteria:** report baseline and ablations, uncertainty or run-to-run variability, data provenance, limitations, and representative errors. Never infer real-world utility from one benchmark score.

## Suggested 12-week cadence

At approximately 10 hours per week, use weeks 1–2 for foundations and tokenization; 3–4 for attention and the Transformer; 5–6 for training; 7 for reference comparison; 8–9 for SFT; 10 for LoRA/quantization; 11 for ablations and reproducibility; and 12 for documentation and portfolio review. Adjust the schedule based on failed exit criteria rather than moving on automatically.
