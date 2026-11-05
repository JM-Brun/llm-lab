# Source reviews and comparative collections

This directory contains source-specific reviews and living multi-source collections. It is the human-readable navigation layer for the machine-readable catalogue in [data/sources.yml](../../data/sources.yml) and atomic evidence records in [data/extractions/](../../data/extractions/).

A collection dossier is not a replacement for the canonical concept graph, bilingual learning pages or project learning route. It compares external perspectives and records their integration decisions.

## Curriculum and learning-path comparisons

| Comparison | Scope | Entry point | Current state |
|---|---|---|---|
| Raschka and Hugging Face learning paths | From-scratch GPT implementation versus ecosystem/task-oriented LLM curriculum; transferable design principles and implications for LLM Lab | [Comparative audit](learning-path-comparison-2026-11-05.md) | Dated structural comparison (2026-11-05); not a learner-outcome evaluation |

## Living collections

| Collection | Scope | Entry point | Current state |
|---|---|---|---|
| Tokenization and embeddings | Text representation, tokenizer construction, corpus preparation, multilingual evaluation, embeddings and similarity geometry | [Cross-source synthesis](tokenization-embeddings-source-collection.md) · [Migration map](tokenization-embeddings-source-migration-map-2026-11.md) | 49 source records in the project catalogue; 11 structured extractions in this collection (16 across the repository); migration PRs #468 and #469 merged; remaining URL and asset-rights gaps are tracked in the migration map and #156 |
| Q/K/V and attention | Query, Key, Value, self-attention, scaled dot-product attention and related teaching perspectives | [Q/K/V source collection](qkv-source-collection.md) · [Learning-graph comparison](qkv-learning-graph-comparison-2026-11.md) | Initial source records and structured extractions integrated |

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
