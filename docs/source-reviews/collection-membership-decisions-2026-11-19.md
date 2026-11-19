# Source-to-collection decision: Andrej Karpathy tokenizer video

**Review date:** 2026-11-19  
**Source ID:** `andrej-karpathy-gpt-tokenizer-video`  
**Collection:** `tokenization-embeddings`  
**Decision:** assign explicit membership.

## Evidence and rationale

The existing [Tokenization and embeddings collection dossier](tokenization-embeddings-source-collection.md) names Karpathy's tokenizer video in its tokenizer-construction and encoding source family. The [source migration map](tokenization-embeddings-source-migration-map-2026-11.md) independently places the same source ID in that family and records its existing audit trail and bilingual destinations (`tokenization-strategies`, `unicode-text`, and `text-data`). Its contribution is directly within the dossier's declared scope: byte-level tokenizer construction and encoding.

This is a topical collection decision based on an existing source-specific audit and an explicit dossier mapping. It is not inferred from tags, title similarity, or page proximity.

## Evidence boundary retained

The catalogue records only a partial scan. The earlier review used public chapter markers and a third-party rendered caption transcript; the full audiovisual work was not watched. The 2026-11-19 metadata check verified the official title, creator and publication date, but did not inspect the full video, comments, linked resources or reuse rights. No stronger scan status, licence, or reuse permission is inferred.

The source's `integration_status: integrated` remains unchanged: this decision does not re-audit pedagogical integration or claim completeness.

## Change

Add `collections: [tokenization-embeddings]` to this canonical source record. No extraction is created and no source, scan, licence, or pedagogical status is changed.


---

# Source-to-collection decision: Philip Gage (1994)

**Review date:** 2026-11-19  
**Source ID:** `philip-gage-byte-pair-compression-1994`  
**Collection:** `tokenization-embeddings`  
**Decision:** assign explicit membership.

## Evidence and rationale

The canonical record classifies this source under `text-tokenization` and links it to the bilingual tokenization-strategies and tokenizer-design-evaluation pages. The [primary-source audit](gage-1994-primary-audit.md) documents the paper's byte-pair substitution algorithm, byte alphabet, block constraints, substitution table, stack-based expansion and historical benchmark protocol. The [source migration map](tokenization-embeddings-source-migration-map-2026-11.md) explicitly places this source in the tokenization/embeddings migration family and points to the prior #114 / PR #155 evidence.

The assignment follows the documented source role and dossier mapping, not tags alone. Gage is a historical primary source for byte-pair compression; it is not treated as a specification for NLP subword tokenizers or GPT byte-level BPE.

## Evidence boundary retained

The source remains `partially-scanned`. C listings were inspected but not compiled or executed, and historical benchmark results were not independently reproduced. The accessible PDF is a 2020 reconstruction of the 1994 article. Licence status and figure/code reuse rights remain `unknown`; no permission is inferred.

This membership decision does not create an extraction or change concepts, pages, routes, learner content, scan status or integration status.

## Change

Add `collections: [tokenization-embeddings]` to this canonical source record only. Existing provenance, scan, integration, licence and reuse fields remain unchanged.


---

# Source-to-collection decision: Mikolov et al. (2013)

**Review date:** 2026-11-19  
**Source ID:** `mikolov-word2vec-2013`  
**Collection:** `tokenization-embeddings`  
**Decision:** assign explicit membership.

## Evidence and rationale

The canonical record maps the paper to the bilingual `embedding-space` and `contextualized-representations` pages, and identifies `token-embedding` and `contextualized-representation` as related concepts. The [collection synthesis](tokenization-embeddings-source-collection.md) explicitly treats Mikolov et al. as the historical source for static word-type vectors, contrasted with Transformer token lookup vectors and contextualized hidden states. The [migration map](tokenization-embeddings-source-migration-map-2026-11.md) places the paper in the token-embedding and representation-geometry source family.

The existing five-item extraction `data/extractions/mikolov-word2vec-2013.yml` records the log-linear architecture, CBOW, Skip-gram, Huffman hierarchical softmax and analogy-benchmark limitations, each with source locators and bilingual destinations. The primary paper's full arXiv v3 PDF and main architecture figure/evaluation tables were reviewed in the existing audit. This is a substantive embedding-foundations contribution, not a classification inferred from tags alone.

## Evidence boundary retained

The source remains `partially-scanned` and `integrated`. The historical implementation, pretrained vectors, linked follow-up paper and code were not independently retrieved or executed. The benchmark is English-centric and measures a narrow exact-match analogy task; it is not evidence of general semantic understanding or multilingual performance. The paper's hierarchical-softmax account is not conflated with later negative-sampling implementations.

Licence and figure/code/data reuse rights remain `unknown`; no permission is inferred. The existing extraction is reused; no duplicate extraction, new concept, page, route or learner-content change is proposed.

## Change

Add `collections: [tokenization-embeddings]` to this source record only. Preserve all existing scan, integration, licence, reuse and provenance fields.

---

# Source-to-collection decision: Li et al. (2020), BERT-flow

**Review date:** 2026-11-19  
**Source ID:** `li-bert-flow-sentence-embeddings-2020`  
**Collection:** `tokenization-embeddings`  
**Decision:** assign explicit membership to the existing canonical source record.

## Evidence and rationale

The canonical source record already identifies the published EMNLP 2020 paper, links it to the bilingual embedding-space and cosine-similarity lessons, and points to the tokenization/embeddings collection dossier and migration map. The existing extraction `data/extractions/li-bert-flow-sentence-embeddings-2020.yml` contains four source-scoped items: sentence-embedding construction from pooled BERT token states; anisotropic sentence-space geometry; the BERT-flow normalizing-flow transformation; and the target-distribution adaptation caveat. The collection dossier explicitly includes Li et al. in its sentence-embeddings-and-geometry family.

This is a clear fit for the collection's embedding-geometry scope. Membership is based on the existing primary-source audit, extraction and explicit dossier mapping, not tags or title matching alone.

## Evidence boundary retained

The source remains `partially-scanned` and `integrated`. The extraction covers the published paper's sentence-level BERT setup and reported STS experiments; the cited implementation and benchmark data were not independently executed. The target-flow setting uses unlabeled sentences from train, validation and test portions, so it must remain described as transductive-style rather than strictly inductive; no claim of test-label use is made. Results are not generalized to all token embeddings, sentence encoders or modern retrieval models.

Licence status remains `unknown`; figure, code and data reuse rights remain unresolved. The existing source record and extraction are reused. No duplicate source, extraction, audit, page, concept, route or learner-content change is created.

## Change

Add `collections: [tokenization-embeddings]` to the existing canonical source record only. Preserve all existing provenance, scan, integration, licence and reuse fields.


---

# Source-to-collection decision: Ethayarajh (2019)

**Review date:** 2026-11-19  
**Source ID:** `ethayarajh-contextualized-representations-2019`  
**Collection:** `tokenization-embeddings`  
**Decision:** assign explicit membership.

## Evidence and rationale

The tokenization/embeddings collection dossier explicitly places Ethayarajh among its sources for token and contextualized embeddings, and its cross-source synthesis uses the paper to distinguish static word-type vectors from contextualized representations and to qualify the interpretation of cosine similarity. The source migration map places it in the token and contextualized embeddings family and links the bilingual contextualized-representations and cosine-similarity lessons. The existing source record and structured extraction provide source-specific provenance rather than relying on topic tags alone.

The extraction records four atomic contributions: the paper's three contextuality measures (self-similarity, intra-sentence similarity and maximum explainable variance), anisotropy-adjusted random baselines, the layer-wise findings for the evaluated ELMo/BERT/GPT-2 models, and the study-specific static-vector explainability bound. These are directly within the collection's declared scope of token and contextualized embeddings and embedding geometry.

## Evidence boundary retained

The source remains `partially-scanned` and `integrated`. The primary EMNLP-IJCNLP 2019 PDF and the stated definitions, figures and results were reviewed, but model checkpoints and analysis code were not independently executed. The empirical findings remain specific to the evaluated ELMo, BERT and GPT-2 configurations, layers, datasets and anisotropy-corrected measures; they are not generalized to contemporary models or treated as evidence that a layer performs a named linguistic task.

Licence status remains `unknown`; figure, code and data reuse rights remain unresolved. No permission is inferred. The existing extraction is reused; no duplicate extraction, new scan claim, page, concept, route or learner-content change is proposed.

## Change

Add `collections: [tokenization-embeddings]` to this canonical source record only. Existing provenance, scan, integration, licence and reuse fields remain unchanged.
