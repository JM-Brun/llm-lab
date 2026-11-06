---
name: audit-skill-routing
description: Select and coordinate the LLM Lab audit skills for page, pedagogical, editorial, scientific, architecture and source-review tasks while avoiding duplicated or conflicting audits.
---

# Audit skill routing

## Mission

Choose the smallest set of specialist skills that fully answers an audit request. Coordinate their order, evidence and finding lifecycle without creating a parallel audit methodology or repeating the same checks in multiple reports.

This is a routing skill, not a substitute for specialist analysis.

## Routing matrix

| User's central question | Primary skill | Add only when needed |
|---|---|---|
| Is this one page pedagogically clear, complete and well structured? | `page-content-audit` | `scientific-content-audit` for technical claims; `editorial-boundary-audit` for cross-page ownership |
| Do these pages form a coherent sequence, family or local window? | `page-group-audit` | `page-content-audit` for deep page-level review; `editorial-boundary-audit` for overlap; `knowledge-architecture-audit` for canonical graph/route changes |
| Are explanations duplicated, misplaced or ambiguously owned? | `editorial-boundary-audit` | `page-group-audit` for sequence implications; `scientific-content-audit` for factual disputes |
| Are concepts, relations, domains, metadata, routes or graph projections coherent and valid? | `knowledge-architecture-audit` | `scientific-content-audit` when relation semantics depend on disputed technical truth; `page-group-audit` for learner-facing route effects |
| Are equations, algorithms, statistical claims, code behavior or experimental conclusions correct? | `scientific-content-audit` | `page-content-audit` for teaching implications; `page-group-audit` for downstream route consequences |
| Should an external source be catalogued and decomposed into evidence-linked items? | `source-extraction` | `source-to-learning-integration` only if integration is also requested |
| Should validated source items change pages, graph, visuals or experiments? | `knowledge-and-learning-integration` | `source-to-learning-integration` when coordinating both phases |

Do not invoke every skill for every request. A named page does not automatically require a group audit; a graph-related word does not automatically require architecture changes.

## Coordination protocol

### 1. Parse the requested outcome

Identify:
- object: page, group, route, concept graph, source, code, experiment or site-wide system;
- question: correctness, pedagogy, overlap, architecture, navigation, visual behavior or integration;
- expected action: diagnose, recommend, implement, create issues or validate an existing change;
- scope: named pages/files, language versions, local window or bounded project area.

If one essential boundary is missing, ask one concise question. Otherwise declare a revisable scope and proceed.

### 2. Select one primary skill

Choose the skill whose responsibility matches the user's main decision. Add a secondary skill only for a distinct question that the primary skill explicitly does not own.

Prefer this sequence for multi-dimension work:
1. establish the relevant canonical architecture and scope;
2. perform scientific verification when correctness is disputed or central;
3. perform page-level or group-level pedagogical analysis;
4. perform editorial ownership decisions;
5. update architecture/navigation only after content and learning implications are established;
6. validate the actual rendered and tested result.

This order is conditional, not a mandatory pipeline. Skip steps that do not materially affect the requested decision.

### 3. Keep evidence and findings traceable

Use one evidence ledger per bounded audit effort. Each claim should identify source path/locator, evidence type, confidence and whether rendered/runtime behavior was observed.

Use one canonical finding ID and owner for each issue. Related skills may reference that ID with their own impact, but must not create duplicate findings or contradictory action items.

Separate:
- source-level evidence from interpretation;
- page metadata from page-body evidence;
- source inspection from rendered observation;
- structural bilingual parity from semantic parity;
- CI/test success from scientific correctness and learner validation.

### 4. Resolve conflicting recommendations

When specialist outputs disagree:
- identify whether they answer different questions or truly conflict;
- prefer canonical schemas and project policy for structural contracts;
- prefer primary evidence, derivation and reproducible implementation checks for scientific truth;
- prefer observed learner purpose and page-body evidence for editorial ownership;
- do not let convenience, page count, visual symmetry or graph metrics override these constraints.

If the conflict remains unresolved, report the decision and evidence needed; do not silently choose a side.

### 5. Keep diagnosis, implementation and validation distinct

Unless implementation is requested, produce findings and a prioritized plan only.

When implementation is requested:
- make a bounded, reviewable change;
- update canonical sources before generated projections;
- preserve content and record any relocation;
- update FR/EN counterparts where applicable;
- run only relevant checks, then shared-system checks where justified;
- report passed, failed, pending and not-run validation separately.

A PR opened is not a merged change. A passing check is not proof of scientific or pedagogical quality.

## Output

For a simple request, name the primary skill and proceed without presenting this routing table.

For a multi-skill audit, state:
1. selected primary and supporting skills, with one-line rationale;
2. bounded scope and exclusions;
3. findings grouped by their owning dimension;
4. shared evidence and canonical finding IDs;
5. ordered actions and dependencies;
6. validation status and unresolved conflicts.

## Maintenance

When a new audit pattern appears:
- first test whether an existing skill can own it through a small, clear extension;
- create a new skill only for a durable responsibility with a distinct trigger, procedure and output;
- do not duplicate full checklists across skills;
- update this routing matrix whenever a skill is added, renamed or retired;
- calibrate material changes against representative past cases and record case-specific evidence in dated reports, not in permanent skill instructions.
