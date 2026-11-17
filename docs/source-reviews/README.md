# Source reviews and comparative collections

This directory contains source-specific reviews and living multi-source collections. It is the human-readable navigation layer for the machine-readable catalogue in [data/sources.yml](../../data/sources.yml) and atomic evidence records in [data/extractions/](../../data/extractions/).

A collection dossier is not a replacement for the canonical concept graph, bilingual learning pages or project learning route. It compares external perspectives and records their integration decisions.

## Compression and information theory

| Review | Scope | Entry point | Current state |
|---|---|---|---|
| Karthik Shashidhar — LLMs and compression algorithms | Critical assessment of the LZW analogy, predictive coding, domain-frequency claims and evidence limits | [Source review](karthik-shashidhar-llms-compression-algorithms-2024.md) · [Comparative synthesis](../source-syntheses/compression-two-meanings-2026-11.md) | Full article text reviewed; anecdotal claims are not treated as empirical evidence |
| Wayland Zhang — Information Theory Is All You Need | Entropy, cross-entropy/KL, attention/MI, Landauer, predictive compression and V-information; includes an audit of the linked notebook | [Source review](wayland-zhang-information-theory-llm-2026-11.md) · [Comparative synthesis](../source-syntheses/information-theory-and-llms-2026-11.md) | Full article and 18 English-notebook cells inspected statically; notebook not executed; invalid attention/MI visualization rejected |
| Lewis — Intelligence and compression | Two-part MDL, causal sequence prediction, model updating, AIXI and active inference | [Source review](lewish-intelligence-and-compression-2025.md) · [Structured extraction](../../data/extractions/lewish-intelligence-and-compression-2025.yml) · [Compression synthesis](../source-syntheses/compression-intelligence-and-inference-efficiency-2026-11.md) | Article text reviewed; creator attribution, figures, code/data, outbound resources and rights remain partially scanned |

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
| Tokenization and embeddings | Text representation, tokenizer construction, corpus preparation, multilingual evaluation, embeddings and similarity geometry | [Cross-source synthesis](tokenization-embeddings-source-collection.md) · [Migration map](tokenization-embeddings-source-migration-map-2026-11.md) · [Hesam's interactive embedding guide](hesam-sheikh-hessani-llm-embeddings-explained-2026-11.md) | 54 source records in the project catalogue; 12 structured extractions in this collection (20 YAML extraction records across the repository); source-registration/extraction PRs #460, #463, #467, #468 and #469 merged. Remaining metadata, URL and asset-rights gaps are tracked in the migration map and #156 |
| Q/K/V and attention | Query, Key, Value, self-attention, scaled dot-product attention and related teaching perspectives | [Q/K/V source collection](qkv-source-collection.md) · [Learning-graph comparison](qkv-learning-graph-comparison-2026-11.md) | Initial source records and structured extractions integrated |
| Visual learning tools: Embedding Atlas and Neuronpedia | Interactive embedding-data exploration versus evidence-led inspection of SAE features and model internals | [Focused review and bilingual integration](embedding-atlas-neuronpedia-integration-2026-11.md) · [Initial ten-resource triage](visual-learning-resources-2026-11.md) | Bilingual guided labs integrated; sources remain partially scanned; no benchmark or model-internals experiment reproduced |

## Introductory overviews and social-media explainers

| Review | Scope | Entry point | Current state |
|---|---|---|---|
| Jose Parreño Garcia — “The 3-layer framework behind chatGPT & friends” | Classical ML analogy for corpus collection, base-model training and fine-tuning; critical assessment of truthfulness, reasoning and the confounded model comparison | [Source review](jose-parreno-garcia-how-llms-work-three-layers-2026-11.md) · [Structured extraction](../../data/extractions/jose-parreno-garcia-how-llms-work-three-layers-2025.yml) | Full article and both embedded images inspected; retained by reference only because the bilingual overview and post-training lessons already cover the technical content |

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
