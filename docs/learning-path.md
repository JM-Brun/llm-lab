# Learning path

> **Editorial boundary (2026-10-30):** the public site distinguishes four reader-facing destinations: **Understand** (the conceptual course), **Build** (the guided implementation route), **Deepen** (optional mathematical/technical depth), and **Practice & experiment** (exercises and evidence-producing investigations). These are destinations, not four duplicated curricula. Build reuses the canonical concept pages and introduces only the local tensor, probability, and gradient operations needed at each milestone. Advanced mathematics is not a blanket prerequisite. The exhaustive page-by-page classification and milestone-to-code/test evidence matrix are maintained in [content-section-mapping.md](content-section-mapping.md); the four-destination navigation complements, rather than replaces, the three learning depths described below.

This plan is a sequence of evidence-producing modules, not a promise of mastery after a fixed number of hours. Each module is complete only when its implementation, tests, experiment notes, and limitations are available. The repository's current status, priorities, and acceptance criteria are tracked in the [roadmap](roadmap.md).

## Reader-facing map: understand → guided build → deepen → practice

This crosswalk connects the public conceptual course to the guided build and optional deep dives. It is a **status-aware map**, not a claim that every lifecycle stage already has a complete lesson or implementation. The sidebar separates the conceptual course, the guided build entry point, optional deep dives, and practice. The mathematical-foundations page remains an optional LLM-specific orientation map in Understand, placed after the core conceptual sequence rather than before the Transformer overview. It exposes existing canonical content; planned stages remain visible here as gaps rather than as empty or misleading links. The navigation coordination is tracked in [issue #130](https://github.com/JM-Brun/llm-lab/issues/130), while this three-depth curriculum map belongs to [issue #87](https://github.com/JM-Brun/llm-lab/issues/87).

| Lifecycle question | Panorama / current navigation | Guided-build milestone | Existing canonical pages (FR / EN) | Status and owner |
|---|---|---|---|---|
| **1. What is an LLM?** What problem does it solve, and how do model families and objectives differ? | Start with the system-level mental model. The current entry point is specifically a GPT/Transformer overview, not yet a broad LLM panorama. | G0 — understand what is being built and distinguish decoder-only GPT from other model families. | [Vue d’ensemble Transformer](../site/fr/transformer.qmd) / [Transformer overview](../site/en/transformer.qmd); [Historique](../site/fr/transformer-history.qmd) / [History](../site/en/transformer-history.qmd); [Glossaire](../site/fr/glossary.qmd) / [Glossary](../site/en/glossary.qmd). | **Partial.** A broad bilingual LLM orientation covering families, objectives, lifecycle, capabilities and limits remains assigned to [#108](https://github.com/JM-Brun/llm-lab/issues/108). |
| **2. How does text become model input?** How are text, tokens, IDs, windows and targets prepared? | Sidebar: **Prepare text and data**. | G1–G2 — tokenize text, form deterministic context windows, align inputs and next-token targets, and define data splits. | [Texte et données](../site/fr/text-data.qmd) / [Text and data](../site/en/text-data.qmd); [Unicode](../site/fr/unicode-text.qmd) / [Unicode](../site/en/unicode-text.qmd); [Tokenisation](../site/fr/tokenization-strategies.qmd) / [Tokenization](../site/en/tokenization-strategies.qmd); [Exemples d’entraînement](../site/fr/training-examples.qmd) / [Training examples](../site/en/training-examples.qmd). | **Existing concept pages; implementation/evidence partial.** Active foundational review: [#82](https://github.com/JM-Brun/llm-lab/issues/82); tokenizer resources: [#114](https://github.com/JM-Brun/llm-lab/issues/114); data-window ownership: [#58](https://github.com/JM-Brun/llm-lab/issues/58). |
| **3. How are token IDs represented?** How do embeddings and positional information become contextualized hidden states? | Understand → **From text to representations**. | G3 — trace IDs to vectors and contextual states; learn only the tensor shapes needed for the next implementation operation. | [Espace des embeddings](../site/fr/embedding-space.qmd) / [Embedding space](../site/en/embedding-space.qmd); [Position](../site/fr/positional-encoding.qmd) / [Position](../site/en/positional-encoding.qmd); [Représentations contextualisées](../site/fr/contextualized-representations.qmd) / [Contextualized representations](../site/en/contextualized-representations.qmd). Optional technical reference: [Tenseurs](../site/fr/tensors.qmd) / [Tensors](../site/en/tensors.qmd). | **Concept pages exist; implementation/evidence partial.** Tensor theory is not a gate: Build introduces the required shapes and operations locally. Keep [#82](https://github.com/JM-Brun/llm-lab/issues/82) as the content-validation gate; page existence does not establish source, browser or learner validation. |
| **4. What computation transforms representations?** How does a Transformer mix information across positions and layers? | Sidebar: **Compute with the Transformer**. | G4–G5 — attention and causal masking, then assemble a GPT block with residual paths, normalization, feed-forward layers and output projection. | [Vue d’ensemble Transformer](../site/fr/transformer.qmd) / [Transformer overview](../site/en/transformer.qmd); [Q/K/V](../site/fr/queries-keys-values.qmd) / [Q/K/V](../site/en/queries-keys-values.qmd); [Attention](../site/fr/scaled-dot-product-attention.qmd) / [Attention](../site/en/scaled-dot-product-attention.qmd); [Masquage causal](../site/fr/causal-masking.qmd) / [Causal masking](../site/en/causal-masking.qmd). | **Conceptual coverage partial; implementation gap.** Concept-to-code sequencing: [#78](https://github.com/JM-Brun/llm-lab/issues/78); attention/masking work remains downstream of #82. |
| **5. How does the model produce a next-token prediction, and what objective is optimized?** | Sidebar: **Produce a prediction** and the learning-objective section. | G6 — align targets, obtain vocabulary logits, compute token-level cross-entropy and define loss reduction/masking. | [Logits](../site/fr/logits.qmd) / [Logits](../site/en/logits.qmd); [Probabilités](../site/fr/probabilites.qmd) / [Probabilities](../site/en/probabilities.qmd); [Vraisemblance](../site/fr/vraisemblance.qmd) / [Likelihood](../site/en/likelihood.qmd); [Entropie croisée](../site/fr/cross-entropy.qmd) / [Cross-entropy](../site/en/cross-entropy.qmd); [Loss](../site/fr/loss.qmd) / [Loss](../site/en/loss.qmd). | **Concept pages exist; end-to-end integration partial.** Keep the distinction between a training objective and factual correctness explicit. |
| **6. How does a model learn from random initialization?** How do optimization, validation and checkpoints fit together? | Planned guided-build stage; do not add an empty sidebar destination. | G7 — use gradients and backpropagation to train a small GPT with a reproducible optimizer/update loop, validation and checkpointing. | The gradients concept page exists; no complete public training module or end-to-end run is currently evidenced. | **Planned / major gap.** The core from-scratch outcome is tracked by the curriculum and upstream Chapter 5 coverage in [full-curriculum-plan.md](full-curriculum-plan.md). |
| **7. How does a trained model generate text?** How do autoregressive decoding and sampling work? | Planned guided-build stage; distinguish inference from training. | G8 — generate from a trained checkpoint; specify decoding, stopping and context-window behavior. | The Transformer overview introduces the system-level distinction, but no complete public generation lesson/run is evidenced. | **Planned / gap.** Existing generation ownership: [#84](https://github.com/JM-Brun/llm-lab/issues/84). |
| **8. How are pretrained models reused and adapted?** How do checkpoint loading, classification, instruction tuning and parameter-efficient adaptation differ? | A separate branch after the from-scratch core, not a continuation of random-initialization training. | A1–A4 — pretrained checkpoint loading, classification, instruction SFT and LoRA/quantization. | No complete bilingual public pathway for these stages is currently evidenced. | **Planned / gaps.** Map against upstream Chapters 6–7 and Appendices A–E in [full-curriculum-plan.md](full-curriculum-plan.md); do not conflate LoRA with quantization or SFT. |
| **9. How do we evaluate claims and investigate failure?** | Sidebar: **Evaluate and challenge** plus optional critical deep dives. Evaluation is introduced before experiments and applies across training, generation and adaptation. | G9 — compare against a reference only under compatible architecture/tokenizer/weight conditions; E1 — define task-specific metrics, baselines, uncertainty, ablations, leakage checks and error analysis. | [Évaluation expérimentale](../site/fr/evaluation-experimentale.qmd) / [Experimental evaluation](../site/en/experimental-evaluation.qmd); [Similarité cosinus](../site/fr/cosine-similarity.qmd) / [Cosine similarity](../site/en/cosine-similarity.qmd); [Linéarité des embeddings](../site/fr/linearite-embeddings.qmd) / [Embedding linearity](../site/en/embedding-linearity.qmd). | **Conceptual and critical-reading pages exist; reusable evaluation workflow partial.** Owner: [#78](https://github.com/JM-Brun/llm-lab/issues/78) and evaluation follow-ups. |
| **10. Where can I go deeper or look things up?** | Sidebar: **Deep dives and critical perspectives**, glossary and references. | Optional detours from any milestone; not a mandatory final stage. | [Glossaire](../site/fr/glossary.qmd) / [Glossary](../site/en/glossary.qmd); [Références](../site/references.qmd); mathematics and critical-reading pages linked above. | **Existing reference structure; traceability still being completed.** #87 owns milestone-to-deep-dive/source links. |

### How the three learning depths work together

- **Panorama:** build a short mental model of an LLM and its lifecycle. The current public overview is GPT/Transformer-centred; the broader family-level panorama remains partial.
- **Guided build:** follow G0–G9 to implement, train, validate and generate with a small GPT from randomly initialized parameters. Stop at unmet evidence gates; the current foundational gate is #82.
- **Deep dives:** enter concept pages, mathematical derivations, critical analyses and experiments when they answer a concrete question. They are optional branches, not a second mandatory syllabus.

The sidebar is intentionally a map of **available canonical pages**, not a complete representation of every future lifecycle stage. In both languages, the mathematical-foundations page remains an optional orientation map at the end of Understand, not a prerequisite at the top of the sequence. The landing page should expose Practice & experiment alongside the other first-visit routes. Planned training, generation and adaptation stages must be described as planned in the curriculum and homepage until their destinations and evidence exist. Do not create empty links merely to make the menu appear complete.

### How to use this map

- Start from the [French landing page](../site/index.qmd) or [English landing page](../site/en/index.qmd), then choose the panorama, guided build or a deep dive.
- Follow the guided milestones in dependency order, but stop at unmet exit criteria. The current active gate is #82; this map does not authorize jumping ahead to attention, full-GPT implementation or training.
- Follow contextual links from an overview to a concept page, and from that concept to code/tests or evidence where available. A deep dive should always provide a route back to its parent question.
- Treat “page exists,” “source checked,” “code executes,” “CI passes,” “rendered desktop/mobile reviewed,” and “learner can transfer the idea” as separate evidence states.

## How the guided milestones relate to the concept pages

The **G0–G9 milestone table above is the authoritative sequence** for the from-scratch GPT build. The topic descriptions below are not a second course sequence: they describe the kinds of knowledge and evidence attached to those milestones.

- **Foundations and text (G0–G3):** mathematical and numerical prerequisites; Unicode and tokenization; context windows and targets; tensor shapes, embeddings and contextualized representations.
- **Architecture and objective (G4–G6):** Q/K/V, attention and causal masking; GPT block composition; logits, likelihood, cross-entropy, loss and gradients.
- **From-scratch training and inference (G7–G8):** optimization, validation, checkpoints, reproducibility, autoregressive generation and decoding.
- **Verification (G9):** reference comparison only under compatible architecture, tokenizer, weights and preprocessing. This is a verification milestone, not a substitute for task-level evaluation.
- **Separate adaptation branch (A1–A4):** pretrained checkpoint reuse, classification, instruction SFT, and parameter-efficient adaptation. These milestones do not belong inside the randomly initialized training route.
- **Cross-cutting evaluation (E1):** task-specific metrics, baselines, uncertainty, ablations, leakage, contamination, distribution shift and error analysis. Introduce evaluation design before experiments; do not postpone it to a final course chapter.

For detailed coverage against Raschka's chapters and appendices, use the [full curriculum map](full-curriculum-plan.md). Avoid maintaining parallel module lists with different ordering or status: update the milestone table and the coverage map instead.

## Critical reading: test default assumptions

The bilingual notes on [cosine similarity](../site/fr/cosine-similarity.qmd) and the [linearity hypothesis](../site/fr/linearite-embeddings.qmd) are cross-cutting modules, not replacements for the implementation sequence above. Use them to practise stating assumptions, finding counterexamples, designing controls, and distinguishing decodability from causal use. Their proposed experiments should be considered complete only when the protocol and results are committed under `experiments/` and summarized under `reports/`.

## Weekly working rhythm

Plan for **up to five focused hours per week**, in sessions of **no more than 60 minutes**. This is a sustainable planning ceiling, not a deadline or a promise that a milestone will fit into a fixed number of weeks.

At the start of each week, select the smallest unfinished acceptance criterion from the current milestone. Allocate sessions to:
1. inspect and understand the relevant concept/source;
2. work through one concrete example or derivation;
3. review a misconception, boundary case or counterexample;
4. inspect or write tests/code only when the prerequisite gate permits implementation;
5. record what is established, uncertain and still missing.

Do not schedule downstream milestones by calendar date. In particular, do not move to attention, full-GPT implementation or training while the active #82 foundational gate remains open. Missed sessions do not create a requirement to exceed the weekly or session limit. Adaptation topics (A1–A4) remain a separate later branch, not a fixed week in the core route.

## 2026-10-29 — End-to-end GPT build route and evidence gates

This section makes the guided path operational while preserving the current prerequisite gate. It does not authorize downstream implementation before the active foundational slice and private knowledge review are complete. It is a route specification and status snapshot, not a claim that the build is already executable.

### Two distinct learning routes

- **Core from-scratch route:** implement a small decoder-only GPT from randomly initialized parameters, train it on a documented manageable corpus, validate it, save a checkpoint, and generate text. This is the defining end-to-end construction outcome.
- **Pretrained adaptation route:** load a compatible pretrained checkpoint and tokenizer, then adapt/evaluate the model for classification or instruction following; later explore LoRA and quantization. This route starts from learned parameters and is not a substitute for the from-scratch route.

The routes share foundations (text, tokenization, tensors, architecture, prediction and evaluation) but diverge at initialization and training objective.

### Guided build milestones

| ID | Learner question and milestone | Prerequisites | Expected learner artifact / evidence | Current public evidence and status | Owner |
|---|---|---|---|---|---|
| G0 | **What are we building?** Understand an autoregressive decoder-only GPT, next-token prediction, and the boundary between model, tokenizer, data and inference. | Basic programming and elementary linear algebra/probability. | Correct component/data-flow explanation; distinguish GPT-style decoder-only models from all LLMs and encoder–decoder Transformers. | Transformer overview, landing pages and glossary exist; optional history is available in Reference; full LLM-family/lifecycle coverage is partial. | #108, #130 |
| G1 | **How does raw text become model input?** Unicode/text normalization, tokenizer, vocabulary, token IDs and special tokens. | Strings, bytes and basic data handling. | Trace one text example through a tokenizer; state tokenizer identity/version and special-token behavior. | Text/data, Unicode and tokenization pages exist; source/resource and transition work remains active. | #82, #114 |
| G2 | **How are examples formed?** Context windows, shifted input/target sequences, batching, padding/truncation and data splits. | G1; tensor indexing. | Deterministic batch with aligned inputs/targets; tests for off-by-one errors, boundaries and train/validation separation. | Training examples page exists; corpus-to-examples implementation is separately tracked. Do not duplicate #58 or revive #83 without a distinct gap. | #58, #78 |
| G3 | **How do tokens become vectors?** Tensor shapes, embedding-table lookup, positional information and the difference between input embeddings and contextualized states. | G1–G2; vector/matrix and indexing basics. | Trace shapes from token IDs [B,L] to vectors [B,L,d]; explain absolute position embeddings versus RoPE. | Conceptual chain is the active #82 slice; worked example and shape explanation exist, but iteration 3 validation must be completed before treating the slice as closed. | #82 |
| G4 | **How does the model mix context?** Q/K/V, scaled dot-product attention, causal masking and multi-head attention. | G3; matrix multiplication, softmax and tensor dimensions. | Explain and test that a position cannot use future tokens; show head split/merge shapes and train/eval behavior for dropout. | Conceptual Q/K/V, attention and causal-mask pages exist; implementation-level shape/invariant evidence remains incomplete. | #79–#81, #78 |
| G5 | **What is a GPT block?** Assemble attention, residual paths, normalization, feed-forward network, positional mechanism and output projection in the selected order. | G3–G4; module composition and initialization concepts. | Documented block diagram and shape trace; parameter-count sanity check; forward/backward tests and explicit configuration. | Transformer overview explains components conceptually; a complete tested GPT implementation is not evidenced. | #78, then scoped architecture issue |
| G6 | **What is the learning objective?** Align shifted targets, obtain vocabulary logits, compute token-level cross-entropy and reduce the loss correctly. | G2, G5; logits, categorical probabilities and log probabilities. Gradients are not required to define or calculate the loss. | Hand-checkable loss example; tests for target alignment, ignored/padded targets, numerical stability and reduction semantics. | Logits, likelihood, entropy, cross-entropy and loss pages exist; full model/data integration is not evidenced. | #58, #79 |
| G7 | **How do parameters learn?** Backpropagation, optimizer updates, learning-rate schedule, clipping, validation, checkpointing and reproducibility. | G5–G6; gradients, chain rule and PyTorch/autograd basics. | Reproducible small training run with fixed configuration/seed, train/validation curves, checkpoint and documented limitations. | The gradients concept page exists; no complete end-to-end pretraining run is evidenced in the public learning path. | Future pretraining issue after prerequisite review |
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
