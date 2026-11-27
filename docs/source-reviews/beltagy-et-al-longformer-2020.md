# Source review — Iz Beltagy, Matthew E. Peters and Arman Cohan, “Longformer: The Long-Document Transformer”

**Source ID:** `beltagy-et-al-longformer-2020`  
**Author/creator:** Iz Beltagy, Matthew E. Peters and Arman Cohan  
**Publisher:** arXiv  
**Publication/version:** 2020-04-10; arXiv:2004.05150v2 (updated 2020-12-02)  
**Canonical URL:** https://arxiv.org/abs/2004.05150  
**Review date:** 2026-11-27  
**Source type / language / audience:** research paper / English / advanced; learners, practitioners and researchers

## 1. Scope, provenance and scan status

The canonical paper PDF was inspected directly for the focused sections listed below. The source record remains `partially-scanned`; this review does not upgrade the scan status.

| Component | Status | Coverage and evidence | Limitations |
|---|---|---|---|
| Author-authored text | partially-inspected | abstract, §3.1 (sliding-window, dilated and global attention patterns), §3.2 (implementation and complexity), and Figure 2 | The linear-scaling claim assumes a fixed local window and a small number of global positions. No CUDA implementation, figures, datasets or model checkpoints were independently executed or copied. Licence and reuse rights remain unknown. |
| Figures/media | partially-inspected | Figure/table references were consulted only where specified by the extraction | No asset-level rights or reuse audit; no figure reused |
| Code/data | not-inspected | — | No implementation or benchmark reproduction |
| Comments/community | not-applicable | Not part of the selected paper scope | — |
| Linked resources | not-inspected | — | No linked repositories or supplementary resources audited |
| Metadata/version | verified | Bibliographic identity and version recorded in `data/sources.yml` | No broader version-history comparison |
| Licence/reuse rights | unknown | See the canonical source record | No asset-specific permission is inferred |

**Overall status:** `partially-scanned`. The inspection is limited to claims used by the Transformer Block Walkthrough. Uninspected components remain unknown.

## 2. Atomic contribution inventory

Structured evidence: [`data/extractions/beltagy-et-al-longformer-2020.yml`](../../data/extractions/beltagy-et-al-longformer-2020.yml). Topic synthesis: [Transformer Block source-to-code dossier](../source-syntheses/transformer-block-walkthrough-source-audit-2026-11.md).

| Item ID | Contribution | Evidence confidence | Disposition | Qualification |
|---|---|---|---|---|
| `beltagy-et-al-longformer-2020:local-dilated-global-attention` | Longformer combines local sliding windows, optional dilation and task-selected global positions with bidirectional global interaction. | `established` | `integrate-by-reference` | §3.1 and Figure 2. This encoder-oriented global/local pattern is distinct from Mistral's sliding-window configuration and causal decoder attention. |
| `beltagy-et-al-longformer-2020:linear-scaling-fixed-window` | For fixed window width w, local attention costs O(n×w); a small number of global positions preserves linear scaling in sequence length. | `context-dependent` | `integrate-by-reference` | §§3.1–3.2. Linear scaling depends on fixed w and a bounded global-token count; it is not dense full attention. |

The extraction retains atomic claims, assumptions, limitations and candidate destinations. This review interprets them; it does not duplicate the full structured evidence.

## 3. Technical assessment

### Correct and useful
- **local-dilated-global-attention** — Longformer combines local sliding windows, optional dilation and task-selected global positions with bidirectional global interaction.
- **linear-scaling-fixed-window** — For fixed window width w, local attention costs O(n×w); a small number of global positions preserves linear scaling in sequence length.

### Claims requiring qualification
- §3.1 and Figure 2. This encoder-oriented global/local pattern is distinct from Mistral's sliding-window configuration and causal decoder attention.
- §§3.1–3.2. Linear scaling depends on fixed w and a bounded global-token count; it is not dense full attention.

### Not established by this inspection
- No claim is made about uninspected sections, supplementary proofs, implementation quality or reproducibility.
- Paper-specific results are not transferred to arbitrary architectures, hardware or workloads.
- Repository tests are not treated as evidence for the paper's research claims.

## 4. Source-local knowledge model

Position interaction pattern: local window (optionally dilated) + selected global positions; the complexity claim follows from fixed local width and a small global set.

This is a reviewer reconstruction from the inspected material, not an ontology or computational graph authored by the source.

## 5. Source teaching route

Only the abstract and selected architecture/complexity sections were inspected. The complete paper route, downstream task experiments and supplementary material were not audited.

The source is a research paper, not a learner-facing course. No exercises, learner outcomes or formal prerequisites are attributed to its authors unless explicitly stated in the inspected sections.

## 6. Differential comparison with LLM Lab

| Learner question | Source treatment | Existing project treatment | Complementarity and decision |
|---|---|---|---|
| What mechanism or result does this paper establish? | Longformer combines local sliding windows, optional dilation and task-selected global positions with bidirectional global interaction. | The bilingual Transformer Block Walkthrough compares this mechanism with the reference NumPy MHA block. | `integrate-by-reference`: preserve the primary citation and its assumptions; do not imply code support. |
| What does the evidence not establish? | §§3.1–3.2. Linear scaling depends on fixed w and a bounded global-token count; it is not dense full attention. | The page and shared dossier distinguish paper evidence, implementation behavior and test assertions. | Keep the limitation adjacent to the comparison; no new page or concept is justified. |

**Implementation boundary:** the repository reference block remains a pedagogical MHA implementation with dense causal attention. This source does not establish implementation of the mechanism unless explicitly stated above.

## 7. Integration decision

- Canonical source record and extraction are maintained in `data/sources.yml` and `data/extractions/`.
- Direct FR/EN page relations were added in merged [PR #1777](https://github.com/JM-Brun/llm-lab/pull/1777).
- The shared topic dossier records the cross-source comparison and code/test evidence.
- No separate concept ID, public page, implementation feature or benchmark is warranted by this bounded review.

## 8. Visual assets and rights

No source figure is reused. Figure/table references in the extraction support claim localization only. Actual asset bytes, figure creators, captions, accessibility and reuse permissions were not audited. Existing project illustrations are not affected.

## 9. Validation evidence

No implementation or benchmark was reproduced; no figure was reused.

This review interprets the registered source and extraction. Repository schema/build validation and learner validation remain separate gates.

## 10. Open questions and next actions

1. Inspect supplementary proofs, code, data and remaining paper sections only if a future page claim requires them.
2. Resolve licence and asset-specific reuse status before any proposed figure reuse.
3. Revisit the source only when the relevant project claim or implementation changes; do not rescan the whole paper by default.
