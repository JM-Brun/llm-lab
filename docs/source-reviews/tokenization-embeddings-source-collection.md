# Tokenization and embeddings — cross-source synthesis

**Status:** living source collection · **Review date:** 2026-11-05  
**Catalogue:** [data/sources.yml](../../data/sources.yml)  
**Migration map:** [Tokenization and embeddings source migration map](tokenization-embeddings-source-migration-map-2026-11.md)  
**Method transfer assessment:** [Source-to-knowledge method transfer validation](../source-syntheses/tokenization-embeddings-method-transfer-validation-2026-11.md)  
**Owning issue:** [#458](https://github.com/JM-Brun/llm-lab/issues/458)

## 1. Purpose and evidence boundary

This dossier compares the source families already audited in #114, #147, #82 and #96. It is a synthesis of prior work, not a new exhaustive review of tokenization or embedding research.

The source catalogue contains **48 records in the 2026-11-05 transfer-pilot branch**: four Q/K/V and KV-cache records (including Codefinity) plus **44 tokenization/embeddings-related records**, including the newly registered TokCollate paper. The pre-pilot `main` baseline contains 47 records (four Q/K/V/KV-cache plus 43 tokenization/embeddings records). The registry distinguishes papers, documentation, repositories, videos, courses and articles. A record's existence does not mean every component was scanned.

The source set is selected because it was already cited, inspected or used in the project. It is not a representative sample of all tokenizer research, embedding research or educational resources.

### Scan boundaries that must remain visible

- Karpathy's tokenizer video was reviewed through public chapter markers and a third-party rendered transcript; the full audiovisual work was not watched.
- The Hugging Face course audit covers relevant BPE, WordPiece, Unigram and construction sections, not the entire course.
- Ahia, Wegmann and some other research sources were reviewed at abstract/metadata level; do not imply full-paper methodology review where the source audit says otherwise.
- Ali, Arnett, Ethayarajh, Li and Steck have more detailed primary-source reviews recorded in #114; preserve each paper's own model, task, corpus and experimental boundaries.
- Sentence Transformers, Hugging Face and PyTorch documentation are living resources. Their inspected pages were not pinned to immutable documentation revisions unless explicitly recorded.
- The Rushang Chauhan image, Arnett/Petrov/Hugging Face figures and other embedded assets remain under the site-wide rights workflow in #156. Attribution and repository-level licences are not substitutes for asset-level permission.
- The two ByteByteGo articles and two Vizuara course resources now have explicit canonical URLs in the catalogue. This does not imply that their full sites/courses were scanned. A potentially separate Vizuara embeddings resource remains unresolved; do not create a guessed record.

## 2. Source families and their distinct roles

| Family | Representative records | What the sources contribute | What they do not establish |
|---|---|---|---|
| Tokenizer construction and encoding | Karpathy video; Raschka Ch. 2; Hugging Face course; Gage; Sennrich; tiktoken; minbpe; HF Tokenizers; SentencePiece | Unicode/bytes distinctions, vocabulary and IDs, BPE training vs encoding, pre-tokenization, algorithm families, special-token handling and practical implementation boundaries | One universal tokenizer pipeline, equivalence between all BPE variants, or complete production compatibility from a toy example |
| Corpus preparation | Raschka Ch. 2; ByteByteGo resources (historical review); canonical LLM Lab corpus pages | Document-level collection/filtering/deduplication, evaluation-aware partitions, tokenizer fitting, encoding and training-example hand-off | A single fixed order suitable for every corpus or a guarantee that deduplication alone prevents leakage |
| Multilingual tokenizer evaluation | Ahia; Ali; Wegmann; Arnett 2025; TokLens; Catherine Arnett 2024 | Language-dependent token costs, token premium/fertility/parity measures, tokenizer design trade-offs, experimental effects and evaluation caveats | A universal tokenizer ranking, a causal account of every language disparity, or a guarantee that lower token count improves downstream quality |
| Token and contextualized embeddings | Mikolov; Ethayarajh; Rushang Chauhan; Raschka Ch. 2 | Static word-type vectors vs token lookup vectors, and why contextual states can vary by context even when the token ID is fixed | Equivalence between Word2Vec and Transformer embeddings, or proof that a particular attention head performs a linguistic task |
| Sentence embeddings and geometry | Li et al.; Steck et al.; Sentence Transformers documentation | Anisotropy, sentence-level pooling/geometry, limits of raw cosine similarity, metric choice and model/API-specific behavior | Universal conclusions about every embedding model or a claim that cosine similarity directly measures semantic similarity |
| Interactive and visual learning | Hugging Face BPE visualizer; Polo Club Transformer Explainer; Vizuara pedagogical review | Manipulable views, question-led exploration, source-code cross-checks and interactive forward-pass observation | Faithful production-tokenizer execution from every visualizer, generalization from GPT-2 small to all LLMs, or learning outcomes for LLM Lab without a separate study |

## 3. Cross-source synthesis by learner question

### 3.1 What is a token, and what is the tokenizer actually doing?

**Convergence.** Karpathy, Raschka, Hugging Face and the implementation repositories all support the separation between raw text representation, tokenizer preprocessing, token vocabulary/IDs and model input. The project's distinction between Unicode code points, UTF-8 bytes, token strings and token IDs is necessary: they are different representations, not interchangeable names for the same object.

**Complementarity.**
- Karpathy's transcript-based walkthrough contributes a byte-level, implementation-oriented narrative.
- Raschka provides a compact build-from-scratch route and a concrete notebook structure.
- Hugging Face's course provides a broader comparison of BPE, WordPiece and Unigram.
- The tiktoken educational module and minbpe make algorithm steps inspectable.
- SentencePiece highlights raw-Unicode input, whitespace handling and the fact that a tokenizer library may support more than one algorithm family.

**Qualification.** Gage's 1994 algorithm is byte-pair compression. NLP subword BPE adapts the pair-merging idea to vocabulary construction and token encoding; GPT-style byte-level BPE adds tokenizer-specific conventions. The three should not be described as the same algorithm unchanged.

**Project decision.** Keep the existing division: high-level text-data overview, dedicated tokenizer-strategies deep dive, Unicode page and separate implementation examples. Do not duplicate the BPE implementation or turn the overview into a library catalogue.

### 3.2 What belongs to corpus preparation, and what belongs to tokenization?

The historical ByteByteGo/Vizuara review and the canonical corpus lesson support a useful boundary:

- Corpus-level operations act on documents or dataset partitions: collection, provenance, parsing, filtering, deduplication and split design.
- Tokenizer-level operations transform text according to a tokenizer configuration: normalization, pre-tokenization, model-specific segmentation, post-processing and decoding.
- Tokenizer fitting is a learned step and must respect evaluation boundaries; held-out text must not leak into a learned vocabulary when the goal is an unbiased held-out evaluation.
- Training examples are a later stage: sequence windows, shifted targets, packing and masks belong to their own lesson.

Deduplication and splitting interact. The project correctly avoids prescribing a universal order and explains why chunks or near-duplicates from one source should not be distributed naively across partitions.

**Project decision.** The bilingual text-data pipeline added in PR #148 is the canonical treatment. The migration adds source traceability, not another pipeline page.

### 3.3 How should tokenizer quality be measured across languages?

The studies do not measure one interchangeable quantity.

| Study | Scope and contribution | Boundary to preserve |
|---|---|---|
| Ahia et al. (2023) | Tokenization cost/utility across 22 languages in commercial API settings | Results belong to the evaluated APIs and benchmarks; they are not timeless properties of all models |
| Ali et al. (2024) | 24 tokenizer configurations and decoder-only models at 2.6B scale; tokenizer choice affected results in the studied training/evaluation setup | Five European languages, one seed, uneven task counts and protocol-specific compute estimates |
| Wegmann et al. (2025) | Task sensitivity to language variation and tokenizer/pre-tokenizer design | Reported pre-tokenizer effect is scoped to BERT-base experiments |
| Arnett et al. (2025) | ~7,000 monolingual tokenizers across 97 languages; token premiums, vocabulary and pre-tokenization effects | No language model was trained; compression results do not establish downstream LM quality |
| TokLens (2026) | Six intrinsic metrics and comparisons across tokenizer configurations/languages | Correlations are not causal evidence; intrinsic metrics and MMLU-ProX use different sample subsets |
| Catherine Arnett (2024) | A pedagogical/community article about tokenizer recycling and fertility | Article experiments are not a universal tokenizer ranking; figure rights are a separate question |

**Synthesis.** Tokenizer design can affect sequence length, cost and downstream performance in particular conditions. Yet fertility, parity, token count and compression do not collapse into a universal measure of quality. Intrinsic metrics may fail to predict downstream results, and a shorter sequence is not by itself evidence of a better model.

**Project decision.** Keep numerical study details and caveats in the advanced tokenizer-design deep dive. Keep the essential path focused on what tokenization does and why it matters.

### 3.4 What does “embedding” mean at different stages?

Mikolov et al. provide historical context for static word-type vectors learned from local context. A Transformer begins with an embedding lookup indexed by token ID, then transforms these vectors through layers into contextualized hidden states.

Ethayarajh's study helps explain context dependence and anisotropy in the specific ELMo/BERT/GPT-2 models evaluated. It does not imply that every model/layer behaves identically. The Rushang Chauhan article offers a high-level visual bridge across the pipeline, but the image's reuse rights remain unresolved in #156.

**Project decision.** The static-vs-contextualized distinction is already integrated in PR #152 and the bilingual embedding/contextualization pages. No second embeddings overview is justified.

### 3.5 What can cosine similarity tell us about embedding geometry?

The source set provides three complementary cautions:

1. **Ethayarajh (2019):** anisotropy affects interpretation of cosine similarity between contextualized occurrences; the study uses layer- and measure-specific baselines.
2. **Li et al. (2020):** BERT sentence embeddings can be anisotropic in the studied setup; BERT-flow is a particular post-hoc transformation, with a transductive target-split caveat.
3. **Steck et al. (2024):** cosine similarity can be non-unique under specified regularized linear factorization/autoencoder objectives; the analytic result is not a theorem about all deep LLM embeddings.

Sentence Transformers documentation further shows that cosine is not the only available metric; dot product, Euclidean and Manhattan options exist, and normalized embeddings can make dot product operationally equivalent to cosine.

**Project decision.** The current cosine-similarity page is appropriately bounded. Do not convert it into an exhaustive API catalogue or imply that a cosine score is a semantic truth value.

### 3.6 What do interactive visualizers really show?

The Hugging Face community BPE visualizer is useful as a schematic of merge operations, but its inspected implementation does not reproduce the full tokenizer pipeline (normalizer, pre-tokenizer, byte-level mapping and post-processing). It should not be treated as a faithful GPT-2 token-boundary trace.

Polo Club's Transformer Explainer offers a different and stronger complement: an interactive GPT-2-small forward pass with source files mapped to visible stages. The code audit also exposed a top-p implementation that truncates logits to the top 50 before computing cumulative probability. This is a useful implementation lesson, not an exact implementation of full-vocabulary nucleus sampling.

**Project decision.** Keep the visualizers optional and critically annotated. LLM Lab's own equations, Python examples and tests remain the source of truth for its canonical explanations.

## 4. Source routes versus LLM Lab's learner route

The source set offers several local teaching sequences, but these should not be concatenated into one mega-course.

| Learning function | Source perspectives | Canonical LLM Lab treatment | Curriculum decision |
|---|---|---|---|
| Understand text representation | Karpathy, Raschka, Hugging Face | text-data → Unicode text → tokenization strategies | Keep the overview short; send byte/Unicode detail to the dedicated page |
| Understand tokenizer construction | BPE, WordPiece, Unigram, tiktoken, minbpe, SentencePiece | tokenizer strategies + reproducible examples | Keep algorithm comparison in deep dive; no second implementation |
| Understand corpus preparation | ByteByteGo review, Raschka, corpus lesson | text-data → training examples | Keep document-level preparation separate from tokenizer internals |
| Understand token embeddings | Mikolov historical contrast, Raschka implementation | embedding-space | Explain lookup and dimensions without adding Word2Vec implementation |
| Understand contextualization | Ethayarajh, Rushang visual, Polo Club interaction | contextualized-representations → attention mechanisms | Keep the same token ID / different context explanation and causal caveats |
| Evaluate embedding similarity | Li, Steck, Sentence Transformers | cosine-similarity | Preserve model/task scope; do not teach cosine as universal semantic similarity |
| Evaluate tokenizer quality | Ahia, Ali, Wegmann, Arnett, TokLens | tokenizer-design-evaluation | Keep advanced research synthesis optional; no essential-path expansion |

The canonical route remains: text and corpus → tokenizer → token IDs → embedding lookup → positional information → contextualized hidden states. The project concept graph records semantic identities and relations; the source-local graphs/routes remain editorial reconstructions. Neither is a replacement for the other.

## 5. Integration decisions

| Contribution | Decision | Rationale |
|---|---|---|
| More ByteByteGo examples for whitespace, case, numbers, Unicode, multilingual text and code | already-covered | Existing EN/FR contrastive mini-lab has reproducible, version-qualified prompts |
| Vizuara question-led micro-lesson | already-covered / integrate-by-reference | Existing question-led mini-lab, BPE merge trace and optional interactive visualizer provide the useful teaching form |
| Second BPE implementation | reject for current scope | Would duplicate the trace and add maintenance without a demonstrated learning gap |
| Gage vs NLP BPE distinction | integrated | A concise bilingual historical note is present via PR #155 |
| Static Word2Vec vs Transformer embeddings | integrated | Existing bilingual embedding-space lesson via PR #152 |
| Special-token API allow-list and untrusted-input caveat | integrated | Existing bilingual tokenizer lesson via PR #151 |
| Multilingual tokenizer evaluation protocols and limitations | integrated | Advanced bilingual deep dive updated via PR #326/#332 |
| Embedding geometry and metric caveats | integrated | Existing cosine-similarity and contextualization pages reconciled via PR #333 |
| Hugging Face visualizer limitations | integrated by reference | Optional external resource is qualified via PR #168 |
| Polo Club interactive forward-pass and top-p caveat | integrated by reference | Interactive companion is source-audited via PR #186/#188 |
| Byte-level production tokenizer implementation | defer | Not required by current conceptual path; only add if a concrete Build milestone requires it |
| Negative sampling, detailed pooling, API catalogues | defer | Optional depth, not a prerequisite for the current GPT build path |
| Multimodal tokenization | defer | Outside the current text-only learning slice |

## 6. Canonical project impact

- **Concept graph:** no new concept IDs proposed by this migration. Existing token, token-embedding, contextualized-representation and positional-encoding nodes cover the stable concepts represented here.
- **Source graph:** source-local graphs and pedagogical routes are not yet backfilled for all sources; create them only for instructional sources where prior evidence contains enough structure.
- **Pages:** no new learner-facing page edits are proposed by this dossier.
- **Learning routes:** no route or prerequisite change is justified.
- **Exercises/experiments:** existing contrastive tokenization mini-lab, BPE trace and implementation examples remain the canonical practical activities.
- **Build/implementation:** no new tokenizer implementation is proposed.
- **Visual assets:** no asset was added, removed, replaced or modified. Rights remain with #156.
- **New pages:** none.

## 7. Provenance, validation and open work

### Existing integration evidence

- #146 — text → token pipeline and contextualized-representation companion pages.
- #148 — corpus preparation pipeline.
- #149 — tokenizer pre-processing comparisons.
- #151 — special-token handling.
- #152 — static Word2Vec vs Transformer embeddings.
- #155 — compression BPE vs NLP subword BPE vs byte-level BPE.
- #168 — community BPE visualizer implementation caveats.
- #172/#173 — Raschka Chapter 2 and Hugging Face course coverage audits.
- #186/#188 — Polo Club Transformer Explainer integration and top-p implementation caveat.
- #326/#332/#333 — TokLens and tokenizer/embedding research-source reconciliation.
- #147 — completed pedagogical comparison of Vizuara and ByteByteGo.

These are evidence pointers, not substitutes for inspecting the final repository state. PR merge state and CI evidence should be rechecked before this dossier is declared complete.

### Structured extraction progress — 2026-11-05

Five primary research papers now have source-scoped atomic extraction records, based on direct inspection of their published PDFs:

- [Ali et al. (2024)](../../data/extractions/ali-tokenizer-choice-llm-training-2024.yml): five items covering intrinsic versus extrinsic evaluation, controlled decoder-only comparison, downstream effects, the limits of fertility/parity as proxies, and the scope of the training-compute estimate.
- [Wegmann et al. (2025)](../../data/extractions/wegmann-tokenization-language-variation-2025.yml): five items covering task-dependent robustness versus sensitivity to linguistic variation, pre-tokenizer boundaries, task-sensitive results, a task-aware proxy, and the paper's within-English scope.

**Why these two are complementary rather than duplicates.** Ali et al. evaluates tokenizer configurations across languages and measures their effects on decoder-only LMs. Wegmann et al. asks a different question: whether tokenization should preserve or suppress *within-language* variation depending on the downstream task's label semantics. The former informs multilingual efficiency and model-training trade-offs; the latter connects tokenizer design to task objectives and linguistic form. These are separate evaluation axes and should not be collapsed into a single “tokenizer fairness” claim.

- [Ethayarajh (2019)](../../data/extractions/ethayarajh-contextualized-representations-2019.yml): four items covering contextuality measures, anisotropy-adjusted baselines, layer-wise findings and the MEV bound.
- [Li et al. (2020)](../../data/extractions/li-bert-flow-sentence-embeddings-2020.yml): four items distinguishing sentence-level BERT embeddings, anisotropic geometry, BERT-flow and the target-distribution adaptation caveat.
- [Steck et al. (2024)](../../data/extractions/steck-cosine-similarity-embeddings-2024.yml): four items covering regularization-dependent geometry, non-uniqueness, uniqueness without semantic validity, and the simulated-data boundary.

**Why these three are complementary rather than duplicates.** Ethayarajh studies contextualized *word/token occurrences* across layers and defines measures that separate context-specificity from anisotropy. Li studies pooled *sentence embeddings* from BERT and proposes a particular normalizing-flow calibration. Steck gives an analytical counterexample in *regularized linear matrix-factorization models*, showing that learned cosine geometry can depend on the training objective. Together they distinguish three different levels of analysis—contextual token representations, sentence-vector distributions and objective-induced embedding geometry. None establishes a universal property of all current LLM embeddings.

**Integration decision.** Both records map to existing bilingual advanced content. No new concept, page, figure, exercise or route step is justified. The value of this backfill is inspectable evidence, explicit scope boundaries and a reusable basis for future comparisons—not more learner-facing prose.

**Evidence boundary.** The papers' main text and relevant tables/figures were inspected. Code, raw data, supplementary material and independent reproduction were not. Both source records therefore remain partially scanned; the extraction files do not imply complete source audits.

### Structured extraction progress — second research backfill

Two further primary papers have now been converted into source-scoped extraction records, bringing the collection to **eight structured extractions** (Karpathy plus seven research papers).

- [Arnett et al. (2025)](../../data/extractions/arnett-explaining-mitigating-crosslingual-tokenizer-inequities-2025.yml): five atomic items covering token premium/CTC measurement, controlled monolingual tokenizer design, language-feature and whitespace effects, language-specific vocabulary sizing, and SuperBPE with its measured-versus-estimated boundaries.
- [Chiu (2026), TokLens](../../data/extractions/chiu-toklens-acl-srw-2026.yml): six atomic items covering the six intrinsic metrics, benchmark/sample design, the English null result, multilingual mixed-effects associations, the Qwen2.5 family analysis, and complementarity with Qtok.

**The three multilingual studies now form a useful evaluation matrix rather than one undifferentiated “fairness” topic.**

| Study | Primary unit / design | What it can support | What it cannot support |
|---|---|---|---|
| Ali et al. (2024) | Controlled decoder-only LM training under selected tokenizer configurations | Downstream effects under a matched training-compute design | A universal tokenizer ranking across languages and tasks |
| Arnett et al. (2025) | Approximately 7,000 monolingual tokenizers across 97 languages; CTC on parallel FLORES text | Language-linked compression differences and tokenizer-design interventions | Downstream LM quality: no LMs were trained with these tokenizers |
| Wegmann et al. (2025) | Within-English linguistic variation and task-dependent sensitivity | Why tokenization should be evaluated against label semantics and task objective | Crosslingual inequity or multilingual compression claims |
| TokLens (Chiu, 2026) | 24 existing tokenizers across 15 languages, then smaller benchmark-overlap analyses | A multi-metric audit framework and scoped observational associations with multilingual scores | Causal attribution to tokenizer quality independent of pretraining data |

**A particularly important metric distinction:** Arnett et al. use corpus token count on parallel FLORES material to compare content-matched compression; TokLens parity uses tokens-per-character on native, non-parallel Wikipedia corpora with a shared character budget. Their denominators and corpus designs differ. They should not be merged into one parity statistic. TokLens fertility/STRR also use whitespace units, which are not linguistic words for Chinese, Japanese and Thai. The detailed extraction records preserve these protocol boundaries.

**Integration decision.** No new canonical concept, learner-facing page, visual asset or route step is proposed. The advanced tokenizer-evaluation lesson already contains the relevant high-level findings. The added value is a machine-readable evidence layer that makes protocols, denominators, results and limitations directly comparable. In particular:
- Arnett's optimal-vocabulary result counters the simplistic assumption that uniformly increasing vocabulary size removes crosslingual token premiums.
- Arnett's SuperBPE results are not equivalent to a proven downstream-model improvement; the paper did not train LMs and some optimal-SuperBPE results are estimated rather than trained.
- TokLens' English benchmark null result and multilingual associations are not contradictory: they concern different benchmark/language subsets, with different statistical power and controls.
- TokLens and Qtok are complementary at different levels: corpus-run output metrics versus vocabulary-entry composition/allocation.

**Evidence boundary.** The published PDFs and selected figures/tables/appendices were inspected. The TokLens repository README and Arnett's linked project destination were identified, but code, raw data and tokenizer artifacts were not executed or independently audited. Both sources remain partially scanned.

### Structured extraction progress — API cost and accessibility perspective

- [Ahia et al. (2023)](../../data/extractions/ahia-do-all-languages-cost-the-same-2023.yml): six atomic items covering token-count billing, controlled byte-level BPE comparisons, estimated API cost disparities, context-window/few-shot utility, socio-economic correlations and reproducibility limits.

**Why this source adds a distinct perspective.** The previous studies primarily measure tokenizer compression, linguistic-form sensitivity or statistical associations with benchmark performance. Ahia et al. traces tokenization to the *user-facing consequences* of a fixed per-token API: higher token counts can increase historical API usage costs and reduce the number of in-context examples or the amount of source text that fits in a fixed context window. It also relates language-level cost and utility patterns to country-level HDI proxies.

This contribution should be used with strict boundaries:
- The reported cost ratios are based on 2023 model/API conditions and are not current price estimates.
- The context-window experiment is tied to historical ChatGPT and BLOOMZ API limits; BLOOMZ's weak few-shot behaviour and truncation are separate confounds.
- The socio-economic analysis is ecological: a country-level HDI proxy is associated with language-level observations, not evidence about every individual speaker or a causal effect.
- FLORES-200 is translated text; the paper uses CC100 as a proxy for unavailable ChatGPT training-language statistics.

**Integration decision.** This adds a meaningful social-accessibility lens to the source compilation, but no new canonical concept or learner route is required. The existing advanced tokenizer-evaluation page is the appropriate reference point. A future optional lab could combine parallel text, a tokenizer, a fixed context budget and a per-token price assumption to let learners quantify how sequence length propagates into cost and few-shot capacity; that is a candidate experiment, not an approved page change.

**Evidence boundary.** The full main paper and main figures/tables were inspected. The linked repository, raw evaluation data and API/model snapshots were not independently audited or executed. The source remains partially scanned.

### Structured extraction progress — static word-vector foundations

- [Mikolov et al. (2013)](../../data/extractions/mikolov-word2vec-2013.yml): five atomic items covering the log-linear architecture, CBOW, Skip-gram, hierarchical softmax and the limits of the analogy benchmark.

**Why this source remains useful despite the existing lesson.** The bilingual embedding-space page already explains the essential static-versus-contextual distinction and gives the CBOW/Skip-gram mental models. The source extraction preserves additional historical details without duplicating that learner-facing explanation:
- CBOW averages shared context projections and predicts the middle word; the original experiment uses both left and right context.
- Skip-gram predicts surrounding words from a centre word and samples a variable context radius.
- The inspected paper describes hierarchical softmax with a Huffman tree. It should not be casually described as the negative-sampling paper: negative sampling is associated with later word2vec follow-up work.
- The analogy benchmark is a specific exact-match, single-token evaluation; it does not establish that vector arithmetic is a universal model of semantics.

**Integration decision.** No new page or route step is warranted. The existing historical paragraph in the embedding-space lesson remains the right level for the core path. The extraction provides an evidence-backed source for optional detail and prevents the common conflation of the original CBOW/Skip-gram paper with later word2vec implementation variants.

**Evidence boundary.** The full arXiv v3 PDF and main architecture/evaluation figures and tables were inspected. The historical code and pretrained vectors were not retrieved or executed; the negative-sampling follow-up was not scanned. The source remains partially scanned.

### Method-transfer validation

The source-to-knowledge workflow has now been retrospectively assessed against this broader collection. The [transfer-validation report](../source-syntheses/tokenization-embeddings-method-transfer-validation-2026-11.md) records the current catalogue/extraction baseline, what transfers from the Q/K/V calibration case, the limitations exposed, and the next validation gates. This is documentation/synthesis evidence, not browser, rights or learner-outcome validation.

### Remaining migration tasks

1. Continue only where an already-audited source has a distinct, evidence-backed contribution not yet represented in the collection. Do not create extraction records solely to increase coverage counts.
2. Reconcile whether a separate Vizuara embeddings resource exists and recover its exact identity only from historical evidence; the currently registered ByteByteGo/Vizuara resources already have canonical URLs.
3. Add source-specific review records only where a durable review cannot be represented adequately by this dossier and migration map.
4. Keep asset rights verification in #156 and deferred browser review in #320/#329.
5. Re-run catalogue/extraction validation and the bilingual Quarto workflow after extraction files and any generated projections are added.

### Final assessment

The source collection reinforces and qualifies the existing curriculum more than it expands it. Its strongest added value is a structured comparison of tokenizer design and multilingual evaluation, a precise distinction between static and contextual representations, and methodological caveats around embedding geometry and interactive visualizers. The right outcome is a traceable compilation of perspectives, not a larger sequence of overlapping lessons.
