# Source-to-knowledge method transfer: tokenization and embeddings

**Status:** retrospective transfer assessment · **Version:** 0.1 · **Review date:** 2026-11-05  
**Protocol:** [Source-to-knowledge validation](../workflows/source-to-knowledge-validation.md)  
**Collection:** [Tokenization and embeddings synthesis](../source-reviews/tokenization-embeddings-source-collection.md)  
**Migration map:** [Source migration map](../source-reviews/tokenization-embeddings-source-migration-map-2026-11.md)  
**Owning issue:** [#496](https://github.com/JM-Brun/llm-lab/issues/496) · **Backfill dependency:** [#458](https://github.com/JM-Brun/llm-lab/issues/458)

## 1. Purpose and boundary

This report tests whether the method calibrated on Q/K/V transfers to a broader, heterogeneous source collection without creating parallel registries, flattening distinct research questions, or requiring every source to produce a new page.

This is a retrospective assessment of existing repository work. It is not a new exhaustive scan, a fresh review of all catalogue entries, or a learner study.

The transfer case is harder than Q/K/V: tokenization and embeddings spans tokenizer algorithms, corpus preparation, multilingual evaluation, static and contextualized representations, sentence-embedding geometry, and interactive learning tools. Sources include research papers, documentation, books, repositories, videos, courses and tutorials. Not every source should have a pedagogical graph or route.

## 2. Audited baseline

At the reviewed repository state, while the structured migration/backfill in #458 remains open:

| Inventory | Observed state |
|---|---:|
| Canonical source catalogue | 47 records: 4 Q/K/V or KV-cache records + 43 tokenization/embeddings records |
| Structured extraction records | 14 YAML files: 10 tokenization/embeddings + 4 Q/K/V/KV-cache |
| Atomic items in the 10 topic-specific extraction files | 59 |
| Topic-level synthesis | One living dossier organized around learner questions and six source families |
| Migration map | One, preserving historical scan boundaries and unresolved metadata |

**Count correction:** the collection dossier still says 46 records, comprising three Q/K/V/KV-cache records plus 43 migrated records. The current catalogue has 47 because Codefinity's Q/K/V lesson is now registered. The correct decomposition is four Q/K/V/KV-cache records plus 43 tokenization/embeddings records. This is a metadata reconciliation, not a new source discovery.

The 10 topic-specific extraction records cover Karpathy, Ahia, Ali, Wegmann, Arnett, Chiu/TokLens, Ethayarajh, Li, Mikolov and Steck. Their 59 extracted items are an inventory count, not 59 independent claims or proof of complete source coverage.

## 3. Transfer assessment

| Dimension | Result | Evidence and limits |
|---|---|---|
| Identity/provenance | Partial | Stable IDs and URLs exist for registered sources; exact historical URLs for some ByteByteGo/Vizuara resources and some immutable revisions remain unresolved. |
| Inspection coverage | Pass with explicit partial states | The dossier distinguishes PDF inspection, transcript/chapter-marker review, documentation and historical audit migration; uninspected code, data, supplements, media and rights remain visible. |
| Extraction fidelity | Promising; final validator check required | Ten topic-specific YAML records contain 59 located items with evidence scope and dispositions. This report does not replace a fresh final-head validation run. |
| Technical validity | Pass within stated scopes | Primary research is distinguished from tutorial explanation; models, tasks, corpora, denominators and limits are preserved. No independent reproduction is claimed. |
| Evidence independence | Pass in synthesis design | Compression, fertility, parity, downstream quality and cosine geometry are not treated as interchangeable measures. |
| Pedagogical reconstruction | Partial | Karpathy's instructional source has a source-local pedagogical model. Most other extracted sources are research papers, where a teaching route is not applicable. Several registered instructional sources still need explicit route triage. |
| Complementarity | Pass | The dossier separates six source families and compares them by learner question, analytical unit and explanatory role. |
| Synthesis coherence | Pass | The collection is organized by learner questions and subdomains rather than concatenating source summaries. It preserves distinctions between BPE variants, multilingual metric denominators and embedding-geometry scopes. |
| Integration value | Pass | Existing pages and routes are reused; integrate-by-reference, already-covered and defer decisions avoid unnecessary new pages and implementations. |
| Resource quality | Not assessed here | This report does not establish rendered-page quality, keyboard accessibility or mobile usability. |
| Maintainability | Partial | Canonical IDs, one catalogue, one extraction directory and one topic dossier support incremental work. The stale source count exposes a need for inventory consistency checks. |
| Learner evidence | Not assessed | No learning outcome is inferred from source audits or the existence of exercises. |

## 4. What transfers successfully

### Source-local pedagogy is not the canonical graph

Research papers are evidence-bearing contributions. Instructional sources may additionally receive source-local teaching models and routes. These are compared with, but do not replace, the canonical concept graph and project learner route. This distinction prevents research papers on tokenizer evaluation or embedding geometry from being forced into artificial lesson sequences.

### Complementarity follows the learner question and unit of analysis

The dossier preserves several genuinely different perspectives:

- **Ali et al.** evaluates tokenizer configurations and downstream decoder-only model outcomes under a controlled training setup.
- **Arnett et al.** compares monolingual tokenizer compression across languages; it does not train LMs and cannot establish downstream quality.
- **Wegmann et al.** studies within-language linguistic variation and task-dependent sensitivity, not crosslingual inequity.
- **TokLens** compares intrinsic metrics and reports scoped multilingual associations; it does not establish causal tokenizer effects independent of pretraining data.
- **Ahia et al.** adds user-facing API cost and context-capacity consequences, distinct from intrinsic compression and downstream benchmarks.
- **Ethayarajh, Li and Steck** concern contextualized token occurrences, pooled sentence embeddings, and regularized linear factorization geometry respectively.
- **Mikolov et al.** provides historical static word-vector foundations, distinct from Transformer token lookup and contextualization.

The synthesis is therefore more complete for its declared learner questions than any one source, without collapsing the findings into a generic claim about tokenizer quality or embedding similarity.

### A no-op can still be a successful integration decision

The dossier often chooses not to add a page, route step, implementation or visual. The contribution may instead improve provenance, caveats, historical precision or optional references. A stronger evidence layer does not require a longer learner-facing core.

## 5. Incremental-addition examples

**Ahia et al. — API cost and context capacity.** Existing coverage already included compression, multilingual disparities and downstream effects. Ahia adds a user-facing lens: historical per-token API billing and the amount of text or number of few-shot examples fitting a fixed context budget, plus ecological socio-economic correlations. Decision: retain in the advanced synthesis and integrate by reference; do not create a new essential-path page or present 2023 prices as current.

**Mikolov et al. — static word-vector foundations.** The embedding-space lesson already distinguishes static word vectors, Transformer token embeddings and contextualized states. The original paper adds historical precision for CBOW, Skip-gram and hierarchical softmax, and prevents attributing later negative-sampling details to the original paper. Decision: preserve as historical evidence and optional depth; do not create a second Word2Vec implementation.

Both cases show how a source can improve the evidence layer without requiring a new canonical concept or route step.

## 6. Defects and scalability limits exposed

1. **Inventory drift:** the source count became stale after Codefinity was registered. A deterministic catalogue/dossier consistency check is needed.
2. **Instructional route status is implicit for some sources:** among the ten topic-specific extraction files, only Karpathy has a pedagogical model. That is appropriate for research papers, but registered instructional sources such as Raschka, the Hugging Face course, Vizuara and ByteByteGo need explicit needed/not-applicable/deferred triage.
3. **Metadata gaps remain:** the registered ByteByteGo/Vizuara resources have canonical URLs, but a potentially separate Vizuara embeddings resource and some upstream revisions still need reconciliation from existing evidence, never guesswork.
4. **Rights and inspection are independent:** reading an article or paper does not clear figures, videos, repositories, code or supplements.
5. **Dossier size needs governance:** future additions should update the relevant learner-question section and compact decision table; large details belong in extraction/review records.
6. **Validation must target the final head:** prior CI success cannot be reused after catalogue, extraction or protocol changes.
7. **Automation is not proven:** schemas help, but deduplication, complementarity, route decisions and learner-value judgements still require human review.

## 7. Instructional-source route triage

This is a bounded triage proposal based on the migration map and existing audits. It is not a new source registry and does not upgrade any source's scan status.

| Registered source | Existing evidence | Route action | Boundary |
|---|---|---|---|
| Karpathy — GPT tokenizer video | Chapter markers and transcript-based review; source-local pedagogical model already present in its extraction | **Reconstructed** | Full audiovisual work was not watched; retain partial scan status |
| Raschka — Chapter 2 | Existing #96 audit and repository/notebook review | **Reconstruct selectively** | Use inspected chapter/notebook sequence; do not infer clean-room execution or unpinned upstream revisions |
| Hugging Face course — tokenizers chapter | Existing #114/#173 coverage matrix for BPE, WordPiece, Unigram and pipeline | **Reconstruct selectively** | Limit to audited chapter sections, not the entire course |
| ByteByteGo — “How LLMs Learn from the Internet” and “How LLMs See the World” | Exact canonical URLs are now present in the source catalogue; #147/#58 historical pedagogical comparison | **Reconstruct from existing evidence if route detail is locatable** | Do not treat the whole site or course as scanned |
| Vizuara — BPE course | #147 pedagogical review and registered course landing page | **Defer** | Landing-page description is not a full course scan; no lesson sequence should be invented |
| Vizuara — “LLMs from 30,000 Feet” | #147 micro-course/pedagogical-format review | **Defer** | Keep the limited source-description evidence; no detailed route inferred |
| Polo Club Transformer Explainer | Repository/code audit and #186/#188 integration evidence | **Reconstruct as an optional interactive route if source steps are locatable** | Preserve GPT-2-small and implementation-specific limits |
| Hugging Face BPE visualizer article/repository | #114 implementation audit and #168 integration evidence | **Optional resource route; otherwise reference-only** | Visualizer is schematic and does not reproduce the complete production tokenizer pipeline |
| Mike X Cohen and Yael Gomez articles | Candidate-source review and reference registration | **Defer** | Optional leads; do not claim a full source-local route without a locatable inspection record |
| Rushang Chauhan embeddings article | Pedagogical bridge and visual-asset follow-up | **Defer** | Image reuse rights and full source scope remain separate questions |

This triage exposes an important workflow distinction: **route reconstruction is conditional on source type and inspection scope**. A research paper can be fully useful as evidence without a learner route; a course with only its landing page inspected cannot be assigned a detailed route. Where the route is not yet justified, record the gap in the existing source review/extraction workflow rather than adding a new global status registry.

## 8. Transfer-specific regression cases

| ID | Scenario | Expected behavior |
|---|---|---|
| T1 | Collection mixes research papers and tutorials | Require source-local pedagogy only for instructional sources |
| T2 | Similar metrics use different denominators | Preserve definitions, corpus and denominator |
| T3 | Result is observational or ecological | Preserve association language; do not infer causality |
| T4 | Historical API price is extracted | Preserve date/model/API context |
| T5 | Primary paper is already covered in a lesson | Add traceable evidence or bounded correction, not duplicate prose |
| T6 | New source adds social or implementation consequences | Test complementarity even if the technical topic is already covered |
| T7 | Exact URL or revision is unresolved | Keep the metadata gap explicit |
| T8 | Items are extracted but code/media remain uninspected | Keep source/component scan status partial |
| T9 | Collection spans multiple subdomains | Organize by learner questions; do not invent one unified concept |
| T10 | Catalogue changes after dossier count | Flag and reconcile the count before validation |

These cases should be added to the canonical adversarial suite only after deciding whether to keep it compact or group cases by domain.

## 9. Verdict and next actions

**Transfer demonstrated at the documentation and synthesis level:** the method handles a broader, heterogeneous collection while preserving source roles, evidence scopes, learner questions and integration dispositions. It supports a cumulative knowledge resource whose evidence layer is richer than any one source while keeping the curriculum selective.

**Full scalability and operational completeness are not yet demonstrated.** Outstanding evidence includes final-head validators, selective instructional-route reconstruction, metadata recovery, rendered/accessibility review, rights checks and independent learner observations. No learning-efficacy or universal-superiority claim is made.

Next:
1. Reconcile this snapshot after #458 closes; the current collection count is 47 (4 Q/K/V/KV-cache + 43 tokenization/embeddings).
2. Run catalogue/extraction validators and record final-head CI/Quarto evidence.
3. Explicitly triage route reconstruction for registered instructional sources, reusing existing fields.
4. Recover missing ByteByteGo/Vizuara URLs only from historical evidence.
5. Keep asset rights and browser review with #156 and #320/#329.
6. Stress-test one small new source end-to-end before scaling to another large collection.
