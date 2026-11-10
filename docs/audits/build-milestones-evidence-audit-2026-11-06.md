# Build milestone implementation-evidence audit — 2026-11-06

**Repository:** `JM-Brun/llm-lab`  
**Baseline:** `main`, inspected 2026-11-06  
**Scope:** G0–G9 implementation evidence for the from-scratch decoder-only GPT route.  
**Method:** inspect source modules, corresponding unit tests, bilingual Build pages and `docs/learning-path.md`. This is an implementation-evidence audit, not a scientific peer review or learner assessment.

## Executive result

The public reference implementation supports a meaningful **inference-only GPT build** through G7. It does not yet support a trained GPT build.

| Milestone | Evidence status | What is actually present |
|---|---|---|
| G0 — system scope | Conceptual | Bilingual system overview and architecture explanations; no code criterion. |
| G1 — text to token IDs | Conceptual only | Lessons and tokenizer references; no tokenizer or text↔ID pipeline in the reference package. |
| G2 — training examples | Partial | Tested sliding input/target windows; no corpus pipeline, split manager, batching, padding, packing or loss masks. |
| G3 — embeddings and positions | Implemented in GPT | Token lookup and learned absolute positions in `GPT`; model-level shape and reproducibility tests. No standalone embedding module or RoPE implementation. |
| G4 — attention | Implemented in block | Q/K/V projections, scaled dot-product attention, causal mask, explicit head split/merge and output projection; unit tests include prefix invariance. |
| G5 — assembled GPT | Implemented, inference-only | Pre-LN Transformer block stack, final normalization and vocabulary projection; shape, finite-output, configuration and parameter-count tests. |
| G6 — prediction and selection | Implemented | Logits are converted to a temperature-scaled distribution and selected greedily or by sampling; optional top-k/top-p filters. |
| G7 — autoregressive generation | Implemented, bounded | Fixed-parameter loop, seeded sampling and sliding context window. No EOS/early stopping, KV cache or checkpoint loader. |
| G8 — parameter learning | Partial primitives only | Shifted examples, cross-entropy and analytical gradient with respect to logits. No gradient through GPT weights, optimizer, parameter update, training loop, validation runner or checkpoint. |
| G9 — reference verification | Specification only | Local invariant tests exist; no parity test against an independent compatible reference is evidenced. |

## Evidence by milestone

### G0 — define the system

**Public evidence**
- `site/{fr,en}/llm-overview.qmd`
- `site/{fr,en}/transformer.qmd`
- `docs/learning-path.md`

**Boundary:** conceptual orientation only. Do not infer code coverage or learner mastery from the existence of these pages.

### G1 — text and tokenization

**Public evidence**
- `site/{fr,en}/text-data.qmd`
- `site/{fr,en}/tokenization-strategies.qmd`
- Optional depth: Unicode and tokenizer design/evaluation pages.

**Implementation finding:** the reference GPT receives integer token IDs directly. The inspected `src/llm_lab/foundations` package has no tokenizer, vocabulary construction, text-to-ID encoder, ID-to-text decoder or special-token pipeline. Corpus preparation is also not implemented as an end-to-end pipeline.

### G2 — training examples

**Implementation**
- `src/llm_lab/foundations/training_examples.py`: `sliding_input_target_pairs`.
- `tests/unit/test_training_examples.py`.

**Verified scope:** one-token-shifted input/target windows, stride and boundary behavior.

**Not evidenced:** corpus ingestion/provenance, train/validation partition management, batching/packing, padding, attention masks or loss masks. The primitive must not be described as a complete data pipeline.

### G3 — embeddings and positions

**Implementation**
- `src/llm_lab/foundations/gpt.py`: token embedding lookup and learned absolute position embeddings.
- `tests/unit/test_gpt.py`: output shape, finite logits, seed reproducibility and parameter-count formula.

**Boundary:** these operations are part of the assembled GPT, not a separately reusable embedding component. RoPE is conceptual/advanced content, not implemented by this reference GPT.

### G4 — attention

**Implementation**
- `src/llm_lab/foundations/attention.py`: causal mask, scaled dot-product attention and stable softmax.
- `src/llm_lab/foundations/transformer_block.py`: Q/K/V projections from the block input, per-head slices, attention aggregation and output projection.
- `tests/unit/test_attention.py`, `tests/unit/test_transformer_block.py`, `tests/unit/test_gpt.py`.

**Verified scope:** mask structure, attention behavior, block output shape/finite values, head-count validation and prefix invariance under future-token extension.

**Boundary:** this NumPy implementation has no dropout or train/eval mode switch. Do not put dropout-mode behavior in the acceptance criteria for this implementation.

### G5 — assembled GPT

**Implementation**
- `src/llm_lab/foundations/gpt_config.py`: immutable validated dimensions.
- `src/llm_lab/foundations/gpt_ops.py`: linear operations, initialization, layer normalization and GELU.
- `src/llm_lab/foundations/transformer_block.py`: pre-LN attention and MLP residual branches.
- `src/llm_lab/foundations/gpt.py`: embeddings, block stack, final norm and vocabulary projection.
- Tests: `test_gpt_config.py`, `test_gpt_ops.py`, `test_transformer_block.py`, `test_gpt.py`.

**Boundary:** the assembled model is a tested forward-pass reference, not a trainable end-to-end GPT. It uses NumPy/float64 and seeded random initialization.

### G6–G7 — prediction and generation

**Implementation**
- `src/llm_lab/foundations/generate.py`
- `src/llm_lab/foundations/decoding_filters.py`
- Tests: `test_generate.py`, `test_decoding_filters.py`.

**Verified scope:** greedy decoding, reproducible sampling, temperature, optional top-k/top-p truncation, `max_new_tokens` bound and sliding context window.

**Explicit limitations:** no KV cache, no EOS/early-stopping rule, no configurable processor chain and no checkpoint loader. The educational reference emits token IDs; a compatible tokenizer is required to interpret them as text.

### G8 — parameter learning

**Implementation**
- `src/llm_lab/foundations/losses.py`: mean cross-entropy from logits and gradient with respect to logits.
- `src/llm_lab/foundations/training_examples.py`: shifted windows.
- Tests: `test_losses.py`, `test_training_examples.py`.

**Verified scope:** numerical loss and its derivative with respect to logits, including a finite-difference check.

**Critical gap:** no chain-rule propagation from logits into GPT parameters, no autograd, optimizer, gradient handling, parameter update, training loop, held-out validation runner or checkpoint. A loss-gradient primitive is not a training implementation.

### G9 — implementation verification

**Current evidence:** local unit tests verify selected invariants and expected outputs. They do not establish parity with an independent reference implementation.

**Required for a future parity claim:** pin a compatible reference and compare only after matching architecture/configuration, tokenizer and special-token behavior, parameter values/weights, input preprocessing and numerical precision. Report tolerances and intermediate comparisons. If the object under test is a trained checkpoint, G8 and a compatible checkpoint are additional prerequisites.

G9 is not E1. G9 asks whether this implementation matches a compatible reference; E1 asks whether a model performs adequately on a task or held-out distribution.

## Dependency correction

The implementation dependencies and the teaching order are not identical:

- **Inference:** G0 → G1 → G3 → G4 → G5 → G6 → G7.
- **Training data:** G1 → G2.
- **Training computation:** G2 + a differentiable G5 forward pass → G8. G7 is a useful pedagogical demonstration before training, not a computational prerequisite.
- **Verification:** G9 can verify G5–G7 against a compatible reference; G8 is additionally needed only when verifying a trained checkpoint.
- **Task evaluation:** E1 is cross-cutting and may inspect random, trained or pretrained models, depending on the question.

The current reference implementation cannot yet satisfy the differentiable-model prerequisite for G8.

## Editorial corrections applied with this audit

- G2 is described as a tested windowing primitive, not a complete training-data pipeline.
- G4 no longer asks for train/eval dropout behavior that the reference implementation does not implement.
- G5 is recognized as an existing inference-only assembled GPT, rather than described as wholly absent.
- G7 names the actual bound (`max_new_tokens`) and sliding window; it does not imply an EOS stopping rule.
- G8 distinguishes the derivative with respect to logits from gradients through model parameters.
- G9 is separated from held-out task evaluation and is no longer made a mandatory successor to G8.

## Remaining work

1. Add/retain a bilingual page-level audit for the shared core, scoring, training and evaluation lessons; inspect scope, page-map metadata, route membership, bilingual semantic parity and links without duplicating the milestone inventory.
2. Decide whether to add a focused G4 test for a future-token perturbation at the block level. The existing GPT prefix-invariance test is useful evidence, but not a complete proof for all inputs.
3. Implement G8 only after the model representation is made differentiable and the data/loss contracts are explicit. Keep optimizer/checkpoint claims out of the current status until tested.
4. Define a reproducible G9 reference-parity fixture only when a compatible reference and weights can be pinned.
5. Keep manual screen-reader and native-breadcrumb checks tracked separately from CI and axe automation.

No new registry, route stage, graph schema or visualization framework is required by these findings.
