# Inventory of existing revision support — 2026-11-19

**Status:** source-level inventory and editorial triage; not a rendered UX or learner-outcome sign-off.  
**Scope:** the 62 published Understand and Build pages in the inventory artifact produced by PR #1379, plus existing page-based and non-page revision candidates.  
**Snapshot:** source SHA `817048ecda141fbf256e42237dc1a4f34bf44a88`; CI artifact `revision-coverage-inventory-0e98372c76a6bf1e4b00f731a9e9654ce3fb06d9`.
**Latest assessment tranche:** ten additional Understand pages (the FR/EN pairs text-data, logits, probabilities, loss and gradients) are recorded as `integrated_sufficient` with explicit `revision-summary` anchors; see the audit trail in issue [#1109](https://github.com/JM-Brun/llm-lab/issues/1109).

## 1. Inventory baseline

| Destination | Published pages | FR | EN | Topic groups |
|---|---:|---:|---:|---:|
| Understand | 46 | 23 | 23 | 23 |
| Build | 16 | 8 | 8 | 8 |
| **Total** | **62** | **31** | **31** | **31** |

The artifact records 144 explicit concept-to-page edges in Understand, 18 in Build, and 10 implementation-resource associations, all in Build. The original snapshot reported all 62 `synthesis_status` values as `not_assessed`. The relation pilot adds four explicit page-aid links and `partial` assessments for the FR/EN entropy and cross-entropy lessons. Integrated assessments now cover 28 pages: the FR/EN corpus-preparation and training-examples Build pages, plus the FR/EN causal-masking, transformer-architectures, LLM-overview, generation, post-training, context-engineering, llm-limits, text-data, logits, probabilities, loss and gradients Understand pages. Each assessment points to an explicit `revision-summary` anchor on the lesson. The other 18 Understand and 12 Build pages remain `not_assessed` until individually assessed.

The editorial observations below come from source reviews recorded in issue [#1109](https://github.com/JM-Brun/llm-lab/issues/1109). The artifact and those comments are the evidence base; this document does not claim that every page has received a paragraph-by-paragraph scientific re-review or rendered accessibility review.

## 2. Existing revision-aid entities

### 2.1 Published Quarto page aids

| Artifact | Existing metadata | Existing learner-facing function | Current disposition |
|---|---|---|---|
| `site/{fr,en}/revision-information-theory.qmd` | `destination:practice`, `type:exercise-collection`; language-specific pages | Dedicated revision sheet: core formulas, cross-entropy/KL identity, worked numerical example, conceptual traps, attention/KL vs mutual information, predictive V-information, self-check and answers | Retain as the canonical learner-facing information-theory revision sheet. The pilot now links each language version to its matching entropy and cross-entropy lessons via `revision_of`; the reverse lesson-to-aids view is derived. |
| `site/{fr,en}/compression-revision.qmd` | `destination:deepen`, `type:concept-bridge`; language-specific pages | Mental map and compact conceptual bridge between predictive data compression, model compression and runtime memory; equations, coding constraints, entropy/surprisal distinctions and references | Retain as a Deepen concept-bridge, with candidate role `synthesis`. The source audit confirms substantive coverage of entropy, cross-entropy and likelihood; typed links are deferred until the first page-aid pilot is reviewed because this is a broad cross-topic bridge, not a narrow revision sheet. Do not create another generic compression sheet. |

The two pairs are not interchangeable: the information-theory page is explicitly a Practice revision sheet, while compression is a Deepen concept bridge. Keep their existing editorial types and destinations; the future relation must not rewrite them into a new page type merely to make the inventory work.

### 2.2 Non-page candidates

| Artifact | Current evidence | Classification |
|---|---|---|
| `docs/revision-sheets/information-theory-and-llms-2026-11.md` | 119-line internal Markdown document; overlaps the Quarto sheet but has additional XOR/zlib examples, seven self-checks and extended discussion | **Not currently a learner-facing companion.** Prior review classifies it as an internal editorial/source-work note unless publication intent changes. Do not register it as a revision aid now. |
| `data/resources.yml` | Five records, all `kind: implementation` (GPT config, GPT ops, Transformer block, GPT model, generation modules) | Implementation resources only. Preserve their current kind and `referenced_by` semantics. |
| `docs/source-syntheses/` and `docs/source-reviews/` | Research-source syntheses and technical source reviews | Research provenance/documentation, not learner revision aids. Do not count them as lesson revision coverage. |
| Dedicated flashcard files | No filename-level flashcard artifact appeared in the recursive repository tree inventory | No dedicated flashcard resource identified in this pass. This is not proof that no inline retrieval prompts exist. |

**Conclusion on non-page resources:** the inspected repository does not currently demonstrate a learner-facing non-page revision aid that warrants a new `kind: revision-aid`. Do not extend `data/resources.yml` yet. Keep the possibility in the contract, but defer the adapter and schema change until a concrete, approved learner-facing file or flashcard dataset exists.

### 2.3 Practice and experiment resources are not automatically revision sheets

Existing Practice pages and experiment guides often provide retrieval questions, worked solutions or reproducible procedures. They remain Practice resources according to their current metadata. A page is not a synthesis aid solely because it links to a lesson or contains exercises. A future typed role should be assigned only after an explicit editorial decision about the function it performs.

## 3. Understand inventory — 23 bilingual topic pairs

The following records summarize existing source-level audits. “Reuse” means use the current lesson/Practice support rather than create a duplicate sheet; it does not imply a rendered accessibility sign-off.

| Topic pair | Existing synthesis / retrieval support observed | Disposition |
|---|---|---|
| `causal-masking` | One-minute mental model, formal causal rule, triangular mask visual, distinction from padding/document/loss masks, invariance check and exercises | Reuse; `integrated_sufficient` via `revision-summary`; no second sheet or diagram |
| `context-engineering` | Three context levels and distinctions between stored history, transmitted context and attention-accessible information; seven applied Practice questions | Reuse; `integrated_sufficient` via explicit `revision-summary`; no duplicate overview |
| `contextualized-representations` | One-minute recap, pipeline, same-ID vs context-dependent state distinction, attention-head caveats; Practice self-check and advanced SAE investigation | Reuse; no separate sheet |
| `cross-entropy` | Per-token objective, target distribution, worked example, sequence alignment, masking/reduction and edge cases; exercises and self-check | Reuse the linked information-theory sheet for conceptual recall; the source lesson is explicitly assessed `partial` because shift/mask/valid-token denominator still need targeted retrieval coverage |
| `embedding-space` | Integrated lookup diagram and distinctions among token ID, embedding row/vector and point in space; Practice questions and NumPy exercise | Reuse; no separate sheet |
| `entropy` | One-minute model, definition, numerical example, bounds, entropy vs observed surprisal and self-check; covered by the information-theory revision sheet | Reuse the linked information-theory sheet; the source lesson is explicitly assessed `partial` because context/temperature/calibration caveats need targeted retrieval coverage |
| `gradients` | One-minute recap distinguishes objective, local variation and backpropagation; worked derivation and three answered questions cover cross-entropy derivative, numerical checking and step size | Reuse; `integrated_sufficient` via `revision-summary`; no generic recap |
| `in-context-learning` | Fixed-weights/changing-context distinction, zero/one/few-shot, relation to fine-tuning and RAG, experimental checklist; bilingual diagram added in PR #1112 | Reuse the integrated visual and Practice material |
| `inference-generation` | Distribution-to-selection loop, decoding policy, prefill/decode and KV-cache distinctions; Practice resources | Reuse; `integrated_sufficient` via `revision-summary`; keep generation separate from scoring and training |
| `llm-limits` | Critical synthesis of next-token objective vs guarantees, model/system evaluation dimensions, mechanical-design case; one-minute recap, quick question and four bilingual retrieval questions on truth, emergence, calibration and benchmark scope | Reuse; `integrated_sufficient` via explicit `revision-summary`; no separate sheet |
| `llm-overview` | Introductory mental model, six-stage computation diagram, generation/scoring/training separation, learning outcomes and Practice checks | Reuse as the orientation synthesis; `integrated_sufficient` via `revision-summary` |
| `logits` | One-minute recap separates scores, probabilities and truth; four answered questions cover vocabulary dimension, unnormalized scores, argmax and common-shift invariance | Reuse; `integrated_sufficient` via `revision-summary`; no duplicate sheet |
| `loss` | One-minute recap covers target alignment, valid positions and aggregation; lesson covers teacher forcing, masking, reduction and perplexity, with three answered questions on denominators, generalization and comparability | Reuse; `integrated_sufficient` via `revision-summary`; preserve distinction from per-token cross-entropy |
| `positional-encoding` | One-minute recap, insertion-point diagram, distinction from causal masking, extrapolation limits and bilingual Practice questions | Reuse; no separate sheet |
| `post-training` | One-minute recap and comparison of pretraining, SFT, preference methods and context-only interventions; four retrieval questions and a transfer scenario choosing interventions for changing facts vs fixed output schemas | Reuse; `integrated_sufficient` via explicit `revision-summary`; no separate sheet |
| `probabilites` | Conditional distributions, temperature, filtering/renormalization and calibration distinctions; bilingual visual increment in PR #1119 and exercises | Reuse; no duplicate sheet |
| `queries-keys-values` | Three-projection visual and explicit distinction between Q/K determining weights and V supplying aggregated content; exercises | Reuse; visual already carries the core synthesis |
| `scaled-dot-product-attention` | Five-step mechanism, equations, counterexamples and limits; bilingual Q/K vs V computation visual in PR #1120 and exercises | Reuse; no extra infographic quota |
| `text-data` | One-minute recap traces Unicode text → tokens → IDs → embeddings → contextual representations; six formative exercises, worked solutions and a reproducible GPT-2 tokenizer trace | Reuse; `integrated_sufficient` via `revision-summary`; introductory examples differ between FR and EN but preserve the same tokenization concepts |
| `training-loop` | End-to-end workflow separating forward pass, loss, backpropagation, optimizer update and validation; examples and exercises | Reuse; keep implementation claims aligned with actual code |
| `transformer` | Canonical computation walkthrough with self-check, exercises and code/test references | Reuse; no separate synthesis page |
| `transformer-architectures` | One-minute mental model, six-dimension comparison, original bilingual diagram, architecture/objective/task distinction, limits and four-question Practice companion | Reuse; established positive exemplar; `integrated_sufficient` via `revision-summary` |
| `vraisemblance` | Likelihood chain linked to generation/probabilities, numerical worked examples and Practice transfer questions | Reuse the lesson and exercises; the compression bridge adds a coding-length perspective but does not replace the likelihood-specific questions. Its typed source link is a follow-up after the first pilot review. |

### Understand limits

- The 16-page first-tranche review was initially a structural source audit; later passes deepened selected pairs (embedding/position/contextualization, entropy/cross-entropy, post-training/context engineering and LLM limits).
- Several visual increments have CI and Quarto validation, but no rendered desktop/mobile, keyboard, screen-reader or learner-outcome sign-off is claimed.
- The inventory records observed support and decisions, not a numeric pedagogical-quality score.
- The relation pilot projects four `partial` Understand assessments, four explicit aid links, and 28 `integrated_sufficient` assessments (24 Understand, four Build) into the generated inventory. The remaining 18 Understand and 12 Build pages are still `not_assessed`; rendered UX, accessibility and learner-outcome validation remain separate.

## 4. Build inventory — 8 bilingual topic pairs

| Build pair | Existing revision support observed | Disposition |
|---|---|---|
| `build-path` | Construction order, milestones, verification evidence and distinction between generate, score and train | Keep as route/orientation; no formula sheet |
| `corpus-preparation` | Five-point revision callout (provenance, transformations, splits, tokenizer isolation, hand-off) plus five Practice questions; deeper treatment of annotation, streaming and dataset cards | Reuse the integrated sheet and Practice companion; no extra checklist |
| `training-examples` | Five-point revision callout, eight-point debugging checklist, scoped NumPy implementation/tests and four Practice questions | Reuse; no separate implementation-contract sheet |
| `reference-gpt-config` | Bilingual code walkthrough, configuration fields, validation/test evidence, exercises and implementation-resource link | Reuse walkthrough/tests; no generic sheet |
| `reference-gpt-ops` | Bilingual numerical operations, tensor shapes/conventions, tests and exercises | Reuse; compare the FR/EN recap presentation, but do not infer a content defect from a marker heuristic |
| `reference-transformer-block` | Bilingual block recipe, Q/K/V/O, residual paths, shapes, tests and exercises | Reuse implementation evidence; no separate sheet |
| `reference-gpt-model` | Bilingual assembly walkthrough, model components, tests, exercises and implementation-resource link | Reuse; no duplicate module summary |
| `reference-gpt-generation` | Bilingual autoregressive generation walkthrough, tests, exercises and implementation-resource link | Reuse; no duplicate generation sheet |

Build's six pages without implementation-resource associations are exactly the two language versions of `build-path`, `corpus-preparation` and `training-examples`. This is not automatically a defect: the first is orientation, and the latter two need a specific resource need established before linking code. The ten implementation associations remain distinct from revision coverage.

## 5. Decisions and next work

1. Keep the two published page-aid pairs as the current explicit revision-aid candidates; do not create more generic sheets.
2. Keep the internal Markdown sheet outside the learner-facing resource graph until its publication and maintenance role is explicitly changed.
3. Do not add a non-page revision resource kind to `data/resources.yml` yet; current records are implementation resources only.
4. Continue individual editorial assessment where evidence is provisional, especially cross-entropy's shift/mask contract and entropy caveats. Causal masking, Transformer architectures, the LLM overview, generation, post-training, context-engineering, LLM limits, text-data, logits, probabilities, loss and gradients now have explicit integrated assessments in both languages; Build corpus-preparation and training-examples remain assessed the same way.
5. The initial page-aid pilot now links `revision-information-theory` to the FR/EN entropy and cross-entropy lessons; the generated coverage inventory reads the ProjectIndex relation and assessment projection. The metadata validator still needs a dedicated follow-up to validate these fields at page-map ingestion.
6. The source audit confirms `compression-revision` as a cross-topic `synthesis` candidate for entropy, cross-entropy and likelihood. Add its typed links after the first pilot is reviewed; do not infer targets from `related` alone.
7. Keep rendered UX/accessibility validation as a separate gate before closing #1109.

## 6. Audit provenance

Relevant issue #1109 records:

- Initial 16-page Understand source triage: [comment 7020226984](https://github.com/JM-Brun/llm-lab/issues/1109#issuecomment-7020226984).
- Existing revision artifacts and information-theory pilot: [comment 7019921778](https://github.com/JM-Brun/llm-lab/issues/1109#issuecomment-7019921778).
- Build audit of all eight topic pairs: [comment 7019937145](https://github.com/JM-Brun/llm-lab/issues/1109#issuecomment-7019937145).
- Causal-masking and Transformer-architectures audit: [comment 7021377526](https://github.com/JM-Brun/llm-lab/issues/1109#issuecomment-7021377526).
- LLM-overview and generation audit: [comment 7021409283](https://github.com/JM-Brun/llm-lab/issues/1109#issuecomment-7021409283).
- Embeddings, position and contextualization audit: [comment 7019976945](https://github.com/JM-Brun/llm-lab/issues/1109#issuecomment-7019976945).
- Post-training and context-engineering audit: [comment 7020045751](https://github.com/JM-Brun/llm-lab/issues/1109#issuecomment-7020045751).
- LLM-limits audit: [comment 7020086727](https://github.com/JM-Brun/llm-lab/issues/1109#issuecomment-7020086727).
- Compression-revision source mapping: [comment 7021256593](https://github.com/JM-Brun/llm-lab/issues/1109#issuecomment-7021256593).
- Build corpus-preparation and training-examples audit: [comment 7021273551](https://github.com/JM-Brun/llm-lab/issues/1109#issuecomment-7021273551).

This inventory is a maintained snapshot, not a second source of truth. Refresh it from the generated inventory artifact and the page-by-page audit records after page moves, additions, translations or content changes.
