# Pedagogical breadcrumb pilot — source audit baseline

**Audit date:** 2026-11-05  
**Status:** guided-route projection implemented on a pilot set; source-level coverage review in progress; rendered/browser, accessibility and learner validation remain pending.  
**Contract:** [Pedagogical breadcrumb and page-navigation contract](pedagogical-breadcrumb-and-page-navigation-contract.md)  
**Coordination:** #368, #225, #415, #337.

## 1. Existing sources inspected

- `data/guided-route.yml`: six bilingual conceptual stages with core and optional page references.
- `docs/learning-path.md`: explains the conceptual inference route and the separate practical GPT construction route.
- `docs/content-section-mapping.md`: page ownership and four destination crosswalk.
- `site/tools/build_learning_map.py`: validates and resolves the guided-route registry, generates learning-map stage cards, and writes per-page guided-context partials.
- `docs/page-metadata-schema.md`: keeps suggested route, conceptual hierarchy, related links, page destinations, and concept relations distinct.
- Five representative French pages: LLM panorama, embeddings, Q/K/V, Build path, and experimental evaluation.

This is a targeted sample, not a complete site inventory. The corresponding English pages and rendered output still require explicit review.

## 2. What the current model already supports

The conceptual route has a suitable single source of truth: `data/guided-route.yml`. It defines six bilingual stages, each with localized title/objective and separate core/optional page lists. The generator resolves those page IDs against published page metadata and fails on missing or unpublished pages.

The curriculum documentation explicitly distinguishes:
- the six-stage conceptual route;
- the separate Build path and its implementation milestones;
- the four published destinations (Understand, Build, Deepen, Practice & reference);
- the exploratory page/concept/resource graphs.

This is sufficient to begin a breadcrumb projection for pages assigned to the six conceptual stages. It is not sufficient to infer a Build milestone breadcrumb or a Practice sequence from the conceptual route.

## 3. Pilot source observations

| Representative page | Existing source-level cues | Initial assessment |
|---|---|---|
| `fr/llm-overview` — system overview | `suggested_route` points to generation; no explicit per-page breadcrumb in the inspected opening; the page already has a concise learning-outcomes callout | A stage breadcrumb can orient the reader in the existing `orientation` stage, provided the stage context does not imply that all pages in it are prerequisites. |
| `fr/embedding-space` — concept lesson | `suggested_route` points from tokenization to positional encoding; an existing custom `pipeline-stepper` shows a five-stop sequence | The stepper is a legacy linear pipeline, not the six-stage curriculum. It omits intermediate representation concepts and compresses unrelated concepts (e.g. Q/K/V, logits, loss) into a misleading single chain. Do not mechanically relabel it as a breadcrumb; review whether it should be replaced by the stage breadcrumb plus local contextual links. |
| `fr/queries-keys-values` — concept lesson | Explicit learner-facing lead explains the boundary with the Transformer and scaled attention; an existing custom `pipeline-stepper` repeats the same five-stop sequence | The local explanation already provides useful context; the global stage context should supplement rather than duplicate it. The generic stepper should not imply QKV is one obligatory stage in a four/five-step pipeline. |
| `fr/build-path` — guided build hub | Distinct Build destination; its own G0–G9 milestones and code/test evidence; no previous suggested-route page | Must not be assigned a conceptual-stage breadcrumb. Any Build breadcrumb must be derived from the Build route/milestone model, not borrowed from `data/guided-route.yml`. |
| `fr/evaluation-experimentale` — experiment guide | Practice destination; explicit objective and useful background links; previous route points to exercises; not listed in the six-stage guided-route registry | Do not fabricate a guided-route stage. Use destination/section navigation and its actual exercise context unless a separately defined Practice route is established. |

## 4. Preliminary design decisions

1. Use the six-stage registry as the sole source for Understand-route breadcrumb membership.
2. A page listed as a core or optional resource in a stage may receive that stage context, but optional membership must remain visibly optional and must not be presented as a prerequisite.
3. Some pages occur in more than one stage (for example generation is used for the early inference preview and later prediction/decoding). The current registry therefore permits multiple valid route contexts. The implementation must not silently choose one based on file order. Decide whether to show the primary context plus an alternate-stage link, or omit the breadcrumb when a unique primary context cannot be justified.
4. Build and Practice remain separate. Do not add artificial stages to the conceptual registry merely to make every page display a breadcrumb.
5. The current `pipeline-stepper` needs a separate audit. It appears to be a legacy five-stop overview, not the guided route. Retain only if its distinct instructional purpose can be demonstrated and its labels/links are corrected; otherwise replace it with the shared route breadcrumb and meaningful local links.
6. The breadcrumb must not duplicate the chapter lead, learning outcomes, or previous/next links.

## 5. Remaining pilot work

- [ ] Inspect English counterparts for all five archetypes and record semantic parity.
- [ ] Inspect the actual rendered site for the five page types on desktop and mobile.
- [ ] Determine how multiple stage membership is presented, especially generation.
- [ ] Inspect the Build milestone source and decide whether it already provides a stable parent/step context suitable for a separate Build breadcrumb.
- [ ] Inspect Practice and Reference pages to confirm that omitting the conceptual breadcrumb remains coherent.
- [x] Identify all current `pipeline-stepper` occurrences and decide retain/replace on evidence (§14: exhaustive scan; eight five-stop blocks retired, text-data local stepper retained per §12.1).
- [ ] Prototype a shared accessible breadcrumb using existing generated route data; do not add new page metadata until the projection is proven.
- [ ] Add focused tests for route membership, localization, ambiguous membership, optional status, and links.
- [ ] Run Quarto/CI and perform separate browser/accessibility/learner checks.

## 6. Evidence boundary

This baseline is based on source files and the generator implementation. It does not establish:
- that the current rendered breadcrumb/navigation is visually or accessibly correct;
- that every French and English page pair is semantically equivalent;
- that the proposed breadcrumb improves learner comprehension;
- that Build or Practice currently has a suitable machine-readable route for breadcrumb generation.

Do not report these as validated until the corresponding checks are completed.

## 7. Bilingual counterpart audit (2026-11-05)

The five archetypes were then checked in both language trees on the current `main` source:

| Archetype | English page | French page | Parity and breadcrumb implications |
|---|---|---|---|
| System overview | `site/en/llm-overview.qmd` | `site/fr/llm-overview.qmd` | Both identify the page as an overview, expose learning outcomes, and point from the index to the generation preview. The French page is not a literal translation, but the scope and role are aligned. Both belong to `orientation`. |
| Concept lesson — representations | `site/en/embedding-space.qmd` | `site/fr/embedding-space.qmd` | Both have the same page-map scope, purpose, suggested previous/next pages, core explanation and self-check structure. Both contain the same five-stop legacy stepper. Keep the bilingual treatment aligned when replacing it. |
| Concept lesson — Q/K/V | `site/en/queries-keys-values.qmd` | `site/fr/queries-keys-values.qmd` | Both explain the same projection roles, use the same local predecessor/successor, include the same five-stop legacy stepper, and provide a self-check. The EN/FR chapter leads and terminology are semantically aligned. |
| Guided build | `site/en/build-path.qmd` | `site/fr/build-path.qmd` | Both state that the route guides inspection and verification of the tested reference implementation, distinguish random-weight inference from training, and expose G0–G9 milestones. Neither should inherit an Understand-stage breadcrumb. |
| Practice / experiment | `site/en/experimental-evaluation.qmd` | `site/fr/evaluation-experimentale.qmd` | Both describe a protocol-design transfer exercise rather than implementation or a benchmark result. Both link to relevant mathematical/training background; neither belongs to the six-stage Understand route. |

The source-level bilingual parity is good for these five representative pages. This is not a full language-parity audit and does not validate translated rendered navigation or responsive behavior.

## 8. Exact legacy stepper inventory and correction

A targeted source search and direct inspection of the four representative lesson files confirmed these four occurrences; this is a bounded inventory, not a claim that no other custom navigation pattern exists:

- `site/en/embedding-space.qmd`
- `site/fr/embedding-space.qmd`
- `site/en/queries-keys-values.qmd`
- `site/fr/queries-keys-values.qmd`

The four blocks encode the same five stops: Text → Embeddings → Attention (Q, K, V) → Logits → Loss & Training.

This sequence is not a valid projection of `data/guided-route.yml`: it omits tokenization as a distinct topic and positional/contextualized representations; places Q/K/V directly after embeddings, omitting Transformer computation context; jumps from Q/K/V to logits, omitting scaled dot-product attention and causal masking; then jumps from logits to loss/training, omitting probabilities, likelihood and the distinction between inference and learning. It presents a single linear chain where the curriculum is staged and includes optional material and an intentional revisit of generation.

**Decision:** retire this five-stop stepper on all four pages. Do not preserve it under a new label and do not make it the breadcrumb. The page-level suggested-route links and explicit local chapter leads already provide valid immediate transitions. Replace the stepper only when the shared route projection is ready; until then, omission is less misleading than a false curriculum.

The separate end-of-page `route-nav-cards` on Q/K/V are useful local previous/next links and should remain distinct from the global curriculum breadcrumb. Their labels should not be treated as proof of a single global linear sequence.

## 9. Membership model confirmed by source

The current six-stage registry supports a deterministic membership projection without new page metadata:

- A page may have zero, one, or multiple memberships.
- Membership must preserve both `core` and `optional` status.
- Membership is language-local at the page-ID level but paired by the stage's localized title/objective.
- `generation` is intentionally core in both `orientation` and `prediction`; the narrative explicitly defines the first as a black-box preview and the second as a return after logits/probabilities.
- A breadcrumb cannot infer which occurrence the reader is following from the page URL alone.

Therefore, a universal page-level breadcrumb is not always semantically well-defined. The safe default is to show the stage context as a **set of valid route contexts**, not fabricate a unique ancestor. For a single-membership page, a normal breadcrumb can identify the stage and current page. For a multi-membership page, show both labelled contexts (preview / prediction) or a compact “also appears in” relation; do not choose by YAML order. If the component cannot express this distinction accessibly and compactly, omit the breadcrumb on that page and retain the stage cards as entry points.

## 10. Implementation sequence updated

1. Remove the misleading five-stop stepper from the four bilingual pages in one coordinated content change.
2. Implement a small, testable projection from the existing route registry to page membership, reusing the route loader/validation path. Do not introduce front-matter membership or another YAML registry.
3. Render a shared component for pages with one unambiguous membership; explicitly handle optional membership and multiple membership.
4. Keep Build, Practice, Deepen and Reference pages out of the Understand breadcrumb unless their own canonical route model is already documented and machine-readable.
5. Add tests for the exact known cases: one core membership, one optional membership, no membership, and `generation` with two core memberships; assert FR/EN labels and stable links.
6. Review rendered desktop/mobile and keyboard/screen-reader behavior before enabling the component broadly.

**Branching note:** this audit is being carried forward from the source-level baseline into a clean documentation PR based on current `main`. The four-page cleanup is isolated in [PR #524](https://github.com/JM-Brun/llm-lab/pull/524); it removes only the misleading stepper and deliberately does not claim that a new breadcrumb is already rendered on those four pages.

## 11. Implementation status after the first merged pilot (2026-11-05)

The first implementation slice is now merged:

- [PR #522](https://github.com/JM-Brun/llm-lab/pull/522) was merged as `84e951d`.
- It adds a typed projection from the validated route model, preserving all page memberships and `core` / `optional` roles.
- It adds a single-membership ordered context and a distinct multi-membership section; generation shows both `orientation` and `prediction` with their separate objectives.
- The existing build script generates per-page context partials before Quarto rendering. The FR/EN overview and generation pages include the new component.
- Stable stage anchors are generated on the guided-route overview.
- Main-branch Python CI, Quarto render, and Quarto publish workflows completed successfully for the merge commit. The PR-level Quarto checks also passed site rendering, generated map checks, knowledge-graph export, timeline parity, and local-link checks.

The Q/K/V and embedding lessons were intentionally not changed in PR #522 because their legacy five-stop stepper needed a separate, bounded content correction.

[PR #524](https://github.com/JM-Brun/llm-lab/pull/524) removes the misleading stepper from the four FR/EN embeddings and Q/K/V pages. It intentionally does not add a breadcrumb replacement: the generated route-context component is currently piloted on overview/generation pages, and the source audit has not yet established that the four lesson pages should receive an unambiguous context without a rendered review.

### Remaining validation and rollout

- [ ] Confirm PR #524 Python CI and Quarto/local-link checks on its latest head.
- [ ] Inspect the rendered FR/EN overview, generation, embeddings, and Q/K/V pages at desktop and mobile widths.
- [ ] Inspect the generated single-membership context and the multi-membership generation context for hierarchy ambiguity, visual weight, and placement relative to the chapter lead.
- [ ] Verify keyboard focus, screen-reader announcement order, `aria-current`, contrast, and responsive wrapping.
- [ ] Record the rendered review and any corrections in #337 / #368 before marking the breadcrumb/context pilot complete.
- [ ] Run a small learner transfer/comprehension check; CI and visual review do not establish pedagogical effectiveness.
- [x] Search for any remaining `pipeline-stepper` occurrence and ensure no misleading linear chain remains (§14; rendered verification via the extended `scripts/site-browser-review.mjs` still to run on the deployed site).

**Evidence boundary:** successful Python CI and Quarto render/publish establish technical generation and link integrity, not accessibility conformance or improved learner comprehension. The new component is a first implementation pilot, not yet a validated site-wide design. The four-page stepper removal is a corrective deletion, not evidence that breadcrumb rollout is complete.


## 12. Reconciliation of the nested-breadcrumb proposal (2026-11-05)

A follow-up source trace clarifies that the desired two levels should be the **site-location breadcrumb** and the **pedagogical route context**, not a breadcrumb derived from conceptual hierarchy.

Evidence from the current source:

- `site/_quarto.yml` defines distinct bilingual navigation trees. The FR Q/K/V page is nested under “Attention et sortie du Transformer”; the FR text-data page is nested under “Du texte aux représentations et au calcul”. Their site-location ancestry therefore differs.
- `site/styles.scss` contains a `.llm-breadcrumb` style block labelled “Global breadcrumb”, but a stylesheet selector is not evidence that a matching element is emitted.
- `site/includes/title-metadata.html` does not contain breadcrumb markup.
- The FR and EN Q/K/V pages include their matching `generated-guided-context-<language>-queries-keys-values.qmd` partials; these are pedagogical-context projections from the shared generator.
- The text-data page retains a local `.pipeline-stepper` block for the text-to-representation sequence. It is not a site breadcrumb or the generated curriculum context and must not be silently repurposed as either.
- Unlike Q/K/V and embeddings, the FR/EN text-data pages did not yet include their generated route-context partials, despite both being core members of the `text-input` stage. This was recorded as a bounded integration gap and is addressed by [PR #530](https://github.com/JM-Brun/llm-lab/pull/530).
- Q/K/V also has explicit previous/next route cards in its page body. These remain reading transitions and must not be conflated with either breadcrumb.

Consequences:

1. Keep the generated pedagogical context as the only pedagogical breadcrumb/context renderer.
2. If a site-location breadcrumb is implemented, derive it from Quarto navigation and label it as site location; do not use `hierarchy.parents`.
3. Do not add a local conceptual breadcrumb. Multi-parent conceptual relations remain contextual links.
4. Before changing runtime code, trace the build generator that emits `generated-guided-context-*` and the remaining global-breadcrumb CSS; verify whether the reported click issue comes from a link in the generated pedagogical context, the sidebar, or a page-level route card.
5. Record actual hrefs and destinations from rendered FR/EN output. Source-level inspection alone does not reproduce the browser behavior.

This addendum supersedes the earlier exploratory proposal to derive a second local breadcrumb from page hierarchy. The canonical contract is this document; no separate nested-breadcrumb contract should be maintained.


### 12.1 Text-data navigation decision

The text-data pages retain their existing local text-to-representation stepper. They do not receive an additional generated guided-route cue because that would stack two page-level navigation elements for closely related instructional orientation. The short-lived inclusion from PR #530 was removed by the corrective navigation change in [PR #534](https://github.com/JM-Brun/llm-lab/pull/534).


## 13. Corrective review after learner-facing feedback (2026-11-05)

The first implementation direction stacked a route-context breadcrumb with other page-level navigation cues and repeated the current page title immediately before the page heading. This did not meet the requested visual harmonization.

Corrective decision:

- Keep the Quarto sidebar as the global site-navigation mechanism; do not add a second page-level site breadcrumb by default.
- For a single guided-route membership, render one compact but visually legible stage cue, using the established green/neutral stepper visual language. The page heading identifies the current page and must not be repeated inside the cue.
- Keep multiple route memberships as a distinct contextual section with all relevant stage objectives; do not force them into a single breadcrumb.
- Do not add the generated route cue to text-data while its existing local text-to-representation stepper is present. Two navigation bars on the same page would be redundant.
- The Q/K/V page should have one pedagogical context cue, not two adjacent representations of the same location.

The corrective implementation and its browser-rendered verification are tracked in [PR #534](https://github.com/JM-Brun/llm-lab/pull/534), merged 2026-11-05 (the earlier reference pointed to PR #532, a number that was never used).


## 14. Exhaustive continuity scan and remaining-stepper correction (2026-11-05)

A full continuity scan of the deployed French site (all published pages) and of every guided-route member in both language trees, cross-checked against `data/guided-route.yml`, the generator, and the deployed site at `d6c5f9f`, found that the §8 inventory was a bounded four-occurrence sample. After #524, ten `pipeline-stepper` occurrences remained on `main`:

- `site/fr/text-data.qmd`, `site/en/text-data.qmd` — the local four-stop text-to-representation stepper, retained by the §12.1 decision.
- `site/{fr,en}/scaled-dot-product-attention.qmd`, `site/{fr,en}/causal-masking.qmd`, `site/{fr,en}/logits.qmd`, `site/{fr,en}/cross-entropy.qmd` — the same five-stop chain retired by §8, with the same defects: from `logits` and `cross-entropy` the step-3 link skips scaled dot-product attention and causal masking; the step-5 link skips probabilities and likelihood; and the step-3 label differs across the four pages.

Decision (extension of the §8 rationale): retire the eight five-stop blocks without relabelling, and add the generated single-membership guided-route context to those four lessons in both languages, mirroring the #524 + #528 sequence. `text-data` stays untouched (§12.1). `scripts/site-browser-review.mjs` is extended so the Chromium route-context audit covers all ten guided-context pages and asserts zero legacy steppers on the four corrected lessons.

The full scan — cue-coverage map, the nested-route mapping, and the remaining rollout gaps (nine core route pages still carry no visual cue; the prediction → learning tail has no route cards after `logits`) — is recorded in [visual-route-continuity-audit-2026-11-05.md](visual-route-continuity-audit-2026-11-05.md).

This closes the §5 and §11 stepper-inventory items at the source level only. Rendered/browser verification, the accessibility review and the learner check remain open, as does the #535 follow-up.


## 10. Rendered header audit — 2026-11-05

A Chromium artifact from the merged browser-review run for PR #534 was inspected at desktop (1440 px) and mobile (390 px), French, light theme, for Q/K/V. The screenshot and `report.json` are retained in the GitHub Actions artifact `site-browser-review-0009a61155216d0fb16779079c1b71b2da0cd175` (run `42100872126`).

### Observed opening

The rendered Q/K/V header contains:

1. a custom `.llm-breadcrumb` generated from the active Quarto sidebar;
2. Quarto's native `.quarto-title-breadcrumbs`, repeating the same sidebar ancestry and current page;
3. the H1 and subtitle;
4. the generated guided-route stage context;
5. the chapter lead;
6. epistemic/status badges;
7. an “L'idée à retenir” callout;
8. the first section heading and its explanation.

The two site-location breadcrumbs are redundant. The browser audit's Axe output independently identifies the native `.quarto-title-breadcrumbs` link and reports a minor contrast shortfall (4.48:1 against a 4.5:1 threshold). The custom breadcrumb is therefore not needed to provide the hierarchy and should be removed rather than visually combined with the native one.

The mobile capture also shows the Quarto sidebar's compact navigation controls. These are global navigation controls, not a third page breadcrumb, and should remain intact.

### Header composition decision

Use a nested but semantically separate composition:

- Quarto native breadcrumb: site location;
- H1/subtitle: page identity;
- generated guided-route context: pedagogical role of the page;
- chapter lead and takeaway: page orientation and core mental model;
- optional local stepper: a process/representation sequence within the content.

The stage context is not appended to the site breadcrumb. A local stepper is not labelled as a learning path. The text-data and scaled-attention pages receive the same generated stage context as Q/K/V, while retaining their distinct local process steppers after the introductory mental model.

### Follow-up verification

- Confirm exactly one native Quarto breadcrumb and no `.llm-breadcrumb` on Q/K/V, text-data, and scaled-dot-product attention, in French and English.
- Confirm the three pages expose their correct guided-route stage (text-input for text-data; computation for Q/K/V and scaled attention).
- Confirm local steppers remain distinct, correctly labelled, and below the introductory explanation.
- Review desktop/mobile screenshots and Axe results before merging.
- Extend the pilot to other page archetypes only after this three-page composition is validated; do not mass-insert a context cue into every page without checking its value.


## 11. Text-data nested context decision — 2026-11-05

The initial §14 continuity decision retained the local text-data stepper and omitted a generated stage context to avoid two adjacent navigation bars. The subsequent page-header review distinguishes their semantics: the generated stage context identifies the page's place in the six-stage curriculum (site-learning context), while the local four-stop stepper explains the internal text-to-representation sequence (within-page process). They are therefore not duplicate navigation cues when visually nested and separated in the page opening.

The explicit reader requirement is to expose both the site breadcrumb and the pedagogical stage context on text-data, while retaining the useful local representation stepper. This addendum supersedes only the §14 statement that text-data must stay without a generated stage context. It does not change the retirement of the misleading five-stop steppers on scaled attention, causal masking, logits, and cross-entropy.

Validation remains pending: rendered FR/EN desktop/mobile screenshots must confirm the three dimensions remain visually distinct and the page opening is not overloaded.
