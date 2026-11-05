# Nested breadcrumb navigation contract

**Status:** design contract for implementation — 2026-11-05.

## Decision

Where both contexts are meaningful, LLM Lab should render two distinct navigation trails:

1. **Global breadcrumb** — derived from the Quarto sidebar ancestry. It answers: “Where am I in the overall site and curriculum?” It describes site organization, not a mandatory learning sequence.
2. **Local topic breadcrumb** — derived only from the page-map `hierarchy.parents/children` relations. It answers: “Where does this page sit in a genuine conceptual hierarchy?” Render it only when a single unambiguous parent chain exists.

These are two projections of existing sources, not two new sources of truth. Do not duplicate the sidebar tree in page metadata or add a parallel breadcrumb hierarchy.

## Keep navigation semantics separate

| Source | Meaning | Reader-facing role |
|---|---|---|
| Quarto sidebar ancestry | Global site organization | Global breadcrumb |
| `hierarchy.parents/children` | Conceptual containment/decomposition | Local breadcrumb, only when unambiguous |
| `suggested_route.previous/next` | Recommended reading transition | Previous/next lesson controls |
| `docs/learning-path.md` | Curriculum dependencies and prerequisites | Explicit prerequisite guidance |
| `related` / typed concept relations | Non-hierarchical association | Contextual links or knowledge exploration |

A suggested previous page is not automatically a parent. A parent is not automatically a prerequisite. Do not infer either relation from sidebar order, data-processing order, lexical similarity or concept association.

## Pilot pages: current source metadata

- `fr/text-data` and `en/text-data`: hierarchy parent is the generation page; suggested previous is generation and suggested next is tokenization strategies.
- `fr/queries-keys-values` and `en/queries-keys-values`: hierarchy parent and suggested previous are Transformer; suggested next is scaled dot-product attention.
- Their global sidebar contexts differ: text/representations versus attention.

This demonstrates that the global and local paths need not be identical. It does not establish which component currently emits the deployed breadcrumb. The reported click behavior must first be reproduced and traced in the browser.

## Rendering contract

- Use two separate navigation landmarks with localized accessible names, e.g. “Parcours global” and “Dans ce thème”.
- Use ordered lists, real links and `aria-current="page"` for the current page.
- Make the global trail visually primary and the local trail secondary; do not render two identical rows.
- Allow wrapping on mobile; no horizontal overflow.
- Preserve keyboard focus, contrast, logical tab order and touch usability.
- Omit the local trail when there is no single defensible parent chain. For multiple parents, do not select one arbitrarily; use a separately labelled contextual-links list if useful.
- Avoid repeating the same clickable ancestor in both trails without adding distinct context.
- Keep FR/EN labels and destinations aligned by the existing `topic` metadata.

## Implementation constraints

1. Keep page-map metadata as the source for local hierarchy and suggested route.
2. Keep the Quarto sidebar as the source for global ancestry.
3. Do not alter the meaning of `hierarchy` to match the sidebar.
4. Do not derive breadcrumbs from the concept graph, learning-map BFS rank or generated display order.
5. Trace the actual HTML/component/filter that emits the current breadcrumb before changing styles or adding a renderer.
6. The existing `.llm-breadcrumb` CSS rules in `site/styles.scss` do not prove that a renderer is active; confirm where the class is emitted.
7. Reuse the existing metadata parser and validator. Any future schema change requires migration, tests and FR/EN parity checks; this two-level policy does not itself require a new metadata field.

## Work sequence

1. Reproduce the reported behavior on deployed FR and EN pages. Record browser, viewport, visible breadcrumb labels, each href and the destination after clicking.
2. Trace the emitting component/filter/template and compare it with sidebar ancestry, local parent chains and suggested-route links.
3. Implement one shared renderer with separate global and local inputs; no page-specific hard-coded markup.
4. Pilot on text-data and Q/K/V in both languages, including immediate parent pages needed to test continuity.
5. Add focused tests for link resolution, current-page semantics, localization and duplicate adjacent items.
6. Inspect desktop/mobile, keyboard, touch and accessible landmark names. Keep browser evidence distinct from CI and Quarto results.
7. Expand only to pages with a genuine local parent chain.

## Acceptance

- Readers can distinguish global curriculum location from local conceptual context.
- Global ancestor links follow the site hierarchy; local ancestor links follow only conceptual containment.
- Previous/next navigation remains independent.
- Ambiguous and multi-parent pages do not receive fabricated breadcrumbs.
- No parallel manually maintained navigation taxonomy is introduced.
- Metadata validation, bilingual render and local-link checks pass; browser/accessibility evidence is recorded separately.

## Ownership

- `docs/page-metadata-schema.md`: page-relation semantics.
- `docs/information-architecture.md`: canonical sources and projections.
- `docs/learning-path.md` and `data/guided-route.yml`: curriculum sequence and prerequisites.
- [#337](https://github.com/JM-Brun/llm-lab/issues/337): global rendered navigation.
- [#415](https://github.com/JM-Brun/llm-lab/issues/415): guided route and resource graph.
- [#483](https://github.com/JM-Brun/llm-lab/issues/483): Q/K/V rendered evidence and reported behavior.

This is a rendering policy over existing sources, not a new source of truth.
