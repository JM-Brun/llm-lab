# Guided-route page membership projection

**Status:** implemented, rendered as a bilingual pilot on overview and generation pages; browser/accessibility and learner validation remain open.  
**Source of truth:** `data/guided-route.yml`.  
**Implementation:** `build_guided_route_memberships()` in `site/tools/build_learning_map.py`.  
**Tests:** `tests/site/test_guided_route_memberships.py`.  
**Coordination:** [#368](https://github.com/JM-Brun/llm-lab/issues/368), [breadcrumb contract PR #516](https://github.com/JM-Brun/llm-lab/pull/516), [stepper cleanup PR #519](https://github.com/JM-Brun/llm-lab/pull/519).

## Purpose

Provide a deterministic page-to-stage index for the Understand curriculum without treating a curriculum stage as a unique conceptual parent. The projection is a read-only view of the existing, validated route model. It does not create a second registry or change page metadata.

## Output contract

The function returns a mapping:

- key: published page ID, including its language prefix;
- value: ordered list of explicit memberships;
- each membership contains the stage ID, localized stage title, and role (`core` or `optional`).

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
- `embedding-space`: core in `representations`;
- `evaluation-experimentale` / `experimental-evaluation`: included because the canonical route explicitly lists it in `learning-evaluation`;
- `build-path`: absent from the Understand route;
- a synthetic unassigned page: absent from the mapping.

## Rendering prototype

The same branch now includes a renderer, `render_guided_page_context_markdown()`, and stable anchors on each generated route stage (`#guided-stage-<stage-id>`). The renderer has two distinct presentations:

- one membership: an ordered breadcrumb-like context with the current page marked by `aria-current=page`; optional membership receives an explicit optional-resource label;
- multiple memberships: a separate section listing every stage and its distinct objective. It is deliberately not marked up as a breadcrumb because there is no unique parent context.

Stage anchors are added to the generated bilingual route fragments, and responsive styles are defined for the two context presentations.

The renderer is covered by tests for a single optional membership, multiple core memberships, stable anchors, and an absent membership. A generator now emits one ignored Quarto partial per route-member page. The English and French overview and generation lessons include these partials as a first page-level pilot: the overview exercises the single-membership path, while generation exercises the multi-membership path. The Quarto build runs the generator before rendering; local builds must run `python site/tools/build_learning_map.py` before `quarto render site`.

The current pilot has selected and implemented a semantic distinction (one membership as a labelled navigation breadcrumb; multiple memberships as a labelled section with all contexts). The rendered presentation still requires browser and assistive-technology review:

- one membership: identify the stage context and current page;
- multiple memberships: show all relevant stage contexts with their distinct purpose, or omit the breadcrumb if the presentation becomes ambiguous or noisy;
- optional membership: label it as optional, never as a prerequisite;
- no membership: do not manufacture a context.

The stage links should target stable anchors on the guided-route overview, not a guessed parent page. Build, Practice, Deepen and Reference require their own canonical route models before any analogous breadcrumb is added.

## Validation boundary

The projection, renderer, fragment writer, page-level includes and regression tests are merged through [PR #522](https://github.com/JM-Brun/llm-lab/pull/522). The pilot is present on the English and French overview pages (single membership) and generation pages (multiple memberships). Python CI and Quarto static rendering passed on the merged PR. A dedicated browser audit is being extended in [PR #524](https://github.com/JM-Brun/llm-lab/pull/526); visual, keyboard, contrast, screen-reader and learner validation remain pending. Do not describe the pilot as fully validated until those checks have been completed.
