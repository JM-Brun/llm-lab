# Tokenization and embeddings — source migration map

**Status:** migration design / evidence reconciliation · **Reviewed:** 2026-11-05  
**Owning issue:** [#458](https://github.com/JM-Brun/llm-lab/issues/458)  
**Related completed audits:** [#114](https://github.com/JM-Brun/llm-lab/issues/114), [#147](https://github.com/JM-Brun/llm-lab/issues/147), [#82](https://github.com/JM-Brun/llm-lab/issues/82), [#96](https://github.com/JM-Brun/llm-lab/issues/96)

## 1. Purpose and migration rule

This document maps existing tokenization/embeddings evidence to the source-registration and extraction workflow introduced in November 2026. It is a migration aid, **not a new source scan** and not a claim that the source set is exhaustive.

The historical evidence is distributed across issue comments, merged PR descriptions, canonical bilingual pages and the references page. The first migration step is to preserve those evidence boundaries before creating catalogue and extraction records.

Rules:

- Reuse prior audit findings; do not repeat scans simply to populate YAML.
- An issue comment is evidence that a review was recorded, not proof of direct inspection beyond the method explicitly stated there.
- Keep source author text, comments, linked resources, code, figures and editor inference separate.
- Use `partially-scanned` unless the component-level evidence supports a stronger status. A source can have a well-audited article body while its figures, comments, links, code or rights remain unresolved.
- Unknown metadata and licences stay `null` / `unknown`.
- Stable source IDs proposed below are migration identifiers; verify uniqueness before adding them to `data/sources.yml`.
- Do not change canonical pages, learner routes or visual assets merely to complete this migration.

## 2. Existing canonical artifacts and evidence locations

| Artifact | Existing role | Migration treatment |
|---|---|---|
| `data/sources.yml` | Canonical source catalogue; currently includes the Q/K/V tutorials and Hugging Face KV-cache documentation | Append migrated source records; do not rewrite existing Q/K/V provenance |
| `data/extractions/` | Structured source-level extraction records | Create only where evidence supports atomic, locatable contributions |
| `docs/source-reviews/` | Source-specific technical/pedagogical reviews and collection syntheses | Reuse existing reviews; add topic-level index and cross-source synthesis |
| `site/references.qmd` | Public bibliography and visual provenance | Use as a cross-check for cited sources and embedded assets, not as a scan ledger |
| `docs/visual-assets-register.md` | Cross-site asset inventory and rights follow-up | Keep all rights verification under #156; do not duplicate asset-level audit |
| `docs/learning-path.md` and canonical concept registries | Learner route and canonical knowledge model | Update only if migration reveals an evidenced omission; no route change is currently proposed |

### Existing audit evidence

- **#114** contains the tokenization and embedding source-by-source audit, coverage assessments, source disagreements, implementation limitations, and follow-up decisions.
- **#147** records the Vizuara / ByteByteGo pedagogical comparison. It is closed; its findings should be migrated as a completed assessment, not rescanned.
- **#82** owns the text → token IDs → embeddings → contextualized states content gate and is closed.
- **#96** records the Raschka Chapter 2 audit.
- **#58** owns corpus preparation and training-example construction.
- **#156** owns site-wide asset provenance and rights verification; it remains open.
- **#320** owns deferred browser review of canonical text-to-embeddings pages; it is not a source-registration blocker.

## 3. Source-family migration inventory

The identifiers below are proposed. The scan status is deliberately conservative and describes the evidence currently available in the project records, not a fresh inspection performed for this migration.

### A. Tokenizer construction, encoding and implementation

| Proposed source ID | Source | Existing evidence / canonical destination | Current evidence boundary | Migration decision |
|---|---|---|---|---|
| `andrej-karpathy-gpt-tokenizer-video` | Andrej Karpathy, [Let's build the GPT Tokenizer](https://www.youtube.com/watch?v=zduSFxRajkE) | #114 timestamped chapter and transcript audits; `tokenization-strategies.qmd`, `unicode-text.qmd` | Public chapter markers and a third-party rendered caption transcript were inspected; the audit explicitly does **not** claim the full video was watched. Figures/audio and video rights not independently audited. | Register as video; link the transcript-based extraction/review; partial scan |
| `sebastian-raschka-llms-from-scratch-ch02` | Sebastian Raschka, [LLMs from Scratch — Chapter 2](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch02) | #96 and #114; PR #172; tokenizer lesson and implementation references | Repository/notebook source was inspected; the audit distinguishes the custom character/string training path from pretrained GPT-2 loading. Clean-room execution and every upstream revision are not implied. | Register as repository/book companion; pin inspected revision only if recoverable from existing audit; partial scan |
| `huggingface-course-tokenizers-chapter6` | Hugging Face, [Course Chapter 6](https://huggingface.co/docs/course/chapter6/8) | #114; PR #173; tokenization strategy pages and references | Source-by-source BPE, WordPiece, Unigram and pipeline coverage matrix exists. Exact chapter/revision scope should be taken from PR #173; do not infer full course coverage. | Register as course/documentation; partial scan |
| `philip-gage-byte-pair-compression-1994` | Philip Gage, [A New Algorithm for Data Compression (1994)](https://www.derczynski.com/papers/archive/BPE_Gage.pdf) | #114; PR #155; bilingual BPE historical note | Original paper was consulted; the project records the distinction between byte-pair compression and NLP subword BPE. PDF figure reuse is not part of this migration. | Register as paper; source-level review linked; partial scan unless page-by-page audit evidence is available |
| `hf-tokenizer-visualizer-sauravp97` | [Hugging Face BPE Tokenizer Visualizer article](https://huggingface.co/blog/SauravP97/bpe-tokenizer-visualize) and [implementation repository](https://github.com/SauravP97/hf-tokenizer-visualizer) | #114 implementation audit; PR #168; source link in tokenization lesson | Repository inspected at commit `1a802315afc0e17dddf3a64972cf25dddda8bbfe`; limitations in pre-tokenization/byte-level fidelity, occurrence identity and dependency metadata are recorded. Execution/reproducibility was not claimed. | Consider article and repository as distinct linked records if their evidence roles differ; do not merge their provenance |
| `vizuara-tokenization-bpe-learning-resource` | Vizuara tokenization/BPE learning material | #147 pedagogical review | Evaluated as a pedagogical resource; the issue records that its useful teaching affordances are already represented. Exact asset-level scan scope should remain as recorded in #147. | Register as course/resource with pedagogical review; partial scan; likely integrate-by-reference/already-covered |
| `bytebytego-tokenization-learning-resource` | ByteByteGo tokenization and corpus-preparation material | #147 and #58 | Examples involving whitespace, case, numbers, Unicode, multilingual text and code were compared with current lessons. Do not claim a complete site/course scan. | Register exact canonical article/page URL only after recovering it from prior evidence; do not guess URL; partial scan |
| `nishanthan-k-qkv-transformers-devto` / `neha-kk-understanding-qkv-medium` | Q/K/V tutorials, outside the core tokenization/embeddings family | Existing `data/sources.yml`, Q/K/V collection | Already registered and audited. | Exclude from this migration; link only where cross-topic relations are useful |

### B. Corpus preparation and data pipeline

| Proposed source ID | Source | Existing evidence / owner | Current evidence boundary | Migration decision |
|---|---|---|---|---|
| `llm-lab-corpus-preparation-synthesis` | LLM Lab's own corpus-to-training-example treatment | #58; PR #148; bilingual corpus/data pages | This is a **project artifact**, not an external source. | Do not register as an external source. Reference it as the canonical comparison target in the dossier. |
| `bytebytego-corpus-preparation-resource` | ByteByteGo corpus/tokenization examples, if distinct from the tokenization article | #147 / #58 | Exact source identity and URL must be recovered from historical records before registration. | Do not create a speculative duplicate record. Resolve whether this is one source or multiple resources first. |

### C. Tokenization research, multilingual efficiency and evaluation

| Proposed source ID | Source | Existing evidence / canonical destination | Current evidence boundary | Migration decision |
|---|---|---|---|---|
| `ahia-tokenizer-multilingual-study` | Ahia et al., tokenizer / multilingual evaluation research | #114; PR #333; tokenization research pages | Source-primary reconciliation is recorded in #333; exact title, DOI/URL and publication metadata must be copied from that merged audit before catalogue entry. | Register only from exact metadata in #333; partial scan unless source coverage is explicitly complete |
| `petrov-tokenizer-language-unfairness` | Petrov et al., [Language Model Tokenizers Introduce Unfairness Between Languages](https://www.adelbibi.com/publication/langugage_unfairness_tokenizers/) | #114; #156; PRs #153/#158/#165; references page | Research findings were reviewed; figure asset rights remain a separate #156 matter. Historical removal/restoration of the figure is not a licence conclusion. | Register paper and figure provenance separately; do not duplicate rights audit |
| `ali-tokenizer-choice-llm-training-2024` | Ali et al. (2024), [Tokenizer Choice For LLM Training](https://aclanthology.org/2024.findings-naacl.247/) | #114; PR #332/#333; advanced tokenizer-design pages | Full paper PDF was reviewed in the #114 primary-source note: 24 tokenizers, decoder-only models at 2.6B, five-language corpus comparison and zero-shot evaluation. Limits include one seed, five Latin-script languages, uneven task counts and a protocol-specific 68% training-compute estimate. | Register paper with detailed protocol and caveats; do not generalize results |
| `wegmann-tokenization-language-variation-2025` | Wegmann et al. (2025), [Tokenization is Sensitive to Language Variation](https://aclanthology.org/2025.findings-acl.572/) | #114; PR #332/#333; advanced tokenizer-design pages | Abstract-level audit recorded that the best tokenizer varies with task type and language variation; pre-tokenizer effect is scoped to BERT-base experiments. Full-paper coverage should not be implied without evidence. | Register paper; partial scan; preserve task/model scope |
| `arnett-explaining-mitigating-crosslingual-tokenizer-inequities-2025` | Arnett et al. (NeurIPS 2025), [Explaining and Mitigating Crosslingual Tokenizer Inequities](https://proceedings.neurips.cc/paper_files/paper/2025/hash/5b91cefbfa52340af2f16f249572dc76-Abstract-Conference.html), [OpenReview PDF](https://openreview.net/pdf?id=0Y7AxxNCYh), [arXiv](https://arxiv.org/abs/2510.21909) | #114; PR #332/#333; advanced tokenizer-design pages | Primary-source review recorded: ~7,000 monolingual tokenizers / 97 languages, CTC-based token premium, vocabulary/pre-tokenization effects and no LM downstream evaluation. This is distinct from the separate Catherine Arnett 2024 Hugging Face community article/figure. | Register the 2025 paper; keep the 2024 article as a separate source if retained in references |
| `chiu-toklens-acl-srw-2026` | Chiu (ACL 2026 SRW), [TokLens](https://aclanthology.org/2026.acl-srw.18/) | #114; PR #326/#333; advanced tokenizer-design pages | Six intrinsic metrics; 24 tokenizer configurations / 15 languages; MMLU-ProX subset 7 models / 11 languages. Findings are correlational and partly confounded; fertility and token/character parity are distinct metrics. | Register paper; preserve distinct denominators and correlational limits |
| `huggingface-tokenizer-pipeline-figure` | Hugging Face course pipeline SVG | #114; #156; PR #153/#158/#165; references page | The image is embedded and preserved. Repository-level Apache-2.0 evidence was recorded, but exact asset authorship/coverage is not fully confirmed. | This is an **asset record**, not a duplicate source article; rights remain with #156 |

### D. Token embeddings, contextualization and representation geometry

| Proposed source ID | Source | Existing evidence / canonical destination | Current evidence boundary | Migration decision |
|---|---|---|---|---|
| `mikolov-word2vec-2013` | Mikolov et al., [Efficient Estimation of Word Representations in Vector Space](https://arxiv.org/abs/1301.3781) | #114; PR #152/#333; `embedding-space.qmd` | Primary paper reviewed; distinction between static word-type vectors and Transformer token lookup/contextual states is integrated. | Register paper; link source review; partial scan if only relevant sections were assessed |
| `ethayarajh-contextualized-representations-2019` | Ethayarajh, [How Contextual are Contextualized Word Representations?](https://aclanthology.org/D19-1006/) | #114; PR #333; contextualized representations page | Primary paper findings reviewed with model/time-scope caveats; no universalization to current LLMs. | Register paper; preserve empirical-scope limitations |
| `li-bert-flow-sentence-embeddings-2020` | Li et al., [On the Sentence Embeddings from Pre-trained Language Models](https://aclanthology.org/2020.emnlp-main.733/) | #114; PR #333; cosine similarity page | Primary paper reviewed; anisotropy/BERT-flow discussion is scoped to studied models. | Register paper; link review |
| `steck-cosine-similarity-2024` | Steck, Ekanadham & Kallus, [Is Cosine-Similarity of Embeddings Really About Similarity?](https://arxiv.org/abs/2403.05440) | #114; PR #333; cosine similarity page | Primary-source reconciliation recorded; retain distinctions between metric geometry and semantic similarity. | Register paper; partial scan unless full-paper coverage is evidenced |
| `sentence-transformers-similarity-docs` | Sentence Transformers official documentation: [STS](https://sbert.net/docs/sentence_transformer/usage/semantic_textual_similarity.html), [similarity functions](https://www.sbert.net/docs/package_reference/util/similarity.html), [model API](https://www.sbert.net/docs/package_reference/sentence_transformer/model.html) | #114; PR #333; cosine similarity page | Specific API behavior reviewed; docs are living and must be revision/date qualified. | Consider three URLs one documentation source family or distinct records by API topic; do not overstate exhaustive documentation coverage |
| `rushang-chauhan-embeddings-context-linkedin` | Rushang Chauhan, [Embeddings: The Bridge Between Tokens and Context](https://www.linkedin.com/pulse/embeddings-bridge-between-tokens-context-rushang-chauhan-oqpzf/) | #114; #156; references page; PRs #150/#161/#162/#165 | Article/illustration provenance recorded. The illustration's rights status is not resolved by attribution; follow #156. | Register article and linked visual asset separately; partial scan, rights unknown |
| `poloclub-transformer-explainer` | Cho et al., [Transformer Explainer](https://poloclub.github.io/transformer-explainer/), [repository](https://github.com/poloclub/transformer-explainer), [CHI 2026 paper](https://doi.org/10.1145/3772318.3791725) | PR #186/#188; references page; interactive explainer lessons | Implementation, interactive behavior and paper version distinctions have prior review. Exact code commit is recorded in prior work; retrieve it before registering revision. | Register paper, demo and repository as linked but distinct records if each is independently used |
| `vizuara-embeddings-learning-resource` | Vizuara embeddings material, if distinct from its tokenization resource | #114/#147 where applicable | Source identity and prior scan scope must be resolved; do not assume it is the same item as the Vizuara BPE resource. | Hold until exact URL and audit evidence are recovered |

## 3A. Additional implementation and historical sources already present in the #114 audit

These records are easy to miss if the migration is based only on the learner-facing bibliography. They were explicitly inspected in the educational-implementation and historical-source audit comments.

| Proposed source ID | Source | Existing evidence | Evidence boundary | Migration decision |
|---|---|---|---|---|
| `openai-tiktoken-educational-bpe` | [OpenAI tiktoken educational BPE module](https://github.com/openai/tiktoken/blob/main/tiktoken/_educational.py) | #114 educational implementation audit; tiktoken encoding test PR #120 | Source code inspected for regex pre-splitting, UTF-8 byte conversion, merge ranks and byte decoding. The module was treated as educational, not the optimized production path. | Register repository file; record revision if recoverable; do not claim code was copied |
| `karpathy-minbpe` | [Karpathy minbpe README](https://github.com/karpathy/minbpe/blob/master/README.md) and [exercise](https://github.com/karpathy/minbpe/blob/master/exercise.md) | #114 educational implementation audit | README and MIT licence checked; implementation was not copied or executed in that audit. | Register repository; partial scan |
| `huggingface-tokenizers-pipeline-docs` | [Hugging Face Tokenizers pipeline](https://huggingface.co/docs/tokenizers/python/latest/pipeline.html) and [components](https://huggingface.co/docs/tokenizers/python/latest/components.html) | #114 implementation audit; PR #149 | Pipeline order and component behavior reviewed; living documentation URLs are not revision-pinned. | Register documentation family; partial scan; do not infer full API coverage |
| `google-sentencepiece-overview` | [SentencePiece overview](https://google.github.io/sentencepiece/) and [normalization](https://google.github.io/sentencepiece/doc/normalization/) | #114 implementation audit; PR #149 | Unicode input, whitespace meta-symbol, normalization and configurable behavior were reviewed; avoid universal claims about defaults/configurations. | Register official documentation; partial scan |
| `huggingface-tokenizer-algorithms-summary` | [Hugging Face tokenizer summary](https://huggingface.co/docs/transformers/main/en/tokenizer_summary) | #114 first-pass audit | Living overview compared BPE, WordPiece and Unigram; URL uses moving `main`. | Register as living documentation; no fixed revision claimed |
| `sennrich-subword-nmt-2016` | Sennrich et al. (2016), [Neural Machine Translation of Rare Words with Subword Units](https://aclanthology.org/P16-1162/) | #114 historical source audit | Abstract-level historical check for BPE-derived subword units in NMT; not a specification of GPT-2 byte-level BPE. | Register paper; partial scan |
| `openai-tiktoken-library` | [OpenAI tiktoken repository](https://github.com/openai/tiktoken) | #114 first-pass audit; PR #120 | README/API scope checked; old README benchmark versions were not reused as current performance evidence. | Register repository; partial scan |
| `huggingface-tokenizers-library` | [Hugging Face Tokenizers repository](https://github.com/huggingface/tokenizers) | #114 first-pass audit | README and Apache-2.0 repository licence checked; detailed APIs remain outside that pass. | Register repository; partial scan |
| `google-sentencepiece-library` | [Google SentencePiece repository](https://github.com/google/sentencepiece) | #114 first-pass audit | README and Apache-2.0 repository licence checked; detailed API behavior is covered only where linked to the lesson. | Register repository; partial scan |
| `pytorch-embedding-api` | [PyTorch Embedding documentation](https://docs.pytorch.org/docs/stable/generated/torch.nn.Embedding.html) | #114 first-pass source check; embedding-space page | Integer-index lookup and tensor-shape semantics checked against official API docs. | Register as documentation; partial scan |
| `su-roformer-rope-2021` | Su et al. (2021), [RoFormer: Enhanced Transformer with Rotary Position Embedding](https://arxiv.org/abs/2104.09864) | #114 first-pass source check; positional-encoding page | Paper used to support conceptual distinction between RoPE and learned absolute position-vector addition. | Register paper; source-specific scan depth should reflect the original review |

**Source identity caution:** the 2024 Catherine Arnett Hugging Face community article (visual resource) and the 2025 Arnett et al. NeurIPS paper are different sources and must never share a source ID.

## 4. Known exclusions and non-source artifacts

These items should not be turned into external-source records:

- LLM Lab's own diagrams, lessons, experiments and corpus pipeline: canonical project artifacts.
- Issue comments or reader suggestions: store as comment/community provenance attached to the relevant source, not as author-authored content.
- A figure URL alone: register it in the visual asset register, not as a new article.
- The whole Hugging Face documentation website: too broad; register only the exact chapter/API pages actually used.
- A source mentioned in a bibliography but not substantively inspected: it may be registered as `not-scanned` / reference-only, but not described as audited.

## 5. Cross-source synthesis dimensions

The eventual collection dossier should compare the sources on a consistent set of questions:

1. What is the unit being tokenized: Unicode code point, UTF-8 byte, pre-tokenized string, word, subword or special token?
2. How are tokenizer training and encoding separated?
3. Which algorithm family is used: BPE, WordPiece, Unigram or another method?
4. What is the role of normalization, pre-tokenization, model, post-processing and decoding?
5. How do corpus composition, frequency weighting, deduplication and train/held-out boundaries affect the learned vocabulary and evaluation?
6. What do fertility, token/character parity, compression, latency and downstream quality measure—and what do they not measure?
7. How do static word-type embeddings, token lookup embeddings and contextualized hidden states differ?
8. What geometric claims are supported about anisotropy, cosine similarity and semantic similarity?
9. What does a visualizer actually execute, omit or approximate?
10. Which teaching moves add value beyond the canonical LLM Lab route?

## 6. Unresolved metadata and evidence retrieval queue

The following are explicit migration blockers for catalogue completeness, not reasons to repeat the technical audit:

- Recover exact title, URL, authors and publication metadata for Ahia, Ali, Wegmann and TokLens from merged PR #326/#332/#333.
- Recover exact ByteByteGo URL(s) and determine whether tokenization and corpus preparation were one article or separate resources.
- Recover exact Vizuara URL(s) and separate BPE from embeddings if they are distinct sources.
- Recover the exact version/commit used for Raschka Chapter 2, Hugging Face course pages and Polo Club repository.
- Confirm whether Karpathy's transcript source and timestamp guide have a stable record URL and preserve the limitation that the full video was not watched.
- Keep all visual asset-level rights checks in #156; do not infer them from source repository licences or attribution.
- Do not invent missing scan dates, creators, publication dates or revision identifiers.

## 7. Recommended migration sequence

1. **Metadata reconciliation:** retrieve exact bibliographic fields from #114 comments, PR #326/#332/#333 and the references page. Resolve duplicates and exact source identity.
2. **Catalogue migration:** add stable records to `data/sources.yml` using the source-registration template. Keep scan and rights status component-specific.
3. **Extraction migration:** create structured extraction files only for sources with sufficiently locatable evidence. Start with high-value primary sources (Karpathy transcript audit, Raschka Chapter 2, Hugging Face course, Gage, Mikolov, Ethayarajh, Li, Steck).
4. **Review migration:** link the existing source-by-source review evidence; do not rewrite the historical issue audit.
5. **Collection synthesis:** create a single tokenization/embeddings dossier with the multi-source template, separating the subdomains above.
6. **Validation:** run existing YAML/schema/catalogue validators, source-link checks, Python CI and Quarto if any rendered data/page is changed.
7. **Review the PR diff:** verify that no canonical learner content, external figure or route has been changed unintentionally.

## 8. Current conclusion

The project already has substantive technical and pedagogical coverage of tokenization and embeddings. The immediate gap is **evidence normalization and provenance navigation**, not a missing introductory lesson. The migration should make the source set inspectable and reusable while preserving partial-scan limitations, existing content decisions and the separation between the source graph, canonical concept graph and learner route.
