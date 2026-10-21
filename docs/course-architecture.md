# Course architecture and coverage plan

Status: **structure only**. This document defines intended coverage and navigation; it is not a claim that the lessons or exercises already exist. Do not add lesson content, model implementations, or experiments merely to fill this outline. Expand topics only when existing knowledge is reviewed and the learning need is clear.

## Design principles

- Bilingual French/English course; equivalent concepts share the same scope, caveats, and references.
- Hierarchical navigation follows conceptual dependencies, not the order in which code happens to be written.
- A synthesis page explains how components connect; a concept page owns one canonical explanation. Avoid duplicating the same derivation in multiple pages.
- Every technical claim should distinguish definition, assumptions, empirical evidence, and limitations.
- Visuals should be original or used with verified permission; cite external sources next to the figure and in the references catalogue.
- Exercises live in a separate section. A lesson's question links to the relevant exercise topic, and exercises link back to prerequisite concepts.
- Do not reproduce the book's prose, figures, exercises, or solutions. Use the book as a coverage checklist and cite it as a source.
- Public portfolio content must not expose private employer data, confidential benchmarks, or unsupported claims.

## Proposed site navigation

1. **Start here / Démarrer**
   - Purpose, prerequisites, learning modes, glossary, how to read equations and diagrams.
   - Course map and coverage matrix.
2. **Mathematical and computational foundations / Fondations**
   - Scalars, vectors, matrices, tensors, dimensions and broadcasting.
   - Linear maps, matrix multiplication, norms, dot products, cosine similarity.
   - Derivatives, chain rule, computational graphs, backpropagation.
   - Probability distributions, log probabilities, entropy, cross-entropy, KL divergence.
   - Logits, softmax, likelihood, loss reductions, numerical stability, gradients and optimization.
   - Train/validation/test splits, leakage, uncertainty, statistical comparisons.
3. **Text and data / Texte et données**
   - Unicode and normalization; word-, character-, subword- and byte-level tokenization.
   - Vocabulary, token IDs, special tokens, BPE, encode/decode and tokenizer/model compatibility.
   - Embedding lookup versus linear projection; embedding spaces and contextual representations.
   - Sequence lengths, truncation, padding, masks, sliding windows, batches and data loaders.
   - Next-token input/target shifts, corpus quality, deduplication and contamination.
4. **Attention / Attention**
   - Motivation and historical context; self-attention versus cross-attention.
   - Queries, keys, values and learned projections.
   - Scaled dot-product attention, softmax axes, tensor shapes and numerical issues.
   - Causal/padding masks; information-flow tests and leakage counterexamples.
   - Multi-head attention, head dimensions, output projection and parameter counts.
   - Position information: absolute embeddings, sinusoidal encodings, RoPE and limits.
   - Attention interpretation: weights are not causal explanations by themselves.
5. **Transformer and GPT architecture / Architecture**
   - Residual paths, LayerNorm/RMSNorm, feed-forward networks and activation functions.
   - Pre-norm/post-norm distinctions; block composition and tensor-shape tracing.
   - Decoder-only versus encoder-only and encoder-decoder architectures.
   - Embedding/output weight tying, vocabulary projection, logits and probability distributions.
   - Parameter counting, context window and architectural trade-offs.
6. **Generation and inference / Génération**
   - Autoregressive factorization and teacher forcing.
   - Greedy decoding, sampling, temperature, top-k/top-p and stopping rules.
   - Repetition and decoding pathologies; probability versus factuality.
   - KV cache, prefill versus decode, batching, latency/throughput and memory.
   - Quantization and inference constraints; compare quality, latency and memory fairly.
7. **Pretraining / Pré-entraînement**
   - Dataset construction, source provenance, filtering, deduplication and contamination.
   - Causal language-model objective, batching and loss masking.
   - Initialization, optimizers, learning-rate schedules, warm-up, gradient clipping.
   - Training loop, checkpoints, validation loss and perplexity; what these metrics do not show.
   - Overfitting, underfitting, data/compute trade-offs, seeds and reproducibility.
   - Debugging loss curves and generated samples without overclaiming from a single run.
8. **Evaluation and experimental reasoning / Évaluation**
   - Evaluation design, held-out sets, baselines, uncertainty and statistical comparisons.
   - Perplexity and tokenization comparability; task-specific metrics.
   - Human evaluation, pairwise preference, rubric quality and inter-rater variability.
   - Calibration, robustness, distribution shift, contamination and data leakage.
   - Error taxonomies, ablations, negative results and reproducible experiment reports.
9. **Fine-tuning / Ajustement**
   - Classification fine-tuning: label mapping, pooling, heads, imbalance and metrics.
   - Instruction data: formats, roles, prompt/response boundaries and target masking.
   - Supervised fine-tuning (SFT), validation, overfitting and catastrophic forgetting.
   - LoRA/QLoRA: low-rank update, rank, target modules, trainable parameters, memory trade-offs.
   - Checkpoint loading, tokenizer compatibility, quantization, merge/unmerge and evaluation.
10. **Instruction following, preference and reasoning / Alignement et raisonnement**
    - What SFT can and cannot teach; preference data and reward-model concepts.
    - High-level map of RLHF/DPO and their assumptions (separate from implementation details).
    - Reasoning-time compute, self-consistency, search, distillation and evaluation pitfalls.
    - Safety, refusal, prompt injection and limitations of benchmark-based claims.
11. **Beyond the book / Au-delà du livre**
    - Retrieval-augmented generation (RAG): chunking, retrieval, reranking, grounding and evaluation.
    - Tool use and structured outputs; orchestration versus model capability.
    - Modern attention variants: grouped-query attention, sliding windows, sparse attention and latent attention.
    - Mixture-of-experts, routing, memory/compute trade-offs.
    - Multimodal extensions: text-image/audio/video at conceptual level.
    - Interpretability and mechanistic hypotheses; correlation versus causal evidence.
    - Data governance, privacy, licensing, environmental cost, societal impact and domain-specific risk.
12. **Exercises / Exercices** (separate section; see below)
    - Concept checks, mathematical derivations, shape tracing, counterexamples, code reading, debugging, experimental design and synthesis tasks.
    - Solutions/hints are separated from prompts; each task declares prerequisites, expected evidence, and difficulty.
13. **References and provenance / Références**
    - Primary papers, books, official documentation, visual sources and licence notes.

## Coverage against *Build a Large Language Model (From Scratch)*

Use the following as a minimum coverage checklist; verify against the current official repository and book edition before declaring coverage complete.

| Book component | Planned destination | Required conceptual coverage |
|---|---|---|
| Ch. 1 — Understanding LLMs | Start here; GPT architecture; generation | What an LLM is, pretraining, generation, limitations and scope |
| Ch. 2 — Working with Text Data | Text and data | Tokenization, token IDs, vocabulary, embeddings, data windows, input/target batches |
| Ch. 3 — Coding Attention Mechanisms | Attention | Basic attention, trainable Q/K/V, causal attention, multi-head attention |
| Ch. 4 — Implementing a GPT Model | Transformer and GPT architecture | GPT components, residual connections, normalization, MLP, output head |
| Ch. 5 — Pretraining on Unlabeled Data | Pretraining; Generation; Evaluation | Training loop, loss, optimizer, sampling, validation, checkpointing and generated outputs |
| Ch. 6 — Finetuning for Text Classification | Fine-tuning | Classification head, labels, pooling/selected token, metrics and evaluation |
| Ch. 7 — Finetuning to Follow Instructions | Fine-tuning; Instruction following | Instruction examples, target masks, training, generation and evaluation |
| Appendix A — PyTorch | Computational foundations | Tensors, modules, autograd, datasets/loaders, optimization and device basics |
| Appendix B — References | References | Traceable bibliography and follow-up reading |
| Appendix C — Exercise solutions | Exercises | Independent practice and separately presented hints/solutions |
| Appendix D — Training-loop improvements | Pretraining | Validation, sampling, checkpointing, training-loop diagnostics |
| Appendix E — LoRA | Fine-tuning | Low-rank adaptation, trainable parameters and efficiency trade-offs |
| Repository bonus materials | Beyond the book | BPE details, embedding-vs-linear distinction, KV cache, FLOPs, architecture variants, performance and memory |

Coverage should be tracked as **planned / existing / needs review / verified**, not inferred from the presence of a page title. A page counts as covered only after the explanation, assumptions, misconceptions, references, and links have been reviewed.

## How to use complementary sources

- **Raschka's book and official repository:** use the chapter order and accompanying notebooks as a completeness checklist for the educational end-to-end path. The repository also points to optional material on BPE, KV cache, FLOPs, modern attention variants, MoE, performance and architecture families. These are scope signals, not a mandate to implement them now.
- **The Illustrated Transformer From Scratch (ACM-hosted page):** use as a complementary conceptual viewpoint for attention as cross-position information flow; distinguish that from the position-wise MLP. Add a careful note about permutation equivariance without positional information, and contrast the article's simplified attention equations with learned Q/K/V projections, scaling and masks in practical GPT blocks. Treat architectural ordering (residual/normalization) as variant-dependent, not universal.
- **Jay Alammar's Illustrated Transformer / Illustrated GPT-2 and 3Blue1Brown:** use for visual sequencing and intuition; do not copy external images unless the licence or explicit permission supports it. Prefer original diagrams with attribution to the ideas and references.
- **Primary sources:** where an explanatory blog simplifies or makes a broad claim, link to the relevant paper or official documentation and state the scope.

## Separate exercise-space structure

Create a top-level **Exercises / Exercices** navigation section, with a bilingual landing page and one index per module. Exercise identifiers should be stable, language-neutral IDs so links remain valid when wording changes.

Each exercise entry should eventually contain:
- ID and title;
- concept page and prerequisites;
- type (conceptual, mathematical, tensor-shape, code reading, debugging, experimental design, synthesis);
- difficulty and estimated effort;
- prompt, expected deliverable and acceptance criteria;
- optional hint, then solution/explanation in a separate disclosure or page;
- references and common failure modes;
- status: planned / drafted / reviewed.

Lesson question blocks should link to a relevant exercise ID, not duplicate the exercise text. Exercise pages should link back to the canonical lesson. The first scaffold must not contain fabricated questions or answers: it should define the categories and stable destinations only.

## Initial implementation sequence (structure only)

1. Add this architecture and coverage plan.
2. Add French and English exercise landing pages with the module taxonomy and explicit “planned, not yet authored” status.
3. Add an Exercises section to Quarto navigation and rendering configuration.
4. Add links from existing control-question sections to the exercise hub/module anchors; do not invent exercise content.
5. Audit FR/EN navigation parity and verify all internal links and rendered pages.
6. Only after review, fill individual exercise prompts; do not add implementations until prerequisites are validated in `career-knowledge`.
