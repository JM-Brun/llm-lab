---
name: knowledge-change-workflow
description: Route and coordinate additions or changes to LLM Lab knowledge, pages, concepts, cross-domain links and source-backed learning content using the existing canonical workflows without creating duplicate registries or learning paths.
---

# Knowledge-change workflow

## Mission

Coordinate a coherent change to the existing LLM Lab knowledge system. Use this skill when the user asks to add knowledge, connect topics, add or restructure a page, integrate a synthesis, or improve how sources support the project.

This is an **orchestration skill**, not a replacement for specialist work. Its normative procedure is [the knowledge-change workflow](../../../docs/workflows/knowledge-change-workflow.md). Read that document before substantial work.

## Route to the right specialist

| User intent | Primary specialist | Add only when required |
|---|---|---|
| Inspect a new external source | `source-to-learning-integration` | `project-learning-resource-audit` for a coherent external learning project |
| Integrate already-extracted source items | `knowledge-and-learning-integration` | `scientific-content-audit`, `visual-asset-audit`, `rendered-site-audit` for distinct unresolved checks |
| Create a new reader-facing page | `new-learning-page` | `knowledge-and-learning-integration` for concept/source/graph updates |
| Improve one existing page | `page-content-audit` | `scientific-content-audit` if technical correctness is central |
| Create, extend, audit or reorganize a series / coherent multi-page group; resolve overlap | `page-group-audit` and/or `editorial-boundary-audit` | `new-learning-page` for genuinely new page owners; `knowledge-and-learning-integration` for source/concept changes; `knowledge-architecture-audit` for canonical graph or route changes |
| Add concepts, typed relations, domains or knowledge-graph projections | `knowledge-architecture-audit` | `knowledge-and-learning-integration` for the learning-content decision |
| Model or revise computational nodes, operations, dataflow edges, operational branches or graph views | `knowledge-architecture-audit` | `scientific-content-audit` when computational correctness is disputed; `knowledge-and-learning-integration` when source-backed learning content also changes |
| Validate the rendered learning experience | `rendered-site-audit` | Page/group skill for pedagogical implications |

Use `audit-skill-routing` for audit requests that do not fit a direct addition/integration task. Select the smallest sufficient skill set.

## Required sequence

1. **Baseline:** inspect current branch/commit, existing issues/PRs, canonical docs, registries, relevant pages and existing source dossiers. Never rely on a prior summary as current repository state.
2. **Learner problem:** state the specific learner question or research capability the change serves.
3. **Smallest intervention:** test correction, existing-page improvement, complementary section, link/reference, then new page—in that order.
4. **Ownership:** identify the one canonical owner for every concept, page, source, resource, route and generated projection.
5. **Evidence:** separate source claims, primary evidence, project observations, inference and learner evidence.
6. **Integration:** apply the specialist workflow; preserve useful material and record exact source-to-destination mappings.
7. **Connections:** add typed concept relations and contextual page links only where they clarify a real relationship. Distinguish semantic relations from prerequisites and reading order.
8. **Parity:** update bilingual counterparts and preserve intentional language-specific editorial choices.
9. **Validation:** report structural tests, technical review, render/browser/accessibility and learner evidence separately.
10. **Handoff:** update the existing owner issue/PR and report accepted changes, no-op decisions, preservation and unresolved risks.

## Hard constraints

- No second source catalogue, concept registry, domain taxonomy, resource registry, knowledge graph or page metadata model.
- No parallel Understand route: `data/guided-route.yml` remains the sole machine-readable source for its nine reader-facing stages. `docs/learning-path.md` remains the overall curriculum narrative and owner of module order, prerequisites, evidence and Build status. Do not confuse the Understand route with the entire curriculum.
- No new page solely because a source or concept is new.
- No concept node solely because a term appears in a heading or extraction.
- No conversion of computational graph edges into concept relations, page-navigation relations or pedagogical prerequisites; use `data/computational-graph.yml` only for computation/dataflow semantics.
- No generic `related-to` relation in place of a typed semantic decision.
- No silent deletion, shortening or relocation of useful content.
- No generated output hand-edits.
- No claim of validation that was not actually performed.
- No merge without explicit authorization.

## Completion report

State:
- the learner problem and selected specialist skill(s);
- the canonical owner(s) and files changed;
- sources/evidence and their limits;
- page/concept/relation/navigation decisions, including intentional no-ops;
- cross-domain links added or rejected and why;
- preservation and bilingual parity;
- validation results by layer;
- follow-up work in the existing issue/PR.
