# Guided-route page membership projection

**Status:** bilingual page-level pilot implemented on overview, generation, embeddings, Q/K/V and the optional attention-score-scaling deep dive; visual and accessibility review remains pending.  
**Source of truth:** `data/guided-route.yml`.  
**Implementation:** `build_guided_route_memberships()`, `render_guided_page_context_markdown()`, and `write_guided_page_context_fragments()` in `site/tools/build_learning_map.py`.  
**Tests:** `tests/knowledge/test_guided_route_memberships.py`.  
**Coordination:** [#368](https://github.com/JM-Brun/llm-lab/issues/368), [#337](https://github.com/JM-Brun/llm-lab/issues/337). Historical implementation attempts: [closed PR #516](https://github.com/JM-Brun/llm-lab/pull/516) and [closed PR #519](https://github.com/JM-Brun/llm-lab/pull/519).

## Purpose

Provide a deterministic page-to-stage index for the Understand curriculum without treating a curriculum stage as a unique conceptual parent. The projection is a read-only view of the existing, validated route model. It does not create a second registry or change page metadata.

## Navigation contract

The route context answers **where this page is used in the guided Understand curriculum**. It is not a projection of the site sidebar, page hierarchy, suggested previous/next links, concept relations, Build dependencies, or the exploratory resource graph. These structures answer different questions and must remain distinct.

- One membership: show a breadcrumb-like ordered context linking to the stage anchor and marking the current page with `aria-current="page"`.
- Multiple memberships: show every valid stage context and its objective in a separate section; do not use breadcrumb semantics or invent a primary parent.
- Optional membership: label it as optional, never as a prerequisite.
- No membership: omit the route context. Build, Practice, Deepen and Reference pages must not receive an Understand context unless explicitly listed in that route.

The shared navigation cue does not impose a universal lesson template. Overview, concept lesson, bridge, guided build, deep dive, practice and reference pages retain their appropriate editorial structures. The component should be placed near the page opening, remain compact, localize its labels, and preserve keyboard and screen-reader semantics.

## Output contract

The function returns a mapping:

- key: published page ID, including its language prefix;
- value: ordered list of explicit memberships;
- each membership contains the stage ID, localized stage title, and role (`core` or `optional`).
- each membership also carries its position, taken from the same registry: the number of stages, and for a `core` membership the page's rank among that stage's core pages and their count. An `optional` membership has no rank and shows no position text: its stage number is already in the stage cue. For core pages, position is rendered as a short text inside the existing context cue («Étape 4 sur 8 · page 2 sur 4»); it is part of the pedagogical context, not a second navigation element, and it makes no claim about reading time or effort.

The list order follows the stage order in `data/guided-route.yml`. The role is preserved per membership, not collapsed into a page-level boolean.

## Invariants

1. Every page listed in a stage's `pages` is emitted as `core` for that stage.
2. Every page listed in `optional_pages` is emitted as `optional` for that stage.
3. A page may have zero memberships (it is absent from the mapping), one membership, or multiple memberships.
4. Memberships are never inferred from `suggested_route`, `hierarchy`, sidebar nesting, concept relations, or Build milestones.
5. A page may have different roles in different stages; do not deduplicate across stages.
6. Localization comes from the already-resolved stage title for the requested language.
7. The function does not choose a primary stage or infer the reader's entry context.

## Regression coverage

The bilingual tests exercise:

- `generation`: core in both `orientation` and `prediction`;
- `transformer-architectures`: optional in `orientation`;
- `attention-score-scaling`: optional in `computation` (mathematical deep dive, not a core prerequisite);
- `embedding-space`: core in `representations`;
- `evaluation-experimentale` / `experimental-evaluation`: included because the canonical route explicitly lists it in `learning-evaluation`;
- `build-path`: absent from the Understand route;
- a synthetic unassigned page: absent from the mapping.

## Rendering prototype

The same branch now includes a renderer, `render_guided_page_context_markdown()`, and stable anchors on each generated route stage (`#guided-stage-<stage-id>`). The renderer has two distinct presentations:

- one membership: an ordered breadcrumb-like context with the current page marked by `aria-current=page`; optional membership receives an explicit optional-resource label;
- multiple memberships: a separate section listing every stage and its distinct objective. It is deliberately not marked up as a breadcrumb because there is no unique parent context.

Stage anchors are added to the generated bilingual route fragments, and responsive styles are defined for the two context presentations.

The renderer is covered by tests for a single optional membership, multiple core memberships, stable anchors, and an absent membership. A generator now emits one ignored Quarto partial per route-member page. The English and French overview and generation lessons exercise the single-membership and multi-membership paths. The embeddings and Q/K/V lessons include their generated route-context partials, exercising the `representations` and `computation` stages respectively. The optional attention-score-scaling deep dive is also listed in the computation stage and receives an explicitly optional route context. The Quarto build runs the generator before rendering; local builds must run `python site/tools/build_learning_map.py` before `quarto render site`.

The remaining work is visual and accessibility validation of the implemented presentation; preserve the semantic distinction between single and multiple memberships:

- one membership: identify the stage context and current page;
- multiple memberships: show all relevant stage contexts with their distinct purpose, or omit the breadcrumb if the presentation becomes ambiguous or noisy;
- optional membership: label it as optional, never as a prerequisite;
- no membership: do not manufacture a context.

The stage links should target stable anchors on the guided-route overview, not a guessed parent page. Build, Practice, Deepen and Reference require their own canonical route models before any analogous breadcrumb is added.

## Validation boundary

The projection, renderer, fragment writer and regression tests are integrated in `main` through PR #522. The four-page embeddings/Q/K/V integration was merged in [PR #528](https://github.com/JM-Brun/llm-lab/pull/528). Python CI and Quarto static rendering passed for the implementation and four-page integration. A dedicated current-main browser audit in [PR #531](https://github.com/JM-Brun/llm-lab/pull/531) covers the learning map and all four route-context pages in FR/EN, desktop/mobile and browser prefers-color-scheme light/dark contexts. Do not describe the learner-facing context as fully validated until the browser run, Axe report, screenshots, keyboard navigation, contrast and screen-reader review have been completed.


## Accessibility remediation

The merged [PR #531](https://github.com/JM-Brun/llm-lab/pull/531) validated the four page-context pilots and the learning map. It varied browser color-scheme preference, but the site currently ships only one light Quarto theme; no dark-theme support is claimed.

The follow-up Axe findings are tracked in [#532](https://github.com/JM-Brun/llm-lab/issues/532) and are being addressed in [PR #535](https://github.com/JM-Brun/llm-lab/pull/535). That PR adds keyboard semantics to Quarto collapsible callouts and fixes the identified navigation/Mermaid contrast issues.

## Extension boundary — pages spanning stages and transitions

The membership projection remains a direct, read-only index of `data/guided-route.yml`. It must not infer additional stages from page metadata or concepts. A multi-membership page retains all stage entries and their individual `core` / `optional` roles; there is no primary membership.

Membership and transition are separate projections:

- **Membership projection:** stage → page, already implemented. It tells where the route explicitly uses the page and is the default evidence of stage coverage.
- **Transition projection:** stage pair → page(s) + bilingual purpose, a proposed extension to the same canonical route model. It tells which conceptual connection the page explicitly teaches. A page may participate in multiple transitions, and a transition may be explained by more than one page.

Do not add a duplicate per-page `coverage` array when the existing stage membership already expresses the same fact. A separately represented cross-stage contribution is justified only when the page teaches material from a stage without being a listed route resource there. Mere mention, a suggested previous/next link, a concept relation, or a hierarchy edge is not sufficient evidence.

### Required transition semantics before implementation

A transition record must identify a stable ID, `from` and `to` stage IDs, canonical page IDs in each published language, and a concise localized purpose. Direction must be intentional; if the relationship is symmetric, encode that explicitly rather than relying on an ambiguous arrow. Transition edges are explanatory, not prerequisite edges. Validate endpoint existence, page publication/language, unique IDs, bilingual purpose, and page association. The renderer should show localized stage titles and purpose, never raw IDs or fabricated step numbers.

The two regression fixtures are `generation` (orientation + inference; early overview and later detailed inference) and `cross-entropy` (scoring core + training optional; observed-target scoring and training objective). Their distinct membership roles must survive generation unchanged. The `text-data` page is a negative boundary fixture: its mention of corpus preparation must not imply Build membership.

No YAML schema, generator, page fragment, or source page is changed by this design note. Implement the schema only after these semantics and the bilingual examples are reviewed.

## Canonical transition schema — implemented in #976

The optional top-level `transitions` collection in `data/guided-route.yml` uses this minimal record:

```yaml
transitions:
  - id: predictive-distribution-to-generation
    from: prediction
    to: inference
    direction: directed # or symmetric
    pages:
      fr: [fr/generation]
      en: [en/generation]
    purpose:
      fr: "Relier la distribution prédictive à la sélection puis à la boucle autorégressive."
      en: "Connect the predictive distribution to selection and the autoregressive loop."
```

- `id` is a stable, unique kebab-case identifier.
- `from` and `to` are distinct existing stage IDs.
- `direction` is mandatory: `directed` or `symmetric`; neither value means prerequisite.
- `pages.fr` and `pages.en` are non-empty, unique lists of published canonical page IDs in the matching language.
- A listed page must be an explicit member (core or optional) of at least one endpoint stage. It need not be a member of both: a bridge page can explain a relation from its own stage to another.
- `purpose.fr` and `purpose.en` are both required and non-blank.
- Unknown fields are rejected, so prerequisite or coverage semantics cannot silently enter this model.

The validator runs as part of the existing guided-route generation. It checks stage identity and endpoints, page publication/language, endpoint association, stable ID uniqueness, explicit direction and localized purpose. It does not modify the membership projection. The reference set is deliberately limited to the evidenced `prediction → inference` connection explained by `generation`, and the symmetric `scoring ↔ training` connection explained by `cross-entropy`. No edge is inferred for `text-data` or for mere mentions of corpus preparation.
