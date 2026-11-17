# Jose Parreño Garcia — How LLMs Work (Part 1): The 3 Essential Layers

**Source:** [LLMs explained (Part 1): The 3-layer framework behind chatGPT & friends](https://joseparreogarcia.substack.com/p/how-llms-work-part-1-the-3-essential-layers)  
**Author:** Jose Parreño Garcia · **Publisher/date:** Senior Data Science Lead (Substack), 5 April 2025  
**Inspection:** 17 November 2026 · complete visible article body and two embedded images  
**Structured extraction:** [YAML extraction](../../data/extractions/jose-parreno-garcia-how-llms-work-three-layers-2025.yml)

## 1. Executive assessment

The article is a useful introductory bridge from classical predictive modelling to LLM construction. Its central three-stage frame—collect data, train a base model, adapt it—gives beginners a memorable orientation. It is not a sufficiently precise technical model to replace LLM Lab's existing learning path.

**Decision: retain as an optional introductory reference; integrate by reference only.** No new lesson, concept, diagram or canonical route node is justified. The bilingual overview, text-data, training-loop, post-training and limits lessons already cover the useful distinctions more precisely.

The strongest teaching move is the contrast between a plausible continuation and an exact continuation of a known speech. The weakest move is turning a legitimate distinction between next-token prediction and truth into categorical claims that LLMs cannot reason or understand, and that fine-tuning makes them knowledgeable and truthful.

## 2. Inspection scope and provenance

- Complete visible author-authored body: introduction, classical ML analogy, three LLM stages, data collection, base-model description, fine-tuning comparison and takeaways.
- Visible outline of the planned series, which announces six parts. Parts 2–6 are signposted as forthcoming; their contents are not treated as inspected.
- Both embedded images: (a) screenshot comparing a Llama 3 8B base-model continuation with Churchill's original speech, and (b) short human/assistant dialogue example.
- Article metadata and visible discussion area.

The embedded Karpathy video was not watched. Outbound links to Common Crawl, FineWeb, nanoGPT architecture and other resources were identified but not systematically audited. The visible ATLAS/ACDQ reader comment is not author-authored material and is not included as evidence. Text and image reuse rights remain unknown; no asset is copied.

## 3. Reconstructed three-stage model

| Stage | What it contributes | What it leaves out |
|---|---|---|
| 1. Collect text data | Web-scale sources, extraction/formatting problems and corpus cleaning | Provenance, licensing, deduplication, filtering, contamination, language balance, quality evaluation and governance |
| 2. Train a base model | Tokenization, large neural network, compute scale and next-word prediction | Tokenizer training, architecture, objective formalization, optimization, validation, scaling trade-offs and evaluation |
| 3. Improve through fine-tuning | Conversation-like examples, behavioural shaping and guardrails | SFT versus preference optimization/RL, data construction, reward signals, evaluation, safety testing, retrieval and tool-use boundaries |

The source-local graph and teaching route are preserved in the extraction. They are not copied into the canonical concept graph or learner routes.

## 4. Technical assessment

### Claims that are useful and broadly correct

- **Data curation matters.** Web text is not a ready-made training corpus. Extraction, normalization, filtering and quality control are substantial processes.
- **A GPT-like base model is trained autoregressively.** The article's “next word” should be read as next **token**: tokens need not align with whole words.
- **The base-model objective does not directly optimize truthfulness or helpful assistant behaviour.** Plausible continuation and factual correctness are different properties.
- **Post-training changes behaviour.** Instruction demonstrations and preference-based signals can make a model more likely to follow instructions and produce conversational responses.
- **Post-training does not eliminate hallucinations.** The author acknowledges that the example fine-tuned model can still hallucinate.

### Claims that need correction or qualification

1. **“The entire internet” is not a realistic or sufficient data strategy.** Corpus construction involves source selection, rights, quality, deduplication, safety, language coverage, contamination and governance. More text is not automatically better.
2. **“Next word” is imprecise.** A GPT predicts tokens from its tokenizer vocabulary, conditioned on context; a token is not necessarily a whole word.
3. **“The goal is to sound coherent” is incomplete.** The formal pretraining objective is to improve likelihood of observed next tokens under the training distribution. Coherence may emerge, but is neither the complete formal objective nor a truth guarantee.
4. **“Base models are mostly useless” is task-dependent rhetoric.** Base models can be useful for continuation, completion and scoring; instruction-following is a different behavioural target.
5. **Fine-tuning does not make a model truthful.** SFT and preference optimization shape response behaviour. They do not guarantee factuality, calibration or resistance to hallucination.
6. **Guardrails are not a truth mechanism.** They can constrain or route behaviour, but reliability depends on design, coverage, evidence access and evaluation.
7. **The claim that LLMs have no reasoning or comprehension is too categorical.** Next-token training does not settle whether a model can perform reasoning-like tasks, what mechanisms support those performances, whether it is grounded, or whether it has human-like understanding. These are distinct empirical and philosophical questions requiring operational definitions.
8. **The model comparison is not causal evidence.** The article contrasts Llama 3 8B base with DeepSeek R1 14B. Model family, parameter count, training history, post-training, prompting and inference settings differ. Without a controlled comparison, the difference cannot be attributed to fine-tuning alone.

## 5. Visual assessment

Both images were opened and inspected.

- **Churchill continuation screenshot:** useful as an anecdotal illustration of a model continuing a familiar text plausibly and then diverging from the source. It is not a benchmark, controlled experiment or evidence about reasoning.
- **Short dialogue screenshot:** illustrates conversational style but does not explain the training process or establish factual reliability.

Neither image adds a distinctive mechanism that justifies reproduction. Keep both link-only; do not copy or trace them without rights clearance. A project-owned diagram should be built from LLM Lab's existing distinctions among pretraining, post-training and inference, not by redrawing these screenshots.

## 6. Relationship to LLM Lab

| Article contribution | Canonical destination | Integration decision |
|---|---|---|
| Three-stage construction frame | [LLM overview](../../site/fr/llm-overview.qmd) / [English overview](../../site/en/llm-overview.qmd) | Already covered more precisely; retain article as optional reference |
| Web corpus collection and cleaning | Text-data lessons | Already covered; no duplicate page |
| Tokenization and next-token prediction | Text-data, tokenization, training-loop and LLM overview | Already covered with token-level precision |
| Base model versus assistant | [Post-training](../../site/fr/post-training.qmd) / [English post-training](../../site/en/post-training.qmd) | Already covered, including SFT, preference methods, prompting and retrieval |
| Truth, hallucination and reasoning claims | LLM limits and evaluation lessons | Existing distinctions resolve the main omissions; no new concept |
| Tools and reinforcement learning | Generation and post-training | Series only announces these topics; ingest later parts separately if published |

The canonical pages already distinguish architecture, learning and use; next-token prediction from truth; and parameter updates from context changes. No bilingual page edit is necessary for this source.

## 7. Source-local learning graph and route

The extraction records the author's graph and teaching route: (1) classical ML data → baseline model → improvement; (2) map the analogy to LLM construction; (3) explain corpus collection; (4) introduce tokenization and next-token prediction; (5) contrast base-model continuation with conversation-oriented adaptation.

This is an explanatory route, not a complete engineering lifecycle. It remains distinct from LLM Lab's Understand, Build, Deepen and Practice & experiment routes.

## 8. Final disposition and open work

- Keep the article in the source catalogue and bibliography as an introductory secondary source.
- Preserve its atomic claims and critical qualifications in the extraction.
- Add no concepts: all relevant canonical concepts already exist.
- Do not edit the bilingual overview or post-training lessons: their current explanations already resolve the main omissions and misconceptions.
- Do not create a synthesis dossier for a single source.
- Revisit Parts 2–6 only when the actual articles are available; do not infer their contents from their titles.
- Keep screenshots and article text link-only pending rights evidence.

**Overall judgement:** pedagogically accessible and useful as an orientation, but technically compressed. Its three-stage frame is a mnemonic, not a model specification; its claims about truthfulness and reasoning need substantial qualification.
