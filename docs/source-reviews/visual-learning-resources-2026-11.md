# Visual learning resources: focused review and integration map

**Review date:** 2026-11-16  
**Input:** a ten-link visual-learning shortlist circulated on LinkedIn.  
**Status:** first-pass source triage and repository integration; not a full scientific or usability audit.

## Executive synthesis

The shortlist spans distinct learning operations: observe a forward pass, inspect architecture, build intuition, manipulate a trainable network, compare modern mechanisms, understand production inference, inspect internal features, and explore embedding datasets.

It is not ten wholly new sources. Existing source records already cover Transformer Explainer, Jay Alammar's Illustrated Transformer, 3Blue1Brown, and related attention material. New source records are added for Bbycroft, TensorFlow Playground, the exact Raschka attention-variants guide, Grootendorst's MoE guide, Modular's inference handbook, Neuronpedia and Apple Embedding Atlas. Existing records are reused rather than duplicated.

## Resource-by-resource disposition

| # | Resource | Prior repository status | Disposition | Learning destination |
|---|---|---|---|---|
| 1 | Transformer Explainer | Existing source record and practice-page coverage | Reuse; strengthen as interactive GPT-2 case study, not universal architecture | Transformer practice |
| 2 | Bbycroft LLM Visualization | Not in source catalogue | Add source record; optional 3D walkthrough | Transformer overview, tensors |
| 3 | 3Blue1Brown | Existing source records and references | Reuse; link GPT and attention lessons | Orientation, attention |
| 4 | Illustrated Transformer | Existing source record and bibliography | Reuse; clarify original encoder-decoder context | Q/K/V, attention |
| 5 | TensorFlow Playground | Not in source catalogue | Add optional prerequisite experiment | Gradients, loss, training |
| 6 | Visual Guide to Attention Variants | Related Raschka attention material exists; exact guide not registered | Add distinct source record; compare MHA/MQA/GQA/MLA/sparse/windowed variants | Attention, inference |
| 7 | Visual Guide to MoE | Not in source catalogue | Add source record; propose guided experiment | Architectures, inference |
| 8 | LLM Inference Handbook | Not in source catalogue | Add source record; map interactive tools to inference module | Generation, KV cache, serving |
| 9 | Neuronpedia | Not in source catalogue | Add source record; advanced investigation with epistemic caveats | Interpretability, representations |
| 10 | Apple Embedding Atlas | Not in source catalogue | Add source record; pair with reproducible dataset | Embedding space |

The LinkedIn short links are not used as canonical source identifiers. Stable publisher, project or author URLs are recorded instead. Exact redirect targets of all short links were not independently resolved.

## Technical and pedagogical findings

### Transformer Explainer

The official project describes a live GPT-2 instance running in the browser, with an overview, progressive transitions between model structures and mathematical operations, and user-controlled inputs. The 2026 CHI paper reports a 90-participant study and learning/engagement benefits; an earlier AAAI 2025 demonstration paper also exists.

**Teaching use:** ask learners to predict the next-token distribution before changing input or temperature; observe tokens, attention, MLP and output probabilities; reproduce one operation numerically or in code.

**Boundary:** GPT-2 implementation. Do not infer that all current LLMs share its exact block, normalization, attention or positional-encoding choices.

### Bbycroft 3D visualization

Indexed walkthrough captures expose embedding, layer normalization, self-attention, projection, MLP, Transformer, softmax and output chapters, with a 3D model view. The walkthrough uses selected GPT-style models and a small nano-GPT learning task.

**Teaching use:** optional spatial overview after the learner has seen the simpler 2D data-flow diagram. Ask which tensors are created, transformed, reused or discarded.

**Boundary:** 3D placement and block size are visualization conventions, not physical model structure. Name the selected model and task.

### Attention variants

Raschka's guide compares MHA, MQA, GQA, MLA, sliding-window and sparse attention.

**Teaching use:** organize comparison by the bottleneck each mechanism changes: query versus key/value head counts; cached K/V size and representation; number of context positions attended to; dense versus sparse computation; kernel/runtime compatibility.

**Boundary:** these are not interchangeable optimization knobs. Lower KV-cache size, fewer attention operations and faster wall-clock inference are different outcomes. Benchmarks require matched hardware, sequence lengths, batch sizes, kernels and quality criteria.

### Mixture of Experts

Grootendorst's guide separates experts, sparse layers, routing, selection, capacity and load balancing.

**Teaching use:** deterministic routing exercise: assign token router scores, select top-k experts, count tokens per expert, then show how capacity or balancing objectives change assignment.

**Boundary:** distinguish total parameters from parameters activated per token, routing FLOPs from expert FLOPs, training-time auxiliary losses from inference-time dispatch, and theoretical sparsity from realized throughput.

### Inference handbook

The Modular handbook covers request lifecycle, prefill/decode, TTFT, tokens per second, continuous batching, prefix caching, GPU memory and serving patterns, with interactive visualizers and calculators.

**Teaching use:** connect the autoregressive loop and KV-cache explanations to operational metrics. Learners should calculate a simple KV-cache estimate and compare prefill-heavy versus decode-heavy requests.

**Boundary:** living vendor-maintained engineering reference. Separate general mechanisms from product-specific guidance and date benchmark/hardware claims.

### Neuronpedia

The platform documents sparse autoencoders, MLP neurons, steering, circuit tracing and attention-head exploration. Its auto-interpretability documentation says many feature explanations are generated by AI models from top activations.

**Teaching use:** inspect a feature's activations, formulate a hypothesis, test counterexamples, compare explanation methods, and distinguish correlation from intervention.

**Boundary:** natural-language feature labels can be incomplete, unstable or misleading. A feature dashboard, attention head or attribution graph is not automatically a faithful causal explanation.

### Embedding Atlas

Apple's research and repository describe interactive projections, clustering and labels, density contours, nearest-neighbour search, metadata cross-filtering and linked dashboards. The software repository declares an MIT licence.

**Teaching use:** explore a known dataset with labels and metadata; compare nearest neighbours, clusters and outliers; inspect original vectors and metadata for selected points.

**Boundary:** a 2D projection is not the original embedding geometry. Apparent distance, cluster shape and separation depend on projection and clustering choices. The software licence does not automatically license paper figures or datasets.

### TensorFlow Playground

The official project is a browser-based neural-network playground, with editable features, hidden layers, activation, learning rate, regularization and train/test loss.

**Teaching use:** vary one factor at a time, state a prediction, observe train/test loss and decision boundaries, and explain overfitting.

**Boundary:** not a Transformer, sequence model or LLM. Its value is general learning dynamics, not token prediction.

## Coverage gaps and proposed work

| Priority | Proposed work | Acceptance criterion |
|---|---|---|
| P1 | Bilingual comparison of attention variants | Compare mechanism, cache/computation impact, assumptions, quality trade-offs and implementation constraints; cite primary references |
| P1 | Inference lifecycle lab | Prefill/decode, KV cache, TTFT/TPOT, batching and memory linked in one traceable request example |
| P1 | MoE routing experiment | Deterministic top-k example, expert-load histogram, capacity edge case, active/total parameter distinction |
| P2 | Visual embedding exploration | Dataset and embedding model pinned; nearest-neighbour and projection caveats; reproducible observations |
| P2 | Interpretability investigation | Feature activation evidence, counterexamples, uncertainty and causal limitations |
| P3 | Transformer practice worksheet | Predict before interacting, record observations, change one variable at a time, check one operation against code/math |

Do not create all proposed pages immediately. Inspect the page inventory and concept graph first; place each activity on an existing page where possible. Create a new page only when its learner question is not already served.

### Existing coverage check before implementation

A repository-level page and review check confirms that several P1 themes already have substantial homes:

- `site/fr/hybrid-llm-architectures.qmd` and its English counterpart already explain GQA, KV-cache scaling, MoE, Mamba-2, and the distinction between global attention and recurrent state. They should be extended only where the new attention-variants comparison adds a genuinely missing mechanism.
- `site/fr/transformer-architectures.qmd` and its English counterpart compare encoder-only, encoder–decoder, and decoder-only families. They answer a different question from MHA/MQA/GQA/MLA and should not be overloaded with head-layout implementation details.
- The existing pedagogical audit `docs/source-reviews/transformer-attention-pedagogical-comparison-2026-11.md` already compares the Illustrated Transformer, 3Blue1Brown, and Transformer Explainer. Reuse its learning sequence and notation warnings rather than repeating that source review.
- `docs/source-reviews/raschka-full-to-hybrid-attention-2026-11.md` already distinguishes sparse/local attention from bounded recurrent state and documents the limits of the author's open-model sample. Do not flatten those mechanisms into a single “efficient attention” category.

**Implementation completed on 2026-11-16:** the comparison is now a bilingual extension to the existing Build-path Transformer-block walkthrough, with two matching exercises. It separates (1) query-head versus KV-head sharing (MHA/MQA/GQA), (2) latent KV compression (MLA), and (3) context-selection patterns (sliding-window/sparse attention). The cache-size equation and a 32-Q-head example make the memory effect calculable; the text distinguishes KV-state size, attention connectivity, and memory-transfer cost. It explicitly states that the NumPy reference block implements MHA only and does not claim to execute the other variants. The conceptual Q/K/V pages link to this comparison. Hybrid recurrent/state-space mechanisms remain a separate family, linked to the existing hybrid-architecture lesson.

## Source and evidence boundary

This review used official project/author pages, repository descriptions and indexed excerpts to identify scope and pedagogical roles. It did not fully inspect every article, execute every interactive tool, reproduce benchmarks, verify every architecture example against primary model papers, or test accessibility/responsive behavior. New source records therefore remain partially-scanned; no figure reuse rights are inferred from public accessibility.

Primary/official destinations consulted:
- Transformer Explainer: https://poloclub.github.io/transformer-explainer/ ; https://research.ibm.com/publications/transformer-explainer-learning-llm-transformers-with-interactive-visual-explanation-and-experimentation
- Bbycroft: https://bbycroft.net/llm
- TensorFlow Playground: https://playground.tensorflow.org/ ; https://github.com/tensorflow/playground
- Attention variants: https://magazine.sebastianraschka.com/p/visual-attention-variants
- MoE: https://www.maartengrootendorst.com/blog/moe/
- Inference: https://handbook.modular.com/ ; https://github.com/modular/llm-inference-handbook
- Neuronpedia: https://www.neuronpedia.org/ ; https://docs.neuronpedia.org/
- Embedding Atlas: https://apple.github.io/embedding-atlas/ ; https://machinelearning.apple.com/research/embedding-atlas ; https://github.com/apple/embedding-atlas
