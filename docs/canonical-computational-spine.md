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

`conditional distribution + observed target → target probability → target log-probability`

The target log-probability then supports two related quantities:

- **Sequence log-likelihood:** sum the target log-probabilities over the included positions. This is the logarithm of the sequence likelihood, whose probability-space form is the product of the conditional target probabilities.
- **Per-token NLL:** negate each target log-probability. For a one-hot next-token target, this is the token-level cross-entropy.

Training can then aggregate per-token NLL using an explicit mask and reduction to obtain an objective value. Scoring need not perform that training reduction or update parameters. In practice, stable computations use log probabilities and reductions rather than multiplying many small probabilities.

### Branch C — evaluation and training

- Evaluation applies observed-target scoring to held-out examples and reports task-appropriate metrics; it does not update parameters. For language modeling, the loss lesson introduces mean per-token NLL and perplexity. The experimental-evaluation lesson is a transfer exercise on a scientific-passage ranker, not an LLM benchmark or evidence of a locally trained GPT evaluation.
- Training differentiates the objective, backpropagates gradients, and applies an optimizer update to parameters.
- The updated parameters are used in a subsequent forward computation.

### Context feedback is a typed relation

Observed-target scoring, evaluation, and training all condition predictions on the observed prefix. Generation and teacher-forced scoring/training use different context sources:
- generation appends the model-selected token before the next prediction;
- at each scoring/training position, teacher forcing supplies only the observed ground-truth prefix preceding that position's target. After the target is scored, it becomes part of the prefix for the next position.

Teacher forcing is a training/scoring context policy, not a separate prediction mechanism. Prefill computes the prompt/context states (and, when used, populates the KV cache); decode advances generation one token at a time using the cache. Neither should be confused with teacher forcing.

## 4. Typed relations and ownership boundaries

The project uses several relation vocabularies because they describe different kinds of connection. Do not merge them into one generic edge taxonomy.

### Computational registry: `data/computational-graph.yml`

The computational graph uses its existing controlled edge types:

| Registry type | Meaning | Example |
|---|---|---|
| `consumes` / `produces` | An operation consumes an input and produces an output | hidden states → Q/K/V projections → Q, K, V |
| `combines` | An operation combines multiple inputs | embeddings + positional information → initial hidden states |
| `constrains` | A control restricts an operation or intermediate result | causal mask → masked attention scores |
| `applies` / `precedes` | A phase or mode applies to a computation, or one phase precedes another | prefill → decode |
| `selects` | The source distribution determines the selected item | next-token distribution → generated token |
| `scores` / `aggregates` | An observed target is scored and per-token/sequence values are aggregated | distribution + target → target probability → sequence log-likelihood |
| `differentiates` / `updates` | An objective yields gradients and an optimizer updates parameters | objective → gradients → updated parameters |
| `feeds-back` | A value becomes context or state for a later iteration | generated token → next context |
| `conditions` | A policy or observed value constrains target selection, context, or target assignment | decoding policy → generated token; teacher forcing → observed-prefix context |
| `uses-optional` | An optional optimization may be used without being required for correctness | KV cache → decode |

The registry may express a familiar high-level idea such as *dataflow*, *transformation*, *decoding*, *optimization* or *evaluation* through these more precise operational relations. Those high-level words are explanatory categories, not additional edge types to add mechanically. In particular, evaluation is represented by scoring held-out targets and aggregating the resulting metrics; it stops before differentiation or parameter updates.

### Other project relations belong to their canonical sources

- **Pedagogical prerequisite:** owned by the curriculum topology in `docs/learning-path.md`; it is not a computational-graph edge.
- **Conceptual/semantic relation:** owned by the typed relations in `data/concepts.yml`; it connects concepts, not executable operations.
- **Implementation correspondence:** expressed through concept/resource associations and the Build crosswalk; it does not imply that a page or code module is a computational node.
- **Editorial navigation:** owned by page-map `hierarchy` and `suggested_route`; it expresses containment or a recommended reading transition, not computation.

A pedagogical prerequisite relation is not a substitute for a computational relation. The computational graph must not infer a total learning order from dataflow, nor infer dataflow from page order. Do not add a new relation type unless a concrete edge cannot be represented accurately by the existing vocabulary and its semantics are documented and validated.

## 5. Reader-facing projections

The existing knowledge architecture remains authoritative by information type: `data/concepts.yml` owns stable concepts and typed semantic relations; `data/domains.yml` owns controlled knowledge domains; `data/resources.yml` owns non-page artifacts; `docs/learning-path.md` owns curriculum modules, scope and pedagogical dependencies; `data/guided-route.yml` is the bilingual reader-facing route projection; page-map metadata owns page hierarchy and suggested page navigation. The computational spine is a crosswalk/projection assembled from these sources, not a replacement registry or a new general-purpose graph. Reader-facing views are projections, not separate competing models. Their level of detail must match the learning task:

- **Overview diagram:** a deliberately simplified learner-facing view: context → model → logits → probability distribution, followed by three clearly distinguished uses (generation, observed-target scoring, training). It is not a rendering of the full computational registry.
- **Detailed computational spine:** shared input/forward/logits/distribution path, used only where the reader needs to inspect the actual computation. It should not be inserted automatically into every overview.
- **Generation view:** highlights decoding, token feedback, prefill/decode, and optional KV-cache optimization in the dedicated inference lesson.
- **Scoring view:** highlights observed targets, target probability, likelihood, log-likelihood, NLL/cross-entropy, reductions and masks in a scoring-focused lesson or reference.
- **Training view:** highlights teacher forcing, objective, gradients, optimizer and parameter update in the training lessons.
- **Evaluation view:** highlights held-out scoring and metrics, explicitly stopping before parameter updates. This is a methodological view, not a required overview diagram.
- **Guided route:** pedagogical order and reading depth; may preview generation early and revisit its mechanics later.
- **Build path:** implementation dependency order; must remain distinct from conceptual/dataflow order.

**Presentation rule:** the computational registry and its generated branch overlays are authoritative structural representations for project consistency. They are not automatically good teaching diagrams. A learner-facing page should show only the subset of relations needed to answer its instructional question, use plain-language labels, and avoid exposing internal graph categories as if they were concepts the learner must memorize. The LLM overview therefore uses the simplified three-use diagram and leaves KV-cache detail to the inference/complexity lessons.

Every page should identify its primary node(s), relevant branch(es), and relation to the shared spine. The early generation overview and the later detailed generation lesson are two depths of one canonical topic, not duplicate concepts.

## 6. Vocabulary and page identity

Use one stable concept identity per concept, independent of language. Reuse existing pages and IDs where valid; do not create duplicate canonical pages for contextualized representations, Q/K/V, scaled dot-product attention, causal masking, logits, probabilities, likelihood, cross-entropy/loss, or generation/decoding.

Candidate canonical page IDs already in the route include `contextualized-representations`, `queries-keys-values`, `scaled-dot-product-attention`, `causal-masking`, `logits`, `probabilites` (FR, preserve existing slug), and `probabilities` (EN).

## 7. Implementation sequence

1. Audit the current concept registry, relation types, route, Build milestones, page metadata, and generated graph before changing them.
2. Extend the existing concept registry only for missing language-independent concepts and reviewed semantic relations; keep curriculum-module identities and dependencies in `docs/learning-path.md`.
3. Validate concept integrity with the existing registry checker: unique IDs, bilingual labels/definitions, valid published page references, domain membership, relation endpoints/types, rationales for prerequisites, and acyclic prerequisite/structural relations.
4. Treat `data/guided-route.yml` as a projection of the curriculum model; reconcile its flat reader-facing stages only after module ownership and dependencies are stable.
5. Generate the persistent spine and branch overlays as filtered projections; provide a semantic text/list fallback for accessibility.
6. Integrate the spine into relevant pages without duplicating concept explanations.
7. Keep the Build dependency crosswalk separate from conceptual/dataflow order; preserve the early generation preview and later detailed inference treatment.
8. Add rendered desktop/mobile, keyboard, screen-reader, link and regression tests before considering the model fully integrated.

## 8. Non-goals and safeguards

- Do not make likelihood, loss, gradients, or optimization prerequisites for inference.
- Do not turn inference and training into one executable loop.
- Do not put corpus preparation, batching, or training-window construction on the inference critical path.
- Do not represent Q/K/V as downstream of final contextualized states.
- Do not imply that every Transformer uses identical residual/normalization ordering.
- Do not move optional mathematical or architectural deep dives into the core route merely to make the diagram linear.
- Do not remove existing content during consolidation; map every displaced explanation to its canonical page or preserve it as a clearly scoped deep dive.


## 10. Integration hand-off

The canonical model, eight-stage guided route, teacher-forcing/prefill teaching, concept metadata, and computational registry/first graph views are now integrated on `main` through [PR #578](https://github.com/JM-Brun/llm-lab/pull/578) and the generated-route refresh [PR #586](https://github.com/JM-Brun/llm-lab/pull/586). The detailed persistent-spine and evaluation views were embedded in the bilingual overview through [PR #589](https://github.com/JM-Brun/llm-lab/pull/589). The subsequent pedagogical review identified that these structural projections were too metadata-like for the overview's introductory audience. [PR #782](https://github.com/JM-Brun/llm-lab/pull/782) replaces them there with a simpler learner-facing diagram while preserving the canonical registry and this architectural document. The revised PR's Quarto rendering and browser review are pending. A manual screen-reader review is still required before claiming full accessibility validation. The active hand-off is [computational-spine-integration-plan.md](computational-spine-integration-plan.md) and child issue [#584](https://github.com/JM-Brun/llm-lab/issues/584). Continue reusing the existing registries and validators rather than introducing a parallel graph or workflow framework.

## 9. Adopted curriculum topology

The module hierarchy and predecessor/successor model are defined in [`docs/learning-path.md`](learning-path.md#canonical-module-topology-shared-core-and-operational-branches). This is a curriculum model, not a new concept ontology. The bilingual eight-stage route in `data/guided-route.yml` now separates the shared prediction core from inference, observed-target scoring and training; evaluation remains cross-cutting. The concept registry includes reviewed concepts for conditional distributions, observed-target scoring, likelihood/NLL, autoregressive generation, prefill/decode/KV cache, teacher forcing, gradients, optimizers, parameter updates, and held-out evaluation. The canonical generation page is intentionally reused for an early overview and a later detailed inference treatment.
