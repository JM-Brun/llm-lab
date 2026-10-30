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

At **five focused hours per week**, using sessions of no more than 60 minutes, treat the following 12-week outline as an illustrative sequence rather than a deadline or mastery promise: weeks 1–2 for foundations and tokenization; weeks 3–4 for attention and the Transformer only after the foundational gate in #82 is explicitly cleared; weeks 5–6 for training; week 7 for reference comparison; weeks 8–9 for SFT; week 10 for LoRA/quantization; week 11 for ablations and reproducibility; and week 12 for documentation and portfolio review. These week labels are provisional and may stretch substantially; do not advance while exit criteria remain unmet or compensate for missed time by exceeding the weekly or session limit.


## 2026-10-29 — End-to-end GPT build route and evidence gates

This section makes the guided path operational while preserving the current prerequisite gate. It does not authorize downstream implementation before the active foundational slice and private knowledge review are complete. It is a route specification and status snapshot, not a claim that the build is already executable.

### Two distinct learning routes

- **Core from-scratch route:** implement a small decoder-only GPT from randomly initialized parameters, train it on a documented manageable corpus, validate it, save a checkpoint, and generate text. This is the defining end-to-end construction outcome.
- **Pretrained adaptation route:** load a compatible pretrained checkpoint and tokenizer, then adapt/evaluate the model for classification or instruction following; later explore LoRA and quantization. This route starts from learned parameters and is not a substitute for the from-scratch route.

The routes share foundations (text, tokenization, tensors, architecture, prediction and evaluation) but diverge at initialization and training objective.

### Guided build milestones

| ID | Learner question and milestone | Prerequisites | Expected learner artifact / evidence | Current public evidence and status | Owner |
|---|---|---|---|---|---|
| G0 | **What are we building?** Understand an autoregressive decoder-only GPT, next-token prediction, and the boundary between model, tokenizer, data and inference. | Basic programming and elementary linear algebra/probability. | Correct component/data-flow explanation; distinguish GPT-style decoder-only models from all LLMs and encoder–decoder Transformers. | Transformer overview, landing pages, glossary and history exist; full LLM-family/lifecycle coverage is partial. | #108, #130 |
| G1 | **How does raw text become model input?** Unicode/text normalization, tokenizer, vocabulary, token IDs and special tokens. | Strings, bytes and basic data handling. | Trace one text example through a tokenizer; state tokenizer identity/version and special-token behavior. | Text/data, Unicode and tokenization pages exist; source/resource and transition work remains active. | #82, #114 |
| G2 | **How are examples formed?** Context windows, shifted input/target sequences, batching, padding/truncation and data splits. | G1; tensor indexing. | Deterministic batch with aligned inputs/targets; tests for off-by-one errors, boundaries and train/validation separation. | Training examples page exists; corpus-to-examples implementation is separately tracked. Do not duplicate #58 or revive #83 without a distinct gap. | #58, #78 |
| G3 | **How do tokens become vectors?** Tensor shapes, embedding-table lookup, positional information and the difference between input embeddings and contextualized states. | G1–G2; vector/matrix and indexing basics. | Trace shapes from token IDs [B,L] to vectors [B,L,d]; explain absolute position embeddings versus RoPE. | Conceptual chain is the active #82 slice; worked example and shape explanation exist, but iteration 3 validation must be completed before treating the slice as closed. | #82 |
| G4 | **How does the model mix context?** Q/K/V, scaled dot-product attention, causal masking and multi-head attention. | G3; matrix multiplication, softmax and tensor dimensions. | Explain and test that a position cannot use future tokens; show head split/merge shapes and train/eval behavior for dropout. | Conceptual Q/K/V, attention and causal-mask pages exist; implementation-level shape/invariant evidence remains incomplete. | #79–#81, #78 |
| G5 | **What is a GPT block?** Assemble attention, residual paths, normalization, feed-forward network, positional mechanism and output projection in the selected order. | G3–G4; module composition and initialization concepts. | Documented block diagram and shape trace; parameter-count sanity check; forward/backward tests and explicit configuration. | Transformer overview explains components conceptually; a complete tested GPT implementation is not evidenced. | #78, then scoped architecture issue |
| G6 | **What is the learning objective?** Align shifted targets, obtain vocabulary logits, compute token-level cross-entropy and reduce the loss correctly. | G2, G5; logits, log probabilities and gradients. | Hand-checkable loss example; tests for target alignment, ignored/padded targets, numerical stability and reduction semantics. | Logits, likelihood, entropy, cross-entropy, loss and gradients pages exist; full model/data integration is not evidenced. | #58, #79 |
| G7 | **How do parameters learn?** Backpropagation, optimizer updates, learning-rate schedule, clipping, validation, checkpointing and reproducibility. | G5–G6; PyTorch/autograd basics. | Reproducible small training run with fixed configuration/seed, train/validation curves, checkpoint and documented limitations. | No complete end-to-end pretraining run is evidenced in the public learning path. | Future pretraining issue after prerequisite review |
| G8 | **How does the model generate?** Autoregressive decoding, sampling, temperature/top-k/top-p, stopping and context-window constraints. | G5 and a trained/checkpointed model (G7). | Generation script with deterministic and sampled modes; tests for stopping/context limits; documented decoding configuration. | No complete public generation module/run is evidenced. | #84 |
| G9 | **How do we know the build is correct?** Compare against a reference only when architecture, tokenizer, weights and preprocessing match. | G5–G8. | Numerical comparison with stated tolerances, parameter/config checks and explanation of mismatches. | Reference comparison is planned; no complete comparison evidence is claimed. | Existing Module 4 in this document |
| A1 | **How do we reuse pretrained weights?** Checkpoint formats, parameter-name mapping, tokenizer compatibility and inference. | G5, G9; checkpoint and state-dict concepts. | Load a known compatible checkpoint; verify parameter coverage and selected outputs. | Upstream coverage requirement; no complete public bilingual learning module evidenced. | Full curriculum plan / future issue |
| A2 | **How do we adapt a model for classification?** Add a task head, fine-tune, compare to a baseline and inspect errors. | A1; supervised learning and evaluation design. | Held-out evaluation, baseline, metrics and error analysis. | Gap; no complete public module/validated implementation evidenced. | Full curriculum plan / future issue |
| A3 | **How do we teach instruction following?** Format instruction data, mask prompt tokens appropriately, batch/pack examples, supervised fine-tune and evaluate. | A1; G2/G6; data quality and leakage discipline. | Reproducible SFT run, held-out prompts, baseline and qualitative/quantitative error analysis. | Gap; no complete public bilingual module evidenced. | Full curriculum plan / future issue |
| A4 | **How can adaptation become more efficient?** LoRA, adapter targeting, rank/alpha, quantization and QLoRA trade-offs. | A3; matrix factorization and memory accounting. | Controlled baseline-versus-adapter comparison with quality, memory, runtime and configuration. | Gap/advanced extension; do not conflate LoRA with quantization or QLoRA. | Full curriculum plan / future issue |
| E1 | **How do we evaluate claims and limitations?** Metrics, calibration where appropriate, contamination, leakage, distribution shift, ablations and uncertainty. | Evaluation design; task-specific prerequisites. | Versioned evaluation protocol, baseline, ablations, representative errors and limitations. | Experimental evaluation and critical-reading pages exist; reusable end-to-end evaluation harness is not evidenced. | #78 and evaluation follow-ups |

**Status vocabulary:** *Exists* means a public page or issue exists; *partial* means the learning outcome is only partly explained or evidenced; *gap* means the route/artifact is not yet present. None of these statuses implies passing CI, rendered browser review or learner mastery.

### Dependency order and safe stopping points

The first complete build should follow:

G0 → G1 → G2 → G3 → G4 → G5 → G6 → G7 → G8 → G9

- Readers may explore G0 and concept deep dives non-linearly.
- G1–G3 form the text-to-representation foundation; G3 is the active content gate under #82.
- G4 and later implementation milestones remain planned until the active gate is complete and the private prerequisite review permits implementation.
- A1–A4 are a separate downstream adaptation branch. They must not be inserted into the from-scratch sequence as if pretrained fine-tuning were how a randomly initialized GPT learns.
- E1 is cross-cutting: evaluation design should be introduced before experiments, not postponed until the final module.

### Evidence required before calling the core route complete

A public “build a GPT from scratch” claim is justified only when all of the following are present and linked from the relevant milestones:

1. **Data:** documented corpus provenance/licence, deterministic preprocessing, tokenizer identity, train/validation split, and batch/target tests.
2. **Architecture:** explicit configuration, parameter count, tensor-shape trace, component ordering, initialization and train/eval semantics.
3. **Objective:** correctly aligned next-token targets, numerically stable loss, documented reduction/masking and tests.
4. **Optimization:** optimizer and schedule configuration, gradient handling, reproducible training loop, validation and checkpointing.
5. **Generation:** checkpoint loading, autoregressive loop, decoding configuration, stopping behavior and an inspectable example.
6. **Verification:** tests and a documented run with limitations; reference comparison only under compatible conditions.
7. **Publication:** EN/FR conceptual parity, working local links, successful Quarto build, desktop/mobile browser review and a clear distinction between source, execution, visual and learning evidence.

A diagram, pseudocode, isolated loss example or conceptual Transformer page is useful preparation, but none alone satisfies the end-to-end build criterion.

### Coordination with existing work

- #82 remains the active foundational slice; finish its adversarial validation and bilingual/render checks before advancing the implementation sequence.
- #58 owns corpus windows and training examples; #83 must not duplicate it.
- #79–#81 own logits/loss, attention and causal masking. Keep their scope bounded and preserve prerequisite order.
- #84 owns generation and its evaluation limitations.
- #78 owns the concept-to-code inventory and page-level evidence; this table provides the end-to-end learner route, not a replacement for that inventory.
- #87 owns the three-depth curriculum relationships; #130 coordinates high-level navigation and coverage.
- Appendix/bonus scope and upstream chapter statuses remain in [the full curriculum coverage plan](full-curriculum-plan.md#8-upstream-repository-inventory-refresh-2026-10-29).

Do not open parallel issues for milestones already owned above. Create a new issue only when a real gap has no existing owner, and keep implementation gated by the private acquired/to-review/missing knowledge review.
