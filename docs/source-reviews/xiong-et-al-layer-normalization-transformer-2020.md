# Source review — Ruibin Xiong et al., “On Layer Normalization in the Transformer Architecture”

**Source ID:** `xiong-et-al-layer-normalization-transformer-2020`  
**Author/creator:** Ruibin Xiong et al.  
**Publisher:** Proceedings of Machine Learning Research (ICML 2020)  
**Publication/version:** 2020-02-12; PMLR 119:10524–10533; arXiv:2002.04745v1  
**Canonical URL:** https://proceedings.mlr.press/v119/xiong20b.html  
**Review date:** 2026-11-27  
**Source type / language / audience:** research paper / English / advanced; learners, practitioners and researchers

## 1. Scope, provenance and scan status

The canonical paper PDF was inspected directly for the focused sections listed below. The source record remains `partially-scanned`; this review does not upgrade the scan status.

| Component | Status | Coverage and evidence | Limitations |
|---|---|---|---|
| Author-authored text | partially-inspected | abstract, §3.3 (initialization assumptions and Theorem 1), §4.2 (translation and BERT experiment results, Figures 4–5) | The complete paper and supplementary proofs were not re-audited. No paper figures, supplementary material, code or datasets were copied or independently executed. Licence and reuse rights remain unknown. |
| Figures/media | partially-inspected | Figure/table references were consulted only where specified by the extraction | No asset-level rights or reuse audit; no figure reused |
| Code/data | not-inspected | — | No implementation or benchmark reproduction |
| Comments/community | not-applicable | Not part of the selected paper scope | — |
| Linked resources | not-inspected | — | No linked repositories or supplementary resources audited |
| Metadata/version | verified | Bibliographic identity and version recorded in `data/sources.yml` | No broader version-history comparison |
| Licence/reuse rights | unknown | See the canonical source record | No asset-specific permission is inferred |

**Overall status:** `partially-scanned`. The inspection is limited to claims used by the Transformer Block Walkthrough. Uninspected components remain unknown.

## 2. Atomic contribution inventory

Structured evidence: [`data/extractions/xiong-et-al-layer-normalization-transformer-2020.yml`](../../data/extractions/xiong-et-al-layer-normalization-transformer-2020.yml). Topic synthesis: [Transformer Block source-to-code dossier](../source-syntheses/transformer-block-walkthrough-source-audit-2026-11.md).

| Item ID | Contribution | Evidence confidence | Disposition | Qualification |
|---|---|---|---|---|
| `xiong-et-al-layer-normalization-transformer-2020:pre-ln-post-ln-gradient-scale` | Initialization gradient bounds differ for Post-LN and Pre-LN under the paper's assumptions. | `well-supported` | `integrate-by-reference` | §3.3, Theorem 1. The simplified setting includes single-head attention, zero-initialized Q/K projections, Gaussian inputs and bounded derivatives; this is not a universal ranking. |
| `xiong-et-al-layer-normalization-transformer-2020:pre-ln-warmup-experiments` | In the reported translation and BERT experiments, Pre-LN can train without the warm-up schedule used for Post-LN and reaches comparable task performance. | `context-dependent` | `integrate-by-reference` | §4.2, Figures 4–5. Optimizer, initialization, datasets and architectures are paper-specific; no project reproduction was performed. |

The extraction retains atomic claims, assumptions, limitations and candidate destinations. This review interprets them; it does not duplicate the full structured evidence.

## 3. Technical assessment

### Correct and useful
- **pre-ln-post-ln-gradient-scale** — Initialization gradient bounds differ for Post-LN and Pre-LN under the paper's assumptions.
- **pre-ln-warmup-experiments** — In the reported translation and BERT experiments, Pre-LN can train without the warm-up schedule used for Post-LN and reaches comparable task performance.

### Claims requiring qualification
- §3.3, Theorem 1. The simplified setting includes single-head attention, zero-initialized Q/K projections, Gaussian inputs and bounded derivatives; this is not a universal ranking.
- §4.2, Figures 4–5. Optimizer, initialization, datasets and architectures are paper-specific; no project reproduction was performed.

### Not established by this inspection
- No claim is made about uninspected sections, supplementary proofs, implementation quality or reproducibility.
- Paper-specific results are not transferred to arbitrary architectures, hardware or workloads.
- Repository tests are not treated as evidence for the paper's research claims.

## 4. Source-local knowledge model

Pre-LN/Post-LN placement → gradient behavior at initialization → warm-up sensitivity in the paper's analyzed/trained settings.

This is a reviewer reconstruction from the inspected material, not an ontology or computational graph authored by the source.

## 5. Source teaching route

Only §3.3 and §4.2 were inspected. The complete paper route, prerequisites, exercises and learner route were not audited.

The source is a research paper, not a learner-facing course. No exercises, learner outcomes or formal prerequisites are attributed to its authors unless explicitly stated in the inspected sections.

## 6. Differential comparison with LLM Lab

| Learner question | Source treatment | Existing project treatment | Complementarity and decision |
|---|---|---|---|
| What mechanism or result does this paper establish? | Initialization gradient bounds differ for Post-LN and Pre-LN under the paper's assumptions. | The bilingual Transformer Block Walkthrough compares this mechanism with the reference NumPy MHA block. | `integrate-by-reference`: preserve the primary citation and its assumptions; do not imply code support. |
| What does the evidence not establish? | §4.2, Figures 4–5. Optimizer, initialization, datasets and architectures are paper-specific; no project reproduction was performed. | The page and shared dossier distinguish paper evidence, implementation behavior and test assertions. | Keep the limitation adjacent to the comparison; no new page or concept is justified. |

**Implementation boundary:** the repository reference block remains a pedagogical MHA implementation with dense causal attention. This source does not establish implementation of the mechanism unless explicitly stated above.

## 7. Integration decision

- Canonical source record and extraction are maintained in `data/sources.yml` and `data/extractions/`.
- Direct FR/EN page relations were added in merged [PR #1777](https://github.com/JM-Brun/llm-lab/pull/1777).
- The shared topic dossier records the cross-source comparison and code/test evidence.
- No separate concept ID, public page, implementation feature or benchmark is warranted by this bounded review.

## 8. Visual assets and rights

No source figure is reused. Figure/table references in the extraction support claim localization only. Actual asset bytes, figure creators, captions, accessibility and reuse permissions were not audited. Existing project illustrations are not affected.

## 9. Validation evidence

No experiment was reproduced; no figure was reused.

This review interprets the registered source and extraction. Repository schema/build validation and learner validation remain separate gates.

## 10. Open questions and next actions

1. Inspect supplementary proofs, code, data and remaining paper sections only if a future page claim requires them.
2. Resolve licence and asset-specific reuse status before any proposed figure reuse.
3. Revisit the source only when the relevant project claim or implementation changes; do not rescan the whole paper by default.
