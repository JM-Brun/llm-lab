# Historical extraction reconciliation — 2026-11-19

**Repository:** `JM-Brun/llm-lab`  
**Audited branch snapshot:** `main` at `1e20c55453421e079aefd6bdd686fe47277d98c8`  
**Scope:** legacy extraction-level `scan` blocks and `canonical_mapping` blocks  
**Status:** mapping inventory and relation comparison completed; scan reconciliation and regression fixtures remain open

This is a conservative, evidence-linked reconciliation. A historical proposal is not proof of canonical integration. No canonical record, relation, route, source or validator rule is changed by this audit.

## 1. Executive findings

The repository inventory documents 36 extraction-level `scan` blocks and 28 `canonical_mapping` blocks. Direct inspection of the 96 extraction files on the audited `main` snapshot found all 28 mapping-bearing files, but only 35 files with an unquoted top-level `scan:` key using the first-pass locator. The 36th scan has **not** yet been identified. This is an unresolved discrepancy, not a reason to revise the documented count.

The 28 mapping blocks are all mappings. Their observed shape is:

| Field | Mappings |
|---|---:|
| `proposed_concepts` present | 28 |
| `proposed_relations` present | 28 |
| `route_implications` present | 28 |
| `decision_summary` present | 28 |
| non-empty `proposed_concepts` | 1 |
| non-empty `proposed_relations` | 2 |
| non-empty `route_implications` | 2 |
| non-empty `integrated_concepts` | 1 |

Interpretation:
- AiEdge is the only mapping with a proposed concept and structured relation objects.
- Marek/Ryabinin is the only mapping with `integrated_concepts`; its six relation proposals are plain-language strings, not normalized relation records.
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

## 4. Historical scan locator — 35 identified, one unresolved

The first-pass exact-key locator found these 35 extraction files with a top-level `scan:` block:

1. `ahia-do-all-languages-cost-the-same-2023`
2. `aiedge-how-cuda-graphs-speed-up-llm-inference`
3. `ali-tokenizer-choice-llm-training-2024`
4. `alliancy-la-compression-strategie-avenir-llm-2026`
5. `andrej-karpathy-gpt-tokenizer-video`
6. `arnett-explaining-mitigating-crosslingual-tokenizer-inequities-2025`
7. `chiu-toklens-acl-srw-2026`
8. `dailydose-augsbert-sentence-similarity-2024`
9. `dailydose-bi-cross-encoders-sentence-similarity-2024`
10. `dailydose-foundations-rag-2024`
11. `ethayarajh-contextualized-representations-2019`
12. `faysse-etal-2025-colpali`
13. `formal-piwowarski-clinchant-2021-splade`
14. `goldman-unpacking-tokenization-2024`
15. `hesam-sheikh-llm-study-roadmap-2024`
16. `jose-parreno-garcia-how-llms-work-three-layers-2025`
17. `jothi-moorthy-llm-processing-linkedin`
18. `karthik-shashidhar-llms-compression-algorithms-2024`
19. `khattab-zaharia-2020-colbert`
20. `lewish-intelligence-and-compression-2025`
21. `li-bert-flow-sentence-embeddings-2020`
22. `marek-ryabinin-score-centering-off-policy-rl-2026`
23. `maarten-grootendorst-visual-guide-multimodal-generation`
24. `mikolov-word2vec-2013`
25. `poloclub-transformer-explainer-paper-2026`
26. `reimers-gurevych-2019-sentence-bert`
27. `santhanam-etal-2022-colbertv2`
28. `sasirekha-cota-understanding-llm-compression-2023`
29. `schmidt-tokenization-more-than-compression-2024`
30. `sennrich-subword-nmt-2016`
31. `sourav-mukherjee-compression-intelligence-2026`
32. `steck-cosine-similarity-embeddings-2024`
33. `thakur-etal-2021-beir`
34. `varis-stephen-libovicky-tokcollate-2026`
35. `wegmann-tokenization-language-variation-2025`

The inventory says 36. The outstanding 36th record must be found by a broader YAML-key locator (including quoted keys, whitespace variants and parser-level key detection), then compared field-by-field against the matching source-level `scan_history`. No scan content is declared migrated, duplicated, stale or richer until that comparison is done.

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

Regression tests should assert:
- exact source/extraction identity pairing by `source_id`, not filename guesswork;
- lossless preservation of all historical blocks;
- the four scan-difference classes above;
- exact relation tuple matching, plus explicit handling of symmetric types;
- missing endpoint and unknown relation-type diagnostics;
- no mutation of canonical registries from candidate-only or prose proposals;
- deterministic report output and stable counts.

**Not yet implemented:** these fixtures and tests. This document records the actual candidate cases and the test contract; it does not claim test execution.

## 7. Remaining ordered work

1. Find the 36th scan using parser-level key detection and produce the 36-file list.
2. Retrieve source-level `scan_history` for all 36 source IDs; compare the ten fields and record differences without migration.
3. Verify all six Marek concepts under `integrated_concepts` against canonical IDs, definitions, pages and source evidence (the first-pass check found all six except any additional proposal IDs to be reviewed individually; do not infer relation integration).
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
