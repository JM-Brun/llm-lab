# Daily Dose of Data Science: selected contributions for the main path

**Review date:** 2026-11-17  
**Scope:** selected material that improves the existing Theory / Understand path, not a wholesale ingestion of the publisher's catalogue.

## Decision

Integrate a small amount of material at existing destinations rather than create a new course stage:

1. **Representations → optional cosine deep dive:** explain how bi-encoders and cross-encoders encode sentence pairs and why similarity scores depend on the encoder and its objective.
2. **Context use → existing RAG deep dive:** clarify the common two-stage pattern (bi-encoder candidate retrieval, optional cross-encoder reranking).
3. Keep the nine-stage Theory route intact. Add `cosine-similarity` as optional depth under representations; do not make retrieval, vector databases or RAG prerequisites for understanding Transformer internals.

## Sources inspected and limits

| Source | Inspected scope | Status | Decision |
|---|---|---|---|
| [Part 1: Bi-encoders and Cross-encoders](https://www.dailydoseofds.com/bi-encoders-and-cross-encoders-for-sentence-pair-similarity-scoring-part-1/) | Introduction, static/contextualized embeddings, BERT MLM/NSP, start of “The problem with BERT” | Partial; paywall immediately after posing the raw-BERT/cosine problem | Use accessible motivation/background only; do not invent inaccessible explanation |
| [Part 2: AugSBERT](https://www.dailydoseofds.com/augsbert-bi-encoders-cross-encoders-for-sentence-pair-similarity-scoring-part-2/) | Bi-/cross-encoder distinction, AugSBERT overview, beginning of data augmentation | Partial; details/implementation paywalled | Integrate architecture distinction; retain AugSBERT as optional reference |
| [Foundations of RAG systems](https://www.dailydoseofds.com/a-crash-course-on-building-rag-systems-part-1-with-implementations/) | Vector database motivation, chunking, embeddings, storage, query embedding, approximate retrieval and cross-encoder reranking | Partial; later implementation sections paywalled | Use as a linked pipeline example, not a canonical specification |

No embedded images were reused; image placeholders were not treated as inspected figures. No code was executed. Text and figures remain link-only because no reuse licence was established.

## Contributions and integration choices

### Integrated

- A bi-encoder independently encodes each side with a shared encoder, producing reusable vectors that can be indexed and compared later.
- A cross-encoder processes the query and candidate together and returns a pair-specific score; this is useful for reranking a shortlist but expensive across a large corpus.
- A common two-stage architecture is candidate generation followed by optional pairwise reranking. Candidate generation need not be vector-only: lexical, sparse, hybrid or structured search can also be used.
- AugSBERT uses cross-encoder pair judgments to augment or supervise bi-encoder training. The high-level idea is retained as optional further reading; detailed method and performance are not claimed as fully inspected.
- Pairwise scoring applies beyond RAG (question answering, information retrieval and duplicate detection), motivating the connection to sentence representations.

### Already covered / no duplication

- Static versus contextualized token representations are already explained in the core representations sequence.
- Cosine limitations, anisotropy, hubness and task-dependent metric selection are already treated in the advanced cosine lesson.
- RAG's storage/retrieval/transmission boundary, chunking, ranking, context assembly and failure modes are already covered in the RAG deep dive.
- Vector databases are not a requirement for every RAG system. The tutorial's vector-centric presentation is one implementation pattern, not a universal definition.
- The article's “75% retrieval / 25% generation” line is rhetorical and has no measured universal status; it is not integrated.

## Files changed

- `data/sources.yml` and three `data/extractions/*.yml` records.
- `site/fr/cosine-similarity.qmd` and `site/en/cosine-similarity.qmd`.
- `site/fr/rag-memory-boundaries.qmd` and `site/en/rag-memory-boundaries.qmd`.
- `data/guided-route.yml`: optional cosine deep dive in the representations stage.
- `docs/references.md`.

## Validation still required

- Run source-catalogue, YAML, guided-route, page metadata, bilingual, link and full site build checks.
- Inspect rendered French and English pages, mobile layout, tables and navigation.
- Verify new source records against current schemas and ensure the generated guided route includes the optional page.
- Technical comparison with original SBERT/AugSBERT papers and current Sentence Transformers documentation remains a separate corroboration task; the tutorial is pedagogical evidence, not primary evidence.
- No learner study has been run; build/CI success must not be presented as learner validation.

## Follow-up audit — architecture alternatives and visual material (2026-11-17)

### Technical correction

- Corrected both language versions: a bi-encoder independently encodes each input through its own branch; weight sharing is optional. Sentence-BERT's original Siamese design ties weights, but this is a specific architecture choice.
- Clarified that cross-encoder output is a task-specific pair score, not necessarily a calibrated probability.
- Added the distinction between a single-vector bi-encoder, a joint cross-encoder and late interaction.

### Complementary points of view now integrated

- **ColBERT / late interaction:** multi-vector contextual token representations and MaxSim, positioned between single-vector retrieval and full cross-encoding. Explicitly note the larger index and serving complexity.
- **ColBERTv2:** residual compression and denoised supervision as an answer to late interaction's storage burden; do not universalize the paper's reported compression factor.
- **BM25:** retained as a strong lexical baseline, especially for exact names, rare terms and identifiers.
- **SPLADE:** learned sparse term-weight representations, distinct from both classic BM25 and dense single-vector retrieval.
- **Hybrid retrieval:** complementary candidate sources may improve recall, but fusion is empirical and can harm some queries.
- **BEIR:** use heterogeneous evaluation to counter single-benchmark generalizations. Keep candidate recall distinct from ranking metrics and track latency/index size.
- **Reranking boundary:** a reranker cannot recover a relevant passage missing from the candidate shortlist.

### Visual audit and new assets

The Daily Dose article's visible HTML contains image placements, but this pass did not verify the underlying image bytes, full image contents or reuse rights. No original article image is reproduced. Instead, two original LLM Lab SVGs were created:
- `site/images/retrieval-architectures-en.svg`
- `site/images/retrieval-architectures-fr.svg`

They compare single-vector bi-encoding, joint cross-encoding and ColBERT-style late interaction, including the MaxSim aggregation. The cosine deep dive embeds the bilingual diagram. The RAG page adds a retrieval-family comparison table alongside its existing pipeline diagram.

### New primary and benchmark references

- Reimers & Gurevych (2019), Sentence-BERT, ACL Anthology.
- Khattab & Zaharia (2020), ColBERT, arXiv/SIGIR.
- Santhanam et al. (2022), ColBERTv2, ACL Anthology.
- Formal et al. (2021), SPLADE, arXiv/SIGIR.
- Thakur et al. (2021), BEIR, arXiv/NeurIPS Datasets and Benchmarks.

All are registered in `data/sources.yml`; extraction notes distinguish inspected abstracts/architecture descriptions from unreviewed experimental tables. References are link-only; original figures are not copied.

### Validation still required

- Run YAML/source-catalogue schema checks, bilingual parity, link checks and the full Quarto build.
- Inspect both new SVGs in rendered desktop and mobile layouts; check text overflow and alt text.
- Confirm no generated navigation or graph metadata requires regeneration.
- No retrieval model benchmark or learner study was performed in this documentation change.
