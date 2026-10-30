# Full LLM curriculum and coverage plan

**Status:** planning only. This document defines scope, dependencies, page ownership, and acceptance criteria. It does not authorize drafting all lessons, adding model implementations, or running new experiments immediately.

**Primary baseline:** Sebastian Raschka, [*Build a Large Language Model (From Scratch)* source repository](https://github.com/rasbt/LLMs-from-scratch). The repository evolves; re-check its README and chapter folders before marking coverage complete.

**Complementary explanations:** [Jay Alammar, The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/), [The Illustrated Transformer From Scratch](https://idtjo.hosting.acm.org/wordpress/the-illustrated-transformer/), [Jay Alammar, The Illustrated GPT-2](https://jalammar.github.io/illustrated-gpt2/), and [3Blue1Brown's GPT lessons](https://www.3blue1brown.com/lessons/gpt/).

## 1. Editorial contract

The first-pass status of existing pages is tracked in the [public page audit inventory](page-audit-inventory.md). It is deliberately partial: source inspection, rendered-page review, scientific validation, and learner mastery are tracked separately.

The shared [reader-experience and editorial method](reader-experience-and-editorial-method.md) defines progressive disclosure, non-linear navigation, page types, and review criteria. This curriculum document defines topic coverage and dependencies; where wording could imply that every reader must follow one fixed sequence, use the shared method as the reader-experience rule.

- Keep the course bilingual (French and English) and the concept pages canonical: explain one concept deeply, then link to it instead of duplicating it.
- Separate overview pages, concept pages, exercises, implementations/tests, experiment reports, and private mastery evidence.
- Treat the curriculum as a navigable concept graph with a suggested route, not a mandatory linear book. Each overview should work without requiring mastery of every linked deep dive; each deep dive should connect back to the system-level question.
- Explain intuition, notation, tensor shapes, assumptions, numerical issues, misconceptions, counterexamples, failure modes, and limits—not just the happy path.
- Cite research papers and official documentation for technical claims. Attribute external diagrams and link to their original pages. Do not copy an illustration merely because it is publicly accessible.
- State clearly what exists, what has been validated, and what is only planned. A passing test, rendered page, low training loss, or completed exercise does not by itself demonstrate mastery.
- Before a new implementation or experiment, validate only the **specific minimum conceptual prerequisites** needed for that next step in the private `career-knowledge` inventory. Learn local tensor, probability, and gradient operations in context; optional general mathematics and advanced derivations are not blanket gates for building a small GPT.
- Use Raschka's book and repository as a **coverage baseline**, not as text, code, or exercise material to reproduce. Write original explanations and exercises; link to the source.
- The ACM-hosted article presents a useful modern-block perspective, but it is not a substitute for explaining the original encoder–decoder Transformer and why decoder-only GPT differs.

## 2. Target information architecture

Organize the learning experience around **conceptual understanding, experimentation, and flexible navigation**, not language count or chapter-by-chapter parity with a source book. Maintain one conceptual source of truth; translations are alternate presentations of the same structure, not separate pedagogical tracks.

### Three complementary learning depths

#### Level 1 — Big-picture overview

Purpose: form a correct mental model of the complete system before studying every detail.

- Explain what an autoregressive LLM does, its inputs and outputs, what training optimizes, and how the main components connect.
- Prefer a coherent visual map, a small number of clear diagrams, and a concise narrative.
- Keep mathematics light initially, but avoid misleading simplifications; link to the precise formulation.
- Make every major component clickable or otherwise directly linked to its concept page and relevant experiment.
- This level should be useful even to readers who do not intend to follow a complete course.

The 3Blue1Brown video is a useful reference for the role of a visual overview, not a template to copy or a substitute for LLM Lab's own map.

#### Level 2 — Guided model-building path

Purpose: provide a dependency-aware route from text to a working small language model. The sequence below follows the computation graph rather than the order in which concepts happen to be introduced in a book.

1. **Text and tokenization:** text normalization, token IDs and special tokens.
2. **Training examples:** context windows, shifted inputs/targets, batching and data hygiene.
3. **Input representations:** tensor shapes, embedding lookup and positional information.
4. **Contextual computation:** Q/K/V, attention, causal masking, multi-head attention, residual connections, normalization and MLP/FFN blocks.
5. **Prediction:** output projection, vocabulary logits and probability distributions.
6. **Learning objective:** likelihood, cross-entropy, loss, gradients and optimization signal.
7. **From-scratch training:** optimizer updates, validation, checkpoints, reproducibility and learning curves.
8. **Inference and generation:** autoregressive decoding, stopping rules and context-window constraints.
9. **Verification and evaluation:** compatible reference comparisons, task-specific baselines, uncertainty and error analysis.

**Separate adaptation branch:** pretrained checkpoint loading, classification, instruction SFT, LoRA and quantization. This branch reuses learned parameters; it is not a stage of training a GPT from random initialization.

Use Raschka's *LLMs from Scratch* as an important implementation and coverage reference, not as a chapter structure to mirror. Connect the build path to concept pages, experiments, mathematical explanations, critical analysis, and tests.

#### Level 3 — Deep dives and open exploration

Purpose: let readers pursue a question without completing the guided path first.

- Define notation, state assumptions, explain local prerequisites, and include a worked example or derivation where appropriate.
- Link to the big-picture component, guided-path position, prerequisite concepts, related concepts, experiments, tests and sources.
- Support lateral exploration rather than only forward/backward navigation.
- Explain why a prerequisite matters and, where practical, offer a short recap or expandable explanation.
- Include counterexamples and failure conditions where they clarify the limits of an intuition or claim.
- Keep advanced topics optional unless needed to understand the core model.

Deep-dive clusters include data/representation; tensors and probability; attention and architecture; training and generation; fine-tuning and efficiency; and critical evaluation (leakage, contamination, uncertainty, ablations, representation geometry and reproducibility).

### Laboratory layer — diagrams, animations, interactions, experiments

The laboratory identity must be substantive, not just branding. Visual material and interactivity should answer specific learning questions.

- **System diagrams:** component relationships, data flow, tensor shapes, and differences between training and inference.
- **Animated explanations:** sequential operations, attention weighting, token-by-token generation, gradient updates, or other genuinely dynamic mechanisms.
- **Interactive visualizations:** controls with visible consequences, such as sequence length, attention masks, temperature, top-k/top-p, learning rate, or embedding geometry.
- **Runnable experiments:** a question, baseline, method, observable result, interpretation, and limitations.
- **Tests and counterexamples:** unit/property tests and minimal examples exposing shape errors, leakage, incorrect assumptions, or cases where a heuristic fails.

Prioritize explanatory value over novelty. A static diagram is preferable to an animation that adds no insight. An interactive widget is justified only if manipulation reveals a relationship that a static explanation would communicate less effectively.

Each artifact should state what it represents, assumptions, what the reader can change, what to observe, and what cannot be concluded. Provide accessible text and a non-interactive fallback. Avoid duplicating core model logic in JavaScript when Python can be reused safely; choose technologies according to portability, maintainability, reproducibility and GitHub Pages constraints.

### Page contract and navigation

Major topics should provide, as appropriate:
- **Role in the system:** why the concept exists.
- **Inputs → operation → outputs:** ideally a diagram, including shapes and notation when relevant.
- **Intuition and precise formulation:** separated where useful, without contradiction.
- **Explore:** prerequisites, related concepts, guided path and relevant experiment.
- **Verify:** worked example, tests, implementation or source evidence where available.
- **Limits:** assumptions, misconceptions, counterexamples and open questions.

Overviews should remain concise and link outward; deep dives should own detailed explanations to avoid duplicated derivations. Not every page needs every artifact; omissions should reflect the topic's scope.

### Concept dependencies and implementation gates

`raw text → tokens/IDs → context windows + shifted targets`

`token IDs → embeddings + positional information → Transformer blocks → contextual states → logits/probabilities`

`logits + aligned targets → loss → gradients → optimizer updates → trained checkpoint`

`trained checkpoint → autoregressive decoding → generated sequence`

`pretrained checkpoint → task/adaptation head or SFT → adapted model` (separate branch)

`evaluation protocol` is cross-cutting: it informs data selection, training decisions, reference checks, generation analysis and adaptation; it is not a final computational stage.

These dependencies guide navigation but are not rigid gates to reading. Introduce concepts intuitively when useful, then link to rigorous derivations. Deep dives must also be accessible from search, glossary entries, diagrams and related-concept links.

Before implementing a downstream mechanism, identify its few genuinely essential prerequisites and review those against the private acquired/to-review/missing knowledge inventory. If one is missing, teach or test that specific concept at the point of use before proceeding. Do not require completion of a general mathematics or tensor curriculum when a local explanation and a small checked operation are sufficient. This gate applies to implementation scope, not to reading the overview or accessing optional deep dives.

### Exercises

Keep exercises distinct from lesson prose, with stable exercise IDs across translations. Each exercise links to its concept page and guided-path context; concept pages link back to relevant exercises. Hide answers by default and distinguish conceptual checks, code tasks, and experimental investigations.

## 3. Coverage map against Raschka

This map follows the chapter and appendix structure advertised in the upstream repository README. It is a scope checklist, not a claim that LLM Lab already covers all details.

| Upstream topic | LLM Lab destination / planned destination | Current coverage status |
|---|---|---|
| Ch. 1 — Understanding LLMs | Orientation, Transformer overview, glossary, history | Partial: high-level GPT flow exists; broaden LLM families, training stages, limits and terminology after prerequisite review. |
| Ch. 2 — Working with text data | Text/data module; tokenization, BPE, special tokens, windows, dataloader | Gap: not yet a dedicated, comprehensive bilingual chapter. |
| Ch. 3 — Coding attention mechanisms | Q/K/V, scaled dot-product attention, causal masking, multi-head attention | Partial: conceptual pages exist; detailed shape contracts and implementation are not yet complete. |
| Ch. 4 — Implementing a GPT model | [EN/FR Transformer overview](../site/en/transformer.qmd); tensor, embedding and positional-encoding concept pairs; audit [#98](https://github.com/JM-Brun/llm-lab/issues/98) | Partial (source audit, 2026-10-29): system data flow and component roles are explained conceptually. Not evidenced as a complete, tested GPT: configuration contract, block-order/shape trace, parameter accounting, weight tying, and train/eval dropout tests remain gaps. See the dated audit section below; no implementation is authorized before the private prerequisite gate. |
| Ch. 5 — Pretraining on unlabeled data | Pretraining, optimizer/training loop, validation, generation, checkpointing | Gap/partial: objective concepts exist; full reproducible pretraining account is not present. |
| Ch. 6 — Fine-tuning for text classification | Fine-tuning/classification | Gap: dedicated coverage and validated implementation not present. |
| Ch. 7 — Fine-tuning to follow instructions | SFT, instruction data, masking, evaluation | Partial elsewhere in the career learning programme, but no complete public bilingual course module yet. Map to existing canonical knowledge before writing. |
| Appendix A — PyTorch introduction | Tensor shapes, autograd, modules, datasets/dataloaders, device and reproducibility | Gap: only add the prerequisite depth actually needed; link official PyTorch docs. |
| Appendix B — References and further reading | Reference library | Partial: references exist; expand and categorize when the plan is reviewed. |
| Appendix C — Exercise solutions | Separate exercise area with hidden answer keys | Planned structure; no new exercises/solutions in this planning change. |
| Appendix D — Training-loop improvements | Training-loop diagnostics, scheduling, clipping, logging and checkpointing | Advanced/optional gap. |
| Appendix E — LoRA | Parameter-efficient fine-tuning, rank/alpha/target modules, memory and evaluation | Conceptual material exists in the private career track; public bilingual coverage needs a future mapped review. |
| Bonus — tokenizer variants, dataloaders, embedding vs linear layers | Text-data concepts and exercise collection | Gap; cover only after core text-data concepts are validated. |
| Bonus — optimized attention, buffers, KV cache, FLOPs | Attention/inference/efficiency modules | Gap; distinguish conceptual description from measured performance. |
| Bonus — GQA, MLA, sliding-window attention, DeltaNet, MoE, KV sharing | Advanced architecture variants | Not core parity for the first pass; add as optional comparative notes with current primary sources. |
| Bonus — other model families, e.g. Llama/Qwen/Gemma | Architecture comparison and reference loading | Optional extension; avoid claiming one GPT implementation represents all LLMs. |
| Bonus — dataset utilities, evaluation, DPO, UI | Data quality, evaluation and preference optimization | Partial/gap; keep UI building out of the core learning objective. |
| Related Reasoning From Scratch material — verifier-based evaluation, self-consistency/refinement, RLVR/GRPO | Advanced evaluation and inference-time reasoning | Beyond the book baseline; candidate extensions, not initial requirements. |

## 4. Complementary perspectives to incorporate

### Jay Alammar — The Illustrated Transformer / Illustrated GPT-2
Use for visual intuition about embeddings, positional information, encoder–decoder flow, residual paths, attention, decoder blocks and GPT-2 data flow. Explicitly distinguish the original encoder–decoder Transformer from decoder-only GPT. Link to the author's figures rather than copying them. Check the source page's current version before citing a particular detail.

### ACM — The Illustrated Transformer From Scratch
Use as a complementary modern-architecture explanation: self-attention as the operation that mixes information across sequence positions; position-wise MLP as a per-vector operation; residual connections and normalization; and a comparison of modern model families. Explain that this framing is an abstraction: convolutional, recurrent, cross-attention, or other interactions can exist in broader architectures, and details vary across implementations.

### Harvard NLP — The Annotated Transformer

Use [the maintained annotated implementation](https://nlp.seas.harvard.edu/annotated-transformer/) to connect the original paper's equations to code and to see implementation choices made explicit. It is a bridge between paper and executable reference, not a current universal GPT blueprint: it follows the original encoder–decoder Transformer and has version-specific software and training conventions. Prefer the current version over the older 2018 URL when linking, and state which version is being discussed.

### DeepLearning.AI — How Transformer LLMs Work

Use [this course by Jay Alammar and Maarten Grootendorst](https://www.deeplearning.ai/courses/how-transformer-llms-work) as a compact, modern visual/video treatment of tokenization, embeddings, attention, Transformer blocks, and selected efficiency variants. It complements rather than replaces written derivations, primary papers, or runnable code. Course access and terms may change; do not make core learning dependent on enrollment or availability.

### Raschka's source repository
Use its chapter README files, notebooks, bonus folders, and code as a living index of topics, not as text to copy. At review time, distinguish:
- book core chapters and appendices;
- optional bonus implementations and architecture variants;
- newer material added after the book's original scope.
Pin links to the most specific upstream file where useful, and record the date reviewed.

### Visual policy
Prefer original SVG diagrams that clarify tensor flow, shapes, masking, train-vs-inference differences, or competing architecture choices. Each figure needs alt text and a nearby explanation of what it does **not** show. External images should be embedded only when reuse terms allow it; otherwise link to the original source. Keep a provenance entry for every external visual actually embedded.

## 4a. Existing-page audit: high-value additions before new lessons

This is a targeted gap analysis, not an instruction to add all the material now. Review each item against the current page and add only information that resolves a real omission or misconception.

| Existing canonical page(s) | Useful complementary material | Proposed treatment |
|---|---|---|
| `site/fr/transformer.qmd`, `site/en/transformer.qmd` | Raschka Ch. 1 and Ch. 4; Alammar's original encoder–decoder diagram and GPT-2 walk-through; 3Blue1Brown's animated intuition; Harvard NLP's annotated implementation; DeepLearning.AI's modern visual course; ACM's modern-block explanation | Keep the overview concise. Curate resources by role (intuition, original formulation, code, modern overview), explain the scope of each, and avoid implying that one architecture or implementation represents all GPT/LLM families. |
| `queries-keys-values.qmd` (FR/EN) | Raschka Ch. 3; ACM's interpretation of attention as cross-position information mixing | Check notation and tensor shapes end-to-end; distinguish learned projections from human-readable semantic labels; make clear that Q/K/V dimensions need not all match. Add shape tables only if they clarify the existing derivation. |
| `scaled-dot-product-attention.qmd` (FR/EN) | Raschka Ch. 3; ACM's weighted-sum derivation; 3Blue1Brown's animated intuition | Ensure the sequence scores → scale → mask where applicable → softmax → weighted sum is explicit, with the axis of softmax and shapes stated. Explain that weights are relative and do not constitute causal explanations of model output. |
| `causal-masking.qmd` / existing causal-mask illustration | Raschka Ch. 3–5; ACM's separation of position-mixing and position-wise operations | Preserve the distinction between a mask matrix and an end-to-end causal invariant. Make the future-token perturbation test the conceptual acceptance criterion; do not add code before knowledge is validated. |
| `tensors.qmd` (currently FR) | Raschka's notebook shapes and PyTorch appendix; Alammar's visual tensor flow | Plan an English counterpart before declaring bilingual coverage complete. Add shape annotations at key operations and distinguish batch, sequence, feature, head and vocabulary axes. |
| `embedding-space.qmd`, `positional-encoding.qmd` (currently FR) | Raschka Ch. 2/4 and the repository's architecture examples; Alammar's embedding/position visuals | Plan English counterparts. Distinguish token embedding lookup, contextual hidden states, learned absolute positions and rotary position mechanisms; avoid implying RoPE is an additive position embedding. |
| `mathematical-foundations.qmd`, logits, probabilities, likelihood, loss, gradients (FR/EN) | Raschka Ch. 5 objective and training code; official PyTorch loss conventions | Link the mathematical objective to shifted targets, ignored tokens, reduction conventions, and the reported validation loss. Keep notation consistent and do not conflate token loss with aggregate training loss. |
| `cross-entropy.qmd`, `entropy.qmd` (FR/EN) | Raschka's pretraining objective; 3Blue1Brown and Shannon/Cover–Thomas references | Preserve the distinction between entropy, cross-entropy, KL divergence, negative log-likelihood and perplexity. Add a compact relation diagram only if it prevents a specific misconception. |
| Existing glossary and Transformer history | Raschka Ch. 1 and upstream model-family examples; Alammar's original-versus-GPT-2 distinction | Add terms only when they appear in the course; date/version claims and link to primary sources. Avoid treating GPT-2 as representative of every current architecture. |
| Existing public course generally | Raschka chapters 2, 5, 6, 7 and appendices D/E | Main coverage gaps: text data/tokenization; complete training/pretraining flow; classification fine-tuning; instruction fine-tuning; evaluation; training-loop details; LoRA. Do not fill these gaps with broad summaries until prerequisite knowledge and page ownership are clear. |

## 5. Suggested sequencing and gates

1. **Inventory first:** map every existing page to the plan; identify duplicates, gaps, language asymmetry, and missing cross-links.
2. **Minimum-knowledge gate:** check only the essential concepts needed for the next implementation step against `career-knowledge`. Introduce the required operation locally; do not make optional mathematical depth a global prerequisite.
3. **Improve existing pages:** correct claims, equations, terminology, counterexamples, references and figures before adding new pages.
4. **Plan review:** confirm scope and ordering; mark each planned module core or optional.
5. **Exercise framework:** create the navigation and link convention first; populate only after course concepts and prerequisite knowledge are validated.
6. **New concept pages:** add one canonical bilingual pair at a time, only for a real gap.
7. **Implementation and experiments:** only after the relevant knowledge gate, with explicit tests, baselines, provenance and limitations.

## 6. Definition of coverage

A topic is considered covered only when:
- a canonical explanation exists in French and English with equivalent claims and caveats;
- notation, tensor shapes and assumptions are explicit where relevant;
- at least one common misconception or discriminating counterexample is addressed where pedagogically useful;
- references support the claims and external visual provenance is clear;
- internal links and rendered math work;
- any implementation claim is backed by actual code/tests, not planned work;
- the learner can answer an unfamiliar transfer question and explain failure conditions, with mastery recorded privately in `career-knowledge`.

A topic is **not** covered merely because it appears in a heading, a diagram, a link, a checklist, or a roadmap.

## 7. Upstream references

- Raschka, [LLMs-from-scratch repository and chapter index](https://github.com/rasbt/LLMs-from-scratch).
- Raschka, [How to best read this book](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch01/reading-recommendations.md).
- Alammar, [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/).
- Alammar, [The Illustrated GPT-2](https://jalammar.github.io/illustrated-gpt2/).
- [The Illustrated Transformer From Scratch (ACM-hosted article)](https://idtjo.hosting.acm.org/wordpress/the-illustrated-transformer/).
- [3Blue1Brown — Transformers, the tech behind LLMs](https://www.3blue1brown.com/lessons/gpt/).


## 8. Original editorial architecture: principles first, not book-chapter parity

**Editorial decision:** LLM Lab is an original, source-synthesizing learning book. No single external book determines its chapter order. Raschka is one practical implementation path and coverage reference among several, not the book's table of contents. Organize the book around scientific questions, mathematical objects, mechanisms, and evidence; compare sources where they disagree or emphasize different aspects.

### 8.1 The central explanatory chain

1. **Uncertainty and information:** probability distributions, entropy, conditional entropy, cross-entropy, KL divergence, and mutual information.
2. **Statistical estimation:** likelihood, log-likelihood, maximum likelihood estimation (MLE), empirical risk, sampling assumptions, and generalization.
3. **Predictive language modeling:** sequence probabilities, autoregressive factorization, conditional next-token prediction, and the training objective.
4. **Optimization and representation learning:** logits, softmax, negative log-likelihood, gradients, backpropagation, optimization, and numerical stability.
5. **Architectural inductive biases:** tokenization, embeddings, positional information, attention, residual paths, normalization, and feed-forward blocks as design choices with trade-offs.
6. **Training and inference:** teacher-forced training versus autoregressive generation, shifted targets, causal constraints, decoding, caching, latency, and memory.
7. **Adaptation and evaluation:** classification fine-tuning, instruction tuning, preference optimization, retrieval-augmented systems, tools, and the limits of each technique.
8. **Evidence and limitations:** held-out data, baselines, calibration, ablations, uncertainty, contamination, robustness, and resource accounting.

This is a dependency graph rather than a rigid linear syllabus: information theory supports the statistical objective; the objective motivates training; the architecture parameterizes the distribution; evaluation tests claims about the resulting system. Each chapter should make these connections explicit.

### 8.2 The mathematical bridge: entropy, likelihood, cross-entropy and LLM training

For a token sequence x₁:T, an autoregressive model defines:

\[
p_\theta(x_{1:T}) = \prod_{t=1}^{T} p_\theta(x_t \mid x_{<t}).
\]

Maximum likelihood chooses parameters that maximize the log probabilities assigned to observed sequences. Equivalently, it minimizes negative log-likelihood (NLL). The usual next-token cross-entropy loss is an empirical average of negative log probabilities assigned to the observed next tokens.

These quantities must not be conflated:

- **Entropy:** H(P) = −Eₚ[log P(x)] measures uncertainty under a distribution.
- **Cross-entropy:** H(P,Q) = −Eₚ[log Q(x)] evaluates the expected negative log score when data follow P and predictions use Q.
- **KL divergence:** Dₖₗ(P‖Q) = Eₚ[log(P/Q)]. Under standard assumptions, H(P,Q) = H(P) + Dₖₗ(P‖Q). Because H(P) is fixed with respect to model parameters, minimizing cross-entropy over Qθ is equivalent to minimizing this KL divergence when the distributions and objective are consistently defined.
- **MLE and cross-entropy minimization** are equivalent only when data weighting, masking, and reduction conventions align. Token averaging, sequence averaging, padding masks, label smoothing, auxiliary losses, and regularization can change the exact objective.
- **Perplexity** is the exponential of average token-level NLL under a specified tokenization and evaluation convention. It is not a tokenizer-independent universal measure of quality.
- **Low training NLL does not establish understanding, factuality, calibration, or downstream usefulness.** These require separate evidence and suitable evaluations.

Every derivation must define its random variables, distributions, support, conditioning context, log base where relevant, and averaging convention. Include a hand-computable numerical example and a counterexample that distinguishes commonly confused quantities.

### 8.3 A reusable scientific chapter template

Each substantial chapter should adapt the following structure:

1. Question and motivation; prerequisites and learning outcomes.
2. Intuition and, where useful, competing viewpoints (statistical, information-theoretic, geometric, computational).
3. Formal setup: notation, assumptions, dimensions, and the object being modeled.
4. Derivation with each step justified and assumptions made explicit.
5. Worked numerical example before large-model complexity.
6. Original visual schema with alt text and an explanation of what the diagram omits.
7. Code and tests linked only after prerequisites are validated; tests should check mathematical invariants, not just successful execution.
8. Misconceptions, counterexamples, failure cases, alternatives, and trade-offs.
9. References, self-checks, and transfer questions that require applying the idea in a new context.
10. French/English parity in claims, notation, caveats, examples, and links.

### 8.4 Source synthesis and provenance

Multiple sources repeating a claim do not automatically validate it. For each important claim, track source type, version/date, claims supported, assumptions, caveats, and license constraints.

- **Primary research:** original papers, proceedings, technical reports, official model cards; use for methods and reported results.
- **Textbooks and lecture notes:** definitions, derivations, and broader context; check edition and assumptions.
- **Official implementations and documentation:** API behavior and implementation details, not universal scientific claims.
- **Pedagogical visualizations, videos, and blogs:** alternative explanations and intuition; verify equations against stronger sources.
- **Independent replications and critiques:** limitations, sensitivity, disagreements, and external validity.
- **Community commentary:** useful for discovering questions, not sole support for consequential claims.

Distinguish consensus, empirical result, interpretation, hypothesis, and open question. Write original explanations, diagrams, and exercises; cite sources without reproducing their prose or visuals. Treat third-party mirrors of books as discovery leads, not publication sources, and check reuse rights before embedding material.

### 8.5 Proposed book-level structure

| Part | Guiding question | Core concepts |
|---|---|---|
| 0. Orientation and evidence | What is an LLM, and what can we conclude about it? | terminology, model/system distinction, training vs inference |
| 1. Uncertainty and information | How do we quantify uncertainty and predictive mismatch? | probability, entropy, cross-entropy, KL, mutual information |
| 2. Statistical learning | What does it mean to fit a model to observations? | likelihood, MLE, empirical risk, generalization |
| 3. Text as a prediction problem | What is predicted from what? | tokenization, context windows, target shift, autoregressive factorization |
| 4. Neural conditional distributions | How do parameters turn context into probabilities? | tensors, embeddings, linear maps, logits, softmax |
| 5. Optimization and learning dynamics | How does the model improve? | derivatives, gradients, backpropagation, optimizers, numerical stability |
| 6. Attention and context mixing | How can positions use information from other positions? | Q/K/V, scaled dot-product, masks, heads, invariants |
| 7. Transformer design | Why this block structure? | positional methods, residuals, normalization, MLP, architecture variants |
| 8. Pretraining | How is a model trained reproducibly? | corpora, batching, schedules, checkpoints, validation, compute/data scaling |
| 9. Generation | How does a distribution become a sequence? | decoding, temperature, top-k/top-p, stopping, KV cache |
| 10. Adaptation | How can an existing model be adapted, and at what cost? | classification fine-tuning, SFT, LoRA/QLoRA, preferences, DPO |
| 11. Evaluation and failure | What can benchmarks and tests establish? | metrics, baselines, contamination, calibration, hallucination, robustness |
| 12. LLM systems | What changes when retrieval, tools, and orchestration are added? | RAG, retrieval evaluation, tool use, system boundaries |
| 13. Research frontiers and responsibility | What remains uncertain, and what are the trade-offs? | interpretability, scaling, efficiency, data governance, impact |

Appendices can cover linear algebra, probability, calculus and optimization, PyTorch/autograd, tokenizer internals, parameter/memory/FLOP accounting, paper-reading methods, glossary, and exercises.

### 8.6 Initial cross-source research anchors

These are starting points, not an exhaustive bibliography or automatic authority for every claim:

- Shannon, *A Mathematical Theory of Communication* (1948), and Cover & Thomas, *Elements of Information Theory*, for information-theoretic foundations.
- Bishop, *Pattern Recognition and Machine Learning*, and Murphy, *Probabilistic Machine Learning*, for probabilistic modeling and estimation.
- Goodfellow, Bengio & Courville, *Deep Learning*, especially probability, information theory, optimization and sequence modeling: https://www.deeplearningbook.org/
- Vaswani et al. (2017), [Attention Is All You Need](https://arxiv.org/abs/1706.03762), for the original Transformer; distinguish encoder–decoder from decoder-only GPT.
- Radford et al. (2019), [Language Models are Unsupervised Multitask Learners](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf), for GPT-2-era language modeling.
- Kaplan et al. (2020), [Scaling Laws for Neural Language Models](https://arxiv.org/abs/2001.08361), and Hoffmann et al. (2022), [Training Compute-Optimal Large Language Models](https://arxiv.org/abs/2203.15556), to compare scaling claims and their differing compute-budget conclusions.
- Raschka, [LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch), for a practical implementation path and coverage audit, not the book's organizing authority.
- Alammar, [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/) and [The Illustrated GPT-2](https://jalammar.github.io/illustrated-gpt2/), as visual perspectives to complement primary sources.
- Official PyTorch documentation, paired with mathematical derivations, for exact implementation semantics.

For the supplied video, playlist, Medium post, AlgoMonster course, and PDF mirror, assess expertise, provenance, date, technical depth, and licensing before using them as substantive evidence.

### 8.7 Immediate execution order

1. Treat the Raschka chapter map as a secondary coverage audit, not the table of contents.
2. Inventory existing French/English pages and map them to the proposed parts, concepts, and prerequisites; identify duplicates and missing language counterparts.
3. Start by auditing the existing entropy, cross-entropy, likelihood, loss, and probability pages. Build the first complete chapter around uncertainty and information, followed by statistical estimation.
4. Write one complete bilingual chapter at a time. Verify equations, assumptions, numerical examples, references, and internal links before moving to the next.
5. Only after review and private knowledge validation, connect the chapter to code and tests. Public pages must not depend on the private career-knowledge repository.
6. Run Quarto rendering, link checks where available, French/English parity review, and scientific review before marking a chapter complete.



### 8.8 Non-binding source-coverage crosswalk

The following crosswalk is an **audit aid only**. It helps check whether major topics from Raschka's book and appendices have been considered. It does not define LLM Lab's table of contents, require one-to-one chapter mapping, or determine the order in which the reader must study topics. The book's own sequence should be chosen from the explanatory needs of LLM Lab; stages may cut across source chapters, and one source chapter may inform several parts.

| External source unit (coverage check only) | Questions and topics worth accounting for | Related LLM Lab themes (not a chapter mapping) | Current gap / caution |
|---|---|---|---|
| Understanding LLMs | Language modeling, next-token prediction, pretraining vs fine-tuning, decoder-only GPT | Orientation, autoregressive objective, architecture | Overview/history are partial; link concepts rather than duplicate definitions. |
| Working with text data | Unicode, normalization, tokenization, BPE, special tokens, token IDs, embeddings, position, windows and target alignment | Data, representations, training objective | High-value theory gap: explain algorithmic principles separately from tokenizer-specific behaviour. |
| Coding attention mechanisms | Q/K/V, scaling, softmax axis, causal masks, weighted sums, multi-head shapes and invariants | Attention and tensor computation | Pages exist in part; connect them and test invariants before claiming a complete implementation. |
| Implementing a GPT model | Embeddings, positions, attention, MLP, residual paths, normalization, output head, parameterization | Architecture and forward pass | Overview exists; full architecture coverage remains partial. |
| Pretraining on unlabeled data | Autoregressive objective, token loss, batching, optimization, validation, perplexity, checkpoints, generation | Training, inference, evaluation | General math ownership must be clarified with the private wiki; reproducible training evidence is not yet complete. |
| Fine-tuning for classification | Task head, label space, loss, freezing, class balance, held-out evaluation, overfitting and forgetting | Adaptation and evaluation | Public bilingual theory and validated implementation remain incomplete. |
| Instruction fine-tuning | Prompt/response formats, target masking, SFT objective, data quality, evaluation and regressions | SFT, data pipeline, evaluation | Coverage is partial; instruction tuning does not by itself guarantee reliable behaviour. |
| PyTorch and appendices | Tensors, autograd, modules, data loading, devices, references and exercises | Prerequisites, source provenance, exercise space | Add framework explanations only when a lesson needs them; exercise navigation is not evidence that exercises exist. |
| Training improvements and LoRA | Schedules, clipping, checkpointing, low-rank adaptation and limitations | Training, efficiency, adaptation | Advanced extensions, not prerequisites for understanding a small baseline. |
| Beyond the book | Baselines, uncertainty, leakage/contamination, ablations, resource measurements, DPO and architecture variants | Evaluation, efficiency, research frontiers | Explicit LLM Lab extensions; do not attribute them to the source book. |

For each planned lesson, the theory-first review criteria below apply to the lesson itself, regardless of how many external source chapters informed it. A source crosswalk entry is not evidence that the corresponding LLM Lab lesson exists or is complete.

### Theory-first definition of done for each lesson

Before a lesson's implementation work begins, its French and English theory pages should:

1. State scope, prerequisites, learning objectives, and relevant source sections (paraphrased; do not reproduce copyrighted text).
2. Define the objects and notation, including tensor shapes and conventions wherever applicable.
3. Derive the central LLM-specific equations step by step and state assumptions, edge cases, and numerical limitations. Cite accessible public sources; keep private Wiki links and concept IDs out of reader-facing content.
4. Include at least one worked LLM-specific example and one misconception/counterexample that distinguishes nearby concepts.
5. Link to canonical concept pages rather than duplicate them; link to implementation/tests only when they exist, otherwise state that they are planned.
6. Cite primary papers or official technical references for substantive claims and pedagogical sources for intuition where useful.
7. Include self-check questions without immediately visible answers; keep solutions in the separate exercise space.
8. Preserve claim-level parity between French and English, or explicitly track a missing language counterpart.
9. Pass the configured Quarto render and link checks; visual inspection and scientific review remain separate checks.

**Working order:** audit sources and concepts → choose the next lesson based on reader questions and explanatory value → write/review its theory in both languages → render and inspect → implement or extend code/tests only when the specific minimum knowledge needed for that step has been validated in the private inventory. Teach low-level operations in context; optional general mathematics is not a prerequisite to the first small GPT. Do not draft all lessons in one bulk change.

## 9. Editorial boundary with wiki-knowledge: general foundations and complete public application

This section refines and takes precedence over any earlier wording in this plan that could imply LLM Lab must reproduce a general mathematics course or follow a fixed mapping between external-book chapters and this project's chapters.

### 9.1 Separate responsibilities

**`wiki-knowledge` owns the reusable foundations.** It should contain the general mathematical concepts and their rigorous treatment: definitions, hypotheses, derivations, proofs where appropriate, and general examples that apply beyond LLMs. Examples include entropy as a general information-theoretic quantity, maximum likelihood as a general estimation principle, gradients and optimization, linear algebra, and probability.

**`llm-lab` owns the LLM-specific application and synthesis.** It should explain why and how those foundations matter for language models and Transformers: how next-token prediction induces a likelihood objective; how cross-entropy is used in training; how logits and softmax define a categorical distribution; how causal attention changes information flow; how tensor shapes and masking implement the mathematics; and what the resulting training objective does and does not guarantee.

LLM Lab is a standalone public book, not a thin client of the Wiki. Each chapter must teach every prerequisite needed to understand its LLM application, including the relevant definitions, notation, assumptions, derivations, worked examples, caveats, and checks. A deeper general treatment may also live in the Wiki, so deliberate overlap is expected. The public page must cite accessible sources and must not require a private Wiki link. If a general foundation is missing or disputed, preserve the local explanation needed by the book and separately record the Wiki gap; do not leave the public reader blocked.

| Question | Canonical home | Role in the other project |
|---|---|---|
| What is entropy, in general, and which identities hold? | `wiki-knowledge` for the transversal treatment | Teach the entropy definitions and identities needed for next-token distributions locally, with LLM examples and interpretation limits |
| What is maximum likelihood estimation, and under which assumptions? | `wiki-knowledge` for the general estimation treatment | Derive locally why autoregressive training uses sequence/token log-likelihood and when the equivalence with cross-entropy holds |
| What is a gradient or the chain rule? | `wiki-knowledge` for general mathematics | Explain and derive locally how gradients flow through embeddings, attention, logits, and the training loss |
| What is a vector space or linear map? | `wiki-knowledge` for the transversal treatment | Teach the linear algebra needed to understand embedding tables, projections, Q/K/V, MLP layers, and tensor dimensions |
| What is generalization or statistical leakage? | `wiki-knowledge` for the transversal treatment | Teach the relevant concepts locally and apply them to corpus deduplication, pretraining/evaluation contamination, benchmark design, and model comparison |
| How does a Transformer block work in code? | `llm-lab` | Link back to the mathematical concepts and to the corresponding implementation/tests |

This boundary is conceptual, not a requirement that every cross-link be one-to-one. A chapter can draw on many wiki concepts; a wiki concept can support many LLM Lab chapters.

### 9.2 The book is organized by explanation, not by external source or wiki page

There is **no mandatory mapping** between a chapter of Raschka's book, a part of this book, a module in the existing learning path, or a page in `wiki-knowledge`. These are different organizational systems with different purposes:

- The book's structure should optimize the reader's understanding of LLMs.
- The wiki's structure should optimize the reusable knowledge graph of concepts and prerequisites.
- The implementation path should optimize the ability to build, inspect, test, and train a small LLM from scratch.
- External books, articles, courses, videos, and repositories are source material and coverage checks—not templates that dictate our table of contents.

Maintain traceability through links and a concept/source ledger, not chapter-number equivalence. A source may inform several chapters, and a chapter may synthesize several sources and viewpoints. If an existing chapter order or module is useful, keep it only when it serves the reader's learning path.

### 9.3 Two integrated outcomes: understanding and building from scratch

LLM Lab must ultimately enable a reader to implement a small decoder-only language model from scratch. "From scratch" should be defined explicitly: the reader writes and understands the main model components and training/generation loop, while using a tensor/autodiff library such as PyTorch for low-level tensor operations and automatic differentiation. Reimplementing all of PyTorch or GPU kernels is a separate advanced track, not a hidden prerequisite.

The implementation should grow as a set of demonstrable milestones rather than a chapter-number checklist:

1. Inspect and prepare a small text corpus; document splits, tokenization, and reproducibility.
2. Implement and test token-to-input/target alignment and a simple baseline.
3. Build a minimal language model and establish the forward pass, tensor shapes, logits, probability distribution, and loss.
4. Train a tiny baseline and validate that loss/overfitting behaviour is consistent with expectations.
5. Implement a decoder-only Transformer block incrementally: embeddings and positions, causal self-attention, multi-head attention, residual paths, normalization, MLP, and output head.
6. Train the complete small model with checkpoints, validation, and reproducible configuration.
7. Generate text with several decoding strategies; distinguish training objective from generation policy.
8. Run controlled tests and ablations that verify causal masking, dimensions, loss calculations, gradient flow, overfitting on a tiny dataset, checkpoint round-trips, and deterministic paths where expected.
9. Compare variants using explicit baselines, resource measurements, and appropriately scoped conclusions.

These milestones can be split across chapters or revisited in several places. Each implementation must be preceded by the concepts needed to understand it, but the book does not need to mirror the implementation sequence exactly. Keep mathematical explanations, code, and tests linked at the concept level.

### 9.4 Applied-foundations chapter pattern

For every mathematical foundation used in LLM Lab:

1. If cross-repository traceability is useful, record the Wiki concept ID in the private `career-knowledge` repository; do not add private URLs or IDs to public lesson content or make them a reader/build dependency.
2. Teach all mathematical prerequisites needed locally, including definitions, assumptions, notation, and derivations necessary to follow the application.
3. Translate the result into the LLM setting: define tokens, context, parameters, tensors, objectives, and computational steps.
4. Work through a small LLM-specific example, including dimensions and/or numeric values.
5. Explain what the concept predicts about behaviour and what it does not imply; include counterexamples to likely misconceptions.
6. Connect to an implementation and a test, when available, and cite accessible public sources.
7. Record any unresolved general-mathematics issue as a Wiki improvement item while preserving the explanation needed by the public book.

Example: the wiki page on maximum likelihood should establish the general estimation principle. LLM Lab should then derive the likelihood of a token sequence under an autoregressive model, show how teacher-forced next-token targets produce the summed negative log-likelihood, explain token averaging and padding masks, and test the implementation against a hand-calculated tiny example.

### 9.5 Immediate work order

The first-pass inventory is recorded in [`docs/editorial-boundary-audit.md`](editorial-boundary-audit.md). It identifies the broad entropy pages as the clearest duplication risk, the cross-entropy and gradients pages as mixed-content pages, and the likelihood/loss pages as already strongly aligned with LLM-specific application.

1. Keep the public information architecture self-contained, labelled as **maths applied to LLMs**, not as the canonical home of general foundations.
2. General concepts were added in [wiki-knowledge PR #23](https://github.com/JM-Brun/wiki-knowledge/pull/23), but their pages remain draft and need scientific/registry follow-up. This is not a prerequisite for the public book, and their existence does not authorize deleting or shortening its explanations.
3. The application pages have been refocused in this branch: entropy → next-token distribution; cross-entropy → token objective, target shift, masks, reduction, perplexity; probabilities → logits, temperature and calibration; tensors → Transformer shapes and axes. Stable URLs are preserved.
4. Each public page retains the full set of definitions, assumptions, derivations, examples, limits, and public references needed to understand its LLM application independently. The Wiki may carry a broader cross-domain treatment in parallel.
5. The tensor, embedding-space, and positional-encoding/RoPE lessons now have French and English versions. This closes the missing-counterpart inventory item, but not the separate semantic-parity, external-reference, rendered-math, or browser visual reviews.
6. Render Quarto, check internal links and image alternatives, and inspect both language paths. Do not add model implementations or experiments until the specific conceptual prerequisites for the next step are validated; do not treat advanced mathematics as a blanket gate.
7. For every retained chapter, ask whether it explains an LLM-specific mechanism and whether it contributes directly or indirectly to implementing, testing, training, generating with, or evaluating a small decoder-only LLM. Neither general-mathematics duplication nor an unmotivated code dump is sufficient.


## 10. Safe coordination with the private wiki

The detailed process is maintained in [Safe, staged coordination plan](safe-wiki-llm-lab-coordination-plan.md). This plan takes precedence over any simplistic “canonical concept lives in the wiki, therefore remove it from LLM Lab” interpretation.

**Public autonomy rule:** `llm-lab` must remain understandable and usable without access to `wiki-knowledge`. A concept may appear in both repositories: the wiki can contain the deeper cross-domain treatment while LLM Lab keeps the definitions, assumptions, equations, examples, caveats, and public references needed to understand its LLM-specific application.

No removal or condensation is accepted without a preservation ledger recording the original item, destination/disposition, and verification. Uncertain content stays public until reviewed. Private links are supplementary only and must never be build dependencies.

The current math-page PR is to be reviewed in bounded steps: inventory original public content; compare it with the proposed public edits and merged wiki concepts; validate scientific correctness; inspect French/English parity and the rendered public site; then decide merge readiness. Green CI is necessary but is not scientific review. Do not start another broad rewrite until the current slice is closed.


## 9. Expanded source-to-site traceability matrix (review snapshot: 2026-10-29)

This section makes the coverage target auditable at finer granularity than the chapter-level map in §3. The source repository is a **living catalogue**: its bonus folders now contain material beyond the original 2024 book. Re-check the upstream README and chapter READMEs whenever this matrix is reviewed. The book's copyrighted explanatory prose, exercises, diagrams, and code are references to learn from—not material to reproduce.

### 9.1 Coverage vocabulary

- **Existing — audit required:** a likely destination exists, but completeness, scientific correctness, bilingual parity, rendering, and learner understanding have not all been verified.
- **Partial:** some relevant explanation exists, but one or more required learning outcomes or implementation/evidence layers are missing.
- **Gap:** no dedicated, sufficiently complete public bilingual treatment has been established.
- **Optional extension:** outside the book's core chapters; include in the target catalogue, but do not block core completion.
- **Not audited:** the source-to-destination relationship or the destination itself has not yet been checked in detail.

A topic is not "covered" merely because it appears in a link, title, diagram, or plan. Apply the definition of coverage in §6. The table below is a **mapping and audit backlog**, not a certification that every row is complete.

### 9.2 Book chapters and appendices — required baseline

| Source section and learning outcomes | LLM Lab canonical destination | Current assessment / required verification |
|---|---|---|
| **Ch. 1 — What an LLM is; applications; build/use stages; Transformer; large datasets; GPT architecture; end-to-end workflow** | `site/{fr,en}/transformer.qmd`, glossary, history; add/extend a concise LLM lifecycle/model-family overview if absent | **Partial.** Audit the distinctions among pretraining, adaptation, inference, applications, and architecture families. The Transformer overview is not a substitute for a complete lifecycle explanation. |
| **Ch. 2 — Embeddings; tokenization; token IDs; special tokens; BPE; sliding-window sampling; token embeddings; positional information** | `site/{fr,en}/text-data.qmd` (planned/verify existence); `tensors.qmd`, `embedding-space.qmd`, `positional-encoding.qmd`; dedicated tokenizer/BPE concept if the text-data page cannot own it clearly | **Gap/partial.** Establish a complete data-to-batch path, including encode/decode, vocabulary, special-token semantics, context windows, shifted input/target pairs, and tokenizer limitations. Verify whether each named page exists in both languages before treating it as a destination. |
| **Ch. 3 — Long-sequence problem; attention intuition; self-attention without learned weights; all-token scores; learned Q/K/V projections; causal attention; masks; attention dropout; multi-head attention** | `queries-keys-values.qmd`, `scaled-dot-product-attention.qmd`, `causal-masking.qmd`, `transformer.qmd`; tensor concepts | **Partial.** Conceptual pages exist. Audit equations, dimensions, softmax axis, masking convention, dropout placement, single-head vs multi-head equivalence, and runnable implementation/tests. |
| **Ch. 4 — LayerNorm; GELU feed-forward network; residual/shortcut paths; Transformer block; GPT assembly; text generation** | `transformer.qmd`; positional and tensor concepts; dedicated block/model/generation pages only if the overview cannot teach these sufficiently | **Partial/gap.** Overview exists; a complete forward pass and tested small GPT are not established. Cover pre-norm/post-norm distinctions only with clear scope; avoid implying every model uses the same block. |
| **Ch. 5 — Generation evaluation; token loss; train/validation loss; training loop; temperature; top-k; sampling; save/load weights; pretrained GPT weights** | `logits.qmd`, `probabilities.qmd`, `likelihood.qmd`, `cross-entropy.qmd`, `gradients.qmd`; generation/decoding and training/evaluation destinations | **Partial.** Mathematical building blocks exist; the full reproducible training-to-generation workflow does not. Include shifted targets, ignore/padding masks, reduction semantics, validation protocol, checkpointing, seeds, decoding controls, and limitations of loss/perplexity. |
| **Ch. 6 — Fine-tuning categories; dataset preparation; loaders; pretrained initialization; classification head; classification loss/accuracy; supervised updates; spam classification** | Fine-tuning/classification module; connect to training/evaluation and data-quality concepts | **Gap.** Require a public bilingual end-to-end explanation and, only after prerequisite validation, a small reproducible baseline with held-out evaluation and error analysis. |
| **Ch. 7 — Instruction tuning; supervised instruction dataset; batching/loaders; pretrained initialization; fine-tuning; response extraction; evaluation** | Instruction fine-tuning / SFT module; connect to data curation, loss masking, generation and evaluation | **Gap/partial.** A complete public bilingual path is not established. Distinguish SFT from classification and preference optimization; discuss prompt/response formatting, which tokens contribute to loss, evaluation contamination, and qualitative plus quantitative error analysis. |
| **Appendix A — PyTorch basics: tensors, autograd, modules, datasets/loaders, devices, multi-GPU/distributed training** | Existing tensor and gradient pages; a concise "PyTorch needed for this lab" guide with official references | **Partial/gap.** Teach only the PyTorch concepts used in LLM Lab, but enough that readers can understand tensor operations, parameter registration, autograd, batching, device placement, and state dictionaries. Distributed training is optional context, not a prerequisite for the CPU-sized core path. |
| **Appendix B — References and further reading** | `site/references.qmd` and per-page citations | **Partial.** Audit source relevance, primary-source support, version/date, accessibility, and attribution; a link list alone is not sufficient. |
| **Appendix C — Exercises and solutions** | `site/{fr,en}/exercises.qmd` and stable bilingual exercise IDs linked from concepts | **Scaffold only.** The exercise area exists as navigation/planning; confirm authored exercises, hidden answer keys, parity, and validation individually. Create original exercises rather than reproducing the book's exercises or solutions. |
| **Appendix D — Training-loop improvements ("bells and whistles")** | Training-loop / experiment protocol / reproducibility module | **Gap; optional after baseline.** Map every upstream technique encountered during review (e.g. scheduling, gradient clipping, logging, checkpointing) to a named concept or explicitly mark it out of scope. Explain why each is used and what evidence supports its effect. |
| **Appendix E — LoRA and parameter-efficient fine-tuning** | Fine-tuning and efficiency cluster; add a dedicated LoRA page if needed | **Gap/partial.** Explain low-rank updates, target modules, rank/alpha/dropout conventions, trainable parameter counts, memory/quality trade-offs, merging/inference implications, and evaluation. Distinguish LoRA from quantization and QLoRA. |

### 9.3 Upstream repository bonus material — explicit catalogue

These topics are not all requirements for the first working GPT. They are nevertheless part of the requested **eventual coverage envelope**. Each must either map to a public explanation/experiment or be explicitly classified as out of scope with a reason. "Optional" means readers can skip it, not that it should silently disappear from the inventory.

| Upstream bonus family | LLM Lab mapping / intended home | Status / acceptance target |
|---|---|---|
| Setup: Python/package installation, environment troubleshooting, Docker | `README.md` / contributor setup docs; link to upstream setup docs | **Not audited.** Give a reproducible supported local setup and CPU path; avoid maintaining a duplicate general Python tutorial. |
| BPE tokenizer from scratch; compare BPE implementations; SimpleTokenizer variants; extend tiktoken vocabulary | Text-data/tokenization cluster; tokenizer comparison experiment | **Gap/partial.** Cover merges/vocabulary/byte-level details at the right depth, special-token handling, encode/decode invariants, compatibility, and why implementations differ. Extensions to a pretrained tokenizer must explain embedding/output-weight consequences. |
| Embedding layer vs linear layer; dataloader intuition with small numbers | Embedding/tensor pages and text-data module | **Partial/gap.** Distinguish lookup from affine projection mathematically and operationally; provide a hand-checkable batch/window example. |
| Efficient multi-head attention implementations; PyTorch buffers | Attention implementation and performance notes | **Optional extension; not audited.** Compare equivalent semantics before speed. Explain buffers/state-dict behavior and validate numerical parity; report hardware/software context for performance claims. |
| FLOPs analysis | Model/efficiency module | **Optional extension.** State counted operations, sequence/batch/model dimensions, and whether estimates include backward pass, optimizer, and memory traffic. Do not treat FLOPs alone as latency. |
| KV cache | Autoregressive generation/inference | **Optional extension.** Explain cached keys/values, prefill vs decode, causal equivalence, memory growth, and measured latency/memory trade-offs. |
| Attention alternatives: GQA, MLA, sliding-window attention, Gated DeltaNet, DeepSeek Sparse Attention, cross-layer KV sharing | Architecture comparison hub with one concise entry per mechanism; deeper pages only where useful | **Optional extension; catalogue required.** For each, state the bottleneck addressed, core operation, constraints, model/source/version using it, and trade-offs. Do not imply these are interchangeable or universally superior. Verify current primary sources before describing rapidly evolving methods. |
| Mixture-of-Experts (MoE) | Architecture comparison hub; routing/load-balancing deep dive if justified | **Optional extension.** Explain expert routing, sparse activation, capacity/load balancing, training/inference costs, and distinction between total and active parameters. |
| Alternative pretrained-weight loading; memory-efficient weight loading | Checkpoints/model-loading and inference-efficiency notes | **Optional extension.** Explain format/conversion assumptions, device/memory constraints, and equivalence checks; distinguish educational code from production loading libraries. |
| Train GPT on Project Gutenberg; hyperparameter optimization; CPU/MPS discrepancies; PyTorch performance tips | Reproducible experiment reports and troubleshooting notes | **Optional extension.** Version data provenance/licensing, configs/seeds, train/validation curves, compute budgets, hardware, numerical tolerance and negative results. No result without an executable config and evidence. |
| Build a UI for pretrained GPT, spam classifier, or instruction-tuned GPT | Optional application/demo layer | **Out of core scope unless it teaches a distinct concept.** The core site must not depend on a live app. Prefer a static or reproducible fallback; avoid duplicating model logic in JavaScript. |
| Convert GPT to Llama; load weights from Llama; chapter 5 with other models as drop-in replacements | Architecture/weight-loading comparison | **Optional extension.** Document architectural and tokenizer differences, conversion assumptions, checkpoint provenance/licence, and numerical checks; never imply GPT weights can be substituted without compatibility work. |
| LLM architecture walkthroughs: Llama 3.2, Qwen3 dense/MoE, Gemma 3, OLMo 3, Tiny Aya, Qwen3.5, Gemma 4 E2B/E4B (and any newer entries in upstream README) | Versioned architecture-comparison index; selected focused deep dives | **Optional extension; living inventory.** Pin model/version/date, official configuration and implementation sources. Update the catalogue as upstream changes. Do not implement every architecture merely to claim breadth. |
| Classification experiments: unfreeze different layers, larger models, 50k IMDb, alternative pretrained models | Fine-tuning/evaluation experiment reports | **Optional extension.** Use controlled comparisons, identical splits/metrics where appropriate, uncertainty, compute/resource accounting, and error analysis. |
| Dataset utilities for near-duplicate detection and passive-voice entries; generate/improve instruction datasets | Data quality and instruction-data curation | **Optional extension.** Explain deduplication method and thresholds, leakage risks, provenance/licensing, synthetic-data quality and filtering limitations. Avoid treating generated examples as ground truth. |
| Evaluate instruction responses using APIs or Ollama | Evaluation methods / experiment protocol | **Optional extension.** Separate reference-based, rubric-based, and model-judge evaluation; disclose judge/model/version, prompt, cost, bias and agreement checks. |
| Preference datasets and Direct Preference Optimization (DPO) | Preference optimization and alignment | **Optional extension beyond core book path.** Explain preference pairs, objective assumptions, relation to SFT and reward-based methods, dataset quality, and evaluation. |
| Related *Reasoning From Scratch* materials: Qwen3 basics/source walkthrough/optimized implementation; verifier-based MATH-500; MMLU; leaderboard evaluation; LLM-as-a-judge; self-consistency; self-refinement; RLVR/GRPO | Advanced reasoning/evaluation cluster, explicitly beyond the book baseline | **Beyond baseline; optional.** Track separately from Raschka-book parity. Define task-specific metrics, contamination risks, sampling/compute budgets, baselines and limitations; do not fold these into "covered" merely because a general evaluation page exists. |

### 9.4 What "the site subsumes the source" should mean

LLM Lab should **subsume the learning objectives and useful technical scope**, not reproduce the source repository file-for-file. The intended relationship is:

1. **Core parity:** every book chapter and appendix objective has a canonical bilingual destination or a deliberate, documented scope decision.
2. **Implementation parity where pedagogically necessary:** core mechanisms have small, inspectable implementations and tests when prerequisites are validated; a conceptual page must not falsely imply tested code exists.
3. **Bonus traceability:** every bonus family above has a destination, an explicit deferral, or an out-of-scope rationale. New upstream bonus entries trigger a review, not automatic implementation.
4. **Greater depth:** LLM Lab adds the mathematical bridge (probability, likelihood, information theory, gradients), careful tensor/axis conventions, misconceptions and counterexamples, source comparison, reproducibility, numerical/property tests, experimental evidence, limitations, and bilingual navigation.
5. **Independent pedagogy:** use a learning graph with a guided route and optional deep dives, rather than mirroring chapter order. Readers must be able to orient first and selectively investigate.
6. **Independent expression and provenance:** write original explanations, diagrams, and exercises; cite/link the book/repository and other sources. Do not copy protected text or exercises. Verify code/asset licences before reuse.
7. **Evidence-based completion:** each row moves to covered only after source-to-page review, scientific review, French/English semantic parity, rendered-site checks, code/test verification where relevant, and learner transfer evidence. Record the evidence and date.

### 9.5 Next audit sequence (small, verifiable slices)

1. **Freeze a source snapshot:** record the upstream commit SHA/date and capture the current README's core chapter/appendix and bonus lists. Revisit the snapshot when the upstream README changes.
2. **Inventory the actual public tree:** enumerate all `site/fr`, `site/en`, `src/llm_lab`, `tests`, `experiments`, and `reports` paths. Do not infer a destination from a planned link or a similarly named private concept.
3. **Audit core Ch. 1–2:** compare each learning objective to the actual rendered French/English pages; list missing concepts and links. Resolve text data/tokenization as a coherent vertical slice.
4. **Audit core Ch. 3–5:** attention → block → generation → training, checking equations, tensor shapes, tests, and end-to-end invariants.
5. **Audit core Ch. 6–7 and Appendices A–E:** classification, SFT, PyTorch prerequisites, exercises, training-loop practices, LoRA.
6. **Audit bonus families:** start with data/tokenizer, efficient inference (KV cache), attention/architecture variants, then training/evaluation/fine-tuning extras. Keep each review narrow.
7. **Validate the result:** bilingual parity, Quarto render and local links, rendered visual review, external references, tests and reproducibility; keep mastery evidence separate in the private knowledge inventory.

**Current conclusion (2026-10-29):** the repository already has a chapter-level plan and a strong editorial contract, but this is not yet evidence of complete coverage. The current evidence supports **partial core coverage**, with substantial unverified or missing areas around end-to-end text data/tokenization, a tested GPT and training workflow, classification fine-tuning, instruction tuning, PyTorch-specific prerequisites, exercises, and LoRA. The upstream bonus catalogue is broader and changes over time; it needs explicit tracking rather than an assumption that covering the seven chapters covers the repository.


## 10. Chapter-by-chapter coverage audit backlog (2026-10-29)

The following issues operationalize §9. They are **audit tasks**, not a commitment to implement every upstream bonus. Each audit must map concepts to current public pages or create narrowly scoped follow-up issues for verified gaps. Check existing work before creating follow-ups; do not duplicate owned deliverables. Chapter 2 explicitly coordinates with the existing token-data issues.

| Source unit | Audit task |
|---|---|
| Chapter 1 — Understanding LLMs | [#95 — audit LLM concepts and system overview](https://github.com/JM-Brun/llm-lab/issues/95) |
| Chapter 2 — Working with Text Data | [#96 — audit text, tokenization, and training examples](https://github.com/JM-Brun/llm-lab/issues/96); coordinate with [#58](https://github.com/JM-Brun/llm-lab/issues/58) and [#83](https://github.com/JM-Brun/llm-lab/issues/83) rather than duplicating them |
| Chapter 3 — Coding Attention Mechanisms | [#97](https://github.com/JM-Brun/llm-lab/issues/97) |
| Chapter 4 — Implementing a GPT Model | [#98](https://github.com/JM-Brun/llm-lab/issues/98) |
| Chapter 5 — Pretraining on Unlabeled Data | [#99](https://github.com/JM-Brun/llm-lab/issues/99) |
| Chapter 6 — Fine-Tuning for Text Classification | [#100](https://github.com/JM-Brun/llm-lab/issues/100) |
| Chapter 7 — Fine-Tuning to Follow Instructions | [#101](https://github.com/JM-Brun/llm-lab/issues/101) |
| Appendix A — PyTorch | [#102](https://github.com/JM-Brun/llm-lab/issues/102) |
| Appendix B — References and Further Reading | [#103](https://github.com/JM-Brun/llm-lab/issues/103); coordinate with [#86 source curation](https://github.com/JM-Brun/llm-lab/issues/86) |
| Appendix C — Exercise Solutions | [#104](https://github.com/JM-Brun/llm-lab/issues/104) |
| Appendix D — Training-Loop Improvements | [#105](https://github.com/JM-Brun/llm-lab/issues/105) |
| Appendix E — LoRA | [#106](https://github.com/JM-Brun/llm-lab/issues/106) |

### Execution order

1. Start with #95 and #96; these establish the core overview and text-data foundations.
2. During the Chapter 2 audit, reconcile #58/#83 and tokenizer-related issues; update/close duplicates rather than creating parallel implementation work.
3. Continue with #97–#99 (attention → architecture → pretraining), then #100–#101 and #102–#106.
4. For every audit, create gap issues only after inspecting actual pages, open/merged PRs, tests and existing issues. Link them back to the audit and update §9's coverage status with evidence.
5. Treat the upstream bonus list as a living catalogue: new bonus items require triage and an explicit disposition, not automatic issue proliferation or implementation.

**Completion rule:** the audit issue may close when the source-to-site mapping, gap links, bilingual checks, source review date, and curriculum-plan updates are recorded. It must not close merely because follow-up issues were created.


### Chapter 1 audit result (2026-10-29; see [audit #95](https://github.com/JM-Brun/llm-lab/issues/95))

**Assessment: partial.** This is based on inspection of the current source files and the publisher's chapter outline; rendered-browser and CI validation have not been run as part of this audit.

| Learning objective | Existing evidence | Assessment |
|---|---|---|
| GPT data flow from text/tokens through representations, Transformer blocks, logits/probabilities and next-token generation | [EN overview](../site/en/transformer.qmd), [FR overview](../site/fr/transformer.qmd) | Covered at overview level; links to canonical deep dives. |
| Training versus autoregressive generation | Same overview pages | Covered conceptually, including parallel processing of training positions versus stepwise generation. |
| Important misconceptions and limits (tokens are not necessarily words; probabilities do not guarantee truth; attention weights alone do not explain a prediction) | Same overview pages | Covered explicitly. |
| Basic vocabulary | [EN glossary](../site/en/glossary.qmd), [FR glossary](../site/fr/glossary.qmd) | Partial: concise definitions exist, but no coherent model-family and lifecycle orientation. |
| Historical context for original Transformer | [EN history](../site/en/transformer-history.qmd), [FR history](../site/fr/transformer-history.qmd) | Partial: historical milestones exist; a comparison of model families and their objectives is still needed. |
| Applications and earlier NLP contrast; AI/ML/deep-learning hierarchy; encoder-only vs encoder–decoder vs decoder-only; BERT vs GPT; pretraining → base model → adaptation → inference; classification fine-tuning vs instruction SFT; zero-/few-shot; scale/diversity; custom-model motivations; careful meaning of “understanding” and “emergent” capabilities | No single canonical orientation page identified in the inspected files | Gap. Follow-up: [#108 — add a bilingual LLM big-picture overview](https://github.com/JM-Brun/llm-lab/issues/108). |

**Source checked:** [Manning's Chapter 1 objectives](https://livebook.manning.com/learn/build-a-large-language-model-from-scratch/chapter-1) and [upstream Chapter 1 README](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch01/README.md). The upstream README lists no chapter code; the extras are reading advice and a video introducing the LLM development lifecycle.

**Disposition:** do not expand the existing GPT overview into an encyclopaedia. Keep it as the canonical architecture/data-flow overview and add a concise bilingual orientation page, linked from the guided path and existing overview, under #108. Reuse canonical token, attention, loss and generation pages rather than duplicating them. Re-audit the status after #108 is implemented and rendered.


### Chapter 2 audit result (2026-10-29; see [audit #96](https://github.com/JM-Brun/llm-lab/issues/96))

**Assessment: substantial conceptual coverage; implementation and rendered validation remain partial.** This is a source-level audit of the current bilingual pages and the publisher's Chapter 2 learning objectives. It is not a certification of every claim, a browser review, or evidence of learner mastery.

| Chapter 2 objective | Current public evidence | Assessment and owner |
|---|---|---|
| Text → tokens → token IDs; Unicode/UTF-8; vocabulary and encode/decode | [EN text-data](../site/en/text-data.qmd), [FR text-data](../site/fr/text-data.qmd) | Covered conceptually. Both pages explain token IDs as discrete labels, contrast tokenization with embeddings, include BPE intuition, examples and counterexamples. Review current references and rendered output separately. |
| Simple vocabulary/unknown tokens versus BPE and special tokens | Same text-data pair | Partial-to-covered conceptually: BPE, unknown strings, special tokens, document boundaries and tokenizer/model compatibility are addressed. Ensure claims remain tokenizer-specific; do not generalize one vocabulary or special-token policy to all models. |
| BPE vocabulary/merges, rare text and tokenizer compatibility | Same text-data pair; issue [#57](https://github.com/JM-Brun/llm-lab/issues/57) is closed | Strong source-level coverage: training versus encoding, byte-level caveats, tokenizers comparison, multilingual examples and source roles. Not independently verified against every current tokenizer implementation. |
| Token embeddings and learned vectors | [EN/FR embedding-space pages](../site/en/embedding-space.qmd) and [EN/FR tensors pages](../site/en/tensors.qmd) | Partial for Chapter 2's narrower goal. The conceptual distinction between ID, embedding and contextualized representation is present; the embedding page is primarily about representation geometry. A small embedding lookup/shape/gradient explanation is already tracked by [#82](https://github.com/JM-Brun/llm-lab/issues/82). |
| Positional information and GPT-style input embeddings | [EN/FR positional-encoding pages](../site/en/positional-encoding.qmd), Transformer overview pair | Covered at conceptual level, including absolute/relative approaches and RoPE. The original GPT-style sum of token and absolute positional embeddings, with a small shape-compatible example, should be explicitly cross-checked in #82; do not duplicate the RoPE deep dive here. |
| Shifted targets, windows/stride, batches, padding, loss masks, document boundaries and tensor shapes | [EN training-examples](../site/en/training-examples.qmd), [FR training-examples](../site/fr/training-examples.qmd) | Conceptually substantial and bilingual: worked one-token shift, window/stride comparison, packing/boundaries, padding/loss masks, shapes and debugging checklist. Implementation/tests and final rendering are not certified. Existing owner is [#58](https://github.com/JM-Brun/llm-lab/issues/58); [#83](https://github.com/JM-Brun/llm-lab/issues/83) substantially duplicates this scope and should be consolidated into #58. |
| Dataset/DataLoader and educational-versus-production pipeline | Training-examples pair and #58 | Partial. Conceptual roles and PyTorch reference are planned/curated in #58; the source pages should be checked for a minimal, precise distinction between sample construction, Dataset, batching/collation, and large-scale packing. Do not prescribe one universal pipeline. |
| Data quality, deduplication, contamination/leakage, reproducibility | Broader curriculum / data-quality topics; not a Chapter 2 objective fully developed by the inspected text-data pages | Deliberate extension rather than a missing core Chapter 2 section. Link to the canonical data-quality and evaluation material where it exists; do not inflate the text/tokenization lesson with a second full lesson. Check #86 source curation before adding references. |
| EN/FR parity, links, render and CI | EN/FR source pairs exist for text-data, training-examples, embedding-space, tensors and positional encoding | Source-level structural parity is visible, but this audit did not run Quarto, check rendered pages, or verify all external links/CI. These remain explicit acceptance checks in #58/#82 and the relevant PRs. |

**Sources checked (2026-10-29):** [Manning Chapter 2 learning objectives](https://livebook.manning.com/learn/build-a-large-language-model-from-scratch/chapter-2), [Manning Chapter 2 contents](https://livebook.manning.com/book/build-a-large-language-model-from-scratch/chapter-2), upstream [Raschka Chapter 2 code](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch02), and the current public source files listed above. The chapter's stated scope includes embeddings, tokenization, IDs, special context tokens, BPE, sliding-window sampling, input/target batches, and positional information.

**Disposition:** no new implementation or duplicate issue is justified by this audit. Route the data-to-training-example work through #58 (consolidate #83); token embeddings/position through #82; causal mask and target-leakage invariants through #81; source selection through #86. Keep #96 open until the documentation PR is reviewed and the remaining EN/FR rendered-site/CI checks have evidence.

### Chapter 3 audit result (2026-10-29; see [audit #97](https://github.com/JM-Brun/llm-lab/issues/97))

**Assessment: core attention mathematics and causal constraints are covered conceptually; implementation-level and multi-head coverage are partial.** This is a source-level audit. It does not certify every derivation, test, or rendered layout.

| Chapter 3 objective | Current public evidence | Assessment and follow-up |
|---|---|---|
| Attention scores, scaling, softmax and weighted aggregation | [EN/FR scaled dot-product attention](../site/en/scaled-dot-product-attention.qmd) | Covered conceptually with shapes, a worked numerical example and explicit additive-mask convention. The arithmetic in the worked example was previously checked; no reusable attention implementation/regression suite is yet established by this page. Existing owner: [#80](https://github.com/JM-Brun/llm-lab/issues/80). |
| Learned Q/K/V projections and their roles | [EN/FR Q/K/V](../site/en/queries-keys-values.qmd) | Covered conceptually; projections are correctly distinguished from token types and semantic labels. Shapes/gradient flow in a tested implementation remain under #80 and #78's roadmap. |
| Causal masking and future-token leakage | [EN/FR causal masking](../site/en/causal-masking.qmd) | Covered as a mathematical contract, including API-specific boolean polarity and additive masks. The pages explicitly state that they do not yet prove the full architecture is causal. Existing owner: [#81](https://github.com/JM-Brun/llm-lab/issues/81). |
| Tensor dimensions, batch/sequence/features and head dimensions | [EN/FR tensors](../site/en/tensors.qmd) | General shape literacy is covered; chapter-specific reshape/transposition contracts for multi-head attention need a concrete treatment or explicit link from the architecture audit. |
| Multi-head attention: split heads, compute attention per head, concatenate and project | Overview and Q/K/V pages mention the concept, but no dedicated bilingual multi-head lesson was found in the checked paths. | Partial. Do not duplicate the single-head attention derivation. Route the architecture-level shape/data-flow treatment through [#98](https://github.com/JM-Brun/llm-lab/issues/98); decide there whether a concise section is sufficient or a separate deep dive is justified. |
| Attention dropout and PyTorch buffers | No dedicated dropout page found in the checked paths; upstream chapter explains dropout on attention weights and a registered lower-triangular buffer. | Optional implementation detail for the first mental model, but required for faithful chapter-to-code coverage. Record it in #98 / source curation #86, with train/eval semantics and the distinction between dropout and causal masking. |
| Batch support and integration with Chapter 2 data loader | Q/K/V and tensor pages describe batch dimensions; training examples page defines shifted targets and data batches. | Conceptual bridge exists; tested end-to-end attention over batches remains open under #80/#81. |
| Efficient multi-head variants and performance claims | Upstream bonus directory contains implementation comparisons and benchmarks. | Optional deep dive, not a core requirement. Do not reproduce benchmark numbers without hardware/software/version context; route source assessment through #86. |
| EN/FR parity, references, render and CI | EN/FR pairs exist for the four core pages above. | Source-level parity is broadly visible, but full browser/mobile review and independent link audit were not performed in this pass. The merged Chapter 2 audit PR's Quarto render and local-link check passed; that is not a visual review of every page. |

**Upstream evidence checked (2026-10-29):** [Chapter 3 README](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch03), [main chapter notebook](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch03/01_main-chapter-code/ch03.ipynb), [efficient multi-head bonus](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch03/02_bonus_efficient-multihead-attention), and [PyTorch buffers bonus](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch03/03_understanding-buffers). The notebook covers simple attention, trainable projections, causal masking, dropout, batched causal attention and multi-head attention.

**Disposition:** no implementation was added and no duplicate single-head attention issue was created. Continue with #80 and #81 only after prerequisites are reviewed/acquired; make #98 explicitly own the architecture-level multi-head shape flow and the role of dropout/buffers. Keep efficiency benchmarking optional and source-backed.

### Chapter 4 audit result (2026-10-29; see [audit #98](https://github.com/JM-Brun/llm-lab/issues/98))

**Assessment: architecture overview covered conceptually; implementation contract and end-to-end validation are not established.** This source-level pass does not certify rendered pages, every equation, or learner mastery.

| Chapter 4 objective | Current public evidence | Assessment and follow-up |
|---|---|---|
| Decoder-only GPT data flow and component roles | [EN overview](../site/en/transformer.qmd), [FR overview](../site/fr/transformer.qmd) | Covered at overview level: token inputs, attention/MLP blocks, residual paths, logits and autoregressive generation. Keep this page an overview rather than turning it into an encyclopaedia. |
| Token embeddings plus learned absolute positional embeddings | [EN/FR embedding-space](../site/en/embedding-space.qmd), [EN/FR positional encoding](../site/en/positional-encoding.qmd), Transformer overview | Partial. The concepts exist, but the precise GPT-style input addition and its shape contract are not yet evidenced as a worked implementation. Route concept ownership through #82; avoid duplicating the RoPE deep dive. |
| Multi-head causal attention, head split/merge and output projection | [EN/FR Q/K/V](../site/en/queries-keys-values.qmd), [EN/FR scaled dot-product attention](../site/en/scaled-dot-product-attention.qmd), [EN/FR causal masking](../site/en/causal-masking.qmd) | Partial. Single-head concepts and causal constraints are explained; the full multi-head reshape/transposition/concatenation/output-projection contract is not a dedicated verified path. Architecture-level treatment stays in #98; single-head invariants in #80 and leakage/boundary tests in #81. |
| Transformer block ordering, residual/shortcut paths, LayerNorm and FFN/MLP | [EN/FR Transformer overview](../site/en/transformer.qmd) | Partial. Roles are introduced, but pre/post-normalization convention, exact sublayer order, FFN hidden width/activation and dimensional transitions are not fully specified together. Describe the baseline as GPT-2-style where appropriate; do not imply all model families share the same block. |
| Repeated blocks, final normalization and vocabulary output head | Transformer overview; logits/probability concept pages | Partial. The overall path is visible, but there is no complete end-to-end shape trace from input IDs through each block to batch × sequence × vocabulary logits in the inspected pages. |
| Configuration and parameter accounting | No compact public configuration/parameter-count derivation found in the inspected candidate pages | Gap in the checked scope. If added later, define dimensions and conventions explicitly, show how parameter counts depend on vocabulary, context length, width, block count and FFN/head choices, and label architecture-specific assumptions. Do not introduce this as implementation work until prerequisites pass. |
| Weight tying, dropout and train/eval behavior | Upstream Chapter 4 notebook discusses these; no corresponding tested public contract found in the inspected pages | Gap in the checked scope. Clarify tied versus untied token embedding/output weights, distinguish dropout from causal masking, and state that dropout behavior differs between training and evaluation. Any tests belong to a future prerequisite-gated implementation iteration. |
| Optional efficiency and architecture variants | Upstream Chapter 4 README links KV cache, performance, MoE, GQA and MLA materials | Optional deep dives, not baseline acceptance criteria. Avoid uncontextualized benchmark claims and avoid implying a GPT-2-style baseline represents every LLM. |
| EN/FR parity, rendered output, links and tests | Candidate bilingual overview/concept pairs exist | Source inspection only. This pass did not run a new Quarto render, external-link sweep or browser/mobile review. CI green for another PR is not evidence that these particular pages were visually reviewed. |

**Upstream evidence checked (2026-10-29):** [Raschka Chapter 4 README](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04), [main-code README and standalone GPT code](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/01_main-chapter-code), and [Chapter 4 notebook](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch04/01_main-chapter-code/ch04.ipynb). These cover a GPT-2-style baseline with learned token/position embeddings, LayerNorm, residual paths, feed-forward sublayers, repeated blocks, final normalization, vocabulary output, weight-tying discussion, dropout/eval behavior and generation. Optional bonus material is not part of the core baseline.

**Disposition:** no new implementation or duplicate issue created in this audit. Keep #98 as the owner for architecture-level multi-head shape flow, block ordering and GPT configuration/accounting gaps. Use #80/#81/#82 for their established concept-specific responsibilities.


## 8. Upstream repository inventory refresh (2026-10-29)

This section records a fresh review of the upstream repository's current root README on 2026-10-29. It supplements the chapter-level audits above, which remain valid for their stated scope and dates. The upstream repository is a living code companion: this inventory is a dated snapshot, not a permanent guarantee that its README lists every file or future addition.

**Source checked:** [Raschka — LLMs-from-scratch README](https://github.com/rasbt/LLMs-from-scratch/blob/main/README.md), including its chapter table, prerequisites, exercise guidance and Bonus Material catalogue. The README describes the core purpose as developing, pretraining and fine-tuning a GPT-like LLM, including both training a small model for education and loading larger pretrained weights for fine-tuning.

### Core book scope: required coverage baseline

| Upstream component | LLM Lab learning outcome | Existing public coverage (2026-10-29) | Gap / rule |
|---|---|---|---|
| Ch. 1 — Understanding LLMs | Explain what an LLM is, its lifecycle and the role of its main components. | Transformer overview, landing pages, glossary and history. | Partial. Expand beyond a single GPT data-flow sketch: model families, pretraining versus adaptation, inference, capabilities and limits. |
| Ch. 2 — Working with text data | Go from raw Unicode text through tokenization, token IDs, embeddings, batches, context windows and next-token targets. | Text/data, Unicode, tokenization, training examples, tensors and embedding-space pages. | Partial. Preserve the distinction between teaching tokenizer, production tokenizer, BPE training and applying a pretrained tokenizer; connect embeddings to the model input path. |
| Ch. 3 — Coding attention mechanisms | Explain and implement attention, causal masking, dropout, batching and multi-head attention. | Q/K/V, scaled dot-product attention, causal masking and tensor pages. | Partial. Multi-head reshape/split/merge/projection, dropout train/eval behavior, buffers and batched shape contracts remain explicit gaps. |
| Ch. 4 — Implementing a GPT model from scratch | Assemble a GPT-2-style decoder-only model from inspectable components and understand its configuration and parameterization. | Transformer overview and related representation/attention concept pages. | Partial. No complete tested GPT contract yet: configuration, parameter accounting, block ordering, residual paths, normalization, FFN, output head, weight tying, dropout semantics and end-to-end tensor-shape trace. |
| Ch. 5 — Pretraining on unlabeled data | Train a randomly initialized small GPT, validate it, checkpoint it and generate text. | Loss/likelihood/gradient concepts and training-example pages. | Major gap. A complete reproducible pretraining loop, data split, optimizer/schedule, checkpointing, validation, generation and reported run are not yet evidenced. This is the core from-scratch completion criterion. |
| Ch. 6 — Finetuning for text classification | Adapt a pretrained GPT for sequence classification and evaluate it against a baseline. | No dedicated complete public bilingual module identified. | Gap. Must cover classification head, supervised dataset, training/evaluation split, metrics, baselines and error analysis. |
| Ch. 7 — Finetuning to follow instructions | Prepare instruction data, perform supervised instruction tuning, mask targets correctly and evaluate responses. | No complete public bilingual module identified. | Gap. Include data format/quality, prompt-target masking, batching/packing where relevant, SFT loop, held-out evaluation and limitations. |
| Appendix A — Introduction to PyTorch | Understand tensors, autograd, modules, datasets/dataloaders and device-aware execution needed by the build path. | Mathematical and tensor concept pages. | Partial. These are not a substitute for a practical PyTorch foundation; add only the required PyTorch concepts and tests, without duplicating general math unnecessarily. |
| Appendix B — References and further reading | Navigate primary papers, implementation references and further study. | Public annotated references and figure provenance. | Partial. Keep source roles and version/date explicit. |
| Appendix C — Exercise solutions | Practise and verify each chapter's learning objectives. | EN/FR exercise entry pages are navigation scaffolding. | Gap. Do not imply exercises or solutions exist until authored, checked and bilingual. |
| Appendix D — Training-loop improvements | Understand and measure learning-rate scheduling, clipping, logging/checkpointing and related training improvements. | No dedicated public module identified. | Gap/advanced extension. Distinguish baseline training loop from optional improvements and measure rather than repeat performance claims. |
| Appendix E — Parameter-efficient finetuning with LoRA | Explain low-rank adapters and implement/evaluate parameter-efficient adaptation. | No complete public bilingual module identified. | Gap/advanced extension. Keep separate from full fine-tuning and from quantization; report quality and resource trade-offs. |

### Upstream bonus catalogue: optional extensions, not prerequisites for the first GPT

The following topics are present in the README's current Bonus Material list. They belong in the long-term coverage map, but should be organized as optional branches after the core concepts they depend on. Their presence upstream does not make every item mandatory for a learner's first end-to-end GPT.

| Upstream bonus cluster | Topics to account for | LLM Lab treatment |
|---|---|---|
| Setup and reproducibility | Python/package setup, Docker environment | Developer setup documentation, not a conceptual course chapter. Keep environment instructions reproducible and separate from model theory. |
| Ch. 2 — tokenizer/data extensions | BPE tokenizer from scratch, comparisons of BPE implementations, embedding layer versus linear layer, dataloader intuition, SimpleTokenizerV3 | Optional deep dives attached to text/data and representation pages. Explain what is a core tokenizer contract versus an implementation-specific choice. |
| Ch. 3 — attention implementation extensions | Efficient multi-head-attention implementations; PyTorch buffers | Optional implementation/performance branch after a correct transparent baseline. Include device, version, shape and benchmark conditions for performance claims. |
| Ch. 4 — architecture and inference extensions | FLOPs analysis, KV cache, GQA, MLA, sliding-window attention, Gated DeltaNet, DeepSeek Sparse Attention, cross-layer KV sharing, MoE | Advanced architecture/inference branches. Compare each against the baseline and state which assumptions or data-flow contracts change. |
| Ch. 5 — pretraining, loading and model-family extensions | Alternative weight loading, Gutenberg pretraining, training-loop improvements, CPU/MPS discrepancies, hyperparameter tuning, UI, GPT-to-Llama conversion, memory-efficient weight loading, tokenizer extension, training performance, Llama/Qwen/Gemma/Olmo/Tiny Aya/Qwen3.5/Gemma 4 implementations, other pretrained LLM drop-in replacements | Separate into (a) reproducibility and performance, (b) checkpoint/tokenizer interoperability, and (c) architecture-family comparisons. A GPT-2-style implementation must not be presented as a universal LLM architecture. UI work is optional and not a core learning outcome. |
| Ch. 6 — classification extensions | Experiments across layers/model sizes, IMDb dataset, classifier UI | Optional experiments only after the baseline classification path exists. UI is not a substitute for evaluation. |
| Ch. 7 — instruction-tuning extensions | Dataset utilities for near-duplicate detection and passive-voice entries; instruction-model evaluation; instruction dataset generation/improvement; preference-data generation; DPO; UI | Split into data quality, SFT, evaluation and preference optimization. DPO is a distinct preference-optimization stage, not synonymous with SFT. Keep dataset-generation provenance and evaluator limitations explicit. |
| Exercises and self-assessment | Chapter exercises, code solutions, external chapter quiz resource | LLM Lab should author original exercises with stable bilingual IDs and hidden answer keys; link external exercises rather than copying protected material. |

### Related but separate sequel: Reasoning From Scratch

The upstream README also links to the separate [Reasoning From Scratch repository](https://github.com/rasbt/reasoning-from-scratch). Its listed topics include verifier-based evaluation (MATH-500), multiple-choice/leaderboard/LLM-as-a-judge evaluation, self-consistency, self-refinement and RLVR/GRPO.

These are **not part of the core LLMs-from-scratch book baseline**. Track them as a separate advanced extension for reasoning, inference-time scaling and reinforcement learning. Do not silently expand the definition of core parity to include the sequel; do not omit the sequel from the wider research/extension map either.

### Definition of complete coverage

LLM Lab should be considered a complete pedagogical companion to the reviewed upstream scope only when:

1. Every core chapter and appendix above has a clear public destination, with bilingual parity and a status backed by page/code/test evidence.
2. A learner can follow one coherent, executable path from raw text to a GPT trained from random initialization, validation and text generation on a manageable corpus.
3. Pretrained checkpoint loading, text-classification fine-tuning, instruction SFT and LoRA are taught as distinct stages with their own data, objectives and evaluation.
4. Every bonus cluster is either mapped to an optional destination, explicitly deferred with rationale, or marked out of scope; no item is accidentally lost because it lives in a bonus directory.
5. The separate reasoning sequel remains clearly classified as an extension rather than being conflated with the core book.
6. “Covered” is not inferred from a link or heading alone: it requires a sufficient explanation, assumptions and limitations, appropriate examples, and—where implementation is claimed—code and tests. Rendering, browser review and learner mastery remain separate evidence states.

**Scope discipline:** this inventory does not authorize bulk lesson creation or implementation. Continue with the existing prioritized issues and prerequisite review; use the inventory to prevent omissions and duplicated ownership.
