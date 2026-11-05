# Guided-route page membership projection

**Status:** implemented as a tested data projection; not yet rendered as page navigation.  
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

The renderer is covered by tests for a single optional membership, multiple core memberships, stable anchors, and an absent membership. The current prototype is not yet inserted into lesson pages; Quarto include-path and rendered-output validation are still required before rollout.

The next design/implementation step must choose an accessible presentation that does not misrepresent multi-membership:

- one membership: identify the stage context and current page;
- multiple memberships: show all relevant stage contexts with their distinct purpose, or omit the breadcrumb if the presentation becomes ambiguous or noisy;
- optional membership: label it as optional, never as a prerequisite;
- no membership: do not manufacture a context.

The stage links should target stable anchors on the guided-route overview, not a guessed parent page. Build, Practice, Deepen and Reference require their own canonical route models before any analogous breadcrumb is added.

## Validation boundary

The projection, renderer and regression tests are committed in the implementation PR. CI is being rerun after a formatting-only correction. Quarto rendering, visual review, keyboard navigation and screen-reader review remain pending. Do not describe this as a validated learner-facing breadcrumb until those checks have been completed.
