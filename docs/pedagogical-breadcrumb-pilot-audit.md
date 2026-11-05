# Pedagogical breadcrumb pilot — source audit baseline

**Audit date:** 2026-11-05  
**Status:** source-level baseline; rendered/browser and learner validation not yet performed.  
**Contract:** [Pedagogical breadcrumb and page-navigation contract](pedagogical-breadcrumb-and-page-navigation-contract.md)  
**Coordination:** #368, #225, #415, #337.

## 1. Existing sources inspected

- `data/guided-route.yml`: six bilingual conceptual stages with core and optional page references.
- `docs/learning-path.md`: explains the conceptual inference route and the separate practical GPT construction route.
- `docs/content-section-mapping.md`: page ownership and four destination crosswalk.
- `site/tools/build_learning_map.py`: validates and resolves the guided-route registry into learning-map stage cards; the route is not currently emitted as per-page breadcrumb metadata.
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
- [ ] Identify all current `pipeline-stepper` occurrences and decide retain/replace on evidence.
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
