# Hugging Face LLM Course — project-level first-pass audit (2026-11-16)

## Scope and evidence boundary

**Audit depth: architecture scan + bounded Chapter 1 inspection + selected lesson-body review of Chapters 2–5 + deep content review of Chapters 10–12.** This is an initial pass within project owner issue [#765](https://github.com/JM-Brun/llm-lab/issues/765), not a claim that all course chapters have been read or that the whole Hugging Face ecosystem has been audited.

Inspected:
- Current English course index: chapters 0–12 and their published headings.
- [French Chapter 1 introduction](https://huggingface.co/learn/llm-course/fr/chapter1/1): course goals, NLP/LLM distinction, prerequisites, chapter outline and stated learning outcomes.
- Existing LLM Lab curriculum, source records, selected bilingual lessons, Build implementation inventory and prior Hugging Face work under #765.

Not yet inspected: lesson bodies and code in Chapters 2–12, notebooks, quizzes, videos, live Spaces, course exercises, Hub model/dataset cards, current library semantics, comments and learner outcomes. The upstream course is living documentation and no immutable commit was pinned in this first pass. English and French outlines differ in places (the English index currently exposes inference with LLMs and newer chapters 10–12; the supplied French Chapter 1 index has an older outline), so locale/version parity must be verified rather than assumed.

## Source-local learning model (index-level reconstruction)

| Course area | Declared role | LLM Lab crosswalk | First-pass decision |
|---|---|---|---|
| 0 Setup | Environment and prerequisites | Python and project setup; Build prerequisites | Reference only; inspect tooling and reproducibility details later |
| 1 Transformer models | NLP/LLM framing, capabilities, internal operation, encoder/decoder/seq2seq, bias and limitations; English index also lists inference | Transformer architecture, tokenization, representations, attention, generation, model limits | Strong conceptual overlap; compare explanations and misconceptions at lesson level |
| 2 Using Transformers | Apply pretrained models and pipelines | Existing model/architecture demonstrations and inference lessons | Likely complementary API workflow; inspect before integrating |
| 3 Fine-tuning a pretrained model | Dataset preparation, Trainer, training loop and learning curves | Training loop, post-training, evaluation and separate Build path | Overlap in fundamentals; likely gap in library workflow, experiment tracking and learning-curve diagnosis |
| 4 Sharing models/tokenizers | Publish artifacts to Hub | Source/resource provenance, model cards and reproducibility | Candidate practitioner reference, not core theory |
| 5 Datasets | Dataset loading, processing and scale | Corpus preparation and Build training branch | Candidate operational gap: streaming, mapping, caching, splits and dataset provenance |
| 6 Tokenizers | Tokenizer algorithms and construction | Existing tokenizer lessons, extraction and experiments | Mostly covered conceptually; inspect whether construction/API examples add distinct value |
| 7 Classical NLP tasks | Token classification, masked LM, translation, summarization, causal LM, QA | Existing architecture/task framing | Use as task exemplars; avoid turning LLM Lab into a broad NLP recipe catalogue |
| 8 Asking for help | Debugging and community workflow | Contributor and reproducibility practices | Potentially useful engineering practice, not a learner curriculum stage |
| 9 Demos | Build and share applications | Existing examples and application references | Potential optional implementation resource |
| 10 Dataset curation | Quality data for LLMs | Data quality, training and evaluation references | Priority candidate for a deeper audit; likely important underrepresented practice |
| 11 Fine-tuning LLMs | Modern LLM adaptation | Post-training, Build adaptation branch | Priority candidate: inspect methods, memory/compute trade-offs and evaluation boundaries |
| 12 Reasoning models | Build reasoning models | Existing reasoning concepts/limits and training foundations | High-value advanced gap candidate; inspect algorithm, reward/evaluation and reproducibility details |

This is a course-index crosswalk, not a verified lesson-by-lesson coverage assessment. Chapter titles indicate intended scope, not the actual depth or quality of the material.

## What LLM Lab already covers well

- A coherent bilingual conceptual route that starts with inference orientation, then input/tokenization, representations, Transformer computation, prediction, generation, context, scoring and learning.
- A distinct Build path with its own implementation dependency order; it should not be collapsed into the course's library-first sequence.
- Canonical concepts and computational graph, plus hands-on GPT implementation and tests.
- Tokenization and embeddings have substantial existing source work, including Hugging Face chapter 6 material, tokenizer algorithm comparisons and a small local embedding inspection exercise.
- Training fundamentals, post-training and experimental evaluation already have bilingual destinations.

## Provisional gaps and improvements to investigate

1. **Operational dataset engineering:** dataset provenance, streaming/large-corpus processing, deterministic splits, deduplication, filtering, quality assessment and data contamination. Distinguish these from the conceptual explanation of the training objective.
2. **Practical fine-tuning workflow:** compare Trainer/high-level abstractions with a transparent training loop; expose what is hidden by the abstraction, checkpointing, evaluation, learning curves and resource constraints.
3. **Modern LLM fine-tuning:** audit instruction tuning and parameter-efficient methods as optional Build/Deepen material, not as a new mandatory theory stage.
4. **Reasoning-model training:** investigate the actual training recipe and evidence, not just the label “reasoning”; distinguish base-model capability, post-training, inference-time search/compute and evaluation.
5. **Hub and reproducibility workflow:** model/dataset cards, pinned revisions, provenance, artifact sharing and runnable demos are practitioner skills that could be linked from existing pages.
6. **Debugging as scientific practice:** failure isolation, minimal reproductions, issue reports and experiment logs could improve Practice & experiment without creating a separate curriculum stage.

## Route-level comparison

The Hugging Face course is an ecosystem/library-oriented route: learn Transformers, use pretrained models, fine-tune, publish, work with datasets/tokenizers, solve tasks, then explore curation, LLM fine-tuning and reasoning.

LLM Lab deliberately separates:
- **Understand:** conceptual/scientific progression;
- **Build:** implementation dependency order for a small GPT;
- **Deepen:** optional advanced detail;
- **Practice & experiment:** observable tests and experiments.

Therefore, do not import the HF chapter order into `data/guided-route.yml`. Use course chapters as contextual resources attached to existing learner questions or Build milestones. New route stages require evidence of a distinct learner outcome and prerequisite relationship.

## Rights and technical qualification

Course prose, diagrams and code remain link-only. No figures, notebooks or code were copied. No licence or reuse permission was established in this scan. The course's use of Hugging Face APIs is version-sensitive; any API claim must be checked against the matching official version or source code before publication.

## Next audit increment

The deep pass on Chapters 10–12 is complete at the lesson-body level. The remaining high-value audit is Chapters 2–5 for the operational workflow, followed by Chapters 6–9 where concrete implementation examples offer distinct value. For each selected chapter: inspect lesson text, equations, code/notebooks, exercises, prerequisites, visuals and version references; record exact locators; extract atomic claims and teaching moves; compare against actual LLM Lab pages, graph, Build path and Practice activities.

## Deep chapter review — 2026-11-16

### Chapter 10 — Curate high-quality datasets (Argilla)

Inspected the chapter introduction, dataset loading/configuration, annotation workflow, export path and quiz. The chapter teaches a concrete human-in-the-loop curation workflow:
- configure fields and annotation questions to match the task;
- map existing labels as suggestions rather than treating them as unquestionable ground truth;
- write annotation guidelines and clarify edge cases;
- distribute work and request multiple independent responses where agreement analysis is useful;
- preserve draft/submitted/discarded states and filter records according to task completion;
- export annotations for downstream training/evaluation or preserve the full Argilla task configuration on the Hub.

**What LLM Lab already covers:** corpus provenance, parsing/filtering, deduplication, leakage-safe splitting, tokenizer fitting and corpus handoff in the bilingual corpus-preparation pages; experimental evaluation already covers target estimands, grouped sampling and protocol design.

**Actual gap:** explicit human annotation as a measurable stage of dataset construction. Existing corpus-preparation content did not explain annotation guidelines, calibration, independent double annotation, adjudication or the interpretation limits of inter-annotator agreement.

**Integration made:** both corpus-preparation lessons now include a bounded section on annotation protocol and traceability; both exercise pages include an active-recall question distinguishing agreement from validity. Argilla is linked as an example workflow, not presented as the canonical or universal solution.

**Limitations:** the chapter is mainly a tool-guided annotation workflow. It is not a comprehensive treatment of corpus deduplication, contamination, sampling bias, licensing, representativeness or statistical reliability. The course's default one-response completion setting should not be mistaken for a reliability protocol; multiple independent annotations are needed when agreement is an intended measurement.

### Chapter 11 — Fine-tune Large Language Models

Inspected the chapter overview, chat-template lesson, SFTTrainer lesson, LoRA lesson and evaluation lesson.

Distinct teaching contributions:
- chat templates serialize roles, messages, boundaries and control markers into model-specific token sequences;
- the course explicitly distinguishes base and instruction-tuned models;
- it recommends testing prompting with an existing instruction model before paying the compute and engineering cost of SFT;
- SFT is framed around instruction/conversation/output-format demonstrations;
- LoRA freezes base weights and trains low-rank adapter parameters;
- evaluation is treated as a necessary stage rather than an optional final score.

**What LLM Lab already covers:** the bilingual post-training lesson already explains SFT, response-only loss masking, preference methods (RLHF/DPO), parameter-efficient adaptation (LoRA) and the context-vs-parameters decision. Its exercise already tests the difference between loss masks and attention masks and the distinction between reward-model RLHF and DPO.

**Actual gap:** chat serialization was not explained, despite being a prerequisite for correctly constructing conversational SFT data. The project did not explicitly teach that templates are model-specific, part of data/tokenizer provenance, and distinct from loss masking or tool execution.

**Integration made:** both post-training lessons now explain chat templates and their relationship to SFT, tokenizer revisions, message/control markers and host-side tool execution. Both exercise pages now test template/version alignment.

**Technical qualification:** the course's short description associates LoRA with attention weights, but LoRA can target different supported modules; the chosen target modules are configuration-dependent. Its reported parameter/memory reductions are examples tied to specific configurations, not universal constants. ChatML is an example format, not a universal chat standard. API examples remain version-sensitive and were not executed.

### Chapter 12 — Build Reasoning Models (Open R1 / GRPO)

Inspected the chapter outline, RL introduction, DeepSeek R1 paper walkthrough, GRPO implementation lesson and selected algorithm details. The course sequence is pedagogically useful:
1. introduce agent, environment, action and reward;
2. read the DeepSeek R1 training recipe;
3. understand group-based relative reward/advantage construction;
4. implement a reward function and train with TRL's GRPOTrainer;
5. proceed to practical GRPO exercises.

**What LLM Lab already covers:** the bilingual glossary already defines GRPO and RLVR; the concept system includes policy-gradient, score-centering, off-policy RL, training/inference mismatch and reasoning-model concepts. Existing post-training pages explain preference learning but explicitly leave detailed algorithms outside their scope. Prior work on score-centering supplies relevant mathematical background.

**Actual gap:** GRPO did not yet have a first-class concept-registry node, and the relation between the chapter's algorithm, the policy-gradient foundation and post-training was not represented. The course also offers an accessible implementation path, but the current project deliberately does not have a dedicated practical GRPO experiment.

**Integration made:** added a bilingual GRPO concept node and graph relations to post-training and policy-gradient; glossary definitions are now cross-linked by the concept registry. No new mandatory route stage or GRPO implementation was added.

**Scientific qualifications required:**
- GRPO compares multiple sampled completions for a prompt and forms relative advantages from their rewards; in its original formulation it avoids a separate critic/value model. It does not prescribe a single reward source.
- The Hugging Face tutorial's illustrative length reward is intentionally simple and would be a poor proxy for reasoning quality if used as a real objective; reward design can create reward hacking.
- DeepSeek-R1 is a particular multi-stage recipe, not synonymous with GRPO. The published R1 pipeline includes cold-start SFT, reasoning RL, rejection sampling plus SFT, and a further RL stage. R1-Zero and R1 should not be conflated.
- The “Aha moment” is a description of an observed output/training pattern, not evidence that a model has human-like introspection or that generated chain-of-thought is a faithful report of internal computation.
- GRPO's group normalization and KL control have nontrivial trade-offs; current TRL documentation notes reward-scaling variants and potential question-difficulty bias. Library defaults and parameters evolve and must be pinned for reproducible experiments.

### Selected review of Chapters 2–5 — 2026-11-16

### Chapter 2 — Using Transformers

Inspected the chapter overview, the pipeline walkthrough and model/tokenizer sections; the chapter navigation also exposes batching and optimized inference deployment.

**Contribution:** a practical bridge from a high-level pipeline to the underlying tokenizer/model calls, model loading/configuration and batched inputs. It is useful for showing what a library abstraction does and where its model-specific components begin.

**LLM Lab coverage:** the conceptual pipeline from prompt text to tokenization, model computation, prefill/decode and token selection is already covered in bilingual canonical lessons. The project does not aim to reproduce the Transformers library API surface.

**Decision:** add the course's pipeline walkthrough and optimized-inference chapter as optional implementation references from the generation lesson. Do not create an API tutorial or duplicate the canonical generation mechanism.

### Chapter 3 — Fine-tuning a pretrained model

Inspected data processing, Trainer, custom training loop and learning-curve sections.

**Contribution:** shows the same task fine-tuning through both a high-level Trainer abstraction and a transparent PyTorch loop; exposes preprocessing, data collators, labels, optimizer steps, evaluation strategy, metrics, mixed precision, gradient accumulation, scheduling and learning curves.

**LLM Lab coverage:** the training-loop lesson already teaches the optimizer/gradient/learning-rate loop and explicitly distinguishes training from validation loss. The Build route deliberately constructs a small GPT rather than teaching the Transformers Trainer API. Post-training explains SFT and preference adaptation conceptually.

**Actual gap:** no major conceptual gap in the selected material. The distinct value is the practical API workflow and a worked interpretation of learning curves for fine-tuning a pretrained task model.

**Decision:** add the custom-loop and learning-curve sections as optional implementation references to the existing training-loop lesson. No new lesson or route stage; pin library versions before turning examples into executable project code.

### Chapter 4 — Sharing models and tokenizers

Inspected the Hub overview and model-card lesson.

**Contribution:** treats a model card as a first-class artifact documenting model description, intended use, limitations/bias, training data/procedure and evaluation results. This connects publication to reproducibility and responsible interpretation rather than merely uploading weight files.

**LLM Lab coverage:** source lineage and provenance are strong at the research/documentation level, and the Build route includes reproducible code/tests. There was no direct model-card learning reference in the Build route.

**Decision:** add the model-card lesson as an optional next-step reference from Build. Do not invent a parallel model-card schema; the project source lineage, model card and training artifact have different purposes.

### Chapter 5 — The Datasets library

Inspected the chapter introduction, data manipulation and large-dataset/memory section; the chapter outline also includes local/remote loading, dataset creation and semantic search with FAISS.

**Contribution:** practical dataset operations (mapping, filtering, slicing, selecting, formatting), loading from local and remote sources, memory-mapped datasets and streaming for large corpora, plus a semantic-search example.

**LLM Lab coverage:** corpus preparation already covers provenance, filtering, deduplication, split leakage, tokenizer fitting and the handoff contract. Embedding-space and retrieval-related lessons cover representation and similarity concepts. The project does not yet teach the Datasets library API or storage backend.

**Decision:** add selected chapter sections as optional implementation references from corpus preparation. Keep Arrow/memory mapping/streaming as implementation concepts, not mandatory additions to the conceptual route. A future runnable example should compare streaming and materialized access under a pinned Datasets version and measured memory use.


## Graph and route decisions

The course has now contributed three bounded changes:
- human annotation and label-quality protocol within the existing corpus-preparation lesson and exercise;
- model-specific chat-template serialization within the existing post-training lesson and exercise;
- GRPO as an advanced concept in the concept graph and glossary.

No new learner-facing page, top-level curriculum stage or Build dependency was added. The chapter's tools (Argilla, TRL, Unsloth) remain contextual ecosystem references. This preserves the distinction between LLM Lab's conceptual route and Hugging Face's library-oriented practice route.


## Summary

The course is valuable less as a replacement curriculum than as a **bridge from conceptual understanding to modern Hugging Face practice**. LLM Lab already has strong foundations in Transformer mechanics, tokenization, generation and training fundamentals. The most valuable validated additions are human annotation protocol, chat-template serialization and a first-class GRPO concept. Chapters 2–5 add contextual implementation references for pipelines, fine-tuning loops, learning curves, model cards and large-dataset handling. A practical GRPO experiment remains optional; Chapters 6–9 still require inspection.


## Follow-up review — Chapters 6–9 (2026-11-17)

### Scope and evidence boundary

This increment inspects the current English chapter index and selected lesson bodies from Chapters 6–9. The course remains living documentation; no immutable upstream revision was pinned. Selected code examples were read but not executed, and no learner outcomes were measured. The audit is about pedagogical transfer to LLM Lab, not a full review of every notebook, quiz, video, linked Space or current library API.

Inspected lesson bodies and outcomes:
- Chapter 6: introduction, fast-tokenizer capabilities, QA pipeline and BPE/tokenizer construction material; the chapter index also lists WordPiece and Unigram.
- Chapter 7: chapter introduction and the causal-language-model-from-scratch lesson (CodeParrot); task families include token classification, masked LM, translation, summarization, causal LM and QA.
- Chapter 8: introduction, forum-question guidance and training-pipeline debugging.
- Chapter 9: introduction and Gradio Blocks lesson; the chapter index includes Interface, sharing, Hub integration and advanced features.

### Chapter 6 — Tokenizers library

The chapter's distinct practical contribution is not the BPE/WordPiece/Unigram theory: LLM Lab already has substantial bilingual coverage of segmentation strategies, tokenizer components, Unicode, special tokens, training/evaluation trade-offs and reproducibility. The useful additional bridge is **fast-tokenizer alignment**:
- BatchEncoding exposes token strings, word_ids(), sentence_ids() and character/token conversion helpers for compatible fast tokenizers;
- offset_mapping maps token positions back to spans in the original input, enabling entity reconstruction and highlighting;
- token-level labels need explicit alignment when one word becomes several subtokens;
- extractive QA uses offsets to map predicted start/end positions to context text, and long contexts require overflow windows plus stride and careful handling of window-local versus source-global positions.

**Gap and integration:** existing tokenizer lessons did not explain offsets and their role in downstream task alignment. Added a bilingual section to tokenization-strategies.qmd with a small inspection example, a conceptual distinction between token IDs and character offsets, and caveats around special tokens, normalization, Unicode and slow-tokenizer support. The lesson links to the official fast-tokenizer and QA examples. This is an additive implementation bridge, not a new canonical algorithm lesson.

**Qualification:** offsets are implementation-provided alignment metadata, not a universal property of every tokenizer API. Do not assume the same methods or semantics for all slow tokenizers, normalizers, paired inputs or library versions. The course's speed comparison is workload-specific and is not generalized into a universal fast/slow speed claim.

### Chapter 7 — Classical NLP tasks

The chapter connects the preceding Datasets, Tokenizers, Trainer/Accelerate and Hub chapters through concrete task recipes: token classification, masked language modeling, translation, summarization, causal language modeling and question answering. Its causal-LM lesson demonstrates a from-scratch code-completion model using a filtered/streamed CodeParrot corpus and a previously trained tokenizer, then a Trainer/Accelerate workflow.

**What LLM Lab already covers:** causal next-token prediction, GPT architecture, shifted targets, loss, training loop, data preparation and evaluation foundations. It is not trying to be a broad catalogue of NLP application recipes or to reproduce a task-specific BERT/translation/summarization training cookbook.

**Disposition:** link the CodeParrot lesson as an optional applied case study from the bilingual training-loop pages. It is a useful example of how a domain-specific corpus, tokenizer, streaming and causal objective fit together, but not a replacement for LLM Lab's minimal GPT Build path. The other task recipes remain reference-only: they are useful transfer examples but do not justify adding several new task-specific curriculum pages at this stage.

**Limitations:** the course's code-generation corpus and filtering heuristics are illustrative, not a general data-quality standard. A source repository dump does not automatically imply a representative, licensed, deduplicated or contamination-free training corpus. No CodeParrot code or benchmark was executed or reproduced in this audit.

### Chapter 8 — How to ask for help

The chapter teaches transferable open-source engineering practices: read the full traceback, write a descriptive title, include environment/version details and a minimal reproducible example, format code, and avoid asking others to infer missing context. Its training-debugging lesson decomposes a high-level Trainer.train() failure into inspectable stages: dataset records, preprocessing/tokenization, dataloader/batching, model inputs/forward pass, gradients/optimizer, then evaluation/metrics. It also shows that a run can complete while producing a poor model, so debugging must include qualitative/quantitative output checks rather than only runtime errors.

**What LLM Lab already covers:** executable examples, tests, assertions, explicit expected evidence, validation and reproducibility practices are already embedded in the Build path and experiment pages. The course adds a useful checklist for diagnosing failures hidden behind high-level training abstractions.

**Disposition:** link the debugging-pipeline lesson from the bilingual training-loop pages. Do not create a separate learner stage: debugging is a cross-cutting scientific and engineering practice. The broader advice on issue writing can inform future contributor templates, but no repository-wide template change is made in this increment.

### Chapter 9 — Building and sharing demos

The chapter introduces Gradio's high-level Interface for simple input/output applications and the lower-level Blocks API for custom layout, event-driven functions, stateful or multi-step data flow and conditional UI behavior. It frames demos as communication and testing surfaces: they can help non-specialists inspect model behavior, reproduce examples, surface failure modes and discover potential biases. It also connects demos to Hub Spaces and sharing.

**What LLM Lab already covers:** the project has interactive conceptual visualizations and a small GPT reference implementation, but its Build path explicitly distinguishes working inference mechanics from the still-incomplete end-to-end data/training/evaluation pipeline. A public-facing demo could falsely suggest a trained or production-ready model where none exists.

**Disposition:** defer a direct Gradio integration. No Gradio app or Space is added, and no mandatory route milestone is proposed. Revisit once there is a clearly scoped, trained artifact or a deliberately pedagogical toy app, with visible model status, limitations, reproducibility information and user-input safeguards. The official course is kept as an optional reference in this review.

### Cross-chapter synthesis and decisions

| Chapter | Actual incremental value for LLM Lab | Decision |
|---|---|---|
| 6 — Tokenizers | Offsets, word/token alignment and overflow-to-source mapping | Integrate bilingual explanation; keep library APIs optional |
| 7 — NLP tasks | End-to-end CodeParrot causal-LM case study; task transfer examples | Link CodeParrot from training-loop; no new task catalogue |
| 8 — Help/debugging | Stage-by-stage diagnosis of hidden pipeline failures and better reproductions | Link debugging workflow; no new route stage |
| 9 — Demos | Interface/Blocks/Spaces patterns and demos as inspection surfaces | Defer until LLM Lab has an artifact whose status can be represented honestly |

No chapter order is imported into the canonical learning route. No source code, figures or prose from the course are copied. Hugging Face API claims remain version-sensitive and links are references, not executed implementation guidance.

### Updated remaining scope

Chapters 2–9 now have selected lesson-body review; Chapters 10–12 have deep lesson-text review. Chapters 0–1 were inspected at overview/introduction level. Remaining work, if a deeper audit is warranted, is to inspect selected Chapters 2–5 implementation details and notebooks, compare the French and English course variants systematically, pin an upstream revision, and execute any API example before turning it into maintained project code.
