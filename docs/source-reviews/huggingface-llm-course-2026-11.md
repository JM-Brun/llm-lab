# Hugging Face LLM Course — project-level first-pass audit (2026-11-16)

## Scope and evidence boundary

**Audit depth: architecture scan + bounded Chapter 1 inspection.** This is an initial pass within project owner issue [#765](https://github.com/JM-Brun/llm-lab/issues/765), not a claim that all course chapters have been read or that the whole Hugging Face ecosystem has been audited.

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

Prioritize a representative deep audit of Chapters 10, 11 and 12 (dataset curation, LLM fine-tuning, reasoning models), then Chapters 2–5 for the operational workflow. For each selected chapter: inspect lesson text, equations, code/notebooks, exercises, prerequisites, visuals and version references; record exact locators; extract atomic claims and teaching moves; compare against actual LLM Lab pages, graph, Build path and Practice activities. Only then decide whether to update a canonical lesson, add an optional resource, create an experiment, or record an intentional no-op.

## Summary

The course is valuable less as a replacement curriculum than as a **bridge from conceptual understanding to modern Hugging Face practice**. LLM Lab already has strong foundations in Transformer mechanics, tokenization, generation and training fundamentals. The most promising additions to investigate are dataset curation, real-world fine-tuning workflows, Hub/reproducibility practice and reasoning-model construction. These remain provisional until their chapter bodies and implementations are inspected.
