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

# Source-to-collection decision: Ali et al. (2024)

**Review date:** 2026-11-19  
**Source ID:** `ali-tokenizer-choice-llm-training-2024`  
**Collection:** `tokenization-embeddings`  
**Decision:** assign explicit membership.

## Evidence and rationale

The canonical source record classifies the paper under `text-tokenization` and links it to both bilingual `tokenizer-design-evaluation` pages. The [cross-source collection dossier](tokenization-embeddings-source-collection.md) places Ali et al. in its multilingual tokenizer-evaluation family and distinguishes its controlled downstream-model study from token-count/compression-only studies. The [migration map](tokenization-embeddings-source-migration-map-2026-11.md) records the full-paper audit in #114 and PRs #332/#333.

The structured extraction `data/extractions/ali-tokenizer-choice-llm-training-2024.yml` preserves five atomic items: intrinsic versus extrinsic evaluation, the controlled decoder-only comparison, downstream results, limitations of fertility/parity as proxies, and the scenario-specific compute estimate. Its candidate destinations are exclusively the bilingual advanced tokenizer-evaluation pages. This direct mapping of the paper's documented role supports membership; tags alone are not the basis.

## Evidence boundary retained

The source remains `partially-scanned` and `integrated`. The published paper and selected result tables/figure were reviewed, but code, raw data, supplementary material and independent reproduction were not. The findings remain scoped to the study's 2.6B decoder-only models, five European languages, uneven task counts and single-seed design. The reported up-to-68% compute estimate is specific to one German-document comparison, not a general multiplier.

Licence and figure/code/data reuse rights remain `unknown`; no reuse permission is inferred. The extraction already exists, so no new extraction is created. No page, concept, route or learner-content change is proposed.

## Change

Add `collections: [tokenization-embeddings]` to this source record only. Preserve all existing scan, integration, licence, reuse and provenance fields.
