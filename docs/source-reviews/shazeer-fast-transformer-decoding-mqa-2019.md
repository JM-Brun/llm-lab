# Source review — Noam Shazeer, “Fast Transformer Decoding: One Write-Head is All You Need”

**Source ID:** `shazeer-fast-transformer-decoding-mqa-2019`  
**Author/creator:** Noam Shazeer  
**Publisher:** arXiv  
**Publication/version:** 2019-11-06; arXiv:1911.02150v1  
**Canonical URL:** https://arxiv.org/abs/1911.02150  
**Review date:** 2026-11-27  
**Source type / language / audience:** research paper / English / advanced; learners, practitioners and researchers

## 1. Scope, provenance and scan status

The canonical paper PDF was inspected directly for the focused sections listed below. The source record remains `partially-scanned`; this review does not upgrade the scan status.

| Component | Status | Coverage and evidence | Limitations |
|---|---|---|---|
| Author-authored text | partially-inspected | §3 (Multi-Query Attention), §3.1 (incremental-decoding performance analysis), §§4.2–4.3 (model quality and speed), and incremental K/V tensor shapes | The speed/quality comparisons use 2019-era models, TPUv2/v3 hardware and fixed sequence/batch settings. No reference implementation, figures or benchmark data were independently executed or copied. Reuse rights remain unknown. |
| Figures/media | partially-inspected | Figure/table references were consulted only where specified by the extraction | No asset-level rights or reuse audit; no figure reused |
| Code/data | not-inspected | — | No implementation or benchmark reproduction |
| Comments/community | not-applicable | Not part of the selected paper scope | — |
| Linked resources | not-inspected | — | No linked repositories or supplementary resources audited |
| Metadata/version | verified | Bibliographic identity and version recorded in `data/sources.yml` | No broader version-history comparison |
| Licence/reuse rights | unknown | See the canonical source record | No asset-specific permission is inferred |

**Overall status:** `partially-scanned`. The inspection is limited to claims used by the Transformer Block Walkthrough. Uninspected components remain unknown.

## 2. Atomic contribution inventory

Structured evidence: [`data/extractions/shazeer-fast-transformer-decoding-mqa-2019.yml`](../../data/extractions/shazeer-fast-transformer-decoding-mqa-2019.yml). Topic synthesis: [Transformer Block source-to-code dossier](../source-syntheses/transformer-block-walkthrough-source-audit-2026-11.md).

| Item ID | Contribution | Evidence confidence | Disposition | Qualification |
|---|---|---|---|---|
| `shazeer-fast-transformer-decoding-mqa-2019:shared-kv-heads` | MQA retains distinct query heads while sharing one key head and one value head across them. | `established` | `integrate-by-reference` | §3. The paper's tensor notation is specific to its formulation. MQA changes K/V head multiplicity; it does not eliminate attention or the KV cache. |
| `shazeer-fast-transformer-decoding-mqa-2019:incremental-decode-bandwidth` | Repeated K/V memory access is identified as an incremental-decoding bottleneck; reported speed gains and quality differences are tied to the tested setup. | `context-dependent` | `integrate-by-reference` | §3.1 and §§4.2–4.3. The speed-up is not portable to current GPUs or arbitrary serving stacks; the paper reports non-zero quality differences. |

The extraction retains atomic claims, assumptions, limitations and candidate destinations. This review interprets them; it does not duplicate the full structured evidence.

## 3. Technical assessment

### Correct and useful
- **shared-kv-heads** — MQA retains distinct query heads while sharing one key head and one value head across them.
- **incremental-decode-bandwidth** — Repeated K/V memory access is identified as an incremental-decoding bottleneck; reported speed gains and quality differences are tied to the tested setup.

### Claims requiring qualification
- §3. The paper's tensor notation is specific to its formulation. MQA changes K/V head multiplicity; it does not eliminate attention or the KV cache.
- §3.1 and §§4.2–4.3. The speed-up is not portable to current GPUs or arbitrary serving stacks; the paper reports non-zero quality differences.

### Not established by this inspection
- No claim is made about uninspected sections, supplementary proofs, implementation quality or reproducibility.
- Paper-specific results are not transferred to arbitrary architectures, hardware or workloads.
- Repository tests are not treated as evidence for the paper's research claims.

## 4. Source-local knowledge model

MHA K/V reads during incremental decoding → shared K/V heads in MQA → reduced repeated K/V memory traffic.

This is a reviewer reconstruction from the inspected material, not an ontology or computational graph authored by the source.

## 5. Source teaching route

Only the definition, performance analysis and selected experiment sections were inspected. The full paper route, supplementary material and exercises were not audited.

The source is a research paper, not a learner-facing course. No exercises, learner outcomes or formal prerequisites are attributed to its authors unless explicitly stated in the inspected sections.

## 6. Differential comparison with LLM Lab

| Learner question | Source treatment | Existing project treatment | Complementarity and decision |
|---|---|---|---|
| What mechanism or result does this paper establish? | MQA retains distinct query heads while sharing one key head and one value head across them. | The bilingual Transformer Block Walkthrough compares this mechanism with the reference NumPy MHA block. | `integrate-by-reference`: preserve the primary citation and its assumptions; do not imply code support. |
| What does the evidence not establish? | §3.1 and §§4.2–4.3. The speed-up is not portable to current GPUs or arbitrary serving stacks; the paper reports non-zero quality differences. | The page and shared dossier distinguish paper evidence, implementation behavior and test assertions. | Keep the limitation adjacent to the comparison; no new page or concept is justified. |

**Implementation boundary:** the repository reference block remains a pedagogical MHA implementation with dense causal attention. This source does not establish implementation of the mechanism unless explicitly stated above.

## 7. Integration decision

- Canonical source record and extraction are maintained in `data/sources.yml` and `data/extractions/`.
- Direct FR/EN page relations were added in merged [PR #1777](https://github.com/JM-Brun/llm-lab/pull/1777).
- The shared topic dossier records the cross-source comparison and code/test evidence.
- No separate concept ID, public page, implementation feature or benchmark is warranted by this bounded review.

## 8. Visual assets and rights

No source figure is reused. Figure/table references in the extraction support claim localization only. Actual asset bytes, figure creators, captions, accessibility and reuse permissions were not audited. Existing project illustrations are not affected.

## 9. Validation evidence

No benchmark was reproduced and no paper figure was reused.

This review interprets the registered source and extraction. Repository schema/build validation and learner validation remain separate gates.

## 10. Open questions and next actions

1. Inspect supplementary proofs, code, data and remaining paper sections only if a future page claim requires them.
2. Resolve licence and asset-specific reuse status before any proposed figure reuse.
3. Revisit the source only when the relevant project claim or implementation changes; do not rescan the whole paper by default.
