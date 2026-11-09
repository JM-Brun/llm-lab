# Learning-path and destination audit — 2026-11-05

**Scope:** reader-facing Understand, Build, Deepen and Practice navigation; the six-stage guided route; and a bounded text-to-attention / prediction-and-loss sample in French and English. **Baseline:** `9ab66d1f6eb12d00e8346b58646f010304282966` (PR [#461](https://github.com/JM-Brun/llm-lab/pull/461), based on main `c383a93faf076d210522e8f88fbd5beb9c0973fc`). The only difference from that main relevant to the sampled route is the proposed text-data heading and diagram correction. The unrelated local Serena configuration was not audited.

**Method and limits:** compared canonical architecture and curriculum guidance with route YAML, generated route, Quarto sidebar, hubs, exercise collections and selected page bodies in both languages. Inspected the published learning-map page in the in-app browser in EN and FR. This is not a complete page-by-page scientific, bilingual, accessibility, or learner-outcome audit. Page-body statements below identify the sampled evidence; labels alone do not prove that learners can meet an objective.

## Status on main, 2026-11-09

This audit is kept as a dated record of the state at its baseline; its findings, counts (for example "21 concepts and 26 relations") and the "published map defect" description are **not** updated below. A later check of `origin/main` at `942cae0` found:

| Finding | Status on main | Evidence checked |
|---|---|---|
| P0 map controls rendered as code | Appears addressed by [#464](https://github.com/JM-Brun/llm-lab/pull/464) ("render interactive learning map") | The generated territory include contains no `<pre>` blocks and the renderer emits the `data-map-mode` and `data-map-viewport` controls. The published site was **not** re-inspected. |
| P1 practice links misstate availability | Appears addressed by [#465](https://github.com/JM-Brun/llm-lab/pull/465) ("clarify exercise availability") | The English `generation` page no longer promises extended exercises; wording and the French pages were not re-reviewed. |
| P1 one prerequisite list for every exercise | Not re-checked | — |
| P1 optional Understand pages called "deep dives" | Addressed by [#466](https://github.com/JM-Brun/llm-lab/pull/466) | Both generated route partials now use "Optional resources" / "Ressources facultatives"; "Optional deep dives" no longer appears. |
| P2 Build promises construction | Addressed in part by [#470](https://github.com/JM-Brun/llm-lab/pull/470) ("clarify Build path evidence") | Commit title only; page content and the G2 partial-slice wording were not re-verified. |
| P2 softmax bridge; P2 actionable stage transitions | Not re-checked | The outcome of PR #456 was not looked up. |

Nothing here is a claim about learner outcomes.

## Assessment

The four destinations are a useful distinction between **reader jobs**, not four difficulty levels. The existing separation between a conceptual route, a practical build and optional depth should remain. The highest-impact problem is that the published interactive map does not currently render its controls and viewport, followed by misleading practice links and status. The next issue is that the route conflates *optional* with *Deepen*, although an optional item can belong to Understand, and a core task can link to Practice. There is not yet evidence that reordering the whole curriculum or inventing another taxonomy would improve learning.

### Reader-job contract

| Destination | Observable reader job | Boundary to preserve |
|---|---|---|
| Understand | Explain a mechanism, trace a small example, and identify its limitations. | Keep the minimum necessary notation and caveats; not a ban on equations or short self-checks. |
| Build | Inspect, run, construct or modify a named artifact and check a concrete result. | Distinguish guided tours of existing code, tasks to implement, and planned training work. |
| Deepen | Answer a more specific why/how/under-which-assumptions question. | Optional relative to a particular first pass, not inherently unnecessary to every learner or task. |
| Practice and experiment | Retrieve, calculate, diagnose, transfer, or test a claim against evidence. | Cross-cutting activity rather than a fourth chronological depth; distinguish a worked exercise from an empirical experiment. |
| Reference | Look up terminology, history or sources. | Useful support, not a mandatory prerequisite sequence. |

## Findings and proposed actions

### P0 — Published map controls and canvas are rendered as code

**Confidence: high for the observed published pages; cause requires confirmation. Confirmed rendered defect.** On the published [English map](https://jm-brun.github.io/llm-lab/en/learning-map.html) and [French map](https://jm-brun.github.io/llm-lab/fr/learning-map.html), the browser DOM contained literal `learning-map-filter` and `learning-map-canvas` markup in two `<pre><code>` blocks. The `data-learning-map` outer element existed, but `[data-map-mode]` and `[data-map-viewport]` did not; a loading message remained. The static guided route and resource list were present. This is more specific than an uncertain JavaScript or network failure: required DOM elements are absent in the observed render.

The source is generated from [`TERRITORY_MAP_TEMPLATE`](../site/tools/learning_map_renderers.py) into [`generated-map-territories-en.qmd`](../site/includes/generated-map-territories-en.qmd) and its French counterpart. Indented nested HTML in a Markdown include is a plausible rendering cause, not yet a proven root cause across Quarto versions. **Next:** reproduce on the current head using the CI-pinned renderer; fix the generating source rather than editing generated HTML; add a render-level regression asserting real controls and viewport in both languages; then verify territory navigation, keyboard and recovery separately under [#337](https://github.com/JM-Brun/llm-lab/issues/337) / [#417](https://github.com/JM-Brun/llm-lab/issues/417). Metadata/link success does not protect this boundary.

### P1 — Practice links misstate what is available

**Confidence: high. Confirmed editorial/status defects.** Both [`generation`](../site/en/generation.qmd) pages promise extended exercises and link to `#generation`, but the [exercise collection](../site/en/exercises.qmd#generation) only lists prerequisites and planned focus. Both [`embedding-space`](../site/en/embedding-space.qmd) pages similarly link to the currently empty `#transformer` collection as extended exercises. The text-data link leads to a collection explicitly marked as planned, without extended tasks. In contrast, the math collection contains seven worked exercises and attention contains two activities, but [`probabilities`](../site/en/probabilities.qmd), [`cross-entropy`](../site/en/cross-entropy.qmd), and [`likelihood`](../site/en/likelihood.qmd) and their French counterparts still say detailed exercises have not been written.

**Impact:** readers can be sent to an empty exercise destination or discouraged from using existing material. Link validity tests pass because the anchors exist. **Next:** align link labels and collection status in FR/EN; link to an actual relevant task where one exists, otherwise say the collection is planned and keep the in-page self-check. For the text-to-representation sequence, reuse the three proposed bundles and independent-review/release gates in [the existing inventory](formative-activity-inventory.md) and [#220](https://github.com/JM-Brun/llm-lab/issues/220); do not describe drafts as released.

### P1 — One list of prerequisites makes individual exercises look harder than they are

**Confidence: high for wording; medium for learner impact.** The math collection lists eight linked prerequisites, including the two Deepen pages mathematical foundations and tensors, before seven heterogeneous exercises. The first exercise asks for softmax, negative log likelihood and a logit gradient; the fourth concerns soft targets and KL, while the fifth asks for tensor shapes. Not every exercise needs every listed prerequisite. The attention collection similarly lists Q/K/V, scaled attention, causal masking and tensors before an initial weighted-sum task that supplies the weights and vectors.

**Next:** present collection-level links as a reading menu and attach minimal task-specific requirements to the available exercises, marking tensor/Deepen references as optional where appropriate. Keep gradient or matrix-notation requirements explicit where genuinely needed; do not declare an exercise beginner-level without checking its actual steps and answer. This makes practice available throughout Understand and Build without treating optional depth as a blanket gate.

### P1 — The route calls optional Understand pages “deep dives”

**Confidence: high. Confirmed projection/label mismatch.** The orientation stage in [`data/guided-route.yml`](../data/guided-route.yml) places `transformer-architectures` and `llm-limits` in `optional_pages`; the [generated route](../site/includes/generated-guided-route-en.qmd) labels that entire group “Optional deep dives” / “Approfondissements facultatifs”. Both pages are in the Understand sidebar and carry `destination:understand`. Conversely, the route intentionally includes the Practice evaluation page among its core resources. This shows that *route role* and *destination* are separate axes, rather than a reason to retag the pages.

**Next:** rename the group to “Optional resources” / “Ressources facultatives”, or explicitly show the destination when a reader benefits from it. Update the generator, tracked bilingual generated partials and targeted renderer tests together. Avoid a migration or a new classification model; retain Practice's legitimate role in a core learning stage.

### P2 — Build promises construction but primarily delivers an annotated tour

**Confidence: high for current page content; medium for the design decision.** Both [Build hubs](../site/en/build-path.qmd) say the path builds a GPT and tell readers to build operations, but the specific outcomes emphasize locating modules, running existing code/tests and explaining a randomly initialized model. The linked [operations tour](../site/en/gpt-ops-walkthrough.qmd) explains existing source, provides checks and contains exercises; it is valuable, but does not by itself show that a learner independently constructed all modules. The G2 row calls the pipeline conceptual while [`training_examples.py`](../src/llm_lab/foundations/training_examples.py) and its [tests](../tests/unit/test_training_examples.py) already implement a restricted sliding-window/shift slice; that does not establish a complete corpus, packing or batching pipeline.

**Next:** state the present mode honestly as “guided inspection, execution and small construction challenges”; identify one build/verify task per available milestone and its starter, expected result, tests and solution. Mark G2 as partial with the narrow implemented slice and remaining gaps. Preserve random-weight, no-trained-quality and incomplete-training caveats. Coordinate any code-boundary work with [#446](https://github.com/JM-Brun/llm-lab/issues/446); do not imply that this documentation change completes an end-to-end training path.

### P2 — Explain the softmax dependency without forcing a rigid reorder

**Confidence: medium. Pedagogical risk to test, not proven learner failure.** The stage 4 attention lesson introduces row-wise softmax and a worked example before stage 5's canonical probability/softmax lesson. The attention page does state that softmax normalizes scores and supplies numerical weights, so this is not an unexplained use in every respect. Still, a reader who cannot reconstruct the weights has no explicitly signposted just-in-time bridge to the full definition before the worked calculation. The existing route is deliberately a progression, not a strict prerequisite DAG.

**Next:** test a brief local explanation (“turn scores into positive relative weights summing to one”) and a contextual link to the existing probabilities page, with the difference between attention-position weights and vocabulary probabilities explicit. Keep the worked attention example and leave the full softmax/temperature treatment canonical in probabilities. Coordinate with open [PR #456](https://github.com/JM-Brun/llm-lab/pull/456), which proposes an attention-depth split; do not duplicate its work or assume it has merged.

### P2 — Make the stage transitions actionable, then test with a learner

**Confidence: medium. Proposed design, not an established outcome.** The guided route has objectives and core/optional links; it has a single Build companion after all stages but no per-stage practice or Build action. Lessons do have local self-checks, and the Q/K/V page already links to a real attention activity and the Transformer-block tour. These good cross-links are not consistently surfaced at route level.

**Next:** prototype one stage only: “Understand: explain why changing V can change output but not weights; Practice: calculate the provided weighted sum; Build: inspect the Q/K/V projections in the block tour; Deepen: cross-attention when comparing streams.” Each is a choice, not a compulsory sequence. Use an existing activity and preserve uncertainty/cancellation in the Q/K/V check. Test navigation and a transfer question with an independent learner using [the pilot protocol](learner-validation-pilot.md) / [#447](https://github.com/JM-Brun/llm-lab/issues/447) before scaling the pattern. Do not equate a click, correct example, or author demonstration with durable mastery.

## Evidence matrix and preservation ledger

| Cluster (FR and EN) | Sampled body evidence | Decision and material to preserve |
|---|---|---|
| Text-data / tokenizer / embedding | Text-data explains the pipeline; tokenizer strategies compares segmentation and whitespace failure; embedding-space works through lookup and distinguishes initial and contextual states. | **Complementary**, not duplicate lessons. Preserve tokenizer/model compatibility, discrete ID vs vector, the hand-checkable matrix, position and contextualization caveats. |
| Q/K/V / scaled attention / causal mask | Q/K/V describes projections and shape/role distinctions; scaled attention computes scores, normalization and aggregation; the mask page owns the future-position constraint. | **Complementary with a potential just-in-time bridge.** Preserve $d_k$ vs $d_v$, weighted cancellation, softmax-axis and all-masked-row caveats. Coordinate changes with #456. |
| Logits / probability / cross-entropy | Logits is now a score/shape lesson; probabilities owns softmax and temperature; cross-entropy connects targets, alignment and loss. | **Complementary.** The old 2026-11-04 softmax-duplication recommendation is stale on this head. Preserve normalization vs calibration vs truth, one-hot NLL and masking/reduction distinctions. |
| Build / exercises | Build provides five tours, tests and milestone statuses; Practice mixes seven math exercises and two attention exercises with planned collections. | **Distinct jobs, incomplete status and navigation.** Preserve worked answers, code and test links; do not turn planned work into a completed implementation or demand all Deepen pages as prerequisites. |

## Architecture and traceability

| Entity or projection | Canonical owner / consumer | Audit boundary |
|---|---|---|
| Curriculum and pedagogical prerequisites | [`learning-path.md`](learning-path.md), with [`content-section-mapping.md`](content-section-mapping.md) for page and milestone ownership | Narrative curriculum, not page route edges. |
| Six-stage conceptual route | [`data/guided-route.yml`](../data/guided-route.yml) → [`build_learning_map.py`](../site/tools/build_learning_map.py) → tracked FR/EN route partials → learning-map pages | Core/optional stage roles are not page destination or strict prerequisites. |
| Page identity, editorial role and links | `LLM-LAB-PAGE-MAP v1` in each `site/{fr,en}/*.qmd`; [`page-metadata-schema.md`](page-metadata-schema.md); [`check_page_metadata.py`](../site/tools/check_page_metadata.py) | Suggested route, hierarchy and related are different relations; `topic` is not a concept ID. |
| Sidebar and territory discovery | [`site/_quarto.yml`](../site/_quarto.yml) and page metadata → map generator → generated includes, data and browser UI | Navigation order does not prove prerequisites. Published interactive UI currently has the rendering defect above. |
| Domains, concepts and semantic relations | [`data/domains.yml`](../data/domains.yml) and [`data/concepts.yml`](../data/concepts.yml), schema version 1; concept registry validator | Six domains; 21 concepts and 26 typed relations validated. Concept domains and a Deepen page's single primary domain are distinct. |
| Learning resources | Published page IDs in concept `resources`; five first-class implementation records in [`data/resources.yml`](../data/resources.yml), schema version 1 | The first-class seed does not represent every exercise, experiment, reference or dataset; do not equate those records with page IDs. |
| Standards projection | [`export_knowledge_graph.py`](../site/tools/export_knowledge_graph.py) → generated JSON-LD | An interchange projection, not the authored curriculum or interactive map. |

## Validation and remaining work

- `.venv/bin/python site/tools/check_page_metadata.py` — passed.
- `.venv/bin/python site/tools/check_concept_registry.py` — passed: 6 domains, 21 concepts, 26 relations.
- `.venv/bin/python site/tools/check_resource_registry.py` — passed: 5 resources.
- The validators check defined metadata/graph contracts, not editorial placement, exercise availability, DOM rendering or learning.
- Published map: inspected in the in-app browser in EN and FR; this was not a full desktop/mobile, keyboard, touch or screen-reader review. The deployment commit was not independently established.
- No new tests or site render were run for this audit. PR #461's hosted CI and Quarto workflows passed at `9ab66d1`; those checks do not disprove the observed published map defect.
- No independent learner pilot, external source re-audit, complete semantic bilingual review, or proof of mastery was performed.

**Recommended order:** (1) reproduce and repair the published map at the render boundary; (2) reconcile exercise promises, availability and per-task prerequisites; (3) rename optional route resources and verify generated bilingual output; (4) clarify Build and the G2 partial slice; (5) coordinate the attention bridge with #456 and pilot one stage-level cross-destination pathway. Review visual navigation separately under #337 and the formative release gates under #220/#320.
