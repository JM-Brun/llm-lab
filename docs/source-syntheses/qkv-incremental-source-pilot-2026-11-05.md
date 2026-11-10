# Q/K/V incremental source pilot — Brenndoerfer

**Date:** 2026-11-05  
**Source:** [Michael Brenndoerfer, Query, Key, Value: The Foundation of Transformer Attention](https://mbrenndoerfer.com/writing/query-key-value-attention-mechanism)  
**Source ID:** `mbrenndoerfer-qkv-attention-mechanism`  
**Protocol:** [Source-to-knowledge validation v0.4](../workflows/source-to-knowledge-validation.md)

## Executive result

The existing Q/K/V workflow handled a fourth tutorial source without creating a new registry, concept, canonical page or learning-route edge. The source adds a useful intermediate-level teaching sequence and an assumption-explicit variance derivation for the `sqrt(d_k)` scale. Its main examples and role analogies overlap with the current curriculum and should remain references rather than duplicated content.

**Decision:** register and extract; keep the source partially scanned; integrate the scaling derivation by reference; defer the convex-hull insight; make no canonical content or graph change.

## End-to-end execution

| Stage | Result | Evidence |
|---|---|---|
| Discovery / deduplication | Pass | Canonical URL checked against the Q/K/V source register; new source ID assigned |
| Inspection | Partial pass | 11-section article structure and key text/equations/code/output inspected; media, interactive runtime, linked references and rights not inspected |
| Extraction | Pass for selected contributions | Structured extraction includes six atomic items and a source-local pedagogical model |
| Comparison | Pass | Compared with three existing tutorials, canonical bilingual Q/K/V and attention pages, and existing exercises |
| Integration decision | Pass | Per-item dispositions recorded; one reference-only integration candidate; no canonical edit |
| Validation | Pending | Schema/validator/build checks and PR review remain to be run |
| Learner validation | Not run | No learner outcomes claimed |

## Coverage and quality boundary

- Source text: substantially inspected.
- Source-wide inspection: partial.
- Extraction: selected relevant items captured; not a claim that every paragraph or asset is exhaustively atomized.
- Synthesis: complete for the selected contribution set; source-dependence is low within the Q/K/V collection, but all four tutorials remain secondary pedagogical sources.
- Project integration: reference-level only; no learner-facing change.
- Learner validation: not run; #447 remains gated by #483.

## Effort

Retrospective manual estimate: **58–85 minutes** across discovery (3–5), inspection (12–18), comparison (8–12), extraction/review (25–35), and catalogue/dossier maintenance (10–15). The estimate is not instrumented: active human time was reconstructed after the work, and tool/CI latency was not measured. Integration decision was included within comparison/review; automated validation time was not separately measured.

| Phase | Active human effort | Measurement quality | Notes |
|---|---:|---|---|
| Discovery / identity | 3–5 min | Retrospective estimate | URL and existing Q/K/V dossier checked |
| Inspection | 12–18 min | Retrospective estimate | Text/equations/code-output text; no media or interaction inspection |
| Extraction / source-local model | Included in 25–35 min | Retrospective estimate | YAML authoring and item-level evidence/caveats |
| Comparison / integration decision | 8–12 min | Retrospective estimate | Existing concepts, pages, routes and three prior tutorials compared |
| Catalogue / dossier / report maintenance | 10–15 min | Retrospective estimate | Six repository files updated |
| Automated validation | Not measured | CI evidence only | First CI run failed on two validator findings; Quarto site run succeeded; corrected head has not yet produced a new Actions run |

Observed correction burden: **2 validator findings → 2 targeted YAML corrections**. This is a useful process signal, not a quality score. Future pilots must timestamp phases prospectively and separate active human time, tool execution, CI queue time, retries and review interventions.

## Workflow transfer result

The protocol transferred cleanly for source identity, atomic extraction, source-local route reconstruction, complementarity comparison and item-level disposition. The main friction is the gap between text completeness and whole-source inspection for interactive/visual articles. A lightweight phase-effort record is also needed to compare operational cost over repeated pilots.

No new skill, registry, taxonomy or composite quality score is justified. Proposed method refinements are limited to explicit per-component inspection states and phase-level effort recording.

## Remaining validation

1. Re-run the source catalogue/extraction validator on the corrected PR head; the first run identified two issues and both were corrected.
2. Confirm a fresh Quarto build and full CI run on the corrected head; the first Quarto run succeeded, but the corrected head has not yet produced a new Actions run.
3. Reconcile the PR branch with the latest `main` commit before merge; the branch is currently one commit behind.
4. Inspect the rendered diff if any site page changes later; this pilot currently changes no canonical page.
5. Keep media/rights and interactive quiz checks open only if a later integration decision depends on them.
6. Reconcile with #447/#483 before any learner-facing efficacy claim.
