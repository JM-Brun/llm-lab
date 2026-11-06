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

## Implemented minimal contract

The follow-up implementation adds one required controlled field to each concept in `data/concepts.yml` (registry schema version 2), not to page metadata:

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

The existing renderer exposes the localized human-readable importance label only as a restrained secondary cue on concept cards and in concept details. The learning-map projection carries the enum unchanged, and the JSON-LD export exposes it as `llmlab:importance`. It must not sort concepts into a false prerequisite sequence, change graph topology, or infer learning order. Domain grouping and relation direction remain authoritative.

## Implementation status

- [x] Classify all 41 concepts against the guided route and computational branches; record the rationale below.
- [x] Upgrade the concept registry to schema version 2 and require the controlled enum in the existing validator; cover missing, unknown, and malformed values in tests.
- [x] Pass importance through the existing learning-map JSON projection.
- [x] Render the localized secondary cue in the existing card and detail components; no parallel card system or registry was introduced.
- [x] Export the value as `llmlab:importance` in the existing JSON-LD concept node and document its semantics.
- [ ] Complete rendered FR/EN browser review, including responsive behavior, keyboard and screen-reader behavior, and search/filter compatibility.

The structural tests cover the projection and generated script. They do not substitute for the outstanding rendered and accessibility review.

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


## 4. Relationship to the other canonical metadata layers

The repository already has several distinct structures. They answer different questions and must not be collapsed into a single graph or tag vocabulary.

| Layer | Canonical source | Question answered | Must not be used as |
|---|---|---|---|
| Concept catalogue | `data/concepts.yml` | Which concepts exist, what they mean, which domains they belong to, and how they relate semantically | A page hierarchy or executable dataflow |
| Concept relations | `relations` and `relation_types` in `data/concepts.yml` | What kind of relation connects two concepts, including direction and whether it is a genuine learning dependency | An undifferentiated edge list or an automatically inferred reading order |
| Computational architecture | `data/computational-graph.yml` | Which data, operations and states participate in each computational branch | A curriculum sequence or concept-importance ranking |
| Reader-facing route | `data/guided-route.yml` | Which pages a learner is invited to visit, in what pedagogical stages, with which optional deep dives | A complete concept ontology or an execution trace |
| Page editorial metadata | Page-map comments in each Quarto page | What a page is, where it belongs editorially, and how it relates to other pages | A duplicate concept registry |

This distinction is already visible in the current route: the inference stage explicitly distinguishes prompt prefill from iterative decode, while the training stage places teacher forcing and shifted examples in a separate learning branch. That is a pedagogical organization, not a reason to make prefill and teacher forcing sequential computational steps in one path.

The concept registry also already contains the canonical IDs `prefill` and `teacher-forcing`, with a typed contrast relation. Their presence in the concept catalogue does not imply that either should become a page tag. Pages remain resources associated with concepts through the existing `resources` field.

### Page tags: do not introduce a second concept/domain vocabulary

The page metadata contract does not currently define `notion:` or `domaine:` as controlled tags. The canonical concept IDs and concept-domain memberships already live in the concept registry. Adding page tags with those names would create a second, potentially divergent representation and would be especially misleading where one page discusses several concepts or one concept belongs to several domains.

If page-level discoverability later proves insufficient, first assess whether the existing learning-map projection can expose the canonical concept-resource associations. Do not solve that by copying concept IDs or domain memberships into every page.

### Importance classification is a display annotation, not a relation

`importance` is an intrinsic annotation on each concept record, with a controlled vocabulary and explicit project-relative definitions. It must not become a relation type, a domain, or an implicit edge weight. In particular:

- it must not change the direction or meaning of existing relations;
- it must not create prerequisite edges;
- it must not reorder the guided route or computational branches;
- it must not be inferred from how many pages mention a concept, its domain count, or its position in the current graph.

The implementation is deliberately small: one required enum, the existing validator, one JSON projection field, one JSON-LD property, and one localized secondary cue in the existing card/detail UI. Importance does not change route ordering, graph topology, domain grouping, or relation semantics.


## Reviewed classification for the 41 current concepts

The assignment uses the canonical guided route and computational branches as evidence. It is a curriculum annotation, not a claim about the intrinsic importance of a scientific topic.

| Importance | Concepts | Classification rationale |
|---|---|---|
| `core` | `token`, `token-embedding`, `contextualized-representation`, `self-attention`, `scaled-dot-product-attention`, `causal-mask`, `positional-encoding`, `output-projection`, `logits`, `softmax`, `conditional-distribution`, `next-token-prediction` | Required to follow the shared input → representation → Transformer → logits → conditional-distribution computation. |
| `core` | `autoregressive-generation`, `prefill`, `decode-step` | Required to explain the principal inference execution path and distinguish initial prompt processing from incremental generation. |
| `core` | `observed-target`, `sequence-likelihood`, `negative-log-likelihood`, `cross-entropy` | Required to explain observed-target scoring and the probabilistic quantity used as a training objective component. |
| `core` | `training-objective`, `training-example`, `teacher-forcing`, `gradient`, `optimizer`, `parameter-update` | Required to explain training from observed examples through differentiation and parameter updates. |
| `core` | `held-out-evaluation` | Required to distinguish evaluation on held-out data from training and parameter updates. |
| `supporting` | `query`, `key`, `value`, `attention-score`, `attention-weight`, `multi-head-attention` | Important internal components and intermediate quantities that unpack attention, but are not separate top-level stages of the shared computational spine. |
| `supporting` | `log-likelihood`, `logarithm`, `negation` | Mathematical steps that explain negative log-likelihood; useful for derivation, but not independent branches. |
| `supporting` | `decoding-policy`, `generated-token-feedback` | Explain how the distribution becomes a selected token and how inference context is extended; subordinate to the autoregressive loop. |
| `supporting` | `operational-competence` | Qualifies interpretation and measurement of model capabilities; it does not participate in the forward computation. |
| `specialized` | `calibration`, `emergent-ability` | Evaluation/research topics that extend interpretation of model outputs and measured capabilities beyond the minimum route. |
| `specialized` | `kv-cache` | Inference-efficiency optimization; the autoregressive process remains conceptually valid without it. |

The classification treats the three operational branches as core even though they are not one linear execution loop. It also treats `training-objective` as core because the learning branch needs an explicit objective, while keeping narrower mathematical derivation steps supporting.

The renderer exposes the localized label as secondary text only. Domain grouping, concept relations, search, and route ordering remain unchanged.
