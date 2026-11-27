# Source reviews and comparative collections

This directory contains source-specific reviews and navigation to living multi-source collections, which are maintained separately in [docs/source-syntheses/](../source-syntheses/). It is the human-readable review layer for the machine-readable catalogue in [data/sources.yml](../../data/sources.yml) and atomic evidence records in [data/extractions/](../../data/extractions/).

Source reviews assess individual sources. Cross-source dossiers compare perspectives and record aggregate integration decisions; neither replaces the canonical concept graph, bilingual learning pages or project learning route.

## Compression and information theory

| Review | Scope | Entry point | Current state |
|---|---|---|---|
| Karthik Shashidhar — LLMs and compression algorithms | Critical assessment of the LZW analogy, predictive coding, domain-frequency claims and evidence limits | [Source review](karthik-shashidhar-llms-compression-algorithms-2024.md) · [Comparative synthesis](../source-syntheses/compression-two-meanings-2026-11.md) | Full article text reviewed; anecdotal claims are not treated as empirical evidence |
| Wayland Zhang — Information Theory Is All You Need | Entropy, cross-entropy/KL, attention/MI, Landauer, predictive compression and V-information; includes an audit of the linked notebook | [Source review](wayland-zhang-information-theory-llm-2026-11.md) · [Comparative synthesis](../source-syntheses/information-theory-and-llms-2026-11.md) | Full article and 18 English-notebook cells inspected statically; notebook not executed; invalid attention/MI visualization rejected |
| Lewis — Intelligence and compression | Two-part MDL, causal sequence prediction, model updating, AIXI and active inference | [Source review](lewish-intelligence-and-compression-2025.md) · [Structured extraction](../../data/extractions/lewish-intelligence-and-compression-2025.yml) · [Source dossier](../source-syntheses/compression-intelligence-and-inference-efficiency-2026-11.md) · [Cross-source synthesis](../source-syntheses/compression-intelligence-cross-source-2026-11.md) | Article text reviewed; creator attribution, figures, code/data, outbound resources and rights remain partially scanned |
| Notion — Intelligence = Compression | Predictive compression, Hutter Prize, Kolmogorov complexity/AIXI and cognitive-architecture claims; claim-by-claim qualification | [Source review](notion-intelligence-compression-2026-11.md) · [Structured extraction](../../data/extractions/notion-intelligence-compression-summary.yml) | All visible page text reviewed; author/date/revision, linked-resource audit and reuse rights remain unknown; retained as critical context |
| AIXI and computability deep dive | Kolmogorov complexity, Solomonoff semimeasure, AIXI computability, ε-optimal variants and resource-bounded AIXI(t,l) | [Technical review](aixi-kolmogorov-computability-2026-11.md) · [Cross-source synthesis](../source-syntheses/kolmogorov-aixi-computability-2026-11.md) · [Bilingual lesson](../../site/en/universal-artificial-intelligence.qmd) | Relevant sections of Hutter (2007), Leike & Hutter (2015) and Hutter et al. (2024) inspected; proofs not audited line-by-line; no implementation benchmark |

## Curriculum and learning-path comparisons

| Review | Scope | Entry point | Current state |
|---|---|---|---|
| Hesam Sheikh — How I Studied LLMs in Two Weeks | Article roadmap plus the author's Days 003–016 journal; attention, fine-tuning, hallucination, distillation, advanced inference, ViT, NLU and multimodality | [Source review](hesam-sheikh-llm-study-roadmap-2026-11.md) · [Structured extraction](../../data/extractions/hesam-sheikh-llm-study-roadmap-2024.yml) · [Author's study journal](https://github.com/hesamsheikh/ml-retreat) | Article and daily README text inspected; image assets and three overview PDFs remain unaudited; route retained by reference, not adopted as canonical curriculum |

| Comparison | Scope | Entry point | Current state |
|---|---|---|---|
| Raschka and Hugging Face learning paths | From-scratch GPT implementation versus ecosystem/task-oriented LLM curriculum; transferable design principles and implications for LLM Lab | [Comparative audit](learning-path-comparison-2026-11-05.md) | Dated structural comparison (2026-11-05); not a learner-outcome evaluation |

## Living collections

| Collection | Scope | Entry point | Current state |
|---|---|---|---|
| Tokenization and embeddings | Text representation, tokenizer construction, corpus preparation, multilingual evaluation, embeddings and similarity geometry | [Cross-source synthesis](tokenization-embeddings-source-collection.md) · [Migration map](tokenization-embeddings-source-migration-map-2026-11.md) · [Hesam's interactive embedding guide](hesam-sheikh-hessani-llm-embeddings-explained-2026-11.md) · [Gage (1994) primary audit](gage-1994-primary-audit.md) · [Sennrich et al. (2016) primary audit](sennrich-2016-primary-audit.md) | 32 source records, 12 extraction files and 45 atomic items in the validated 2026-11-26 report (PR #1696). Counts are joined through `extraction.source_id -> source.id -> source.collections`; historical snapshots are superseded. See the collection synthesis for source-to-concept coverage. |
| Q/K/V and attention | Query, Key, Value, self-attention, scaled dot-product attention and related teaching perspectives | [Q/K/V source collection](qkv-source-collection.md) · [Learning-graph comparison](qkv-learning-graph-comparison-2026-11.md) | Initial source records and structured extractions integrated |
| Visual learning tools: Embedding Atlas and Neuronpedia | Interactive embedding-data exploration versus evidence-led inspection of SAE features and model internals | [Focused review and bilingual integration](embedding-atlas-neuronpedia-integration-2026-11.md) · [Initial ten-resource triage](visual-learning-resources-2026-11.md) | Bilingual guided labs integrated; sources remain partially scanned; no benchmark or model-internals experiment reproduced |

## Tokenization source models

The tokenization collection now distinguishes source-specific meta-representations from atomic evidence extraction:

| Source | Representation |
|---|---|
| Karpathy GPT Tokenizer | [Structured extraction](../../data/extractions/andrej-karpathy-gpt-tokenizer-video.yml) |
| Raschka, Chapter 2 | [Structured extraction](../../data/extractions/sebastian-raschka-llms-from-scratch-ch02.yml) |
| Hugging Face Course, Chapter 6 | [Pedagogical audit](huggingface-course-tokenizer-pedagogical-audit-2026-11-19.md) |
| Vizuara, Tokenization from Scratch | [Structured extraction](../../data/extractions/vizuara-tokenization-from-scratch-bpe.yml) |
| ByteByteGo, How LLMs See the World | [Structured extraction](../../data/extractions/bytebytego-how-llms-see-world-2025.yml) |
| Hugging Face Tokenizers | [Implementation/documentation audit](tokenization-implementations-huggingface-tiktoken-minbpe-2026-11.md) |
| OpenAI tiktoken | [Implementation audit](tiktoken-implementation-audit-2026-11-19.md) |
| Karpathy minbpe | [Structured extraction](../../data/extractions/karpathy-minbpe.yml) |
| Google SentencePiece | [Structured extraction](../../data/extractions/google-sentencepiece-documentation.yml) |

The current concept model adds 21 tokenization-specific concepts and typed relations; five new source extractions complement the existing Karpathy extraction and the source-specific Hugging Face/tiktoken reviews. Use the cross-source synthesis for the comparative concept spine. The extraction records retain source-local graphs and teaching routes; the canonical concept registry remains a separate project-level model. Existing reviews remain the representation of record where a new extraction would duplicate already-audited claims or exceed the evidence.

## Introductory overviews and social-media explainers

| Review | Scope | Entry point | Current state |
|---|---|---|---|
| Jose Parreño Garcia — “The 3-layer framework behind chatGPT & friends” | Classical ML analogy for corpus collection, base-model training and fine-tuning; critical assessment of truthfulness, reasoning and the confounded model comparison | [Source review](jose-parreno-garcia-how-llms-work-three-layers-2026-11.md) · [Structured extraction](../../data/extractions/jose-parreno-garcia-how-llms-work-three-layers-2025.yml) | Full article and both embedded images inspected; retained by reference only because the bilingual overview and post-training lessons already cover the technical content |
| Damien Benveniste — “How LLMs Encode Token Position” | Short-form comparison of learned absolute vectors, sinusoids, RoPE and ALiBi; distinguishes positional information from causal visibility | [Source review](aiedge-positional-encoding-2026-11.md) · [Structured extraction](../../data/extractions/aiedge-how-llms-encode-token-position-2026.yml) · [Cross-source synthesis](../source-syntheses/positional-encoding-source-synthesis-2026-11-26.md) | Partial indexed scan only; full article, figures, examples and implementation remain uninspected |

| Review | Scope | Entry point | Current state |
|---|---|---|---|
| Jothi Moorthy — “When you type a prompt, the LLM sees numbers, not words” | Five-stage prompt → token IDs → embeddings → Transformer → next-token overview | [Source review](jothi-moorthy-llm-processing-linkedin-2026-11.md) | Author text inspected; infographic and comments not inspected; redundant with the bilingual Understand path, so no canonical integration |

## How to navigate the evidence

1. **Catalogue** — source identity, version, scan history, rights and links to related artifacts.
2. **Extraction** — atomic claims, examples, equations, code, limitations and pedagogical reconstruction with exact locators.
3. **Source review** — technical correctness, evidence quality, pedagogical value and disposition.
4. **Collection dossier** — cross-source convergence, complementarity, disagreements, route comparison and project impact.
5. **Visual asset register** — asset-level provenance and rights; separate from article-level source scanning.

See the [source integration workflow](../workflows/source-to-learning-system-integration.md), its [templates](../workflows/templates/), and the [source-to-knowledge validation protocol](../workflows/source-to-knowledge-validation.md). The workflow distinguishes source-local graphs/routes from the canonical concept graph and learner routes; the validation protocol checks both the knowledge product and the repeatability of the method.

## Scope and status rules

- A source appearing in the catalogue does not imply that it was fully scanned.
- Text, figures, code/data, comments, linked resources, metadata and rights have independent evidence boundaries.
- Unknown values remain unknown; do not infer publication metadata, revisions, licences or permission.
- A useful source may be redundant with the project and still be retained as a reference; no page edit is required.
- A collection can have no curriculum impact. Source quantity is not a quality metric.
- Do not remove or replace existing visual assets as part of rights auditing; follow the preservation policy and issue #156.
