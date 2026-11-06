# Computational curriculum reorganisation

**Status:** page-migration specification; canonical module topology is maintained in [docs/learning-path.md](learning-path.md#canonical-module-topology-shared-core-and-operational-branches)  
**Date:** 2026-11-06  
**Scope:** page ownership, core/advanced boundaries, guided route, Build crosswalk.  
**Preservation rule:** no explanation, example, equation, citation, or exercise is deleted during restructuring. Every moved section must be mapped to a canonical destination.

This document is subordinate to the canonical curriculum model in `docs/learning-path.md`. It maps page ownership, progressive disclosure and migration boundaries; it must not be treated as a second source of module hierarchy or dependency edges. The current page bodies, route projection and generated fragments remain unchanged until the later refactor.

## 1. Four connected parts

The minimum course for understanding and building a small autoregressive LLM has four connected parts:

1. **Shared computational core:** how a context becomes a conditional next-token distribution.
2. **Observed-target scoring:** how the same distribution assigns probability to a token already observed.
3. **Inference/generation:** how a token is selected and fed back while parameters remain fixed.
4. **Training:** how observed targets, a differentiable objective, gradients, and parameter updates improve the shared predictor.

Evaluation is cross-cutting: it applies scoring to held-out data and does not update parameters. It is not another step in the training loop.

These are not four independent models and not one linear execution chain. They reuse the same predictor but have different inputs and state transitions after the conditional distribution.

## 2. Minimum shared computational core

### Input and representation

`text → tokens → token IDs → token embeddings + positional information → initial hidden states`

The core route must distinguish text, tokens, IDs and vectors; explain embedding lookup and the need for position information; and distinguish initial hidden states from states transformed by Transformer blocks.

Unicode/UTF-8 internals, tokenizer training, vocabulary optimisation, tokenisation inequities, embedding geometry, and alternative positional schemes are Deepen material.

### Repeated Transformer computation

For each block, current hidden states are projected to Q/K/V; attention scores are computed; the causal constraint excludes future positions; normalised weights aggregate values; attention and MLP sublayers transform the residual stream. Repeated blocks produce final contextualised states.

`block input → Q/K/V → scores → causal constraint → attention weights → value aggregation → output projection → residual/normalisation + MLP → block output`

Q/K/V are projections of each block's input, not operations after final contextualisation. Residual/normalisation order is architecture-dependent; the main route must not universalise the repository's Pre-LN implementation.

Multi-head derivations, cross-attention, RoPE mathematics, alternative attention variants, kernel-level attention, and complexity analysis belong in Deepen unless a Build milestone requires them.

### Shared prediction head

`final hidden states → vocabulary projection → logits → softmax → conditional next-token distribution`

The minimum mathematical statement is:

`z_t = f_θ(x_<t), p_θ(·|x_<t) = softmax(z_t)`

The learner needs the meaning of logits and the role of softmax, not a full treatment of entropy, calibration, or probability geometry.

## 3. Part A — Shared computational core: page ownership

| Existing page | Canonical responsibility | Main-route status |
|---|---|---|
| `llm-overview` | System orientation; distinguish model, data, parameters, inference and learning | Core, concise |
| `text-data` | Text → tokens → token IDs | Core |
| `embedding-space` | Embedding lookup and vector representation | Core; geometry in Deepen |
| `positional-encoding` | Why and where position information enters | Core intuition; variants in Deepen |
| `contextualized-representations` | Initial embeddings vs evolving hidden states across blocks | Core bridge |
| `transformer` | Whole-block synthesis: attention, MLP, residual stream, repeated blocks | Core synthesis |
| `queries-keys-values` | Q/K/V projections from block input | Core concept; detailed algebra in Deepen |
| `scaled-dot-product-attention` | Scores, scaling, softmax weights, weighted value aggregation | Core |
| `causal-masking` | Exclusion of future positions in decoder-only GPT | Core |
| `logits` | Vocabulary projection and unnormalised scores | Core |
| `probabilites` / `probabilities` | Softmax and conditional distribution | Core |

The route need not force every resource to become a separate chapter. Pages remain canonical reference resources; route groupings may combine them. Do not merge pages mechanically if this destroys independent explanations or stable links.

## 4. Part B — Observed-target scoring

**Question:** How probable was a token that actually occurred?

`context → shared predictor → distribution + observed next token → target probability → log-probability → sequence likelihood/log-likelihood`

The training bridge is:

`target log-probability → negative log-likelihood/token cross-entropy → batch loss`

| Existing page | Canonical responsibility | Main-route status |
|---|---|---|
| `likelihood` / `vraisemblance` | Probability of an observed sequence as a product of conditional probabilities; log form as a sum | Core scoring |
| `cross-entropy` | Per-target penalty; one-hot next-token target as negative log probability | Core bridge |
| `loss` | Aggregate valid per-token penalties; target shift, masking, reduction | Core objective |

Scoring does not choose a token and does not update parameters. Held-out scoring is one input to evaluation. Perplexity is a derived metric; detailed comparability caveats can be optional after the basic definition.

## 5. Part C — Inference and generation

**Question:** How does a fixed model extend a context?

`prompt/context → prefill → shared predictor → logits/distribution → decoding → generated token → append to context → next decode step`

| Existing/proposed page | Canonical responsibility | Main-route status |
|---|---|---|
| `generation` | End-to-end autoregressive loop; fixed parameters; stop criteria | Core inference |
| `decoding-strategies` | Greedy selection and sampling; temperature | Core summary; top-k/top-p and beam search in Deepen |
| Prefill (no dedicated page identified) | Process prompt/context before incremental generation; optionally populate cache | Brief core concept in generation |
| Decode step (no dedicated page identified) | Incremental next-token computation after prefill | Core concept in generation |
| KV cache (no dedicated concept page identified) | Reuse past keys/values to avoid recomputing the prefix | Deepen / efficiency |

Prefill/decode are phases of inference execution. Teacher forcing is not a synonym for prefill: teacher forcing supplies observed previous tokens during scoring/training; inference feeds back model-selected tokens.

Explain the simple uncached loop first. KV-cache internals, cache layouts, paged attention, batching, speculative decoding, and serving trade-offs remain optional.

## 6. Part D — Training

**Question:** How are parameters changed so observed next tokens become more probable?

`training examples → shifted inputs/targets → teacher-forced forward pass → target probabilities → token losses → batch loss → gradients → optimizer update → updated parameters`

| Existing/proposed page | Canonical responsibility | Main-route status |
|---|---|---|
| `training-examples` | Construct inputs and shifted next-token targets; valid positions | Core |
| Teacher forcing (no dedicated page identified) | Feed observed previous tokens as context for parallel next-token predictions | Core concept in training-examples |
| `cross-entropy` | Per-token objective relative to observed target | Core, shared with scoring |
| `loss` | Aggregate valid target losses and define reduction | Core |
| `gradients` | Chain rule/backpropagation from scalar loss to parameters | Core minimum: one SGD update |
| Optimizer/training loop | Apply updates over batches and epochs | Core Build milestone; AdamW details in Deepen |

Teacher forcing does not create a different predictor. It determines the source of previous tokens: observed tokens in teacher-forced training, generated tokens in free-running inference. The input/target shift must be explicit. A plausible loss can still result from incorrect alignment.

A minimum Build path must include the complete loop from examples to updated parameters. A codebase that only computes loss or gradients must be labelled partial, not a functioning training pipeline.

## 7. Evaluation is cross-cutting

Keep three claims separate:

1. **Implementation verification:** does code compute the intended operation?
2. **Optimisation:** does the training objective decrease on training data?
3. **Evaluation/generalisation:** does the model perform acceptably on held-out data and the intended task?

The existing experimental-evaluation page is an applied protocol exercise. It belongs to a Practice branch, not as the next conceptual page after gradients. Preserve its ranking example and AP/calibration/leakage content in its stated scope; do not relabel it as an LLM benchmark.

## 8. Main route versus Deepen

Reuse existing metadata dimensions:
- `destination:understand`: conceptual course;
- `destination:build`: implementation walkthrough;
- `destination:deepen`: optional depth;
- `destination:practice`: exercises and investigations;
- `level:core`: minimum-route material;
- `level:advanced` (or the repository's governed advanced value): material that must not block the main route.

Classify by dependency on the stated learning outcome, not difficulty alone:
- **Core:** omission prevents explaining or implementing the minimum predictor, scoring, inference loop, or parameter update.
- **Deepen:** refines, optimises, generalises, or analyses a working mechanism without being required to understand it.
- **Practice:** applies or tests understanding rather than introducing a prerequisite.
- **Build:** gives code-level evidence for a concept and references, rather than duplicates, the concept lesson.

| Topic | Main route | Deepen |
|---|---|---|
| Text/tokens | Tokenisation and IDs | Unicode/UTF-8 internals, tokenizer design trade-offs |
| Embeddings/positions | Lookup, vector role, need for position | Embedding geometry, linearity, RoPE mathematics/variants |
| Transformer | Block flow, Q/K/V, causal attention, MLP, residual stream | Multi-head derivations, cross-attention, alternatives, kernel/complexity analysis |
| Prediction | Logits, softmax, conditional distribution | Entropy, calibration, numerical-stability details |
| Scoring | Observed target probability, likelihood/log-likelihood, NLL/cross-entropy | Perplexity comparability, advanced probabilistic interpretations |
| Inference | Greedy/sampling, feedback, stopping, prefill/decode distinction | Top-k/top-p, beam/speculative decoding, KV-cache internals, serving |
| Training | Shifted targets, teacher forcing, cross-entropy, loss, gradients, one update | AdamW, schedules, clipping, mixed precision, distributed training |
| Evaluation | Train/validation/test distinction and held-out scoring | Metric selection, calibration, uncertainty, leakage, benchmark design |

This is a target classification, not a claim that all current pages already have matching metadata. Audit both languages before changing tags.

## 9. Proposed guided route

The current six-stage route does not expose scoring as a distinct branch and shows generation both in orientation and prediction. Preserve the early generation preview; distinguish it from the detailed inference lesson.

1. **Orient and preview:** LLM overview; short generation preview with fixed parameters.
2. **Build the shared predictor:** text/IDs; embeddings/positions; hidden states; Transformer block; logits/probabilities.
3. **Score an observed target:** likelihood/log-likelihood; token cross-entropy; batch loss.
4. **Run inference:** prefill/context processing; decoding; token feedback; stopping.
5. **Train the predictor:** examples and shifted targets; teacher forcing; loss; gradients; optimizer update.
6. **Check the result:** implementation verification and held-out evaluation, distinct from training loss.

This is a pedagogical route, not an execution trace. A branch diagram should show the shared predictor feeding scoring, inference, and training/evaluation without implying that inference requires likelihood or gradients.

## 10. Migration sequence

Do not rewrite all pages in one pass.

1. Audit FR/EN page-map records, front matter, guided-route membership and Build milestones. Record current and target role.
2. Revise the contextualized-representations and Transformer overview pages to bridge embeddings, block computation and logits. Keep Q/K/V inside each block.
3. Clarify likelihood as observed-target scoring; cross-entropy as the per-target penalty; loss as batch aggregation and masking.
4. Make generation the owner of the fixed-parameter loop; add concise prefill/decode definitions and cross-links; keep cache internals optional.
5. Make training-examples the owner of target alignment and teacher forcing; connect it to cross-entropy, loss, gradients and optimizer update.
6. Update guided route only after ownership and dependencies are stable. Keep conceptual order separate from code implementation order.
7. Apply structural and metadata changes to EN and FR together; preserve translated slugs.
8. Run metadata, concept registry, route, learning-map, local-link, Quarto and CI checks; separately inspect responsive and keyboard navigation.

### Content-preservation ledger

For every moved, shortened or collapsed section, record source page/heading, destination page/heading, treatment (retained, summarised with link, or split), bilingual counterpart, and links/exercises to repair. Advanced content is relocated behind a Deepen link or retained in an optional section; it is not deleted.

## 11. Acceptance criteria

- A reader explains the shared computation from token IDs to a next-token distribution without first learning training.
- A reader distinguishes a generated token from an observed target.
- A reader explains scoring without implying decoding or parameter updates.
- A reader traces inference with fixed parameters and describes prefill/decode conceptually.
- A reader traces training from shifted targets and teacher forcing through loss, gradients and one parameter update.
- Evaluation is distinct from optimisation and implementation verification.
- Advanced material is discoverable but does not block the core route.
- FR and EN routes have equivalent conceptual coverage and ownership.
- Build maps each required concept to code/tests/evidence and marks implementation gaps.
- Existing content remains accounted for in the preservation ledger.

## 12. Immediate implementation slice

First classify the participating pages as core, applied/build, deepen or practice; identify missing teacher-forcing and prefill/decode explanations; establish canonical ownership and cross-links; and validate the proposed route against current Build milestones. Only then edit page bodies in small bilingual groups.
