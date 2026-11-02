# Page metadata and learning-graph contract

**Status:** initial metadata baseline for the published Quarto pages.  
**Purpose:** make page scope, editorial role, suggested reading order, conceptual hierarchy, and discovery tags explicit in source files so the site can be audited and reorganized without guessing from sidebar order.

## 1. Two complementary metadata locations

Every reader-facing `.qmd` page carries the same information in two forms:

- **Quarto `keywords`** in YAML front matter: compact, machine-readable tags for search, indexing, and future filters.
- **A hidden HTML comment** immediately after the YAML front matter: richer maintainer metadata. It is not rendered as reader-facing page content.

The comment begins with `LLM-LAB-PAGE-MAP v1`. Keep the marker stable so scripts can locate the block.

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

## 7. Coverage boundary

This baseline covers the pages currently listed for rendering in `site/_quarto.yml` plus the French root landing page. The bilingual inference/generation lesson in PR #229 already carries the same metadata block on its feature branch with `status:planned`; change that tag to `status:published` when it is integrated. New pages added on separate branches must receive the same metadata before or immediately after they enter the published render list.
