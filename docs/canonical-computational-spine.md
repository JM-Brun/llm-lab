# Canonical computational spine: shared prediction mechanism and typed branches

**Status:** architectural decision for issue #575  
**Date:** 2026-11-06  
**Scope:** conceptual model, knowledge graph, guided route, page-level orientation, and Build crosswalk.

## 1. Decision

LLM Lab represents next-token prediction as **one shared conditional-prediction mechanism with sibling operational uses**, not as one flat sequence and not as independent inference/training pipelines.

For context (x_{<t}), the model computes:

[
z_t = f_\theta(x_{<t}), \qquad
p_\theta(\cdot \mid x_{<t}) = \operatorname{softmax}(z_t).
]

The conditional distribution is the convergence point. It supports:

1. **Generation / inference:** select or sample a token, append the generated token to the context, and repeat with unchanged parameters.
2. **Observed-target scoring:** select the probability assigned to an observed target token. Across positions, this yields sequence likelihood and log-likelihood.
3. **Evaluation:** reuse observed-target scoring on held-out data; compute metrics and stop without parameter updates.
4. **Training:** aggregate target-level negative log-likelihood / cross-entropy into an objective, differentiate it, and update parameters. The next training step recomputes predictions using updated parameters.

These are typed relations, not a total order. Likelihood, loss, gradients, and parameter updates are not steps in ordinary generation.

## 2. Two levels must remain distinct

### 2.1 Input and representation pipeline

`text → tokens → token IDs → embedding lookup → positional information → initial hidden states`

The terms **initial hidden states** and **contextualized hidden states** must not be treated as synonyms.

### 2.2 Transformer block computation

For each block, the input hidden states are projected to Q, K, and V. Attention scores are computed from Q and K; the causal constraint is applied to the scores before softmax; the resulting weights aggregate V. The attention output is combined with residual connections, normalization, and the feed-forward/MLP sublayer. Repeated blocks progressively transform the hidden states.

`block input hidden states → Q/K/V projections → attention scores → causal masking → attention weights → value aggregation → output projection → residual/normalization → MLP → block output hidden states`

The final hidden state at each position is projected to vocabulary logits. Q/K/V are not a stage that follows already-final contextualized representations: they are internal computations that produce the next layer's contextualized representations.

The exact placement/order of normalization and residual operations depends on the architecture (e.g. Pre-LN vs Post-LN); the spine must not encode one implementation as universal.

## 3. Canonical graph structure

### Shared input and prediction mechanism

- Text/context is tokenized into token IDs (for raw-text interfaces).
- Token IDs are mapped to embeddings; positional information is incorporated according to the architecture.
- Transformer blocks compute contextualized hidden states.
- The output projection produces logits.
- Softmax defines the next-token conditional probability distribution.

### Branch A — generation

`conditional distribution → decoding policy → selected/generated token → append to context → next forward computation`

Temperature, top-k, top-p, greedy decoding, and sampling are decoding policies. They modify selection from the distribution; they do not modify model parameters. KV cache is an inference optimization that reuses previously computed key/value states. It belongs to the prefill/decode execution strategy, not between probability and token selection as a conceptual prerequisite.

### Branch B — observed-target scoring

`conditional distribution + observed target → target probability → sequence likelihood / log-likelihood → NLL / token cross-entropy → aggregation and masking → objective value`

For one-hot next-token targets, token-level cross-entropy equals negative log probability assigned to the target. Sequence likelihood is the product of the conditional probabilities over positions; log-likelihood is their sum. In practice, stable computations use log probabilities and reductions rather than multiplying many small probabilities.

### Branch C — evaluation and training

- Evaluation consumes the scoring/objective results on held-out examples and reports metrics; it does not update parameters.
- Training differentiates the objective, backpropagates gradients, and applies an optimizer update to parameters.
- The updated parameters are used in a subsequent forward computation.

### Context feedback is a typed relation

Both generation and teacher-forced scoring/training extend the context, but with different sources:
- generation feeds back the model-selected token;
- teacher forcing feeds back the observed ground-truth token.

Teacher forcing is a training/scoring context policy, not a separate prediction mechanism. Prefill computes the prompt/context states (and, when used, populates the KV cache); decode advances generation one token at a time using the cache. Neither should be confused with teacher forcing.

## 4. Relation taxonomy

The graph and its visual projections must distinguish at least:

| Relation | Meaning | Example |
|---|---|---|
| `dataflow` | Tensor/value produced and consumed | hidden states → Q/K/V |
| `transforms` | Operation transforms an input | logits → probabilities |
| `conditions` | Restricts valid computation | causal mask → attention scores |
| `aggregates` | Combines values or positions | probabilities → sequence likelihood |
| `scores` | Compares prediction with an observed target | distribution + target → target probability |
| `decodes` | Selects a token from a distribution | distribution → generated token |
| `feeds-back` | Extends the next context | generated/observed token → next context |
| `optimizes` | Computes parameter update from objective | gradients → updated parameters |
| `evaluates` | Applies a scoring/metric procedure to held-out data | scoring → evaluation metrics |
| `implements` | Conceptual operation realized by a component | attention → attention module |
| `prerequisite` | Genuine pedagogical dependency | probabilities → likelihood |

A prerequisite edge is not a substitute for a computational edge. The graph must not infer a total learning order from dataflow, nor infer dataflow from page order.

## 5. Reader-facing projections

The canonical graph is the source of truth. Reader-facing views are projections, not separate competing models:

- **Persistent spine:** shared input/forward/logits/distribution path, always visible on relevant pages.
- **Generation view:** highlights decoding, token feedback, prefill/decode, and KV cache.
- **Scoring view:** highlights observed targets, target probability, likelihood, log-likelihood, NLL/cross-entropy, reductions and masks.
- **Training view:** highlights teacher forcing, objective, gradients, optimizer and parameter update.
- **Evaluation view:** highlights held-out scoring and metrics, explicitly stopping before parameter updates.
- **Guided route:** pedagogical order and reading depth; may preview generation early and revisit its mechanics later.
- **Build path:** implementation dependency order; must remain distinct from conceptual/dataflow order.

Every page should identify its primary node(s), relevant branch(es), and relation to the shared spine. The early generation overview and the later detailed generation lesson are two depths of one canonical topic, not duplicate concepts.

## 6. Vocabulary and page identity

Use one stable concept identity per concept, independent of language. Reuse existing pages and IDs where valid; do not create duplicate canonical pages for contextualized representations, Q/K/V, scaled dot-product attention, causal masking, logits, probabilities, likelihood, cross-entropy/loss, or generation/decoding.

Candidate canonical page IDs already in the route include `contextualized-representations`, `queries-keys-values`, `scaled-dot-product-attention`, `causal-masking`, `logits`, `probabilites` (FR, preserve existing slug), and `probabilities` (EN).

## 7. Implementation sequence

1. Audit the current concept registry, relation types, route, Build milestones, page metadata, and generated graph before changing them.
2. Add the canonical graph as structured data with bilingual labels/descriptions, stable IDs, typed edges, branch membership, and explicit page references.
3. Validate graph integrity: unique IDs, valid endpoints, valid relation types, valid page references, no cycles in prerequisite-only edges, bilingual parity.
4. Generate the persistent spine and branch overlays from the canonical graph; provide a semantic text/list fallback for accessibility.
5. Integrate the spine into relevant pages without duplicating concept explanations.
6. Reconcile the guided route and Build crosswalk as separate projections; preserve the early overview / later deepening distinction.
7. Add rendered desktop/mobile, keyboard, screen-reader, link and regression tests.
8. Update the route reconciliation and close this issue only when generated artifacts and tests agree.

## 8. Non-goals and safeguards

- Do not make likelihood, loss, gradients, or optimization prerequisites for inference.
- Do not turn inference and training into one executable loop.
- Do not put corpus preparation, batching, or training-window construction on the inference critical path.
- Do not represent Q/K/V as downstream of final contextualized states.
- Do not imply that every Transformer uses identical residual/normalization ordering.
- Do not move optional mathematical or architectural deep dives into the core route merely to make the diagram linear.
- Do not remove existing content during consolidation; map every displaced explanation to its canonical page or preserve it as a clearly scoped deep dive.
