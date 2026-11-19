# Historical extraction reconciliation — 2026-11-19

**Repository:** `JM-Brun/llm-lab`  
**Audited branch snapshot:** `main` at `fcd5d04781408140f65a8ac49c9553bd6318c1c0`  
**Scope:** legacy extraction-level `scan` blocks and `canonical_mapping` blocks  
**Status:** all 36 scan identities, dates and ten-facet semantics compared; all 28 mappings and relation proposals reconciled; CI verification is required on the follow-up head

This is a conservative, evidence-linked reconciliation. A historical proposal is not proof of canonical integration. No canonical record, relation, route, source or validator rule is changed by this audit.

## 1. Executive findings

The repository inventory documents 36 extraction-level `scan` blocks and 28 `canonical_mapping` blocks. Direct inspection of all 96 extraction files first found 35 blocks; a second locator allowing leading whitespace identified the missing 36th block in `bdtech-next-concept-modeling-2026.yml`. The 36-file inventory is now reconciled. All 36 corresponding source records exist and have `scan_history` entries.

The 28 mapping blocks are all mappings. Their observed shape is:

| Field | Mappings |
|---|---:|
| `proposed_concepts` present | 27 |
| `proposed_relations` present | 28 |
| `route_implications` present | 28 |
| `decision_summary` present | 28 |
| non-empty `proposed_concepts` | 1 |
| non-empty `proposed_relations` | 2 |
| non-empty `route_implications` | 2 |
| non-empty `integrated_concepts` | 1 |

Interpretation:
- AiEdge is the only mapping with a proposed concept and structured relation objects.
- Marek/Ryabinin is the only mapping with `integrated_concepts` instead of `proposed_concepts`; its six relation proposals are plain-language strings, not normalized relation records.
- The other 26 mappings have empty proposed concept/relation/route lists. Their decision summaries still carry editorial decisions and evidence; empty lists do not mean the source itself is obsolete or irrelevant.

## 2. Complete inventory of the 28 mappings

| # | Extraction | Decision supported by the mapping text |
|---:|---|---|
| 1 | `ahia-do-all-languages-cost-the-same-2023` | **Non-change.** Socio-economic/token-cost dimension is complementary; no new concept or route step. |
| 2 | `aiedge-how-cuda-graphs-speed-up-llm-inference` | **Deferred.** Partial extraction; preserve two candidate relations and a candidate CUDA Graph concept pending full article/figure inspection. |
| 3 | `ali-tokenizer-choice-llm-training-2024` | **Integrated by reference.** Findings are already in the advanced bilingual lesson; no new page, concept or route. |
| 4 | `arnett-explaining-mitigating-crosslingual-tokenizer-inequities-2025` | **Non-change.** Preserve the distinctions and evidence; no new canonical concept or route. |
| 5 | `chiu-toklens-acl-srw-2026` | **Non-change.** Evaluation framework and statistical qualifications are complementary; no new concept or route. |
| 6 | `codefinity-qkv-building-blocks` | **Partially integrated.** Geometric and lexical perspectives are included as bounded optional material in the Q/K/V lesson; assessment references retained, no graph/route change. |
| 7 | `dailydose-augsbert-sentence-similarity-2024` | **Partially integrated.** Bi-/cross-encoder roles belong in existing retrieval material; AugSBERT remains optional because implementation details are paywalled. |
| 8 | `dailydose-bi-cross-encoders-sentence-similarity-2024` | **Partially integrated.** Static/contextualized representation distinction and pairwise scoring are useful; paywalled material is not treated as evidence for architecture details. |
| 9 | `dailydose-foundations-rag-2024` | **Partially integrated.** Introductory RAG pipeline is already covered; cross-encoder reranking after retrieval is the incremental contribution. |
| 10 | `ethayarajh-contextualized-representations-2019` | **Integrated by reference.** Geometric measures and anisotropy cautions are already reflected; retain precise scope as evidence. |
| 11 | `faysse-etal-2025-colpali` | **Non-change.** Preserve task scope, offline/online distinction and internal sample-size discrepancy; no graph/route proposal. |
| 12 | `formal-piwowarski-clinchant-2021-splade` | **Non-change.** Existing bilingual retrieval pages and concepts suffice. |
| 13 | `goldman-unpacking-tokenization-2024` | **Non-change.** Preserve protocol-specific result and limitations; do not promote compression to a universal KPI. |
| 14 | `jothi-moorthy-llm-processing-linkedin` | **Obsolete/redundant as an integration candidate.** Mapping calls the overview redundant; retain provenance and caveats rather than adding canonical content. |
| 15 | `khattab-zaharia-2020-colbert` | **Non-change.** Preserve the historical architecture and benchmark boundaries; no concept/relation/route proposal. |
| 16 | `li-bert-flow-sentence-embeddings-2020` | **Non-change.** Retain the BERT anisotropy/calibration evidence and its transductive/configuration limits; no new curriculum step. |
| 17 | `marek-ryabinin-score-centering-off-policy-rl-2026` | **Partially integrated.** Six concepts are listed under `integrated_concepts`; six relation proposals remain prose and require explicit semantic review before graph changes. |
| 18 | `mikolov-word2vec-2013` | **Non-change.** Existing static/contextualized representation material suffices; preserve source-specific CBOW/Skip-gram evidence. |
| 19 | `philip-gage-byte-pair-compression-1994` | **Integrated by reference.** Use as the byte-pair compression primary source; keep distinct from NLP subword BPE and GPT byte-level tokenization. |
| 20 | `poloclub-transformer-explainer-paper-2026` | **Partially integrated.** Link to existing Transformer/learning-science pages; retain study design and limitations, no causal or long-term learning claims. |
| 21 | `reimers-gurevych-2019-sentence-bert` | **Non-change.** Preserve SBERT pooling/objective and benchmark qualifications; no new concept or route. |
| 22 | `santhanam-etal-2022-colbertv2` | **Non-change.** Preserve denoising, compression and benchmark evidence with language/configuration limits. |
| 23 | `schmidt-tokenization-more-than-compression-2024` | **Non-change.** Retain as a counterpoint to Goldman et al.; no universal conclusion. |
| 24 | `sennrich-subword-nmt-2016` | **Integrated by reference.** Cite as the NLP adaptation of pair merging; keep separate from GPT-style byte-level tokenization. |
| 25 | `steck-cosine-similarity-embeddings-2024` | **Non-change.** Preserve the restricted mathematical counterexample; no new canonical concept or route. |
| 26 | `thakur-etal-2021-beir` | **Non-change.** Preserve heterogeneous zero-shot evaluation and annotation/protocol limits. |
| 27 | `varis-stephen-libovicky-tokcollate-2026` | **Deferred.** Optional advanced reference only after independent inspection of repository/live interface; no page/route/graph/exercise mutation yet. |
| 28 | `wegmann-tokenization-language-variation-2025` | **Integrated by reference.** Task-objective lens is already integrated in the advanced bilingual deep dive. |

These are decisions recorded by the mapping text, not a fresh audit of every downstream page. “Integrated by reference” means the mapping says the substance is already covered; it does not assert a dedicated canonical relation edge.

## 3. Exact relation reconciliation

### 3.1 AiEdge — two structured proposals

Current concept relation vocabulary is declared in `data/concepts.yml`. It includes `represented-by`, `prerequisite`, `part-of`, `constrains`, `contributes-to`, `applies-to`, `mapped-by`, `produces`, `normalized-by`, `contrasts-with`, and `evaluated-by`. It does not include `optimizes` or `complements`.

| Proposal | Endpoint status | Relation-type status | Exact canonical edge? | Decision |
|---|---|---|---|---|
| `cuda-graphs —optimizes→ decode-step` | `decode-step` exists; `cuda-graphs` does not | `optimizes` is not declared | No | **Not representable as-is; deferred candidate.** Do not add an edge or concept from partial source evidence. |
| `cuda-graphs —complements→ kv-cache` | `kv-cache` exists; `cuda-graphs` does not | `complements` is not declared | No | **Not representable as-is; deferred candidate.** The decision summary explicitly distinguishes execution-plan replay from KV reuse. |

Neither proposal matches a canonical relation by endpoint/type triple. The existing `decode-step` and `kv-cache` concepts do not establish integration of the proposed CUDA Graph node.

### 3.2 Marek/Ryabinin — six prose proposals

The six proposals are strings rather than records with `from`, `type`, and `to`; they cannot be matched mechanically as canonical edges without editorial normalization.

| Historical proposal | Relevant canonical edges already present | Exact match? | Classification |
|---|---|---:|---|
| policy-gradient uses score-function | `score-function —part-of→ policy-gradient` | No exact normalized triple; semantic coverage exists | **Already covered in the canonical graph.** The score-function concept is a component of policy-gradient; no duplicate edge is needed. |
| off-policy-reinforcement-learning creates training-inference-mismatch | `off-policy-reinforcement-learning —part-of→ post-training`; `training-inference-mismatch —constrains→ policy-gradient` | No | **Context partially covered, causal claim not represented.** “Creates” is stronger than the current edges and no declared relation type expresses this causal claim safely. |
| training-inference-mismatch can induce policy-drift | No canonical `policy-drift` concept was found | No | **Not representable as-is.** The page explains the drift mechanism, but a graph edge would require an explicit concept decision and evidence review. |
| score-centering corrects score-function drift | `score-function —prerequisite→ score-centering`; `score-centering —applies-to→ off-policy-reinforcement-learning` | No | **Covered by bilingual lesson, not by an equivalent graph edge.** The page explains the additive correction; do not reinterpret prerequisite/applies-to as “corrects”. |
| importance-sampling reweights off-policy samples | `importance-sampling —applies-to→ off-policy-reinforcement-learning` | No | **Covered by concept definition and bilingual lesson; graph records context only.** No additional edge is required to restate the definition. |
| score-centering composes with compatible importance-sampling corrections | `importance-sampling —contrasts-with→ score-centering` | No | **Covered by bilingual lesson, not by graph edge.** Composition is conditional: supported for compatible ratio-based corrections and rejected for the TV-based case. `contrasts-with` means conceptual distinction, not incompatibility or composition. |

Relevant canonical neighborhood edges (all exact triples in `data/concepts.yml`):
- `policy-gradient —part-of→ post-training`
- `score-function —part-of→ policy-gradient`
- `off-policy-reinforcement-learning —part-of→ post-training`
- `training-inference-mismatch —constrains→ policy-gradient`
- `score-centering —applies-to→ off-policy-reinforcement-learning`
- `importance-sampling —applies-to→ off-policy-reinforcement-learning`
- `importance-sampling —contrasts-with— score-centering`

**Conclusion:** one proposal is already covered semantically by a canonical edge; three are covered in the bilingual page/definitions but not by an equivalent graph edge; one is not representable because `policy-drift` is absent; and one causal proposal is too strong for the available relation vocabulary. None should be promoted as a new canonical edge. The page's importance-sampling composition claim remains conditional on the implementation contract. Do not infer an edge or reverse a relation from prose alone.

## 4. Historical scan locator — all 36 identified

The first-pass exact-key locator found 35 files; the broader locator found the final `bdtech-next-concept-modeling-2026` record. The complete list is:

- `ahia-do-all-languages-cost-the-same-2023`
- `aiedge-how-cuda-graphs-speed-up-llm-inference`
- `ali-tokenizer-choice-llm-training-2024`
- `alliancy-la-compression-strategie-avenir-llm-2026`
- `andrej-karpathy-gpt-tokenizer-video`
- `arnett-explaining-mitigating-crosslingual-tokenizer-inequities-2025`
- `bdtech-next-concept-modeling-2026`
- `chiu-toklens-acl-srw-2026`
- `dailydose-augsbert-sentence-similarity-2024`
- `dailydose-bi-cross-encoders-sentence-similarity-2024`
- `dailydose-foundations-rag-2024`
- `ethayarajh-contextualized-representations-2019`
- `faysse-etal-2025-colpali`
- `formal-piwowarski-clinchant-2021-splade`
- `goldman-unpacking-tokenization-2024`
- `hesam-sheikh-llm-study-roadmap-2024`
- `jose-parreno-garcia-how-llms-work-three-layers-2025`
- `jothi-moorthy-llm-processing-linkedin`
- `karthik-shashidhar-llms-compression-algorithms-2024`
- `khattab-zaharia-2020-colbert`
- `lewish-intelligence-and-compression-2025`
- `li-bert-flow-sentence-embeddings-2020`
- `marek-ryabinin-score-centering-off-policy-rl-2026`
- `maarten-grootendorst-visual-guide-multimodal-generation`
- `mikolov-word2vec-2013`
- `poloclub-transformer-explainer-paper-2026`
- `reimers-gurevych-2019-sentence-bert`
- `santhanam-etal-2022-colbertv2`
- `sasirekha-cota-understanding-llm-compression-2023`
- `schmidt-tokenization-more-than-compression-2024`
- `sennrich-subword-nmt-2016`
- `sourav-mukherjee-compression-intelligence-2026`
- `steck-cosine-similarity-embeddings-2024`
- `thakur-etal-2021-beir`
- `varis-stephen-libovicky-tokcollate-2026`
- `wegmann-tokenization-language-variation-2025`

### Source-history correspondence and content differences

All 36 extraction `scan.accessed_at` dates occur in the corresponding source record's `scan_history`. For 34 records, the extraction scan date is also the latest source-history date. Two records have later source-history events that are not represented by the extraction-level scan snapshot:

- `andrej-karpathy-gpt-tokenizer-video`: extraction scan is dated 2026-10-30; source history also records a 2026-11-19 metadata-only check of the official YouTube title, creator and publication date. This is an additional event, not evidence that the 2026-10-30 transcript inspection was superseded.
- `maarten-grootendorst-visual-guide-multimodal-generation`: extraction scan is dated 2026-11-07; source history adds a 2026-11-15 event covering the original bilingual Deepen pages, a Mermaid map/tables, four live article image elements, and navigation updates. That later work is not reflected in the extraction-level scan block.

A concrete content comparison is available for AiEdge. Its extraction scan separates the partial indexed author text, uninspected figures/code/comments/linked resources, partial metadata, unknown rights, and three explicit unresolved questions (full article/figures, original assets/code/links/references, and possible vLLM-specific settings or measurements). The source event on the same date compresses this into three inspected-scope bullets and five limitations. It preserves the broad retrieval caveats, but not the ten facet-level status/coverage/notes or the three questions as separate structured entries. This is a real example of richer extraction-level facet detail alongside a more concise chronological event summary—not evidence that one record can replace the other.

The content models are not structurally equivalent. Each extraction `scan` is a ten-key facet snapshot (`accessed_at`, `retrieval_method`, `author_text`, `figures_media`, `code_data`, `comments`, `linked_resources`, `metadata`, `rights`, `unresolved_questions`). Source `scan_history` is an append-only event list with `accessed_at`, `status`, `inspected_scope`, and `limitations`. Therefore a date match is not content equality: facet-level evidence and unresolved questions cannot be reconstructed losslessly from the source event summary without a deliberate migration mapping. The two later source events are unique chronological content and must remain preserved.

The current comparison establishes identity/date correspondence for all 36 and two clear later-event differences. A field-by-field semantic comparison of all facet notes against each event's `inspected_scope` and `limitations` remains required before declaring any field duplicated, richer, stale or safe to migrate.


### Semantic comparison completed — all 36 scans

The comparison was performed facet-by-facet against each corresponding source event: `author_text`, `figures_media`, `code_data`, `comments`, `linked_resources`, `metadata`, `rights`, `unresolved_questions`, plus the scan timestamp and retrieval method. The ten-key extraction shape is invariant, but the event shape is intentionally coarser: source-level `scan_history` records an overall status, inspected scope and limitations. It is not a second copy of the ten-facet snapshot. “Aligned” below means that the event supports the extraction's account; it does not mean the text is identical.

| # | Source | Semantic comparison and decision |
|---:|---|---|
| 1 | `ahia-do-all-languages-cost-the-same-2023` | **Aligned; facet-richer extraction.** The 2026-11-05 event supports the full EMNLP PDF and figures. The extraction adds explicit facet statuses, the ten-figure scope and two reproducibility/current-price questions. |
| 2 | `aiedge-how-cuda-graphs-speed-up-llm-inference` | **Aligned but materially more granular extraction.** The same-date event compresses the scan into three scope bullets and five limitations. It does not preserve the per-facet “not inspected/unknown” states or the three separate unresolved questions. Keep both representations; neither reconstructs the other losslessly. |
| 3 | `ali-tokenizer-choice-llm-training-2024` | **Aligned; facet-richer extraction.** The 2026-11-05 event covers the same PDF, protocol, results and limitations. The extraction separates figures, code, linked resources, rights and seed/reproducibility questions. |
| 4 | `alliancy-la-compression-strategie-avenir-llm-2026` | **Aligned; extraction carries more explicit open questions.** Both records cover the article and the later official challenge corroboration. The extraction preserves four separate unresolved technical/evidence questions and details the Epoch.AI attribution boundary. |
| 5 | `andrej-karpathy-gpt-tokenizer-video` | **Stale facet snapshot relative to later source event.** The 2026-10-30 transcript scan remains valid historical provenance. The 2026-11-19 source event verifies the official title, creator and publication date (2024-02-20), while the extraction metadata still says the exact date was not recorded and retains it as unresolved. Do not overwrite the transcript scan; the later metadata event supersedes only that metadata gap. |
| 6 | `arnett-explaining-mitigating-crosslingual-tokenizer-inequities-2025` | **Aligned; facet-richer extraction.** The 2026-11-05 event supports the published NeurIPS PDF, selected figures and five-item extraction. The ten facets retain the distinction between paper/code inspection and independent execution, plus the downstream-model-quality limitation. |
| 7 | `bdtech-next-concept-modeling-2026` | **Aligned; facet-richer extraction.** The 2026-11-09 event supports the full indexed article, Stanford project and official repository README. The extraction separately records figure non-inspection, partial code/resource review and four unresolved implementation/benchmark questions. This is the recovered 36th scan. |
| 8 | `chiu-toklens-acl-srw-2026` | **Aligned; facet-richer extraction.** The 2026-11-05 event supports the paper, figures and README review. The extraction retains the critical denominator distinction (24 tokenizers/15 languages versus 7 models/11 languages) and the unexecuted-code boundary. |
| 9 | `dailydose-augsbert-sentence-similarity-2024` | **Aligned.** The event matches the canonical HTML/paywall boundary and metadata review. The extraction makes image placeholders, uninspected code and the paper/code follow-up explicit. |
| 10 | `dailydose-bi-cross-encoders-sentence-similarity-2024` | **Aligned.** The event matches the introduction, BERT background and paywall boundary. The extraction's unresolved question correctly prevents attributing the inaccessible Part 1 comparison to the source. |
| 11 | `dailydose-foundations-rag-2024` | **Aligned.** The event matches the visible pipeline through reranking and paywall. The extraction separately records the vector-database-centered framing as non-universal and that retrieval does not guarantee factual grounding. |
| 12 | `ethayarajh-contextualized-representations-2019` | **Aligned; later event refines the earlier abstract-level event.** The 2026-11-05 event supports the complete focused PDF review; the extraction keeps the specific measures, figures and model-family boundary. |
| 13 | `faysse-etal-2025-colpali` | **Aligned; extraction more precise.** The 2026-11-18 event covers Table 2, latency/storage and Appendices B.3–B.4. The extraction explicitly preserves the paper's 100-page versus 1,000-document discrepancy and the distinction between Figure 2 and Table 5 protocols. |
| 14 | `formal-piwowarski-clinchant-2021-splade` | **Aligned; extraction more precise.** The 2026-11-18 event covers the formulation and evaluation. Both records preserve the 100-versus-1,000 sample discrepancy; the extraction additionally separates equations, figures and production-latency caveats. |
| 15 | `goldman-unpacking-tokenization-2024` | **Aligned.** The event and extraction cover the same ACL PDF, English/Turkish protocols, result tables and correlations. The extraction makes the three-condition Turkish downstream experiment and no-reproduction boundary explicit. |
| 16 | `hesam-sheikh-llm-study-roadmap-2024` | **Aligned; extraction facet-richer.** The event supports mirror-based article reconstruction and Days 003–016. The extraction preserves the per-day sequence, inaccessible image/PDF assets, book-derived image rights and the non-generalizability of the author's two-week duration. |
| 17 | `jose-parreno-garcia-how-llms-work-three-layers-2025` | **Aligned.** The event supports the complete visible article and both images. The extraction separately excludes reader comments as author evidence and keeps the Llama/DeepSeek comparison anecdotal and uncontrolled. |
| 18 | `jothi-moorthy-llm-processing-linkedin` | **Aligned.** Both records say the text and author metadata were visible, the image bytes were unavailable, the publication date was not verifiable and the complete comment thread/newsletter was not inspected. |
| 19 | `karthik-shashidhar-llms-compression-algorithms-2024` | **Aligned.** The event supports the full opinion article and visible discussion excerpt. The extraction separates absent code/benchmarks and retains three open questions about training-data frequency, transfer and model-size comparisons. |
| 20 | `khattab-zaharia-2020-colbert` | **Aligned; latest event supersedes the abstract-level event.** The 2026-11-18 event supports architecture, equations and selected tables. The extraction preserves the exact hardware/pipeline boundary for latency comparisons and the non-executed repository status. |
| 21 | `lewish-intelligence-and-compression-2025` | **Aligned with additional source-history detail.** The event and extraction both record nine sections, the AI-generated musical-score asset and author attribution. The event records more of the checked outbound references; the extraction correctly leaves the compressor configuration and benchmark reproduction unresolved. |
| 22 | `li-bert-flow-sentence-embeddings-2020` | **Aligned; latest event refines the earlier review.** The 2026-11-05 event supports the full focused PDF review and explicitly records the train/validation/test target-sentence calibration. The extraction retains the transductive-style caveat and non-executed repository. |
| 23 | `marek-ryabinin-score-centering-off-policy-rl-2026` | **Materially stale source history, now reconciled.** The original 2026-11-09 event says only selected alphaXiv sections were reviewed and official tests were not run; the extraction records a later full canonical PDF/appendix audit and seven passing CPU test cases. A separate 2026-11-19 source-history event has now been appended to document that later work. The original extraction scan date and original source event are preserved. |
| 24 | `maarten-grootendorst-visual-guide-multimodal-generation` | **Stale facet snapshot relative to later source events.** The 2026-11-07 extraction says article figures were not inspected. Source history adds 2026-11-15 work: four in-body image elements inspected, original bilingual Deepen pages and Mermaid/tables created, and navigation updated. The article's advertised 50+ visuals remain unreconciled; do not change the extraction's broad figure status without a scoped new facet record. |
| 25 | `mikolov-word2vec-2013` | **Aligned; latest event refines the earlier scope.** The 2026-11-05 event supports the full arXiv v3 PDF and figures. The extraction preserves the distinction from later negative-sampling implementations and the English-centric analogy benchmark. |
| 26 | `poloclub-transformer-explainer-paper-2026` | **Aligned; latest event supersedes earlier partial events.** The 2026-11-19 event supports the published CHI paper, Figures 1–12, Table 1 and CC BY 4.0 statement. The extraction correctly keeps repository/raw-data audit and reproduction open, and does not infer reuse rights for third-party assets. |
| 27 | `reimers-gurevych-2019-sentence-bert` | **Aligned; latest event refines the abstract-level event.** The 2026-11-18 event supports the full focused PDF and six extraction items. The extraction retains the 2019 hardware and task/language scope. |
| 28 | `santhanam-etal-2022-colbertv2` | **Aligned; latest event refines the abstract-level event.** The 2026-11-18 event supports the architecture, selected tables and dossier. The extraction preserves English-only evaluation, judgment false negatives and non-reproduction. |
| 29 | `sasirekha-cota-understanding-llm-compression-2023` | **Aligned.** The event supports the complete introductory article and abstract-level checks of selected primary papers. The extraction keeps the article's non-systematic scope and four implementation/evaluation questions. |
| 30 | `schmidt-tokenization-more-than-compression-2024` | **Aligned.** The 2026-11-18 event supports the full EMNLP PDF, PathPiece and English-only setup. The extraction retains non-executed artifacts and the language-generalization limit. |
| 31 | `sennrich-subword-nmt-2016` | **Aligned.** The 2026-11-18 event supports Algorithm 1, Figure 1, WMT tables and the historical BPE distinction. The extraction explicitly prevents conflation with GPT byte-level BPE. |
| 32 | `sourav-mukherjee-compression-intelligence-2026` | **Aligned with additional editorial/research activity in source history.** The event also records a toy entropy-versus-surprisal experiment and several follow-up papers; these are project-side corroboration, not additional article content. The extraction correctly keeps the article's own low-entropy reasoning-token pruning claim unverified. |
| 33 | `steck-cosine-similarity-embeddings-2024` | **Aligned; latest event refines the earlier review.** The 2026-11-05 event supports both regularization objectives, diagonal rescaling and simulated-data scope. The extraction prevents generalization to arbitrary nonlinear LLM embeddings. |
| 34 | `thakur-etal-2021-beir` | **Aligned; latest event refines the abstract-level event.** The 2026-11-18 event supports benchmark composition and lexical-judgment bias. The extraction keeps the 18 zero-shot datasets distinct from MS MARCO reference/training rows. |
| 35 | `varis-stephen-libovicky-tokcollate-2026` | **Aligned.** The 2026-11-05 event supports all ten paper pages and records that repository/live demo were not inspected. The extraction keeps software licence, implementation and live accessibility unverified. |
| 36 | `wegmann-tokenization-language-variation-2025` | **Aligned; latest event supersedes abstract-level review.** The 2026-11-05 event supports the full ACL PDF and five pre-tokenizer settings. The extraction preserves the English/BERT-base scope and explicitly distinguishes it from cross-lingual inequity evidence. |

#### Cross-cutting findings

- No extraction facet can be reconstructed losslessly from `scan_history`: the event model has no per-facet status, coverage, notes, or separate unresolved-question field. Similar wording is not equality.
- The source event's overall `partially-scanned` status is not interchangeable with a facet status such as `complete`, `partial`, `not-inspected`, `unavailable`, or `unknown`.
- Three sources require explicit stale/divergence handling: Andrej Karpathy (later metadata verification), Marek/Ryabinin (later full-paper and code-test audit), and Maarten Grootendorst (later page/visual/navigation work). Sourav Mukherjee has additional project-side experiment/research activity in the source event that must not be misattributed to the article.
- The correct reconciliation is append-only provenance plus an explicit comparison report. Do not migrate, overwrite, or delete either historical representation.

The ten-facet semantic comparison is complete at the level of all 36 scan records and their corresponding source events. It does not authorize automatic field migration or a second canonical registry.

## 5. Compatibility and non-regression contract

The historical fields remain optional legacy data. The following invariants should be tested before any validator change:

1. Absence of top-level `scan` or `canonical_mapping` is accepted.
2. Existing scan mappings are preserved losslessly during the compatibility window.
3. The scan comparison distinguishes exact equality, source-only fields, extraction-only fields, conflicting values and stale timestamps/metadata; it must not overwrite either record.
4. A mapping's proposal is never interpreted as integration merely because its endpoint IDs resolve.
5. Canonical relation identity is the exact tuple `(from, type, to)`; symmetric relation semantics are normalized only according to the canonical relation-type metadata.
6. Candidate relations with undeclared relation types or missing endpoints remain report-only/editorial decisions, not automatic validator errors.
7. Prose relation proposals remain unparsed until a human-approved normalization provides endpoints, type, rationale and evidence.
8. Empty proposal lists are not errors and do not imply source obsolescence.
9. Historical `integrated_concepts` is not treated as a canonical registry; each ID must be checked against `data/concepts.yml` and its actual page/source coverage.
10. No route is inferred from `route_implications`, source-local `teaching_route`, or `comparison.canonical_routes`.

## 6. Fixtures and tests still required

Build real fixtures from the repository records after the 36th scan is found and its source-level counterpart is retrieved:

- `scan-identical.yml`: same ten fields and same values at source and extraction level.
- `scan-source-richer.yml`: source-only keys/values, with extraction record retained.
- `scan-extraction-richer.yml`: extraction-only keys/values, with source record retained.
- `scan-conflict.yml`: same key, different values; report conflict without choosing a winner.
- `scan-stale.yml`: timestamps or retrieval metadata differ; preserve chronology.
- `mapping-aiedge-unrepresentable.yml`: candidate node and undeclared relation types.
- `mapping-marek-prose-relations.yml`: prose-only relation proposals plus existing canonical neighborhood.
- `mapping-already-covered.yml`: empty proposals and a decision summary pointing to existing content.
- `mapping-deferred.yml`: proposal explicitly deferred pending source inspection.
- `mapping-obsolete.yml`: redundant source retained for provenance, no canonical mutation.

The implemented regression tests assert:
- exact source/extraction identity pairing by `source_id`, not filename guesswork;
- lossless preservation of all historical blocks;
- the four scan-difference classes above;
- exact relation tuple matching, plus explicit handling of symmetric types;
- missing endpoint and unknown relation-type diagnostics;
- no mutation of canonical registries from candidate-only or prose proposals;
- deterministic report output and stable counts.

**Verification status:** tests are committed, but a successful run on the latest PR head has not yet been observed. The initial CI attempt found formatting issues, which were corrected in subsequent commits; the cancelled test run must not be treated as a pass.

## 7. Remaining ordered work

1. Find the 36th scan using parser-level key detection and produce the 36-file list.
2. Retrieve source-level `scan_history` for all 36 source IDs; compare the ten fields and record differences without migration.
3. Verify all six Marek concepts under `integrated_concepts` against canonical IDs, definitions, pages and source evidence. All six IDs resolve in `data/concepts.yml`; page-level support and source evidence still require individual review. Do not infer relation integration.
4. Decide whether any Marek prose relation should be normalized; retain non-representable propositions if no declared relation expresses them accurately.
5. Keep both AiEdge relations deferred until full source inspection; do not extend the relation vocabulary solely to accommodate them.
6. Build the real fixtures and tests above; run focused tests, full Python tests, inventory and relevant CI on the new commit.
7. Update `docs/extraction-destination-inventory.md` only after the new report has been regenerated from the current corpus.

## 8. Explicit non-changes

- No canonical concept, relation, page, resource or route was added or removed.
- No `scan` block was migrated, deleted or rewritten.
- No validator rule was tightened.
- No new relation type was introduced.
- No candidate destination or historical prose proposal was promoted to an integrated canonical edge.
