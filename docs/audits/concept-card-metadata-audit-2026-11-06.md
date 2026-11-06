# Concept-card metadata audit — 2026-11-06

**Scope:** verify where canonical notion identity, domain membership, and relative importance belong before extending the concept cards.

**Inspected baseline:** `main` at `3e36b7827a34a6c901922e37df3bebd9351063f8`.

## Findings

### 1. The existing ownership boundaries are sound

| Information | Current canonical source | Meaning |
|---|---|---|
| Notion identity and bilingual definition | `data/concepts.yml` | One language-independent concept ID, with FR/EN labels and definitions |
| Knowledge-domain membership | `data/concepts.yml` + `data/domains.yml` | Many-to-many concept classification; domain vocabulary and localized descriptions are centrally controlled |
| Page editorial role and discovery tags | `LLM-LAB-PAGE-MAP v1` + Quarto `keywords` | Page type, destination, topic, depth, language and publication status |
| Page primary domain | Page-map `domain` | Exactly one primary domain for Deepen content pages only |
| Non-page implementation resources | `data/resources.yml` | Stable resource identities, implementation metadata and concept associations |

The word *notion* should not become another page tag or page-map field. The stable concept ID is already the canonical notion identity. Page-level `topic` is an editorial discovery facet, not a substitute for concept identity.

Likewise, concept domains must not be copied into page-level `domain`: the former are multi-valued memberships; the latter is a single primary classification restricted to Deepen pages. The page metadata contract explicitly prohibits adding concept-list fields merely to control visual emphasis.

### 2. The concept-card projection currently omits importance

The checked-in concept registry contains 41 concepts. Each record currently carries `id`, bilingual `labels`, bilingual `definitions`, `domains`, and `resources`; no `importance` field is defined.

The learning-map builder projects each concept to `id`, localized `label`, localized `definition`, `domains`, and resolved page `resources`. The interactive concept card renders the label and definition. Domain memberships are used to group cards under localized domain headings. There is no importance value in the projection, card, or concept-detail panel.

Therefore, the statement that concept cards already expose importance metadata is not supported by the current `main` implementation. This is a concrete metadata/UI gap, not a reason to duplicate the concept registry.

### 3. Importance must not duplicate page depth

The existing page `level` classifies a resource's editorial depth (for example, overview/core/applied/advanced/reference). It cannot express whether the underlying concept is central to the LLM Lab conceptual model.

A concept may be central while being treated in an advanced page, and a core page may introduce supporting concepts. Reusing page `level` for concept importance would therefore conflate two independent dimensions.

## Recommended minimal contract

If concept-card prioritization is retained as a requirement, add one controlled field to each concept in `data/concepts.yml`, not to page metadata:

```yaml
importance: core | supporting | specialized
```

Interpretation must be relative to the project's conceptual learning objective, not as a universal measure of scientific importance:

- `core`: required to explain or follow a principal part of the shared model or one of its operational branches;
- `supporting`: materially clarifies, qualifies, or helps apply a core concept, but is not itself a central step;
- `specialized`: a narrower mechanism, optimization, or research concept that is useful for depth but not needed for the core conceptual route.

This field must remain independent of:
- `domains`: subject-matter classification;
- page `level`: resource depth;
- `destination`: where the page sits in the site;
- concept relations: semantic connections and genuine pedagogical prerequisites.

The renderer should expose the localized human-readable importance label only as a restrained secondary cue on concept cards and in concept details. It must not sort concepts into a false prerequisite sequence, change graph topology, or infer learning order. Domain grouping and relation direction remain authoritative.

## Implementation gates

1. Review and assign importance to all existing 41 concepts against the canonical curriculum and computational branches. Do not infer values from page level or domain.
2. Add the controlled value to the concept-registry validator and its fixture/tests; reject missing or unknown values once the field becomes required.
3. Pass the value through the existing learning-map JSON projection.
4. Render the localized cue in the existing concept-card component; do not create another card system or another metadata registry.
5. Test bilingual labels, filter/search compatibility, accessibility, and preservation of existing domain grouping and typed relations.
6. Update the page-metadata and knowledge-graph documentation to make the ownership boundary explicit.

## Explicit non-goals

- No `notion:` page tag or per-page concept list.
- No copying concept domains into page-level `domain`.
- No new domain taxonomy, graph, registry, or generic metadata framework.
- No importance-based route reordering or automatic prerequisite generation.
- No visual prominence that overwhelms the concept name or definition.

## Evidence and limitations

Inspected:
- `data/concepts.yml` and `data/domains.yml`;
- `docs/page-metadata-schema.md`;
- `site/tools/check_concept_registry.py`;
- `site/tools/build_learning_map.py`;
- `site/tools/learning_map_renderers.py`;
- `site/includes/learning-map.html`;
- `site/styles.scss`.

This is a source-level audit. It does not claim rendered desktop/mobile, keyboard, screen-reader, or learner-comprehension validation.
