---
name: knowledge-architecture-audit
description: Audit and evolve the existing LLM Lab information architecture, knowledge graph, learning path, page metadata, and their automated checks without creating competing models.
---

# LLM Lab knowledge-architecture audit

## Purpose

Use this skill for every future iteration that audits, reorganizes, extends, or validates the information architecture of the LLM Lab repository.

The task is to preserve and improve the project's existing architecture. This is not permission to create a replacement taxonomy, a second graph, or a new canonical registry.

## Non-negotiable model

The knowledge graph has three domain dimensions:

1. **Domains** — the six controlled knowledge families.
2. **Concepts** — stable, language-independent notions with bilingual labels and typed semantic relations, including prerequisite, generalization, application, and opposition.
3. **Resources** — pages, demonstrations, experiments, implementations, and references associated with concepts. Associations can be many-to-many.

It has two complementary graph projections:

- **Pedagogical path:** learning order and dependencies needed to understand and build an LLM.
- **Knowledge map:** domains, concepts, advanced material, and cross-cutting relations without imposing a reading order.

Keep the underlying domain model distinct from its projections. Also keep the page-navigation graph distinct from the concept graph: page IDs, concept IDs, topic tags, headings, route edges, hierarchy edges, and semantic concept relations are not interchangeable.

The repository is autonomous. Do not import or depend on the taxonomy or runtime of another repository. Bilingual French/English pages are counterparts, not duplicates. In French material, use both *embedding* and *plongement* where appropriate.

## Operating procedure

### 1. Establish the baseline before editing

- Read `docs/information-architecture.md`, `docs/page-metadata-schema.md`, `docs/learning-path.md`, `docs/full-curriculum-plan.md`, `docs/page-template-system.md`, `docs/design-system.md`, and `CONTRIBUTING.md`.
- Inspect the current default branch, all relevant open PRs, and the exact branch/commit being modified.
- Locate the canonical source and schema for each of the three graph dimensions and both projections. Do not infer that a model exists in code merely because it is described in prose.
- Record exact file paths, schema versions, ID namespaces, relation vocabularies, generators, consumers, tests, and CI jobs.
- Distinguish confirmed implementation, documented intent, generated projection, and unresolved assumption.

### 2. Build a traceability matrix

For each entity/relation, record:

| Element | Required traceability |
|---|---|
| Domain | Canonical record, stable ID, allowed values, concept membership |
| Concept | Canonical record, stable ID, FR/EN labels, definition, aliases, provenance |
| Concept relation | Source/target IDs, exact relation type, directionality, inverse rule if any |
| Resource | Canonical record, stable ID, kind, language, status, source path/URL |
| Concept-resource association | Concept ID, resource ID, association role, evidence/description |
| Pedagogical step | Canonical curriculum location, prerequisites, learning outcome, evidence/deliverable |
| Knowledge-map projection | Generator, included node/edge types, filters, stable links |
| Page-navigation node | Page ID, page metadata source, route/hierarchy/related semantics |

Every row must name one authoritative owner. If two sources appear authoritative, report the conflict; do not silently choose one or synchronize by hand.

### 3. Audit semantic integrity

Check at minimum:

- Stable IDs are unique, durable, language-independent where the entity is language-independent, and never derived from translated display labels.
- Every relation endpoint resolves to an entity of the expected type.
- Relation types belong to a controlled vocabulary; directionality and inverse semantics are explicit.
- Prerequisite and hierarchy relations are acyclic where the model requires a DAG. Do not impose acyclicity on inherently symmetric or cyclic relations such as opposition or application without a domain justification.
- Inverse/reciprocal constraints are enforced only for relation types whose semantics require them.
- FR/EN labels exist for published concepts; translations share entity identity rather than duplicate entities.
- Every published concept has at least one useful resource, unless explicitly marked abstract/non-resource-backed.
- Resources can support multiple concepts; concepts can have multiple resources.
- Resource links resolve to source files or valid external references; status and language are consistent.
- Domain membership is classification, not a prerequisite or semantic edge.
- Generated projections preserve source IDs and relation meaning; no projection invents semantic edges or turns headings into concepts.
- Pedagogical order and knowledge-map connectivity remain separate.

### 4. Audit curriculum and editorial structure

- Treat `docs/learning-path.md` as the curriculum sequence source of truth; do not reconstruct it from sidebar order or page-map edges.
- Preserve the main conceptual route separately from advanced material and implementation branches.
- Each concept should have one canonical explanatory home. Other pages may orient, apply, or briefly recall it, but must not duplicate its full explanation without a distinct learning outcome.
- Check prerequisites against learner knowledge, not merely code execution dependencies.
- Keep optional advanced material from becoming an implicit prerequisite of the core route.
- Verify bilingual semantic parity, page templates, navigation language, and visual consistency.
- Do not change content ownership or move material based only on keyword overlap; inspect learning outcomes and explanatory responsibility.

### 5. Design tests from invariants

Prefer small deterministic tests at the layer where an invariant belongs:

- **Schema/unit tests:** required fields, types, controlled vocabularies, ID format, uniqueness, and version compatibility.
- **Graph-integrity tests:** dangling endpoints, duplicate edges, illegal relation types, inverse/reciprocity rules, self-loops, and justified cycle constraints.
- **Bilingual tests:** shared canonical IDs, required labels, equivalent relation topology, and valid resource language.
- **Resource-link tests:** local path existence, external URL syntax, status consistency, and many-to-many association coverage.
- **Projection tests:** stable IDs, deterministic output, expected node/edge counts, and no accidental collapse of distinct relation types.
- **Curriculum tests:** prerequisite resolution, acyclicity where required, and consistency between step status and evidence.
- **Regression tests:** known edge cases and previously fixed audit findings.

Use fixtures with small synthetic graphs. Include both valid examples and one failing fixture per invariant. Assert actionable error messages containing the entity ID and relation/field. Avoid snapshot tests for large generated files unless snapshots are deliberately normalized and reviewed.

Do not add tests for hypothetical schemas that have not been located. If the canonical concept/resource model is not yet machine-readable, first document the gap and propose the smallest source-compatible contract; do not create a competing registry just to make tests possible.

### 6. CI policy

- Reuse existing checks before adding another workflow or dependency.
- Keep fast metadata/schema/graph checks in the existing Python quality workflow.
- Keep a render-level validation in the Quarto workflow when it protects a distinct build boundary.
- Run unit tests through the existing `pytest` step; avoid duplicating the same test invocation in multiple workflows.
- Add generated-output freshness checks only when the output is tracked or a deterministic build artifact can be compared without committing generated files.
- Pin or constrain new dependencies, justify them, and keep checks CPU-only and bounded.
- A CI check must fail on a real invariant violation and print the source path/entity ID and violated rule.

### 7. Change and review discipline

- Make one coherent, reviewable change at a time.
- Update canonical data, schema, generator, consumer, tests, and documentation together when a contract changes.
- Version breaking schema changes and provide a migration; do not silently reinterpret existing IDs or relation types.
- Never hand-edit generated JSON.
- Do not add a graph database, RDF store, JSON-LD export, or external taxonomy dependency without a concrete interoperability/query requirement.
- Do not rename or repurpose a field merely to make an incomplete implementation look complete.
- Keep the public site self-contained; no private repository, file, or knowledge-base dependency.
- Do not claim tests, CI, rendering, or deployment passed unless the corresponding run result was observed.

## Required audit deliverable

For each iteration, report:

1. **Scope and commit/branch inspected.**
2. **Architecture inventory** with canonical owners and exact paths.
3. **Traceability matrix** for domains, concepts, resources, relations, curriculum steps, and projections.
4. **Findings** classified as confirmed defect, missing automation, documentation gap, or unresolved implementation question.
5. **Proposed changes** ordered by impact and dependency.
6. **Tests and CI** added or reused, including the invariant each protects.
7. **Validation evidence** with exact commands and observed results.
8. **Residual risks** and next smallest useful step.

State confidence and distinguish evidence from inference. Do not repeat a previous audit wholesale: update the matrix and findings based on the changed files and current branch state.
