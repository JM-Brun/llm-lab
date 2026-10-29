# Learning path

This plan is a sequence of evidence-producing modules, not a promise of mastery after a fixed number of hours. Each module is complete only when its implementation, tests, experiment notes, and limitations are available. The repository's current status, priorities, and acceptance criteria are tracked in the [roadmap](roadmap.md).

## Reader-facing map: overview → guided path → deep dives

This first-pass crosswalk connects the existing homepage's six questions to the guided modules and canonical public pages. It is a navigation aid, not evidence that every linked concept has a reusable implementation, has passed browser review, or has been mastered. The source-level review is tracked in [issue #87](https://github.com/JM-Brun/llm-lab/issues/87) and coordinated with [the high-level audit #130](https://github.com/JM-Brun/llm-lab/issues/130).

| Homepage question | Guided-path connection | Existing canonical pages (FR / EN) | Status and owner |
|---|---|---|---|
| **What does the model receive?** Text, tokens, context, inputs and targets. | Module 1 — text data and tokenization; connect to training examples before discussing the loss. | [Texte et données](../site/fr/text-data.qmd) / [Text and data](../site/en/text-data.qmd); [Exemples d'entraînement](../site/fr/training-examples.qmd) / [Training examples](../site/en/training-examples.qmd); [Unicode](../site/fr/unicode-text.qmd) / [Unicode](../site/en/unicode-text.qmd). | The overview and deep dives exist. The text-to-representation bridge remains the active review slice: [#82](https://github.com/JM-Brun/llm-lab/issues/82); source/resource audit: [#114](https://github.com/JM-Brun/llm-lab/issues/114). |
| **What does it compute?** Tensors, embeddings, logits and probabilities. | Modules 0–2 — numerical foundations and representations before attention. | [Tenseurs](../site/fr/tensors.qmd) / [Tensors](../site/en/tensors.qmd); [Espace des embeddings](../site/fr/embedding-space.qmd) / [Embedding space](../site/en/embedding-space.qmd); [Logits](../site/fr/logits.qmd) / [Logits](../site/en/logits.qmd); [Probabilités](../site/fr/probabilites.qmd) / [Probabilities](../site/en/probabilities.qmd). | Concept pages exist; page-specific implementation/test coverage must be checked in [#78](https://github.com/JM-Brun/llm-lab/issues/78). IDs are indices, not coordinates; embedding lookup alone does not contextualize a token. |
| **How does it learn?** Likelihood, cross-entropy, loss and gradients. | Module 0 — derive the objective and validate the gradient before a training loop. | [Vraisemblance](../site/fr/vraisemblance.qmd) / [Likelihood](../site/en/likelihood.qmd); [Entropie croisée](../site/fr/cross-entropy.qmd) / [Cross-entropy](../site/en/cross-entropy.qmd); [Loss](../site/fr/loss.qmd) / [Loss](../site/en/loss.qmd); [Gradients](../site/fr/gradients.qmd) / [Gradients](../site/en/gradients.qmd). | Explanations and a small tested NumPy loss implementation exist according to the repository roadmap; do not infer that a complete model-training path exists. Check each claim against tests and the roadmap before extending it. |
| **How does it use context?** Attention, causal masking, position and Transformer blocks. | Module 2 — attention and Transformer blocks, after the text-to-representation prerequisites. | [Transformer](../site/fr/transformer.qmd) / [Transformer](../site/en/transformer.qmd); [Q/K/V](../site/fr/queries-keys-values.qmd) / [Q/K/V](../site/en/queries-keys-values.qmd); [Attention](../site/fr/scaled-dot-product-attention.qmd) / [Attention](../site/en/scaled-dot-product-attention.qmd); [Masque causal](../site/fr/causal-masking.qmd) / [Causal masking](../site/en/causal-masking.qmd); [Position / RoPE](../site/fr/positional-encoding.qmd) / [Position / RoPE](../site/en/positional-encoding.qmd). | Overview and concept pages exist. The concept-to-code roadmap owns implementation sequencing; attention and masking remain later slices [#80](https://github.com/JM-Brun/llm-lab/issues/80) / [#81](https://github.com/JM-Brun/llm-lab/issues/81). Do not advance them while #82 remains open. |
| **How does it generate text?** Training, validation, decoding and evaluation. | Module 3 — small GPT and pre-training; later connect to Module 8 evaluation. | [Évaluation expérimentale](../site/fr/evaluation-experimentale.qmd) / [Experimental evaluation](../site/en/experimental-evaluation.qmd); use the Transformer overview for the system-level context. | A complete tiny-GPT implementation and documented training run are **not yet demonstrated** in the roadmap. Treat generation/training as planned until code, tests, configuration, validation results and limitations are evidenced. |
| **When does it fail or generalize poorly?** Leakage, metrics, uncertainty, ablations and representation limits. | Module 8 — evaluation, efficiency and robustness; critical-reading pages can be explored independently. | [Évaluation expérimentale](../site/fr/evaluation-experimentale.qmd) / [Experimental evaluation](../site/en/experimental-evaluation.qmd); [Similarité cosinus](../site/fr/cosine-similarity.qmd) / [Cosine similarity](../site/en/cosine-similarity.qmd); [Linéarité des embeddings](../site/fr/linearite-embeddings.qmd) / [Embedding linearity](../site/en/embedding-linearity.qmd). | Critical pages exist, but the roadmap records the underlying reproducible experiments as not yet demonstrated. Do not present a critique page as experimental validation. |

### How to use this map

- **Panorama:** start at the [French landing page](../site/index.qmd) or [English landing page](../site/en/index.qmd), then use the linked Transformer overview for system context.
- **Guided build:** follow the module sequence below, but stop at unmet exit criteria. The current active gate is #82; this map does not authorize jumping ahead to attention, full-GPT implementation, or training.
- **Deep dives:** enter any canonical concept page directly. Follow only genuinely essential prerequisites, and use its links back to the overview or implementation where available.
- **Status discipline:** “page exists,” “source checked,” “code executes,” “CI passes,” “rendered desktop/mobile reviewed,” and “learner can transfer the idea” are separate states. Update the owner issue with evidence instead of inferring one from another.

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

## Critical reading: test default assumptions

The bilingual notes on [cosine similarity](../site/fr/cosine-similarity.qmd) and the [linearity hypothesis](../site/fr/linearite-embeddings.qmd) are cross-cutting modules, not replacements for the implementation sequence above. Use them to practise stating assumptions, finding counterexamples, designing controls, and distinguishing decodability from causal use. Their proposed experiments should be considered complete only when the protocol and results are committed under `experiments/` and summarized under `reports/`.

## Suggested 12-week cadence

At approximately 10 hours per week, use weeks 1–2 for foundations and tokenization; 3–4 for attention and the Transformer; 5–6 for training; 7 for reference comparison; 8–9 for SFT; 10 for LoRA/quantization; 11 for ablations and reproducibility; and 12 for documentation and portfolio review. Adjust the schedule based on failed exit criteria rather than moving on automatically.
