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
| `ali-tokenizer-efficiency-study` | Ali et al., tokenizer efficiency research | #114; PR #332 and #333 | Research claims and protocol caveats were reconciled; exact bibliographic fields must be copied from merged review. | Register from primary-source metadata; link the review |
| `wegmann-tokenizer-efficiency-study` | Wegmann et al., tokenizer efficiency research | #114; PR #332 and #333 | Same as above; preserve distinctions among compression, compute cost and downstream quality. | Register from primary-source metadata; link the review |
| `catherine-arnett-tokenizer-fertility` | Catherine Arnett, [Dangers of tokenizer recycling](https://huggingface.co/blog/catherinearnett/dangers-of-tokenizer-recycling) | #114; PRs #153/#158/#165; references page | Article findings reviewed; exact embedded image is tracked in #156. No universal ranking should be inferred from the article's experiments. | Register article; link the asset register; do not mark rights verified |
| `toklens-tokenizer-analysis` | TokLens research / analysis resource | #114; PR #326; bilingual tokenization research pages | Sample sizes, causal limits and distinction between fertility and token/character parity were clarified. Exact primary URL and bibliographic metadata must be recovered from PR #326 or #333. | Register only after exact source identity is resolved |
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
