# Comparative audit of LLM learning paths

**Audit date:** 2026-11-05  
**Purpose:** record the external curriculum comparison referenced by [#225](https://github.com/JM-Brun/llm-lab/issues/225), and make explicit which design principles are transferable to LLM Lab. This is an existing, dated project-level baseline and must be reused by the [project-level learning resource audit workflow](../workflows/project-learning-resource-audit.md) and coordinator [#756](https://github.com/JM-Brun/llm-lab/issues/756), not recreated as a new portfolio report.  
**Scope:** public curriculum structure and stated learning activities, not a full evaluation of lesson quality or learner outcomes. The two external courses evolve; this is a dated snapshot.

## November 21 update: the nine-stage Understand route

**Baseline:** [Understand registry at `0b728a2`](https://github.com/JM-Brun/llm-lab/blob/0b728a2b8f8598cdfad2b49eab3e0e8cb0baea57/data/guided-route.yml), [conceptual map](../../site/fr/learning-map.qmd#conceptual-route), and review plans ([FR](../../site/fr/review-path.qmd), [EN](../../site/en/review-path.qmd)). The registry links nine stages, twenty lessons and their revision sheets. Use each lesson's topic ID to find its contract and bilingual sheet in `lesson_contracts`; sequence and exercise links remain maintained in the registry. The original November 5 comparison follows this update.

This is a source-level comparison of public outlines and selected lessons or code, with the degree of inspection stated below. It covers Understand. Use implementation-heavy comparisons against the separate [Build path](../learning-path.md) when the external outcome is a working implementation. The sample covers contrasting ways to teach GPT and one French-language alternative. It provides no measured learner outcomes.

### External routes and evidence

| Resource | Progression in the inspected material | Audience, evidence and what to compare |
|---|---|---|
| **Raschka** | Overview → text, embeddings and shifted examples → causal attention → GPT and initial generation → loss, pretraining and sampling → fine-tuning. | Python/PyTorch construction with chapter exercises and official code. The [companion chapter map](https://sebastianraschka.com/llms-from-scratch/) and [publisher's contents](https://www.manning.com/books/build-a-large-language-model-from-scratch) locate chapters 1–5. Use chapters 2–4 for representation and model assembly and chapter 5 for the connection between target scores, training and decoding. |
| **Karpathy** | In *Zero to Hero*, micrograd → character bigram with loss and sampling → MLP and diagnostic work → GPT → dedicated tokenizer lesson. In *Let's build GPT*, the bigram already exposes loss and generation before self-attention extends the model. | Basic Python and some calculus for the opening lecture. Evidence is the [official syllabus](https://github.com/karpathy/nn-zero-to-hero) and the [GPT lecture's chapter markers and code](https://www.youtube.com/watch?v=kCc8FmEb1nY). Use the bigram as a baseline for asking which operations survive a change of architecture. |
| **Hugging Face** | Pretrained model and task pipeline → inputs, model outputs and postprocessing → fine-tuning and sharing → dedicated tokenizers → causal pretraining example among other tasks. | Good Python and introductory deep learning recommended. The [introduction](https://huggingface.co/learn/llm-course/en/chapter1/1), [pipeline walkthrough](https://huggingface.co/learn/llm-course/en/chapter2/2), [tokenizer chapter](https://huggingface.co/learn/llm-course/en/chapter6/1) and [causal training example](https://huggingface.co/learn/llm-course/en/chapter7/6) expose call boundaries and framework abstractions. The chapter 2 walkthrough uses classification. Its label probabilities are an analogy for postprocessing, while the causal example supplies language-model evidence. |
| **Stanford CS336 (Spring 2026)** | Overview and tokenization → compute accounting and architectures. The first assignment couples tokenizer, model, optimizer and a minimal training run. Later meetings cover systems, inference, scaling, data and post-training. | University course with Python, machine-learning and math prerequisites. The [syllabus and assignment descriptions](https://cs336.stanford.edu/) establish the teaching sequence and expected implementation evidence. Later systems and scaling material belongs to a different learning objective. The assignment was inspected at syllabus level. |
| **Construire un LLM de zéro** | A first language-machine example → learning and autograd → randomness and networks → tokenization, embeddings, attention and Transformer → training, data and evaluation → adaptation and inference. | French-language reference with an optional Python chapter, runnable notebooks and graded exercises with assertions. The [official chapter and notebook table](https://github.com/kevindegila/construire-un-llm-de-zero#les-22-chapitres) supports conclusions on sequence and stated practice. Its interactive book and the notebooks were not tested here. |
| **Jay Alammar, The Illustrated GPT-2** | Observe autoregression → trace an active token through the decoder stack → open embeddings, positions, Q/K/V and causal attention → return to output token selection and applications. | Visual companion focused on GPT-2. [Part 1](https://jalammar.github.io/illustrated-gpt2/#part-1-gpt2-and-language-modeling) shows successive tokens and positions; [Part 2](https://jalammar.github.io/illustrated-gpt2/#part-2-the-illustrated-self-attention) opens the attention calculation. Its use here is to compare explanatory order and representation of objects. |

### Nine stages and twenty lesson contracts

Coverage in the right column refers to the cited sample and its level of inspection. A course's chapter order describes when an idea is introduced. It supplies a technical prerequisite only when the learner cannot carry out the target operation without that idea.

| Stage ID | Canonical lessons, in study order | What the external material exposes |
|---|---|---|
| `orientation` | `llm-overview` — next-token prediction and a two-step preview | Alammar also starts with generation as an observable behavior. Hugging Face starts with a complete task pipeline. Both support a short preview whose internals are opened later. |
| `text-input` | `text-data` — tokens, vocabulary and IDs | Raschka ch. 2 and Stanford lecture 1 introduce tokenization early. Hugging Face ch. 2 uses the interface before ch. 6 builds tokenizers; Karpathy's GPT lesson uses characters before the dedicated subword lesson. The LLM Lab entry depends on the ID contract; BPE is useful optional detail. |
| `representations` | `embedding-space` — base lookup; `positional-encoding` — positional information; `contextualized-representations` — resulting hidden states | Raschka ch. 2 and Alammar both connect lookup to position. Alammar opens contextualization inside attention; LLM Lab first lets readers compare contextualized outputs, then explains their production. Keep the same token and position fixed when testing the effect of the accessible prefix. |
| `computation` | `transformer` — block and stack; `queries-keys-values` — projections; `scaled-dot-product-attention` — scores, weights and aggregation; `causal-masking` — allowed positions | Raschka ch. 3 and *Construire un LLM de zéro* ch. 9 teach attention before assembly (their next chapters). LLM Lab gives the block overview first, then opens the same computation. Alammar's highlighted position is a useful visual counterpart to LLM Lab's fixed-position causal counterexample. |
| `prediction` | `logits` — vocabulary scores per position; `probabilites` — predictive distribution; `entropy` — uncertainty over that distribution | Raschka ch. 4 gives the vocabulary head and greedy generation. Hugging Face ch. 2 makes output postprocessing visible in classification. LLM Lab can isolate the vocabulary axis and compare the distribution's entropy with surprisal on an observed token. The selected source sections do not establish that last distinction as a dedicated learning outcome. |
| `inference` | `inference-generation` — decoding policy, feedback, stopping, prefill/decode | Karpathy gives early executable feedback with a bigram; Raschka separates the first greedy generator (ch. 4) from sampling refinements (ch. 5); Alammar follows two successive positions. Each makes a different part of the same loop observable. |
| `context-use` | `in-context-learning` — response to supplied demonstrations; `context-engineering` — application-side selection and assembly | Hugging Face's pipeline helps locate preprocessing and the model call. It does not supply evidence for the full two-call ICL/context-engineering distinction. LLM Lab's exercise already asks which example or token reaches a second call with fixed parameters. Preserve the context intervention upstream of prediction in the compact view. |
| `scoring` | `vraisemblance` — sequence likelihood and log-likelihood; `cross-entropy` — penalty for an observed target | Karpathy's early bigram lesson scores targets with NLL. Raschka ch. 5 uses target probabilities to evaluate the model and prepare training. LLM Lab explicitly contrasts observed-prefix scoring with generated-prefix feedback and distinguishes entropy, likelihood and one-target cross-entropy. |
| `training` | `loss` — reduce token penalties; `gradients` — derivatives and update; `training-loop` — repeated steps and held-out validation | Karpathy and the French course teach gradients early through autograd. Raschka and CS336 use a trainable GPT as the end-to-end implementation test. Understand already makes reduction, gradient computation, update and fixed-parameter validation separate learner actions. This comparison does not establish Build parity. |

### Transitions and their evidence

| Teaching transition | What to check in the existing route, lesson or sheet |
|---|---|
| 01 → 02, preview → tokenization | Can the learner identify which object is fed back after a selection and why a piece of text needs an ID representation? Read the first two [review-plan stages](../../site/fr/review-path.qmd#orientation). |
| 02 → 03, IDs → vectors | At fixed table, repeated IDs give identical base vectors. A joint relabeling of IDs and table rows preserves lookup. [Lookup exercise](../../site/fr/exercises/text-data.qmd#ex-text-to-embedding-lookup) |
| 03 → 04, what changes an input or hidden state | Vary position, then accessible prefix, then future-only suffix while holding the relevant other factors fixed. The last comparison tests causal invariance. [Position exercise](../../site/fr/exercises/text-data.qmd#ex-token-to-block-input) · [Causality exercise](../../site/fr/exercises/contextualized-representations.qmd#ex-contextualization-causal-boundary) |
| 04 → 05, hidden state → vocabulary logits | Carry one position across the output head. Identify the two softmax axes and the prediction row for an unpadded prefix. At the study-order boundary, make explicit why visiting SDPA before its dedicated mask lesson still means applying the mask before softmax in the causal computation. [Causal-mask sheet](../../site/fr/revision-causal-masking.qmd) · [Output-head exercise](../../site/fr/exercises/logits.qmd#ex-final-state-to-next-token) · [Softmax axes exercise](../../site/fr/exercises/logits.qmd#ex-attention-vocabulary-softmax) |
| 05 → 06, predict → generate | Hold logits fixed and compare greedy selection with sampling at unit temperature with all candidates kept. Only then extend the prefix. [Decoding-policy exercise](../../site/fr/exercises-generation.qmd#ex-generation-distribution-selection) |
| 06 → 07, one generation → another application call | Trace what carries over between token steps and what the application has to supply on the next call. [Two-call exercise](../../site/fr/exercises/context-engineering.qmd#ex-context-between-calls) |
| 07 → 08, study transition to scoring | Start from the shared prediction (05). Scoring takes an observed target and its observed prefix. Context engineering is not a prerequisite. Compare both continuations at the second step and use distributions with equal observed-token scores and different entropies. [Prefix exercise](../../site/fr/exercises/vraisemblance.qmd#ex-generation-versus-scoring) · [Entropy exercise](../../site/fr/exercises/entropy.qmd#ex-entropy-and-observed-score) |
| 08 → 09, score → objective → update | With a one-hot target, reduce token penalties over valid positions. Equal token losses need not produce equal updates. Compute a gradient while holding parameters fixed, then apply the optimizer and make a fresh prediction. [Score-to-update exercise](../../site/fr/exercises/gradients.qmd#ex-score-to-parameter-update) · [Validation-loss exercise](../../site/fr/exercises/loss.qmd#ex-validation-loss-by-token) |

### Decisions and next check

- **Keep the current study order.** French and English construction resources show that leading with gradients or attention serves a build-first objective. The current preview → mechanism → applications progression answers a different question. Keep the four uses visible in the simplified view: generation feeds a chosen token back, context design changes the input upstream, scoring evaluates an observed target and training updates parameters after calculating an objective and its gradient.
- **Reuse a continuous trace for review before editing lessons or sheets.** The useful feature of Karpathy's baseline and Alammar's active-position trace is being able to identify the same object across an explanation. In the [existing trace](../../site/fr/exercises/contextualized-representations.qmd#ex-contextualization-causal-boundary), changing the future target from `U` to `V` keeps the prediction row at `X` fixed. Reading the two target columns of that row gives different local losses, `ln 2` and `ln 4`. Use the [existing learner protocol](../audits/learning-path-learner-evaluation.md) to check whether learners independently recover the causal query position, the vocabulary axis and the observed target from the lesson → sheet → exercise links. A failure to locate a step points first to the link or sheet wording; a recurrent failure to explain a needed concept before it is introduced would justify reviewing the order. This comparison provides neither observation.
- **Reuse the same matrix on the next substantive route revision.** Record the LLM Lab revision and the external section inspected. Classify each comparison in prose as an equivalent lesson, a different visit order, an optional companion or a gap in the inspected evidence. Keep bilingual outcomes and exercises connected by their existing topic IDs. The comparative audit stores observations and decisions; the canonical registry remains the source for order, contracts and links.

---

**Historical baseline, November 5, 2026.** The reference to a six-stage route below describes that snapshot.

## Executive conclusion

LLM Lab should remain a **concept-first, implementation-supported, bilingual learning system** rather than reproduce either external course's chapter order.

- **Raschka's _Build a Large Language Model (From Scratch)_** is the closest implementation baseline: it develops a GPT-like model from text data and embeddings through attention, model assembly, pretraining and fine-tuning, with executable Python/PyTorch code and chapter exercises.
- **The Hugging Face Course** is an ecosystem- and task-oriented curriculum: it teaches Transformer concepts and practical use, then covers fine-tuning, sharing, datasets, tokenizers, classical NLP, demos, dataset curation, LLM fine-tuning and reasoning models.
- **LLM Lab's differentiator** is the explicit separation of conceptual understanding, practical construction, optional depth and evidence-producing practice. Its inference-first conceptual route is deliberately not the same as the dependency order for training a model.

These are complementary reference points, not competitors to rank on one scale. They optimize for different learner outcomes.

## 1. Source inventory and scope

| Source | Publicly stated scope | Main organizing logic | Primary evidence / activity |
|---|---|---|---|
| Raschka, book companion hub and official code repository | Build a GPT-style LLM in Python/PyTorch: text data, embeddings, attention, GPT implementation, pretraining and fine-tuning | Chapter-by-chapter bottom-up implementation path | Read, optional video pass, code along, chapter exercises |
| Hugging Face Course | LLM/NLP concepts and practical use of Transformers, Datasets, Tokenizers, Accelerate and the Hub; includes demos, dataset curation, LLM fine-tuning and reasoning | Modular tool/task curriculum with chapter-level outcomes | Explanations, notebooks, quizzes, model/dataset workflows and practical exercises |
| LLM Lab | Understand LLM mechanisms, build a small GPT, investigate mathematical/technical depth and practice with experiments/evidence | Conceptual route plus a distinct implementation dependency path and optional branches | Canonical bilingual lessons, guided build, exercises, code/tests and experiments |

### Primary sources

**Raschka**
- [Book companion hub and chapter map](https://sebastianraschka.com/llms-from-scratch/index.html)
- [Official source repository](https://github.com/rasbt/LLMs-from-scratch)
- [Manning book contents](https://www.manning.com/books/build-a-large-language-model-from-scratch)

The companion hub recommends reading a chapter first, optionally using video as a second explanation, implementing the code, and then attempting exercises. Its chapter map runs from orientation and text data through attention and GPT implementation, then pretraining, classification fine-tuning and instruction fine-tuning. It also identifies advanced architecture guides and implementation articles as follow-up material.

**Hugging Face**
- [Current course introduction and chapter navigation](https://huggingface.co/docs/course/chapter1/1)
- [Course source repository](https://github.com/huggingface/course)

The current course navigation is broader than a single from-scratch GPT build. It includes Transformer models; using Transformers; fine-tuning a pretrained model; sharing models/tokenizers; Datasets; Tokenizers; classical NLP tasks; demos; dataset curation; LLM fine-tuning; and reasoning models. The introduction states that learners should have good Python knowledge and recommends a prior introductory deep-learning course.

**LLM Lab**
- [Narrative learning path](../learning-path.md)
- [Full curriculum and coverage plan](../full-curriculum-plan.md)
- [Reader-experience and editorial method](../reader-experience-and-editorial-method.md)
- [Content ownership map](../content-section-mapping.md)
- [2026-11-05 route reconciliation](../learning-route-reconciliation-2026-11-05.md)

## 2. Comparison by pedagogical dimension

### A. What question organizes the curriculum?

**Raschka — how can I build a small GPT-like language model from the ground up?**  
The chapter sequence is implementation-oriented. Concepts are introduced in service of progressively constructing and training a model. This gives the learner a tangible end-to-end artifact and a concrete reason to understand each component.

**Hugging Face — how can I understand and use the Transformer/NLP ecosystem to solve real tasks?**  
The course moves from Transformer concepts to library use, pretrained-model fine-tuning and sharing, then to data/tokenizer tooling and a broad range of NLP/LLM tasks. Its structure is appropriate for practical work in the Hugging Face ecosystem.

**LLM Lab — what does an LLM do, how does its computation work, and how can I inspect and reproduce a small version?**  
The conceptual route starts with a high-level system model and an inference/generation preview. It then unpacks text, representations, Transformer computation, prediction and learning. The Build route follows implementation dependencies separately.

**Decision:** retain LLM Lab's two related orders. Do not force the conceptual route into the training implementation order.

### B. Inference before training

Raschka's book places GPT implementation and text generation before the dedicated pretraining chapter, but the book's overall build path remains organized around constructing and then training the model.

The Hugging Face course introduces inference and Transformer architectures early, then proceeds to library usage and fine-tuning.

LLM Lab makes the pedagogical distinction explicit: a randomly initialized model can demonstrate the autoregressive inference loop with fixed parameters, even though its output is poor. This gives a concrete reason to study training later without implying that useful generation can be obtained without trained or pretrained parameters.

**Transferable principle:** distinguish the *mechanics* of inference from the *quality and provenance* of parameters. Keep inference and training dependencies separate in diagrams, explanations and implementation checkpoints.

### C. Conceptual explanation versus implementation

Raschka tightly connects explanations to code and exercises. The official companion hub explicitly recommends a read → optional video → code → exercises workflow. This is a strong pattern for making each conceptual step observable.

Hugging Face connects conceptual material to practical library workflows and notebooks. It is especially useful for understanding how model, tokenizer, dataset and Hub abstractions fit together in actual applied work.

LLM Lab already separates:
- Understand: canonical explanations and system-level concepts;
- Build: implementation milestones and their dependencies;
- Deepen: optional derivations, architecture variants and implementation details;
- Practice & experiment: exercises and evidence-producing investigations.

**Transferable principle:** every central concept should have a purposeful route to an implementation, exercise or experiment when one exists. But a code example must not become the only explanation, and a conceptual page must not imply that unimplemented work already exists.

### D. Depth and progressive disclosure

Raschka's companion hub explicitly places modern architecture concept guides and selected implementation articles after the core book path. This is a useful model for separating a stable baseline implementation from changing architecture variants.

Hugging Face distributes depth across chapters and specialist topics: tokenization algorithms, tokenizer construction, optimized inference, dataset curation, LLM fine-tuning and reasoning. It also exposes quizzes and chapter completion signals.

LLM Lab uses a graph of canonical pages with optional Deepen branches. It should preserve the distinction between:
- a prerequisite required to understand a claim;
- a concise reminder needed locally;
- a useful optional derivation or variant;
- an implementation-specific detail;
- a separate practice activity.

**Transferable principle:** make advanced material discoverable without turning every advanced topic into a mandatory prerequisite. Do not hide a caveat that changes the validity of the core explanation.

### E. Scope and ecosystem

Raschka is a focused from-scratch GPT implementation baseline. It is not intended to be a comprehensive course on every model family, NLP task, data platform or deployment workflow.

Hugging Face is intentionally broader and ecosystem-oriented. Its current course includes model use, sharing, datasets, tokenizers, demos, curation, LLM fine-tuning and reasoning. That breadth is valuable, but it is not the same objective as deriving and implementing a small model with minimal abstraction.

LLM Lab should not duplicate the Hugging Face library tutorial. Instead, it should explain underlying mechanisms and use external ecosystem documentation when the learning objective is practical library operation.

**Transferable principle:** define exclusions as carefully as inclusions. A curriculum becomes confusing when a reader cannot tell whether a page teaches a general mechanism, a particular software API, or an operational workflow.

### F. Bilingual and navigational design

The reviewed sources provide structured chapter navigation and supporting code/resources. LLM Lab adds a specific requirement: French and English must remain semantically equivalent, with shared conceptual IDs and a single route definition rather than two independently maintained curricula.

**Transferable principle:** treat translation as an alternate presentation of one curriculum. Validate the meaning, scope, optionality and route of each counterpart, not just the presence of a translated page.

## 3. Transferable design principles and LLM Lab decisions

| Principle observed | Why it is useful | LLM Lab decision |
|---|---|---|
| End-to-end implementation makes abstract mechanisms concrete (Raschka) | Gives concepts a coherent operational purpose | Preserve the small-GPT Build path, but keep its dependency graph separate from the conceptual sequence |
| Read before coding; use video as an optional second pass; test with exercises (Raschka) | Supports multiple representations and retrieval practice | Use explanations first, optional visual/interactive companions, then exercises and executable evidence where available |
| Chapter-level outcomes and practical notebooks (Hugging Face) | Makes expected learner capability and application visible | State page/stage outcomes and link them to concrete practice; do not equate completion with mastery |
| Real model/tokenizer/dataset workflows (Hugging Face) | Exposes abstractions and operational constraints hidden by toy examples | Link to ecosystem practice where it adds value, while keeping conceptual explanations framework-independent |
| Advanced concept guides after the core path (Raschka) | Prevents architecture churn from destabilizing the foundations | Keep variants, efficiency topics and derivations in optional Deepen branches |
| Specialist modules for data, tokenization, fine-tuning and reasoning (Hugging Face) | Provides lateral routes for different applied goals | Keep specialist branches discoverable; add them only when a distinct learning outcome and evidence are defined |
| Explicit route and chapter navigation (both) | Reduces uncertainty about where to start and what follows | Maintain the six-stage guided conceptual route, the separate G0–G9 Build route and the exploratory resource graph as distinct projections |

## 4. What LLM Lab should not copy

1. **Do not copy Raschka's chapter order mechanically.** LLM Lab intentionally teaches the inference loop before the detailed training objective, and explicitly represents corpus preparation and training-example construction as a separate branch.
2. **Do not copy Hugging Face's library-first progression.** LLM Lab is not a replacement for API documentation or an ecosystem certification course.
3. **Do not reproduce source explanations, diagrams, code or exercises.** Use these works as references, cite them, and create original teaching material.
4. **Do not flatten all topics into one linear book.** A learner should be able to stop after an overview, enter a concept directly or follow an optional deep dive.
5. **Do not treat quizzes, tests, rendered pages or completed code as proof of mastery.** They are different forms of evidence with different limits.

## 5. Implications and remaining gaps

The current LLM Lab architecture is consistent with the transferable principles above. The route reconciliation in [the 2026-11-05 audit](../learning-route-reconciliation-2026-11-05.md) records the correspondence between conceptual curriculum, guided route, Build milestones, Quarto navigation and graph projections.

The comparison identifies the following **coverage questions**, not automatic requests to add pages:

- Does the project provide enough explicit practice for readers to retrieve and apply concepts, rather than only read explanations?
- Are model evaluation, data quality, leakage, contamination, baselines and uncertainty connected to the Build path at the point where evidence is produced?
- Are adaptation methods (prompting/context, retrieval, supervised fine-tuning, instruction tuning and parameter-efficient adaptation) distinguished without implying a universal sequence?
- Is the transition from the small educational GPT to modern pretrained architectures clearly presented as a scope transition rather than a claim of production equivalence?
- Are library-specific workflows linked only where they serve a defined learning objective?

Resolve a gap only after checking the canonical page inventory and existing exercises/experiments. Prefer improving an existing canonical page or practice activity over creating another page.

## 6. Evidence limits and maintenance

- This is a comparison of public curriculum structure, navigation and stated activities as observed on 2026-11-05. It is not a controlled comparison of learning effectiveness.
- The Raschka companion hub and Hugging Face course are living resources. Re-check their current chapter maps before making future coverage claims.
- The Hugging Face course spans a broader ecosystem and task scope than the focused from-scratch book; apparent differences in topic coverage must be interpreted in light of that scope.
- A source's presence in this comparison does not grant permission to reuse its protected illustrations or prose. Check the specific asset license and attribution requirements before reuse.
- Update this note when the external course structure materially changes or when LLM Lab changes its curriculum architecture. Do not create a recurring workflow solely to re-check static source lists.

**Next review trigger:** a substantial curriculum redesign, a new major version of either external course, or a change to the boundary between Understand, Build, Deepen and Practice.

---

*Source snapshot accessed 2026-11-05. External source URLs are linked inline; LLM Lab's internal decisions are linked to their canonical project documents.*
