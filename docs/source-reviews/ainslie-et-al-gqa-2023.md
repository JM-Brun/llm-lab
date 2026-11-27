# Source review — Joshua Ainslie et al., “GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints”

**Source ID:** `ainslie-et-al-gqa-2023`  
**Author/creator:** Joshua Ainslie et al.  
**Publisher:** Association for Computational Linguistics (EMNLP 2023)  
**Publication/version:** 2023-05-22; EMNLP 2023 proceedings; arXiv:2305.13245v3  
**Canonical URL:** https://aclanthology.org/2023.emnlp-main.298/  
**Review date:** 2026-11-27  
**Source type / language / audience:** research paper / English / advanced; learners, practitioners and researchers

## 1. Scope, provenance and scan status

The canonical paper PDF was inspected directly for the focused sections listed below. The source record remains `partially-scanned`; this review does not upgrade the scan status.

| Component | Status | Coverage and evidence | Limitations |
|---|---|---|---|
| Author-authored text | partially-inspected | §§2.1–2.2 (checkpoint uptraining and GQA head grouping), Figure 2, and §§3.1–3.3 (experimental setup, main results and ablations) | The reported 5% uptraining budget and quality/speed trade-off are specific to the T5 checkpoints, datasets, hardware and training recipe. Figures, code and datasets were not copied or independently reproduced. |
| Figures/media | partially-inspected | Figure/table references were consulted only where specified by the extraction | No asset-level rights or reuse audit; no figure reused |
| Code/data | not-inspected | — | No implementation or benchmark reproduction |
| Comments/community | not-applicable | Not part of the selected paper scope | — |
| Linked resources | not-inspected | — | No linked repositories or supplementary resources audited |
| Metadata/version | verified | Bibliographic identity and version recorded in `data/sources.yml` | No broader version-history comparison |
| Licence/reuse rights | declared | See the canonical source record | No asset-specific permission is inferred |

**Overall status:** `partially-scanned`. The inspection is limited to claims used by the Transformer Block Walkthrough. Uninspected components remain unknown.

## 2. Atomic contribution inventory

Structured evidence: [`data/extractions/ainslie-et-al-gqa-2023.yml`](../../data/extractions/ainslie-et-al-gqa-2023.yml). Topic synthesis: [Transformer Block source-to-code dossier](../source-syntheses/transformer-block-walkthrough-source-audit-2026-11.md).

| Item ID | Contribution | Evidence confidence | Disposition | Qualification |
|---|---|---|---|---|
| `ainslie-et-al-gqa-2023:grouped-query-head-sharing` | GQA partitions query heads into groups; each group shares one key head and one value head. The MQA and MHA cases are the two boundaries. | `established` | `integrate-by-reference` | §2.2 and Figure 2. The definition does not prescribe one universally optimal group count. |
| `ainslie-et-al-gqa-2023:mha-checkpoint-uptraining` | The method converts MHA checkpoints by mean-pooling K/V projections within target groups, then performs additional pre-training. | `established` | `integrate-by-reference` | §2.1 and Figure 1. The 5% compute budget is specific to the paper's T5 experiments, not a general conversion guarantee. |
| `ainslie-et-al-gqa-2023:gqa-quality-speed-tradeoff` | In the reported T5 experiments, uptrained GQA approaches MHA quality while retaining inference speed closer to MQA. | `context-dependent` | `integrate-by-reference` | §§3.2–3.3. The result depends on checkpoints, group counts, datasets and TPUv4 timing; it is not a universal quality/speed guarantee. |

The extraction retains atomic claims, assumptions, limitations and candidate destinations. This review interprets them; it does not duplicate the full structured evidence.

## 3. Technical assessment

### Correct and useful
- **grouped-query-head-sharing** — GQA partitions query heads into groups; each group shares one key head and one value head. The MQA and MHA cases are the two boundaries.
- **mha-checkpoint-uptraining** — The method converts MHA checkpoints by mean-pooling K/V projections within target groups, then performs additional pre-training.
- **gqa-quality-speed-tradeoff** — In the reported T5 experiments, uptrained GQA approaches MHA quality while retaining inference speed closer to MQA.

### Claims requiring qualification
- §2.2 and Figure 2. The definition does not prescribe one universally optimal group count.
- §2.1 and Figure 1. The 5% compute budget is specific to the paper's T5 experiments, not a general conversion guarantee.
- §§3.2–3.3. The result depends on checkpoints, group counts, datasets and TPUv4 timing; it is not a universal quality/speed guarantee.

### Not established by this inspection
- No claim is made about uninspected sections, supplementary proofs, implementation quality or reproducibility.
- Paper-specific results are not transferred to arbitrary architectures, hardware or workloads.
- Repository tests are not treated as evidence for the paper's research claims.

## 4. Source-local knowledge model

K/V-head sharing continuum: MQA (one shared K/V head) ↔ GQA (groups) ↔ MHA (one K/V head per query head); checkpoint conversion/uptraining is a separate method axis.

This is a reviewer reconstruction from the inspected material, not an ontology or computational graph authored by the source.

## 5. Source teaching route

Only the cited definition, uptraining and experiment sections were inspected. The complete paper route, exercises and supplementary material were not audited.

The source is a research paper, not a learner-facing course. No exercises, learner outcomes or formal prerequisites are attributed to its authors unless explicitly stated in the inspected sections.

## 6. Differential comparison with LLM Lab

| Learner question | Source treatment | Existing project treatment | Complementarity and decision |
|---|---|---|---|
| What mechanism or result does this paper establish? | GQA partitions query heads into groups; each group shares one key head and one value head. The MQA and MHA cases are the two boundaries. | The bilingual Transformer Block Walkthrough compares this mechanism with the reference NumPy MHA block. | `integrate-by-reference`: preserve the primary citation and its assumptions; do not imply code support. |
| What does the evidence not establish? | §§3.2–3.3. The result depends on checkpoints, group counts, datasets and TPUv4 timing; it is not a universal quality/speed guarantee. | The page and shared dossier distinguish paper evidence, implementation behavior and test assertions. | Keep the limitation adjacent to the comparison; no new page or concept is justified. |

**Implementation boundary:** the repository reference block remains a pedagogical MHA implementation with dense causal attention. This source does not establish implementation of the mechanism unless explicitly stated above.

## 7. Integration decision

- Canonical source record and extraction are maintained in `data/sources.yml` and `data/extractions/`.
- Direct FR/EN page relations were added in merged [PR #1777](https://github.com/JM-Brun/llm-lab/pull/1777).
- The shared topic dossier records the cross-source comparison and code/test evidence.
- No separate concept ID, public page, implementation feature or benchmark is warranted by this bounded review.

## 8. Visual assets and rights

No source figure is reused. Figure/table references in the extraction support claim localization only. Actual asset bytes, figure creators, captions, accessibility and reuse permissions were not audited. Existing project illustrations are not affected.

## 9. Validation evidence

No uptraining or benchmark was reproduced; no paper figure was reused.

This review interprets the registered source and extraction. Repository schema/build validation and learner validation remain separate gates.

## 10. Open questions and next actions

1. Inspect supplementary proofs, code, data and remaining paper sections only if a future page claim requires them.
2. Resolve licence and asset-specific reuse status before any proposed figure reuse.
3. Revisit the source only when the relevant project claim or implementation changes; do not rescan the whole paper by default.
