# Computational graph registry

**Status:** first canonical structured model, under validation  
**Source of truth:** `data/computational-graph.yml`  
**Validator:** `site/tools/check_computational_graph.py`  
**Tests:** `tests/site/test_computational_graph.py`  
**Architecture decision:** `docs/canonical-computational-spine.md`  
**Tracking:** [#575](https://github.com/JM-Brun/llm-lab/issues/575), [#579](https://github.com/JM-Brun/llm-lab/issues/579)

## 1. Purpose and boundaries

The computational graph describes **what is computed, which data is consumed or produced, and how operational branches relate to a shared prediction mechanism**. It is not a learning sequence and it is not the conceptual knowledge graph.

| Representation | Question answered | Canonical source |
|---|---|---|
| Computational graph | What is computed, in what dataflow relation, and where are the loops? | `data/computational-graph.yml` |
| Knowledge graph | Which concepts are related, and how? | `data/concepts.yml` |
| Guided Understand route | In what pedagogical order should a learner encounter topics? | `data/guided-route.yml` |
| Build path | In what order can the reference implementation be inspected or constructed? | Build lessons and their code evidence |

A computational edge must never be converted automatically into a pedagogical prerequisite. Likewise, page order, sidebar hierarchy, and Build order must not be used to infer computation.

## 2. Registry structure

The YAML registry contains five top-level collections:

- `branches`: named operational contexts with bilingual labels and descriptions;
- `nodes`: data, operations, controls, and policies;
- `relation_types`: the controlled vocabulary for directed computational relations;
- `edges`: typed relations between node IDs;
- `views`: named subgraphs that select nodes and edges for a diagram or page overlay.

All IDs are stable, language-independent kebab-case strings. Labels and descriptions must contain non-empty `fr` and `en` values.

### Node contract

Each node declares:

- `id`: stable identity;
- `kind`: one of `data`, `operation`, `control`, or `policy`;
- `role`: a more specific editorial/computational classification;
- `labels` and `descriptions`: bilingual text;
- `branches`: explicit membership in one or more operational branches;
- `resources`: published FR and EN page IDs that explain the node.

The `role` is descriptive metadata, not another graph ontology. New roles should be introduced only when they improve interpretation or validation.

### Edge contract

An edge has a stable `id`, a `from` node, a controlled `type`, and a `to` node. The relation definitions explain the direction and meaning.

Optional edge flags are deliberately narrow:

- `feedback: true` marks a real state/context loop, such as generated tokens extending the next context or updated parameters becoming the parameters of the next training step. It is valid only for `feeds-back`.
- `repeated: true` marks a repeated module boundary, such as the output of one Transformer block becoming the input to the next instance of that block. It is valid only for `produces`.
- `optional: true` marks an optimization that is not required for correctness, such as cache population. It is valid only for `produces` or `uses-optional`.

The validator removes only explicitly marked feedback and repeated edges before checking the remaining graph for cycles. This catches accidental cycles without forcing a naturally iterative model into a DAG.

## 3. Semantic decisions encoded in the first version

### Shared prediction mechanism

The shared computation maps a token context through embedding lookup, positional information, Transformer computation, output projection, logits, and a vocabulary distribution. The distribution is the convergence point for generation and observed-target scoring.

The registry contains both a high-level `forward-computation` node and a more detailed representation/Transformer subgraph. They are different levels of abstraction, not two sequential forward passes. Future visualizations should choose one level or explicitly reveal the detail; they must not draw both as consecutive operations.

### Transformer block

Q, K, and V projections consume the input hidden states of a Transformer block. The resulting attention computation, causal constraint, value aggregation, residual/normalization and MLP contribute to the block output. The block is repeated across layers.

This representation intentionally avoids saying that Q/K/V are calculated after the final contextualized states. The exact ordering of residual and normalization operations remains architecture-dependent; the first graph records a conceptual block computation rather than a universal Pre-LN/Post-LN implementation.

### Generation

The generation branch selects a token from the conditional distribution and feeds that token back into the context. The feedback edge is an intentional loop. Ordinary generation does not require target likelihood, loss, gradients, or parameter updates.

### Observed-target scoring and evaluation

Observed-target scoring extracts the probability assigned to a known target token. Per-token values can contribute to sequence log-likelihood or token NLL. Evaluation aggregates held-out scores and metrics but does not update model parameters.

The graph keeps the scoring operation (`target-probability`) distinct from the resulting scalar data (`target-probability-value`).

### Training and teacher forcing

Teacher forcing is represented as a conditioning policy that supplies reference-sequence prefixes. The shifted training context is evaluated at all positions under causal masking; the objective is computed from target losses, differentiated, and passed to an optimizer.

The optimizer update is a separate operation. Updated parameters become the parameters used by the next forward computation. This is a training loop, not a generation step.

### Prefill, decode, and KV cache

Prefill and autoregressive decode are execution phases applied to the shared forward computation:

- prefill processes the initial prompt as a sequence before the first generated-token selection;
- decode advances generation iteratively, normally one new token per step;
- a KV cache may be populated during prefill and reused during decode.

The cache is marked optional. Its presence in the conceptual graph does not claim that the current NumPy reference implementation uses a cache; the generation lesson documents the implementation limitation.

## 4. Views are projections, not new sources of truth

The current views are:

- `persistent-spine`: compact shared context-to-distribution path;
- `representation-pipeline`: embedding lookup, positional information, and contextualized states;
- `transformer-block`: internal attention and block update;
- `generation`: distribution, selection, and context feedback;
- `observed-target-scoring`: target probability and sequence likelihood;
- `evaluation`: held-out scoring and metrics;
- `training`: teacher forcing, loss, gradients, and parameter update;
- `inference-execution`: prefill, decode, and optional KV cache.

Each view declares one branch, a set of nodes, and a set of edges. Every selected edge must have both endpoints in the view, and every selected node must belong to the declared branch. These rules prevent a view from quietly mixing operational branches.

A node may belong to multiple branches. That is how the registry expresses shared computation without duplicating node identities.

## 5. Validation

Run:

```bash
uv run python site/tools/check_computational_graph.py
uv run pytest --no-cov -q tests/site/test_computational_graph.py
```

The validator checks:

- schema version and stable unique IDs;
- bilingual labels and descriptions;
- valid node kinds and branch membership;
- published bilingual page references;
- valid edge endpoints and controlled relation types;
- branch overlap across edge endpoints;
- explicit marking of feedback and repeated-module edges;
- absence of unmarked directed cycles;
- view branch membership and node/edge references.

The graph is not yet consumed by a renderer. This first iteration stabilizes the data contract and validation boundary before introducing visual output.

## 6. Deliberate exclusions and next steps

Not represented yet:

- corpus construction, batching, padding, and training-window sampling;
- architecture-specific normalization variants as separate subgraphs;
- cross-attention and encoder-decoder computation;
- speculative decoding, beam search, and advanced serving schedulers;
- optimizer families and distributed training details;
- code-module dependency edges.

These should be added only when a canonical lesson or implementation path needs them and when their semantics can be represented without conflating conceptual computation with implementation dependencies.

Next iterations should:

1. validate the registry against the complete published page inventory and add focused negative tests;
2. review the graph semantically against the bilingual lessons and the reference code;
3. generate an accessible textual representation and one persistent visual spine from this registry;
4. add page-level highlighting as a projection, not as hand-maintained per-page diagrams;
5. reconcile Understand and Build as separate projections without deriving one from the other.

## 7. Rendering selected views

`site/tools/render_computational_graph.py` renders selected views from this registry as bilingual Mermaid fragments. The renderer does not create a second graph model: node labels, relation labels, and topology are read directly from the YAML source.

The current lesson mappings are deliberately limited to views with a clear instructional owner:

| View | French page | English page |
|---|---|---|
| `representation-pipeline` | `fr/transformer` | `en/transformer` |
| `transformer-block` | `fr/transformer-block-walkthrough` | `en/transformer-block-walkthrough` |
| `generation` | `fr/generation` | `en/generation` |
| `inference-execution` | `fr/generation` | `en/generation` |
| `observed-target-scoring` | `fr/vraisemblance` | `en/likelihood` |
| `training` | `fr/training-examples` | `en/training-examples` |

The `persistent-spine` remains represented by the existing hand-maintained overview SVG; it is not yet generated from the registry. The `evaluation` view remains available in the registry until a lesson with matching scope is selected. These boundaries are intentional: a view is not embedded merely because it exists, and an existing pedagogical illustration is not silently replaced.

Generated fragments are ignored by Git and rebuilt by both CI and the Quarto workflow before rendering. Run locally with:

```bash
uv run python site/tools/render_computational_graph.py
quarto render site
```

The generated callouts are collapsed by default to keep the lesson readable. Mermaid arrows follow the declared edge direction; labels are the localized names of the controlled relation types.
