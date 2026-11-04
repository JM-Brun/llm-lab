# Page metadata and learning-graph contract

**Status:** initial metadata baseline for the published Quarto pages.  
**Purpose:** make page scope, editorial role, suggested reading order, conceptual hierarchy, and discovery tags explicit in source files so the site can be audited and reorganized without guessing from sidebar order.

## 1. Two complementary metadata locations

Every reader-facing `.qmd` page carries the same information in two forms:

- **Quarto `keywords`** in YAML front matter: compact, machine-readable tags for search, indexing, and future filters.
- **A hidden HTML comment** immediately after the YAML front matter: richer maintainer metadata. It is not rendered as reader-facing page content.

The comment begins with `LLM-LAB-PAGE-MAP v1`. Keep the marker stable so scripts can locate the block.

## Relationship to page templates

The `type` tag is the stable editorial classification, not a filename convention. Its default relationship to reusable page structures is documented in the [page archetype implementation map](site-page-design-system.md). Do not add a parallel `archetype` field unless a demonstrated need cannot be expressed by the existing taxonomy.

## 2. Comment schema

```yaml
id: "fr/tokenization-strategies"
scope: "Tokenisation : stratégies et conséquences"
purpose: "Explain what this page covers and why it exists in the learning path."
suggested_route:
  previous: "fr/unicode-text"
  next: "fr/embedding-space"
hierarchy:
  parents: ["fr/text-data"]
  children: ["fr/training-examples"]
related: ["fr/build-path"]
tags:
  - "type:concept-lesson"
  - "destination:understand"
  - "topic:tokenization"
  - "level:core"
  - "language:fr"
  - "status:published"
```

The source comment is YAML-like documentation, not a second Quarto front matter block. Keep it simple and avoid relying on it as executable YAML unless a validator explicitly parses it.

## 3. Relation semantics

These fields must not be conflated:

| Field | Meaning | Constraint |
|---|---|---|
| `scope` | The boundary of the page: what it covers and what it does not own | One concise statement; avoid generic descriptions |
| `purpose` | The learning job the page performs | State what the reader should understand or be able to connect |
| `suggested_route.previous` | A useful page to read immediately before this one on the suggested route | A recommendation, not a hard prerequisite |
| `suggested_route.next` | A useful next page on that route | A recommendation; branching is allowed |
| `hierarchy.parents` | Broader concepts or pages that structurally contain or motivate this topic | Not merely the previous page |
| `hierarchy.children` | More specific concepts or pages that unpack this topic | Not merely the next page |
| `related` | Useful cross-links that are neither parent nor child | Use sparingly and explain the connection in the page itself |
| `tags` | Controlled labels for page type, destination, topic, level, language, and status | Keep values stable across French and English counterparts |

A page can have several parents or children. The learning path is a **graph with suggested routes**, not a mandatory linear sequence. Optional deep dives must not become hidden prerequisites for the core conceptual course.

### 3.1.1 Do not encode a processing sequence as conceptual containment

A parent/child edge is stronger than “comes before”, “is used by”, or “is mathematically related to”. Use `suggested_route` for a recommended reading transition and `related` for an important connection that is not genuine conceptual containment or decomposition. For example:

- Text preprocessing and tokenization feed a Transformer, but are not thereby sub-concepts of the Transformer architecture.
- Training examples provide observations on which likelihood is evaluated; they do not conceptually contain likelihood.
- Likelihood, predictive entropy, and cross-entropy are distinct mathematical quantities. Their relationships belong in `related` unless a page genuinely generalizes or decomposes another concept.
- A causal mask constrains attention; it does not contain or decompose the output logits.
- Cross-entropy can reasonably be modelled as an extension of entropy, while batch loss is an aggregation built from per-target cross-entropy.

When an edge is removed from `hierarchy`, preserve discoverability with a reciprocal `related` link where the connection remains pedagogically useful. This keeps the hierarchy a map of conceptual ownership rather than a diagram of every dependency in the computation pipeline.

## 3.1 Specificity: scope versus learning purpose

The two fields answer different editorial questions and should not paraphrase one another:

- **Scope:** what this page owns, including the boundary with adjacent pages. Name the object, process, or level of abstraction covered; state important exclusions when a neighbouring page could plausibly claim the same material.
- **Purpose:** what the learner should be able to explain, distinguish, trace, calculate, or decide after reading. Prefer observable intellectual outcomes over a description of what the page contains.

| Field | Insufficient | Specific and useful |
|---|---|---|
| `scope` | `"What is a Transformer?"` | `"Traces an autoregressive GPT computation through its network to the logits; excludes the black-box decoding loop and parameter training."` |
| `purpose` | `"Explain the Transformer and its role in an LLM."` | `"Readers should be able to trace a token context to the logits and distinguish initial embeddings from contextualized representations."` |
| `scope` | `"Text and tokens."` | `"Covers text as model input, Unicode representation, and tokenization as distinct preprocessing stages; excludes vector representations produced after tokenization."` |
| `purpose` | `"Introduce text data."` | `"Readers should be able to explain why visible characters, Unicode code points, token IDs, and embedding vectors are different representations."` |

A useful scope can mention an adjacent topic, but only to establish a boundary. A useful purpose is learner-centred and testable by asking the learner to perform the stated action. Do not turn every purpose into a long list: one or two tightly related outcomes are usually enough.

## 4. Tag vocabulary

Use these dimensions consistently:

- **`type`**: `entry-point`, `system-overview`, `concept-lesson`, `concept-bridge`, `guided-build`, `deep-dive`, `exercise-hub`, `experiment-guide`, `glossary`, `historical-reference`, `bibliography`.
- **`destination`**: `orient`, `understand`, `build`, `deepen`, `practice`, `reference`.
- **`topic`**: a stable kebab-case concept identifier; use the same identifier for French and English counterparts even when their filenames differ.
- **`level`**: `overview`, `core`, `applied`, `advanced`, `reference`.
- **`language`**: `fr`, `en`, or `shared` for language-neutral resources.
- **`status`**: `published`, `planned`, or `retired`. Do not label a planned page as published.

## 5. Stable identifiers and bilingual parity

- Use `fr/<source-slug>` and `en/<source-slug>` as page IDs. The two IDs may have different slugs, but their `topic` tag and editorial role should match.
- Use repository-relative IDs in relations, not rendered HTML URLs. This keeps the graph stable if output paths or navigation labels change.
- Only reference pages that exist in the current source tree. If a destination is planned but not yet published, record it as planned work in the curriculum/backlog rather than as a live relation.
- Keep French and English metadata semantically equivalent. Wording can differ, but scope, purpose, relation structure, and tag dimensions should remain aligned.

## 6. Maintenance rules

1. When adding or renaming a page, update its YAML keywords and comment block in the same change.
2. Keep hierarchy reciprocal: if page A lists page B as a child, page B must list A as a parent, and vice versa. Update incoming and outgoing relations when a page is renamed, split, merged, or moved to another destination.
3. Do not infer hierarchy from sidebar indentation alone. Check the curriculum map and the page's actual learning objective.
4. Do not force a single `previous/next` route where the subject has genuinely different entry points. Use `null` and meaningful parent/child or related links instead.
5. Keep metadata concise; the page body remains the source of truth for the full explanation.
6. Before merging a navigation or curriculum change, review both the rendered navigation and this source-level graph.

## 7. Automated validation

Run the validator locally from the repository root:

```bash
uv run --with-requirements docs/requirements-history-validation.txt python scripts/check_page_metadata.py
```

The validator reads the actual `project.render` list from `site/_quarto.yml`; it does not infer coverage from sidebar indentation. It checks:

- exactly one correctly placed page-map comment and valid YAML front matter per rendered page;
- required fields, stable IDs derived from source paths, unique IDs, and matching Quarto `keywords` / comment tags;
- one value for each controlled tag dimension and valid vocabulary values;
- resolvable relations, reciprocal parent/child and suggested-route edges, and an acyclic conceptual hierarchy;
- French/English counterpart coverage, matching editorial dimensions, and equivalent relations after mapping translated IDs to canonical topic tags;
- published status for every page in the render list.

The validator runs in both the Python quality workflow and the Quarto workflow, before site rendering. It reports the source page and offending field or target. It deliberately does not generate navigation or treat a suggested reading route as a prerequisite graph.

## 8. Coverage boundary

The baseline covers every page in the current `site/_quarto.yml` render list, including the French root landing page, the bilingual inference/generation lesson, and the shared references page. The inference lesson is now published and must carry `status:published`. New pages must receive complete metadata in the same change that adds them to the render list.


## 9. Advanced knowledge domains

Pages with `destination:deepen` and a content-page type (not an entry point) must declare one top-level `domain` in the page-map comment. This field assigns the page to exactly one primary discovery domain; it is not a prerequisite, a graph edge, or a claim that the page has no cross-domain relevance.

Controlled values:

| Identifier | Primary learning question |
|---|---|
| `architectures-mechanisms` | How do specialized mechanisms and architectures change information flow or computation? |
| `text-tokenization` | How do text representation and tokenizer design affect model inputs? |
| `mathematical-tools-geometry` | Which mathematical tools help analyze tensors and representation spaces? |
| `probabilistic-foundations-training` | How do probabilistic quantities, objectives, and optimization connect? |
| `inference-efficiency` | How does a model use context, select outputs, and consume compute or memory? |
| `scale-research` | What empirical regularities and capability claims are supported by evidence? |

The domain is exported into the generated learning-map JSON and can be used as a discovery filter. French and English counterparts must use the same identifier. Pages outside Deepen must not declare this field. Use `related` for cross-domain connections instead of assigning multiple primary domains.


## 10. Language-independent concept registry

The page graph and the concept graph answer different questions:

- A **page** is a maintained learning resource with a scope, audience, language, and pedagogical role.
- A **concept** is a language-independent knowledge entity that may be explained by several pages and recur across the curriculum.
- A **resource link** connects a concept to a page; it does not assert that the page is the concept's only owner.
- A **concept relation** connects two concepts with an explicitly typed semantic relation. It is not a reading-order edge.

The initial registry lives in `data/concepts.yml`. Each concept has a stable kebab-case `id`, French and English labels and definitions, and zero or more page IDs in `resources`. Translations share one concept ID; do not create separate French and English concept nodes.

### Relation vocabulary

Relations are directed from `from` to `to`; their direction is part of their definition.

| Type | Meaning |
|---|---|
| `prerequisite` | Understanding the source is needed to understand the target. Use sparingly; this is a conceptual dependency, not a suggested reading order. |
| `part-of` | The source is a constituent or structural component of the target. |
| `generalizes` | The source is a more general concept that subsumes the target. |
| `contrasts-with` | The source is meaningfully distinguished from the target; do not infer opposition from mere difference. |
| `analogy` | The source is used as an analogy for the target, not as a mathematical equivalence. |
| `implemented-by` | The source is realized or operationalized by the target in the stated context. |
| `applies-to` | The source mechanism or method is applied to the target object/process. |
| `constrains` | The source imposes a constraint on the target. |
| `produces` | The source operation or process produces the target quantity/state. |
| `normalized-by` | The source quantity is transformed/normalized by the target operation. |
| `evaluated-by` | The source prediction/distribution is evaluated using the target criterion. |

Do not use a generic `related-to` relation as a substitute for deciding what the connection means. Add a relation type only when multiple real examples justify it and its direction can be stated unambiguously.

### Validation and scope

Run `python scripts/check_concept_registry.py` to check stable IDs, bilingual labels/definitions, resource-ID syntax, relation vocabulary, endpoint existence, self-links, and duplicate edges. The same check runs in CI. This first registry is intentionally a seed, not a complete ontology: it covers a small set of central concepts and should grow only alongside reviewed page content.

The concept registry is not yet rendered as a second interactive graph. The existing learning map remains a page graph; a later integration should expose concept-to-page links and concept relations without conflating them with page navigation or the Understand/Build/Deepen destinations.
