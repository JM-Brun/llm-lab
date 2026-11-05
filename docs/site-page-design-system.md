# Page archetype implementation map

**Purpose:** map the repository's stable page metadata to common reader-facing roles and identify the source of truth for each design concern. This is an index, not a second template or visual system.

## Sources of truth

| Concern | Canonical document |
|---|---|
| Reader experience, progressive disclosure, editorial method | [Reader-experience and editorial method](reader-experience-and-editorial-method.md) |
| Pedagogical breadcrumb and route-context projection | [Pedagogical breadcrumb and page-navigation contract](pedagogical-breadcrumb-and-page-navigation-contract.md) and [pilot audit](pedagogical-breadcrumb-pilot-audit.md) |
| Shared composition model and soft page templates | [Flexible page-template system](page-template-system.md) |
| Scientific explanatory patterns | [Page patterns](page-patterns.md) |
| Code-facing walkthroughs, verification, experiments, and performance | [Implementation-page patterns](implementation-page-patterns.md) |
| Visual identity, typography, spacing, responsive behavior, accessibility | [Visual design system](design-system.md) |
| Stable page metadata, controlled tags, and learning graph | [Page metadata contract](page-metadata-schema.md) |
| Page inventory, ownership boundaries, and content placement | [Content-section mapping](content-section-mapping.md) |
| Contributor rules and scientific/engineering expectations | [Contributor guiding principles](contributor-guiding-principles.md) |

If guidance conflicts, preserve the responsibility of the canonical source above and update the relevant guide. Do not create a parallel rule to work around a conflict.

## Existing metadata types and their usual roles

The LLM-LAB-PAGE-MAP v1 metadata and controlled type tags remain the repository's stable editorial classification. The table below is a **default mapping**, not a constraint on page composition:

| Existing type | Usual reader-facing role | Existing quick start |
|---|---|---|
| entry-point | Route selection and orientation | [Overview](overview-page-template.md), adapted to help choose a path |
| system-overview | System-level explanation | [Overview](overview-page-template.md) |
| concept-lesson | Explanation of one concept or mechanism | [Concept](concept-page-template.md) |
| concept-bridge | Connect a concept to prerequisites or applications | [Concept](concept-page-template.md), with emphasis on the relevant relationship |
| deep-dive | Focused technical explanation | [Concept](concept-page-template.md), with the required formal or technical depth |
| guided-build | Procedural construction and verification | [Guided build](guided-build-page-template.md) |
| exercise-hub | Sustained practice | [Practice and experiment](practice-page-template.md), exercise-collection prompts |
| experiment-guide | Reproducible investigation | [Practice and experiment](practice-page-template.md), experiment prompts |
| glossary | Concise lookup | [Reference](reference-page-template.md) |
| historical-reference | Chronology and historical context | [Reference](reference-page-template.md) |
| bibliography | Source discovery and provenance | [Reference](reference-page-template.md) |

A page may use a different quick start when its actual reader task calls for it. The type tag does not dictate headings, section count, or scientific pattern.

## Keep the classification layers separate

These terms answer different questions and must not become competing labels:

- **Documentation job:** tutorial, how-to, reference, or explanation describes the reader's need. It is a useful design lens, not a new metadata field.
- **Metadata type:** the existing controlled type identifies the page's stable editorial role in this repository.
- **Scientific pattern:** concept, algorithm, mathematical object, physical law, architecture, technology, method, or overview describes the subject's explanatory structure.
- **Composition modules:** intuition, definition, derivation, example, comparison, limitation, implementation, or self-check are optional ingredients selected for the page's purpose.
- **Visual treatment:** Quarto components and SCSS belong to the shared [design system](design-system.md), not to individual template files.

Do not add archetype, diataxis, or another metadata dimension to encode the scientific pattern. If a real future query cannot be answered with the existing type and learning-graph metadata, document that use case before proposing a schema change.

## Practical use

1. Read the page's current scope, purpose, type, and learning-graph relations.
2. Identify the dominant reader question; do not infer it from the filename.
3. Choose a scientific or implementation pattern only as a source of relevant prompts.
4. Keep the modules that materially improve explanation, retrieval, execution, or verification.
5. Reuse existing visual treatments and preserve French/English semantic parity.
6. Validate the rendered page; source inspection and a green build are not substitutes for checking the actual reader experience.

The objective is gradual convergence in clarity, navigation, and visual language—not a mass rewrite or identical page outlines.
