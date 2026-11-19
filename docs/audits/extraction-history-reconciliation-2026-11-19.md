# Historical extraction reconciliation — 2026-11-19

**Repository:** `JM-Brun/llm-lab`  
**Audited branch snapshot:** `main` at `fcd5d04781408140f65a8ac49c9553bd6318c1c0`  
**Scope:** legacy extraction-level `scan` blocks and `canonical_mapping` blocks  
**Status:** all 36 scan identities, dates and semantic differences reconciled; all 28 mappings and relation proposals reconciled; Marek's six integrated concepts verified against canonical IDs and bilingual pages; historical audit CI passed on merged PR #1383

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
| policy-gradient uses score-function | `score-function —part-of→ policy-gradient` | No (direction and predicate differ) | **Already covered conceptually**, but proposal wording is not a canonical triple. |
| off-policy-reinforcement-learning creates training-inference-mismatch | `off-policy-reinforcement-learning —part-of→ post-training`; `training-inference-mismatch —constrains→ policy-gradient` | No | **Partially covered**, not an equivalent causal edge. |
| training-inference-mismatch can induce policy-drift | No canonical `policy-drift` concept was found | No | **Not currently representable** without a concept decision and evidence review. |
| score-centering corrects score-function drift | `score-centering —applies-to→ off-policy-reinforcement-learning`; `attention-score —contrasts-with→ score-centering` | No | **Partially covered** by method/context associations; correction claim is not encoded. |
| importance-sampling reweights off-policy samples | `importance-sampling —applies-to→ off-policy-reinforcement-learning` | No | **Partially covered**; the edge records applicability, not the reweighting mechanism. |
| score-centering composes with compatible importance-sampling corrections | `importance-sampling —contrasts-with→ score-centering` | No | **Not represented.** The current symmetric `contrasts-with` relation explicitly means “distinguish these concepts”, not incompatibility; it does not assert composition. |

Relevant canonical neighborhood edges (all exact triples in `data/concepts.yml`):
- `policy-gradient —part-of→ post-training`
- `score-function —part-of→ policy-gradient`
- `off-policy-reinforcement-learning —part-of→ post-training`
- `training-inference-mismatch —constrains→ policy-gradient`
- `score-centering —applies-to→ off-policy-reinforcement-learning`
- `importance-sampling —applies-to→ off-policy-reinforcement-learning`
- `importance-sampling —contrasts-with— score-centering`

**Conclusion:** no one of the six historical prose proposals is an exact duplicate of a canonical edge. Four are partially covered by the current graph neighborhood; one references a missing `policy-drift` concept; the final compatibility/composition claim is not represented. Do not infer any edge or reverse a relation based on wording alone.

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

### Source-history correspondence and content differences — completed 2026-11-19

The semantic comparison was completed against the corresponding source-history event for each of the 36 extraction snapshots. The comparison is semantic rather than a YAML equality test: the extraction snapshot has ten keys (retrieval method plus eight evidence facets and date), while a source-history event has four keys (accessed_at, status, inspected_scope, limitations). The source event is a chronology; the extraction is a faceted snapshot. They are not losslessly interchangeable.

| Measure | Result |
|---|---:|
| Extraction scans with a source-history event on the exact same date | 36 / 36 |
| Records whose latest source-history event is the extraction scan date | 33 / 36 |
| Records with a later source-history event | 3 / 36 |
| Records with structurally identical scan/history objects | 0 / 36 (different contracts) |

The three later source-history events are distinct additions, not automatically superseding scans:
- Karpathy tokenizer video: 2026-11-19 checks official YouTube title, creator and publication date only; it does not replace the 2026-10-30 transcript/chapter review.
- Maarten Grootendorst guide: 2026-11-15 records bilingual Deepen-page work and inspection of four article image elements; it does not complete the advertised inventory of 50+ visuals.
- Marek/Ryabinin: the original 2026-11-09 source event was stale relative to the extraction snapshot (it said the canonical PDF and official tests had not been checked). A new 2026-11-19 source event was appended to record the 16-page arXiv v1 PDF/appendix review and the seven passing upstream test cases, together with the JAX-version caveat. The historical 2026-11-09 event was retained, not rewritten.

#### Per-record comparison matrix

“Aligned” means the event scope and limitations support the same inspected material and caveats as the extraction snapshot. “Facet detail” means the extraction adds statuses, coverage, notes or unresolved questions that the event compresses into scope/limitations. Neither label means the two records are identical.

| Source ID | Matched scan date | Semantic comparison |
|---|---:|---|
| ahia-do-all-languages-cost-the-same-2023 | 11-05 | Aligned. The event covers the full paper, figures and table; the extraction separates uninspected code/data, unknown reuse rights and historical API-price/reproducibility questions. |
| aiedge-how-cuda-graphs-speed-up-llm-inference | 11-06 | Aligned with facet detail. The three scope bullets and five limitations summarize the same indexed excerpt; the extraction separately marks figures/code/comments/links uninspected and preserves three explicit open questions. |
| ali-tokenizer-choice-llm-training-2024 | 11-05 | Aligned. The event captures the controlled setup/results; the extraction makes the no-reproduction and single-seed caveats explicit by facet. |
| alliancy-la-compression-strategie-avenir-llm-2026 | 11-17 | Aligned. The event includes the later official challenge/UNESCO checks; the extraction preserves four operational questions and distinguishes secondary parameter-growth reporting from corroborated challenge facts. |
| andrej-karpathy-gpt-tokenizer-video | 10-30 | Aligned for the transcript/chapter snapshot. The separate 11-19 metadata-only event is source-history-only and does not imply audiovisual inspection. |
| arnett-explaining-mitigating-crosslingual-tokenizer-inequities-2025 | 11-05 | Aligned with facet detail. The extraction distinguishes figures, linked code/data, metadata and rights; the event preserves the study's 97-language design and downstream-LM limitation. |
| bdtech-next-concept-modeling-2026 | 11-09 | Aligned. Both records cover indexed article text plus primary-paper/project/repository cross-checks; the extraction keeps figures uninspected and lists implementation/reproduction questions. |
| chiu-toklens-acl-srw-2026 | 11-05 | Aligned. The event and extraction both preserve the 24-tokenizer/15-language intrinsic versus 7-model/11-language MMLU-ProX denominator distinction. |
| dailydose-augsbert-sentence-similarity-2024 | 11-17 | Aligned. Both stop at the paywall boundary; the extraction records image placements, no code/data inspection and the unresolved need for primary paper/code. |
| dailydose-bi-cross-encoders-sentence-similarity-2024 | 11-17 | Aligned. Both explicitly stop before inaccessible Part 1 details; the extraction separates visible background from inaccessible comparisons and uninspected image assets. |
| dailydose-foundations-rag-2024 | 11-17 | Aligned. Both stop after cross-encoder reranking; the extraction adds the non-universality of vector databases and the fact that retrieval alone does not ensure correctness. |
| ethayarajh-contextualized-representations-2019 | 11-05 | Aligned. The extraction decomposes mathematical measures, figures, code, rights and model-family limits; the event summarizes the same PDF review. |
| faysse-etal-2025-colpali | 11-18 | Aligned with an earlier 11-17 abstract event. The extraction preserves the internal 100-versus-1,000 sample-size discrepancy and distinguishes Figure 2 from Table 5 protocols. |
| formal-piwowarski-clinchant-2021-splade | 11-18 | Aligned with an earlier 11-17 abstract event. The extraction identifies equations, Table 1 and paper-specific efficiency limits; the event records the same primary audit and unresolved sample-size discrepancy. |
| goldman-unpacking-tokenization-2024 | 11-18 | Aligned with an earlier 10-29 migration note. The extraction separates English/Turkish protocol, tables, unknown rights and reproduction questions; the event records the correlation-table review and Turkish subset limitation. |
| hesam-sheikh-llm-study-roadmap-2024 | 11-17 | Aligned. The event lists the Day 003–016 sequence; the extraction separately records mirror retrieval, uninspected PDFs/images, author-reported durations and the author's prior-experience caveat. |
| jose-parreno-garcia-how-llms-work-three-layers-2025 | 11-17 | Aligned. The event covers both inspected images and the visible comment; the extraction excludes community content from author claims and records missing prompts/evaluation conditions. |
| jothi-moorthy-llm-processing-linkedin | 11-17 | Aligned. Both record the five-stage post and failed image retrieval; the extraction makes the relative/unverified publication date and unknown asset rights explicit. |
| karthik-shashidhar-llms-compression-algorithms-2024 | 11-16 | Aligned. Both treat the piece as opinion rather than empirical research and distinguish the visible reader comment from author evidence. |
| khattab-zaharia-2020-colbert | 11-18 | Aligned with an earlier 11-17 abstract-only event. The extraction adds architecture, MaxSim, indexing, tables and protocol-specific latency qualifications. |
| lewish-intelligence-and-compression-2025 | 11-17 | Aligned. The event includes attribution and inspection of the sole inline musical-score image; the extraction marks code/benchmarks/comments uninspected and does not grant reuse rights. |
| li-bert-flow-sentence-embeddings-2020 | 11-05 | Aligned. The extraction records the full-target unlabeled calibration protocol and transductive scope; the event captures the same BERT-flow/STS review. |
| marek-ryabinin-score-centering-off-policy-rl-2026 | 11-09 | Corrected by a new 11-19 event. The extraction is richer than the original same-date event: full arXiv v1 and appendices plus exact upstream test execution. The new event now records that evidence without erasing the earlier history. |
| maarten-grootendorst-visual-guide-multimodal-generation | 11-07 | Aligned for the indexed-text/primary-source snapshot. Later 11-15 source events record page/navigation work and four inspected images; the extraction remains a historical 11-07 snapshot. |
| mikolov-word2vec-2013 | 11-05 | Aligned. Both cover the full v3 paper, CBOW/Skip-gram, hierarchical softmax and English-centric analogy limits; code/vectors remain unexecuted. |
| poloclub-transformer-explainer-paper-2026 | 11-19 | Aligned. Both distinguish the published CHI paper from arXiv versions and retain the CC BY 4.0 statement while leaving repository/data replication open. |
| reimers-gurevych-2019-sentence-bert | 11-18 | Aligned with an earlier 11-17 abstract event. The extraction adds pooling/objectives, tables, AFS evaluation and hardware-specific efficiency limits. |
| santhanam-etal-2022-colbertv2 | 11-18 | Aligned with an earlier 11-17 abstract event. The extraction adds architecture, denoised supervision, residual compression, LoTTE/BEIR evidence and English/hardware limits. |
| sasirekha-cota-understanding-llm-compression-2023 | 11-16 | Aligned. Both treat the article as introductory, distinguish abstract-level primary-paper checks from reproduction, and preserve hardware-specific claims. |
| schmidt-tokenization-more-than-compression-2024 | 11-18 | Aligned with an earlier 10-29 migration note. The extraction adds PathPiece, English-only experiments and explicit model/code reproduction limits. |
| sennrich-subword-nmt-2016 | 11-18 | Aligned with an earlier 10-30 abstract note. The extraction and event both distinguish word-level NMT BPE from GPT byte-level BPE; the extraction points to the bilingual Gage/Sennrich distinction. |
| sourav-mukherjee-compression-intelligence-2026 | 11-16 | Aligned. Both distinguish entropy-guided cache methods from the unvalidated reasoning-token pruning claim and retain the third-party mirror limitation. |
| steck-cosine-similarity-embeddings-2024 | 11-05 | Aligned. The extraction separates the linear-model theorem, simulated experiment, no-code status and limits on generalizing to nonlinear LLM embeddings. |
| thakur-etal-2021-beir | 11-18 | Aligned with an earlier 11-17 abstract event. The extraction adds benchmark composition, task families and annotation-bias qualifications; no benchmark rerun is claimed. |
| varis-stephen-libovicky-tokcollate-2026 | 11-05 | Aligned. Both cover all ten paper pages and the CC BY 4.0 proceedings licence; the implementation, live visualizer and metric code remain unverified. |
| wegmann-tokenization-language-variation-2025 | 11-05 | Aligned with an earlier 10-30 abstract note. The extraction adds five pre-tokenizer settings, English task scope and the distinction from cross-lingual token-premium work. |

#### Cross-model differences and decisions

- Extraction-only detail: all ten facet fields remain useful: per-facet status, coverage, notes, rights state and explicit unresolved questions are not represented as separate fields in source events. Keep the snapshots during the compatibility window.
- Source-history-only detail: event chronology, event status, inspected-scope bullets and limitations are not fully reconstructible from a single extraction snapshot. Preserve all source events, including older abstract-only and later follow-up events.
- No destructive reconciliation: date matches establish identity and chronology, not equivalence. No scan snapshot was copied over a source event, and no event was deleted.
- Marek correction: the stale 2026-11-09 limitations are now superseded chronologically by the appended 2026-11-19 event; the older event remains as a truthful record of the earlier review state.
- AiEdge remains deferred: the canonical article still lacks full direct retrieval; unknown relation types and the missing cuda-graphs concept are not repaired by metadata reconciliation.
- Maarten remains incomplete at asset level: four images were inspected, but the advertised 50+ visual inventory remains unverified.


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

## 6. Fixtures and non-regression tests — closeout

The repository corpus itself is used as the fixture source. This avoids copying 36 scan records and 28 mappings into synthetic YAML files that could drift from the authoritative records. Tests read the actual extraction files, source catalogue, concept registry and bilingual page files.

The test module covers:
- all 36 scan records, exact source_id pairing, ten-key snapshot shape and matching source-history date;
- the three later source-history events (Karpathy, Maarten and the newly reconciled Marek event);
- the AiEdge example of facet-level extraction detail versus compressed event scope/limitations;
- all 28 canonical mappings and their observed field-shape counts;
- exact AiEdge endpoint/type checks and rejection of undeclared relation types;
- the six Marek prose proposals remaining non-normalized, with no automatic relation promotion;
- all six Marek integrated concept IDs resolving to canonical concepts and to both published bilingual score-centering pages;
- explicit absence of policy-drift from the canonical concept registry.

No artificial fixtures named scan-identical.yml, scan-conflict.yml, etc. were added: those would test a hypothetical migration model rather than the real corpus. The real records cover the important cases: compact source event versus rich facet snapshot (AiEdge), source-only later chronology (Karpathy/Maarten), and a stale event corrected by a later append (Marek).

CI evidence for the already merged PR #1383: commit 64ed7b490186b25258555853e6c82f70d0fa0598; CI run 44568073905 succeeded (test suite and Python/domain checks), Quarto run 44568073875 succeeded, and secret scanning run 44568074091 succeeded. The new closeout commit has its own CI pending; do not infer its result from PR #1383.


## 7. Remaining work, blockers and ordered follow-up

The historical reconciliation itself is closed. The remaining items below are source-access/reproducibility blockers, not unresolved matching of the 36 scans or the 28 mappings.

1. AiEdge — source retrieval blocker. Retrieve the complete canonical article and inspect its figures, code, links and references. Until then, retain the proposed cuda-graphs concept and both optimizes/complements relations as deferred and non-representable under the current vocabulary.
2. Cameron R. Wolfe — separate source blocker. The Substack body remains unavailable. Keep its source record distinct from Marek/Ryabinin's primary paper and do not attribute any claims from the inaccessible article.
3. Varis/TokCollate — implementation blocker. Inspect the official repository, pin dependencies, verify the CLI/data contract and metric calculations, and test the live visualizer including accessibility. The proceedings paper alone does not establish current software behavior.
4. Marek/Ryabinin — reproducibility boundary. The canonical PDF and upstream unit test module have been inspected/executed as recorded, but declared-minimum JAX compatibility, framework integrations, paper-scale sweeps and independent reproduction of reported model results remain open.
5. Maarten — visual inventory. Reconcile the four inspected in-body images against the article's advertised 50+ visuals, with creator/provenance and reuse-rights checks. Do not reproduce any asset without permission.
6. Cross-corpus reproducibility. For sources whose linked repositories/data/checkpoints remain marked not inspected, run targeted audits only when a lesson or experiment depends on implementation-level claims. The historical scan audit does not imply these experiments were reproduced.

No further changes to canonical concepts, relation types, route definitions or page associations are justified by the historical proposals alone. Keep the existing 28-entry decision register unchanged unless new primary-source evidence changes a specific decision.


## 8. Explicit non-changes

- No canonical concept, relation, page, resource or route was added or removed.
- No `scan` block was migrated, deleted or rewritten.
- No validator rule was tightened.
- No new relation type was introduced.
- No candidate destination or historical prose proposal was promoted to an integrated canonical edge.
