---
name: knowledge-architecture-audit
description: Audit and evolve LLM Lab's canonical knowledge, computational, curriculum, source and page-navigation models, their projections and machine-checkable invariants without creating competing structures.
---

# LLM Lab knowledge-architecture audit

## Purpose and ownership

Use this skill whenever a change audits, reorganizes, extends or validates the formal information architecture. Preserve the existing canonical owners. Do not create a replacement taxonomy, graph, registry, route or metadata model.

This skill owns **structural architecture and machine-checkable invariants**. It does not certify scientific truth, editorial quality, asset rights, rendered behavior or learner effectiveness; delegate those distinct questions to the specialist skills below.

## Non-interchangeable models

Treat these as separate models with explicit links, not one universal graph:

| Model | Question answered | Canonical owner | Main contract / validation |
|---|---|---|---|
| Knowledge domain and concept graph | Which stable concepts exist, how are they classified, and what typed semantic relations connect them? | `data/domains.yml`, `data/concepts.yml` | `docs/information-architecture.md`, `site/tools/check_concept_registry.py`, concept tests |
| Non-page learning resources | Which reusable implementation artifacts have stable identities and how do concepts/pages reference them? | `data/resources.yml`; page associations also remain in `concepts[].resources` | Resource contract in information architecture; `site/tools/check_resource_registry.py`, resource tests |
| Computational graph | What is computed, which data is consumed/produced, and how do inference, scoring, evaluation and training branches relate? | `data/computational-graph.yml` | `docs/computational-graph-schema.md`, `docs/canonical-computational-spine.md`, `site/tools/check_computational_graph.py`, `tests/site/test_computational_graph.py` |
| Theory / Understand guided route | In what reader-facing conceptual progression are the core Understand stages presented? | `data/guided-route.yml` (nine stages) | `docs/learning-path.md`, `site/tools/build_learning_map.py` and route tests |
| Overall curriculum and Build path | What modules, prerequisites, evidence and implementation milestones define the learning/build programme? | `docs/learning-path.md`, `docs/full-curriculum-plan.md` and existing Build lesson/code evidence | Relevant curriculum and Build audits; do not infer from sidebar order |
| Page-navigation graph | Which pages are recommended before/after, structurally contain one another, or are usefully related? | `LLM-LAB-PAGE-MAP v1` blocks in `site/**/*.qmd` | `docs/page-metadata-schema.md`, `site/tools/check_page_metadata.py`, learning-map generator/tests |
| External-source and extraction model | Which external source/version was inspected, what evidence/items were extracted, and what is their provenance and disposition? | Current source catalogue: `data/sources.yml`; extractions: `data/extractions/<source-id>.yml`; staged target split is defined in source-lineage architecture | `docs/source-catalogue-schema.md`, `docs/source-lineage-architecture.md`, source validators/tests |
| Source-local pedagogical/computational models | What model or teaching route does one external source itself present? | `pedagogical_model` and source-local structures in extraction records | Source-to-learning workflow and validation protocol; never treat as canonical LLM Lab models |

The computational graph is not the knowledge graph, the Understand route, the Build path or page navigation. Its edges describe computational dataflow/operation semantics. Do not convert them automatically into concept relations or pedagogical prerequisites.

The knowledge model has three dimensions—domains, concepts and resources—and complementary projections. The page graph is a separate navigation model. The computational graph is another independent model with its own registry and generated views. The source lineage graph records provenance, not scientific semantics or execution flow.

The repository is autonomous. Do not import another repository's taxonomy or runtime. Bilingual French/English pages are counterparts, not duplicate concepts or resources. In French material, use both *embedding* and *plongement* where appropriate.

## Operating procedure

### 1. Establish the baseline

Before editing:

- Read `docs/information-architecture.md`, `docs/page-metadata-schema.md`, `docs/learning-path.md`, `docs/full-curriculum-plan.md`, `docs/computational-graph-schema.md`, `docs/canonical-computational-spine.md`, `docs/source-catalogue-schema.md`, `docs/source-lineage-architecture.md`, `docs/page-template-system.md`, `docs/design-system.md` and `CONTRIBUTING.md`, as relevant.
- Inspect the current default branch, relevant open PRs/issues, and exact branch/commit being changed.
- Inspect the canonical data, schema, validator, tests, generator and consumers for each affected model. Use the actual paths in the table above; do not infer paths from old reports.
- Record schema versions, ID namespaces, relation vocabularies, generated projections and CI jobs.
- Separate confirmed implementation, documented intent, generated output and unresolved assumptions.

### 2. Build a concise traceability matrix

For every affected entity/relation, identify exactly one authoring owner and the relevant consumer/validator:

| Element | Required traceability |
|---|---|
| Domain | Canonical bilingual record, stable ID, allowed values, concept membership |
| Concept | Stable language-independent ID, FR/EN labels and definitions, aliases/provenance, page associations |
| Concept relation | Source/target concept IDs, controlled type, direction, inverse/storage rule, cycle constraint |
| Non-page resource | Stable resource ID, kind/status, language, local/external location, provenance, page/concept associations |
| Computational node | Stable node ID, kind/role, bilingual labels/descriptions, branch membership, explanatory page IDs |
| Computational edge | Stable edge ID, source/target node IDs, controlled relation type, direction and justified loop/repetition/optional flags |
| Computational view | Selected node/edge IDs, owning page/use, deterministic projection |
| Understand stage | Stage ID/order, bilingual title/objective, core and optional page IDs in `data/guided-route.yml` |
| Curriculum/Build module | Canonical module order, prerequisites, status, deliverable and evidence in the curriculum/Build owner |
| Page-navigation relation | Page IDs and exact `suggested_route`, `hierarchy` or `related` semantics |
| Source/extraction | Source identity/version, scan events, exact locators, evidence, item disposition and lineage |
| Projection | Generator, source inputs, included node/edge types, stable IDs and consumers |

Do not conflate `concepts[].resources` (published page IDs) with first-class non-page resources in `data/resources.yml`. The latter currently contains a deliberately bounded seed of five implementation modules; do not claim that every demo, experiment, test or external reference is already a first-class resource.

The source catalogue is in a staged migration: `data/sources.yml` is the current canonical source catalogue and scan-history owner; the distributed `data/sources/<source-id>.yml`, `data/source-scans/` and `data/source-lineage/` layout is the documented target. Do not treat the target as implemented until the migration is verified on the branch.

### 3. Audit semantic integrity

Check, as applicable:

- Stable IDs are unique, durable and language-independent where the entity is language-independent; never derive them from translated labels.
- Every relation endpoint resolves to the expected entity type; relation types are controlled and directional semantics are documented.
- Enforce only justified inverse, reciprocity and cycle rules. Concept prerequisite/generalization constraints, page hierarchy constraints and computational feedback/repeated edges have different semantics.
- The symmetric concept relation `contrasts-with` uses its canonical lexical orientation rather than reciprocal duplicates.
- Computational graph feedback and repeated-module edges are explicitly marked according to its schema; do not force the operational graph into a DAG by deleting real loops. Unmarked cycles remain defects.
- FR/EN labels and descriptions exist where required; translations share stable entity identity.
- Domain membership is classification, not a causal, semantic or prerequisite edge. Page-level primary `domain` is distinct from many-to-many concept `domains`.
- Resource locations resolve and remain within permitted repository paths; distinguish page associations from non-page resource entities.
- Source scan status, extraction completeness, synthesis, integration, resource validation and learner validation remain independent states.
- Generated projections preserve source IDs and relation meaning. No projection invents semantic edges, promotes headings into concepts, or turns computational edges into learning prerequisites.
- Pedagogical order and knowledge-map connectivity remain separate.

### 4. Audit curriculum and editorial structure

- Treat `data/guided-route.yml` as the machine-readable source for the nine-stage reader-facing Understand route. `docs/learning-path.md` explains that route and owns the overall curriculum narrative, module order, prerequisites, evidence and Build status. Do not reduce the entire curriculum to the Understand registry.
- Keep the Build path distinct from Understand. Inspect its existing lesson/code evidence and curriculum documentation; do not invent a parallel Build registry.
- Preserve advanced optional material without making it an implicit core prerequisite.
- Check prerequisites against learner knowledge, not merely code execution dependencies.
- Keep page hierarchy, suggested reading transitions, curriculum prerequisites, concept relations and computational dependencies distinct.
- Verify bilingual semantic parity, page templates, navigation language and visual consistency.
- Do not change explanatory ownership or move content based only on keyword overlap; inspect learner questions and learning outcomes.

### 5. Design tests from invariants

Prefer small deterministic tests at the layer where an invariant belongs:

- **Concept/domain tests:** required fields, controlled vocabularies, stable IDs, endpoints, relation direction/storage and justified cycle constraints.
- **Resource tests:** IDs, kind/status, BCP 47 language, discriminated locations, path containment, external URL syntax and page/concept references.
- **Computational graph tests:** schema version, node/branch/edge IDs, endpoint resolution, controlled relation types, allowed flags, bilingual labels, cycle handling and deterministic views.
- **Page metadata tests:** schema/tags, page references, route/hierarchy semantics and bilingual parity.
- **Curriculum tests:** stage resolution/order and evidence/prerequisite consistency at the actual owning layer.
- **Source tests:** source identity, taxonomy, scan-history and extraction locators/dispositions; respect the current versus target lineage migration state.
- **Projection tests:** stable IDs, deterministic output and preservation of distinct relation types.
- **Regression tests:** known edge cases and previously fixed audit findings.

Use the existing test suites and CI jobs. Do not add tests for hypothetical schemas or duplicate a pytest invocation in another workflow. When a missing invariant is demonstrated, add a small fixture-based test to the owning suite and integrate it into existing CI.

### 6. CI and generated-output policy

- Reuse existing checks before adding dependencies or workflows.
- Keep fast metadata/schema/graph checks in the existing Python quality workflow.
- Keep Quarto/render checks in the existing Quarto workflow when they protect a distinct build boundary.
- Never hand-edit generated JSON, route fragments or graph projections.
- Add generated-output freshness checks only when deterministic output can be compared reliably.
- A failing check must identify the source path/entity ID and violated invariant.
- Do not create a GitHub Action or workflow per concept, page, graph branch or skill.

### 7. Change and review discipline

- Make one coherent, reviewable change at a time.
- When a canonical contract changes, update its owner, schema, validator, tests, generator/consumer and documentation together as required.
- Version breaking schema changes and provide a migration; never silently reinterpret IDs or relation types.
- Do not add graph databases, RDF stores, exports or external taxonomy dependencies without a concrete interoperability/query requirement.
- Do not rename or repurpose fields to make incomplete implementation appear complete.
- Keep the public site self-contained; no private repository, file or knowledge-base dependency.
- Never claim tests, CI, rendering, browser inspection or deployment passed unless the result was observed.

## Required audit deliverable

For each iteration, report:

1. Scope and exact commit/branch inspected.
2. Architecture inventory with canonical owners and exact paths.
3. Traceability matrix for affected models, projections, validators and tests.
4. Findings classified as confirmed defect, missing automation, documentation gap or unresolved implementation question.
5. Changes proposed or made, ordered by impact and dependency.
6. Tests/CI reused or added and the invariant each protects.
7. Validation evidence with exact commands and observed results.
8. Residual risks and the next smallest useful step.

State confidence and distinguish evidence from inference. Update only the affected matrix rows; do not repeat previous audits wholesale.

## Specialist boundaries and delegation

- Use `scientific-content-audit` for correctness, assumptions, scope and evidence of scientific claims, algorithms or computational semantics.
- Use `page-group-audit` for learner-facing sequence, group membership, transitions and cross-destination coherence.
- Use `editorial-boundary-audit` for canonical explanatory ownership, overlap, duplication and relocation.
- Use `page-content-audit` for internal pedagogy of an individual page.
- Use `rendered-site-audit` for actual rendered route, layout, keyboard, responsive and accessibility behavior.
- Use `visual-asset-audit` for asset provenance, licence and permitted reuse.
- Use `audit-skill-routing` when a request spans multiple audit dimensions.

A valid schema, graph edge or passing validator proves structural conformance only; it does not prove a concept definition, scientific statement, external visual licence, rendered usability or learner outcome.
