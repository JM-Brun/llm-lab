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
