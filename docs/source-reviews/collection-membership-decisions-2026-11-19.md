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
