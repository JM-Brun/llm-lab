# Revision-resource relationship contract

**Status:** proposed canonical contract; not yet an implemented metadata schema.  
**Date:** 2026-11-19  
**Scope:** explicit links from revision aids to the published Understand/Build lessons they support, plus a separate assessment of each lesson's revision coverage.

This document reconciles the competing designs discussed in [#1109](https://github.com/JM-Brun/llm-lab/issues/1109). It supersedes the earlier page-owned `revision.resources` sketch. No page metadata, resource registry, validator, graph or generated output is migrated by this proposal.

## 1. Design requirements

1. A lesson may have zero, one or several revision aids.
2. One aid may support several lessons; do not duplicate a shared aid to manufacture one-to-one links.
3. An aid may be a published Quarto page or a non-page artifact with a stable resource ID.
4. The aid declares its relationship to its source lesson(s); the reverse lesson-to-aids view is derived.
5. Link existence and pedagogical sufficiency are separate facts.
6. Missing metadata means **not assessed**, not “no revision support”.
7. Never infer a relationship from filenames, titles, body links, tags, topic overlap, sidebar position or generic graph proximity.
8. Keep revision relationships separate from reading order, hierarchy, generic related links, concepts and source provenance.
9. Language-specific aids target the corresponding language version. A genuinely bilingual aid may target an explicitly paired French/English source set.
10. Existing page and resource identities remain owned by their canonical registries.

## 2. Terminology and identity

| Term | Meaning | Canonical identity |
|---|---|---|
| Lesson | Published Understand or Build page whose learning is supported | Existing page ID from `LLM-LAB-PAGE-MAP v1` |
| Page aid | Revision aid published as a Quarto page | Existing page ID; never duplicate it in `data/resources.yml` |
| Non-page aid | Revision aid that is not a published Quarto page | Stable resource ID in `data/resources.yml` |
| Revision role | Learner-facing function of an aid | Controlled value declared by the aid |
| Revision edge | Directed link from an aid to a lesson | Aid identity + role + lesson page ID |
| Revision assessment | Evidence-backed judgement of support sufficiency for one lesson | Field on the source lesson page |

Page IDs and resource IDs are separate namespaces. Resolve a page target only against the published-page index and a non-page target only against the resource registry. `concepts[].resources` continues to contain page IDs and must not be overloaded.

## 3. Canonical relation direction and representation

The canonical edge direction is **aid → source lesson**. This represents the provenance of the learning aid, supports one aid serving several lessons without duplicating declarations, and allows the reverse lesson → aids index to be generated deterministically.

### 3.1 Page-based aid

A published Quarto page that is a revision aid declares:

- `revision_role`: one controlled primary role;
- `revision_of`: a non-empty list of stable page IDs for the source lessons.

Illustrative only:

```yaml
revision_role: revision_sheet
revision_of:
  - fr/entropy
  - fr/cross-entropy
```

A source lesson must not use these fields to point to an aid.

### 3.2 Non-page aid

A non-page aid is represented in `data/resources.yml` with a distinct resource kind, provisionally `kind: revision-aid`, and the same `revision_role` / `revision_of` semantics. Its kind-specific required fields must be finalized after the non-page artifact inventory. Do not add `revision_of` to an `implementation` resource and do not reinterpret `referenced_by`.

Illustrative only:

```yaml
- id: information-theory-revision-notes
  kind: revision-aid
  revision_role: revision_sheet
  revision_of:
    - fr/entropy
    - en/entropy
  language: mul
  status: published
  location:
    type: local
    path: docs/revision-sheets/information-theory-and-llms-2026-11.md
```

The BCP 47 language tag `mul` is appropriate only when the artifact genuinely contains multiple languages. This example remains a sketch until the Markdown file is confirmed as a learner-facing aid rather than a source artifact.

### 3.3 Controlled revision roles

The initial vocabulary is:

- `synthesis`: concise recovery of the central question, mechanism, distinctions and limits;
- `flashcards`: retrieval prompts with answers;
- `revision_sheet`: a compact structured aid for later recall or exam preparation.

An aid has one primary role. Do not infer roles from file extensions or titles. Multiple roles should be represented separately only when each provides a distinct learner-facing function.

## 4. Separate lesson-level assessment

A relation says that an aid is associated with a lesson. It does **not** prove that the aid is accurate, current, complete or pedagogically sufficient. Each in-scope source lesson therefore needs a separate evidence-backed assessment, provisionally:

```yaml
revision_support:
  status: companion_sufficient
  evidence:
    - aid: fr/revision-information-theory
      note: "Core identities, worked example and self-check cover the lesson's revision needs."
```

Controlled statuses:

| Status | Meaning |
|---|---|
| `not_assessed` | No individual editorial assessment has been completed |
| `integrated_sufficient` | The lesson's own recap, diagrams, examples and retrieval prompts are sufficient |
| `companion_sufficient` | One or more linked aids are sufficient for the lesson |
| `partial` | Some revision support exists but a material gap remains |
| `missing` | Reviewed; no sufficient revision support exists |
| `not_applicable` | The page is explicitly outside the agreed revision-support scope; a reason is required |

Evidence should point to a section anchor, page-aid ID or resource ID and state briefly what it covers. `companion_sufficient` requires at least one valid published aid relation. `integrated_sufficient` requires evidence on the lesson itself. `missing` and `not_applicable` require a concise rationale. Absence of `revision_support` remains `not_assessed` during migration.

Do not infer assessment from a “one-minute” callout, a Practice page, a generic related edge or an aid title. Sufficiency is an editorial judgement made page by page.

## 5. Proposed validation constraints

These are requirements for future validator behavior, not current implementation behavior.

### 5.1 Aid structure

- `revision_role` must be one of `synthesis`, `flashcards`, or `revision_sheet`.
- `revision_of` must be a non-empty list of unique stable page IDs when present.
- An aid cannot target itself.
- Every target must resolve to a published Understand or Build lesson. Exclude Practice-only aids, exercise collections, references and other revision aids as targets.
- Page-aid fields must be retained in the normalized page projection.
- A non-page aid must use the dedicated revision-aid kind and satisfy that kind's required fields. Implementation resources remain unchanged.
- Only published aids enter the public reverse index; draft, deprecated and retired lifecycle states must be handled explicitly.

### 5.2 Language and multiple sources

- A French page aid targets French lessons; an English page aid targets English lessons.
- A `shared` page aid or `mul` non-page aid may target a bilingual pair only when it genuinely contains both language versions.
- A language-neutral artifact may be shared only when no language-specific learner text is required.
- Multiple source lessons are allowed, but every target must independently satisfy destination, publication and language rules.
- Duplicate targets, unknown IDs, unpublished targets, ineligible targets and incompatible languages are errors.

### 5.3 Lesson assessment

- `revision_support.status` must use the controlled vocabulary above.
- `evidence` must be structured references, not unsupported free-form claims alone.
- `companion_sufficient` must reference at least one published aid that points back to this lesson.
- `integrated_sufficient` must reference an anchor or identifiable integrated section on the lesson itself.
- `missing` and `not_applicable` require a non-empty rationale.
- Link integrity and editorial sufficiency must be reported separately.

## 6. Compatibility audit against current code

This records the inspected `main` implementation as of 2026-11-19.

### 6.1 Page metadata validator

`site/tools/check_page_metadata.py` parses page-map YAML and returns a normalized dictionary containing only currently recognized fields. It validates route, hierarchy and `related` targets, publication status, reciprocity, cycles, tags, language/topic parity and render-list coverage.

It does **not** currently validate or return `revision_role`, `revision_of` or `revision_support`. The page-map parser does not reject every unknown key, so these fields could be silently ignored downstream. The proposed relation and assessment are therefore not implemented or safely validated.

### 6.2 Published page index

`site/tools/page_index.py` stores the raw page-map mapping on `PublishedPage.metadata`. It already preserves additional page-map keys when loading published pages. It does not need a new dataclass field merely to transport the revision fields; the normalized metadata validator and downstream projections still need explicit support.

### 6.3 Non-page resource validator

`site/tools/check_resource_registry.py` has a strict field allow-list and currently accepts only `kind: implementation`. It validates BCP 47 language, lifecycle status, locations, page references, concepts and optional provenance. It does not accept a revision-aid kind or revision relationships. The existing `referenced_by` field records pages that reference an implementation resource; it is not aid → lesson ownership.

A distinct revision-aid kind is technically possible, but its required fields and lifecycle semantics must be based on the inventory of actual non-page aids before changing this validator.

### 6.4 Revision inventory generator

`site/tools/audit_revision_coverage.py` currently projects Understand and Build pages, concept links and implementation-resource references. It assigns `synthesis_status: not_assessed` to every lesson and does not inspect Practice/Deepen pages or non-page files as candidate aids. It therefore cannot calculate incoming revision aids or evidence-backed support status.

### 6.5 Identity boundaries

- `data/concepts.yml` associates concepts with published page IDs; keep this unchanged.
- `data/resources.yml` remains the canonical registry for non-page resources; do not create a parallel revision registry unless the artifact inventory demonstrates that the existing registry cannot represent the required distinction.
- Generic `related`, `parents`, `children` and `suggested_route` edges retain their existing meanings.

**Compatibility conclusion:** the aid → lesson relation respects existing identity boundaries, and `page_index` already transports raw metadata. However, the current page validator, resource validator and inventory generator do not implement or enforce the contract. Do not write these fields into production metadata until validators and projections are updated.

## 7. Migration and implementation order

1. Inventory existing aids across published Quarto pages and non-page files. Record identity, language, role, lifecycle, candidate source lessons and whether the artifact is genuinely learner-facing. Do not create new aids during this inventory.
2. Confirm the resource-kind representation for concrete non-page aids. Keep implementation resources unchanged.
3. Add validator tests first: page aid → lesson, non-page aid → lesson, multiple sources, bilingual pairs, unknown/unpublished/ineligible targets, self-link, duplicate, wrong language, draft/retired lifecycle, and malformed assessment evidence.
4. Extend `check_page_metadata.py` to validate and preserve page-aid fields and lesson assessments; validate references against published page descriptors.
5. Extend `check_resource_registry.py` only for non-page kinds justified by the inventory, validating target IDs, language and lifecycle.
6. Extend the inventory generator to inspect all published pages and eligible non-page resources, then derive lesson → aids reverse links. Keep implementation resources in a separate field.
7. Keep assessment status independent from relation existence; publish explicit unknown/unassessed counts.
8. Migrate only reviewed lessons and aids in bounded, auditable batches. Do not rewrite the 62-page historical inventory snapshot wholesale.
9. Validate the learner-facing revision index only after relation and assessment projections are deterministic and tested.

## 8. Decisions still open

- Confirm the final controlled role vocabulary and whether a separate role is needed for short recall prompts embedded in a lesson.
- Confirm whether the Markdown file in `docs/revision-sheets/` is a learner-facing non-page aid or a source artifact.
- Decide the exact structured evidence fields and whether section anchors need static existence validation.
- Define legitimate exceptions for `shared`/multilingual resources and pages outside Understand/Build.
- Agree the first bounded migration sample after the resource inventory.

Until these decisions are closed, this remains a proposed contract. No metadata, registry, validator, graph or generated output should be changed on the assumption that these fields already work.
