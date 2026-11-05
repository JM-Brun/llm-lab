# Comparative audit of LLM learning paths: Raschka, Hugging Face and LLM Lab

**Audit date:** 2026-11-05  
**Purpose:** record the external curriculum comparison referenced by [#225](https://github.com/JM-Brun/llm-lab/issues/225), and make explicit which design principles are transferable to LLM Lab.  
**Scope:** public curriculum structure and stated learning activities, not a full evaluation of lesson quality or learner outcomes. The two external courses evolve; this is a dated snapshot.

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
- [Narrative learning path](learning-path.md)
- [Full curriculum and coverage plan](full-curriculum-plan.md)
- [Reader-experience and editorial method](reader-experience-and-editorial-method.md)
- [Content ownership map](content-section-mapping.md)
- [2026-11-05 route reconciliation](learning-route-reconciliation-2026-11-05.md)

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

The current LLM Lab architecture is consistent with the transferable principles above. The route reconciliation in [the 2026-11-05 audit](learning-route-reconciliation-2026-11-05.md) records the correspondence between conceptual curriculum, guided route, Build milestones, Quarto navigation and graph projections.

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
