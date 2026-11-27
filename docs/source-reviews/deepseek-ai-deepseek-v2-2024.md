# Source review — DeepSeek-AI, “DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model”

**Source ID:** `deepseek-ai-deepseek-v2-2024`  
**Author/creator:** DeepSeek-AI  
**Publisher:** arXiv  
**Publication/version:** 2024-05-07; arXiv:2405.04434v5 (updated 2024-06-19)  
**Canonical URL:** https://arxiv.org/abs/2405.04434  
**Review date:** 2026-11-27  
**Source type / language / audience:** research paper / English / advanced; learners, practitioners and researchers

## 1. Scope, provenance and scan status

The canonical paper PDF was inspected directly for the focused sections listed below. The source record remains `partially-scanned`; this review does not upgrade the scan status.

| Component | Status | Coverage and evidence | Limitations |
|---|---|---|---|
| Author-authored text | partially-inspected | §2.1.1 (standard MHA baseline), §2.1.2 (low-rank joint K/V compression, equations 9–11), §2.1.3 (decoupled RoPE), §2.1.4 (KV-cache comparison, Table 1), and Figure 3 | This pass covers MLA only; DeepSeekMoE, training, alignment and full evaluation sections were not audited. No figures, code, model checkpoints or datasets were copied or independently executed. Licence and reuse rights remain unknown. |
| Figures/media | partially-inspected | Figure/table references were consulted only where specified by the extraction | No asset-level rights or reuse audit; no figure reused |
| Code/data | not-inspected | — | No implementation or benchmark reproduction |
| Comments/community | not-applicable | Not part of the selected paper scope | — |
| Linked resources | not-inspected | — | No linked repositories or supplementary resources audited |
| Metadata/version | verified | Bibliographic identity and version recorded in `data/sources.yml` | No broader version-history comparison |
| Licence/reuse rights | unknown | See the canonical source record | No asset-specific permission is inferred |

**Overall status:** `partially-scanned`. The inspection is limited to claims used by the Transformer Block Walkthrough. Uninspected components remain unknown.

## 2. Atomic contribution inventory

Structured evidence: [`data/extractions/deepseek-ai-deepseek-v2-2024.yml`](../../data/extractions/deepseek-ai-deepseek-v2-2024.yml). Topic synthesis: [Transformer Block source-to-code dossier](../source-syntheses/transformer-block-walkthrough-source-audit-2026-11.md).

| Item ID | Contribution | Evidence confidence | Disposition | Qualification |
|---|---|---|---|---|
| `deepseek-ai-deepseek-v2-2024:mla-joint-kv-compression` | MLA jointly compresses K/V into a lower-dimensional latent, reconstructs the attention representations and caches the latent during inference. | `established` | `integrate-by-reference` | §2.1.2, equations 9–11 and Figure 3. MLA is not simply GQA with fewer groups; it changes the cached representation. |
| `deepseek-ai-deepseek-v2-2024:mla-cache-comparison` | The paper compares per-token KV-cache representations across MHA, GQA, MQA and MLA and reports a model-specific MLA footprint. | `context-dependent` | `integrate-by-reference` | §2.1.4, Table 1. The reported 93.3% cache reduction is relative to DeepSeek 67B; it must not be generalized. |

The extraction retains atomic claims, assumptions, limitations and candidate destinations. This review interprets them; it does not duplicate the full structured evidence.

## 3. Technical assessment

### Correct and useful
- **mla-joint-kv-compression** — MLA jointly compresses K/V into a lower-dimensional latent, reconstructs the attention representations and caches the latent during inference.
- **mla-cache-comparison** — The paper compares per-token KV-cache representations across MHA, GQA, MQA and MLA and reports a model-specific MLA footprint.

### Claims requiring qualification
- §2.1.2, equations 9–11 and Figure 3. MLA is not simply GQA with fewer groups; it changes the cached representation.
- §2.1.4, Table 1. The reported 93.3% cache reduction is relative to DeepSeek 67B; it must not be generalized.

### Not established by this inspection
- No claim is made about uninspected sections, supplementary proofs, implementation quality or reproducibility.
- Paper-specific results are not transferred to arbitrary architectures, hardware or workloads.
- Repository tests are not treated as evidence for the paper's research claims.

## 4. Source-local knowledge model

K/V projections → joint low-rank latent → latent cache → reconstructed K/V for attention, with a decoupled positional pathway.

This is a reviewer reconstruction from the inspected material, not an ontology or computational graph authored by the source.

## 5. Source teaching route

Only the MLA-related sections were inspected. The broader MoE model, training/evaluation route and unrelated sections were outside this review.

The source is a research paper, not a learner-facing course. No exercises, learner outcomes or formal prerequisites are attributed to its authors unless explicitly stated in the inspected sections.

## 6. Differential comparison with LLM Lab

| Learner question | Source treatment | Existing project treatment | Complementarity and decision |
|---|---|---|---|
| What mechanism or result does this paper establish? | MLA jointly compresses K/V into a lower-dimensional latent, reconstructs the attention representations and caches the latent during inference. | The bilingual Transformer Block Walkthrough compares this mechanism with the reference NumPy MHA block. | `integrate-by-reference`: preserve the primary citation and its assumptions; do not imply code support. |
| What does the evidence not establish? | §2.1.4, Table 1. The reported 93.3% cache reduction is relative to DeepSeek 67B; it must not be generalized. | The page and shared dossier distinguish paper evidence, implementation behavior and test assertions. | Keep the limitation adjacent to the comparison; no new page or concept is justified. |

**Implementation boundary:** the repository reference block remains a pedagogical MHA implementation with dense causal attention. This source does not establish implementation of the mechanism unless explicitly stated above.

## 7. Integration decision

- Canonical source record and extraction are maintained in `data/sources.yml` and `data/extractions/`.
- Direct FR/EN page relations were added in merged [PR #1777](https://github.com/JM-Brun/llm-lab/pull/1777).
- The shared topic dossier records the cross-source comparison and code/test evidence.
- No separate concept ID, public page, implementation feature or benchmark is warranted by this bounded review.

## 8. Visual assets and rights

No source figure is reused. Figure/table references in the extraction support claim localization only. Actual asset bytes, figure creators, captions, accessibility and reuse permissions were not audited. Existing project illustrations are not affected.

## 9. Validation evidence

No model or cache benchmark was executed; reuse rights remain unknown.

This review interprets the registered source and extraction. Repository schema/build validation and learner validation remain separate gates.

## 10. Open questions and next actions

1. Inspect supplementary proofs, code, data and remaining paper sections only if a future page claim requires them.
2. Resolve licence and asset-specific reuse status before any proposed figure reuse.
3. Revisit the source only when the relevant project claim or implementation changes; do not rescan the whole paper by default.
