# Revision-resource relationship contract

**Status:** partially implemented for page-based aids through ProjectIndex; unified page-metadata validation and non-page revision aids remain open.  
**Date:** 2026-11-23  
**Scope:** explicit links from revision aids to the published Understand/Build lessons they support, plus a separate assessment of each lesson's revision coverage.

This document reconciles the competing designs discussed in [#1109](https://github.com/JM-Brun/llm-lab/issues/1109). It supersedes the earlier page-owned `revision.resources` sketch. Current `main` already contains page-based `revision_role`, `revision_of` and `revision_support` handling in `ProjectIndex`, plus a derived revision inventory. This document now distinguishes that implemented subset from the still-proposed complete contract. No non-page revision-aid kind or broad metadata migration is authorized.

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

## 5. Validation contract and current enforcement

The page-based subset is enforced by `ProjectIndex._load_revision_relations`. The normal CI workflow runs `audit_revision_coverage.py`, which builds ProjectIndex and therefore exercises these semantic checks against the repository's actual pages. `check_page_metadata.py` remains responsible for the general page-map contract and does not duplicate revision semantics. Non-page revision aids are not supported by the current resource registry validator.

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

## 6. Compatibility audit against current main — 2026-11-23

### 6.1 Page metadata validator

`site/tools/check_page_metadata.py` validates page identity, controlled tags, route/hierarchy/related links, reciprocity, cycles, bilingual topic parity and render-list coverage. It contains no handling for `revision_role`, `revision_of` or `revision_support`.

The page-map parser does not reject every unknown key. Therefore the revision fields are not validated by this validator itself. Do not describe the page metadata validator as enforcing the revision contract.

### 6.2 Published page index and ProjectIndex

`site/tools/page_index.py` preserves the raw page-map mapping on `PublishedPage.metadata`.

`site/tools/project_index.py` now implements a page-based revision adapter:

- Allowed roles: `synthesis`, `flashcards`, `revision_sheet`.
- `revision_of` must be a non-empty list of unique page IDs.
- A revision aid cannot also be an Understand/Build lesson.
- Every target must resolve to a published Understand or Build page.
- Aid and lesson languages must match, except for the explicitly supported `mul` and `shared` cases.
- Lesson assessments validate the controlled status vocabulary, structured evidence, aid-to-lesson consistency, explicit section anchors and required rationales.
- `not_assessed` is distinct from `missing`; `integrated_sufficient` requires anchor evidence and `companion_sufficient` requires a linked aid.

The index derives both directions: aid → lesson and lesson → aids. It does not author reciprocal duplicate declarations.

### 6.3 Non-page resource validator

`site/tools/check_resource_registry.py` currently accepts only `kind: implementation`. It validates resource identity, language, lifecycle, location, page references, concept associations and optional provenance.

No non-page revision-aid kind or resource → lesson revision relationship is implemented. The existing `referenced_by` field records pages that reference an implementation resource; it is not a revision-aid ownership relation. Keep implementation resources unchanged.

### 6.4 Revision inventory generator

`site/tools/audit_revision_coverage.py` now consumes `ProjectIndex` revision assessments and reverse aid links. It reports the revision status for each Understand/Build lesson and the explicit page-based aids attached to it. It no longer assigns every lesson an unconditional `not_assessed` without inspecting page-aid declarations.

The migration inventory in PR [#1550](https://github.com/JM-Brun/llm-lab/pull/1550) records **50 typed revision-aid links across 40 pages** in its affected page neighborhood. This is a structural relation count, not a claim that every lesson has sufficient revision support.

The generator does not discover non-page files as revision aids. Implementation-resource associations remain a separate field.

### 6.5 Existing regression tests

`tests/knowledge/test_project_index.py` covers page-aid bidirectional queries and assessment, eligible published targets, duplicate targets, language mismatches, page-aid evidence consistency, and explicit heading anchors.

These tests establish the ProjectIndex behavior. They do not establish that `check_page_metadata.py` independently validates the same fields or that non-page revision aids are supported.

### 6.6 Compatibility conclusion

The page-based revision relation is **implemented and exercised through ProjectIndex and the CI revision-inventory step**. It is a complete supported subset, but not a complete all-artifact revision model:

- page-based relationships and lesson assessments are parsed and validated by ProjectIndex;
- `check_page_metadata.py` does not validate these fields; the CI-invoked ProjectIndex revision audit is the semantic validation boundary, avoiding duplicate validators;
- the non-page resource registry does not support revision-aid resources;
- the revision inventory projects page-based aids and assessments but not non-page aids;
- the reader-facing peer Review route remains a separate projection owned by [#1541](https://github.com/JM-Brun/llm-lab/issues/1541).

Do not create a second revision registry. Reconcile the existing adapter, validator and contract before expanding the model.

## 7. Updated implementation order

1. **Preserve the existing page-based implementation.** Do not remove or rewrite the current `revision_role`, `revision_of` and `revision_support` metadata.
2. **Keep one semantic validation boundary.** The CI-invoked `audit_revision_coverage.py` builds ProjectIndex and exercises the page-based revision checks. Do not duplicate these rules in `check_page_metadata.py` unless a second consumer demonstrates a concrete need.
3. **Preserve the integration tests.** Existing ProjectIndex tests cover malformed roles, duplicate/unknown/unpublished/ineligible targets, language mismatches and invalid assessment evidence; keep them aligned with any future schema change.
4. **Retain and extend the existing revision inventory.** Keep aid links, assessment state and implementation-resource associations separate; report unknown/unassessed counts explicitly.
5. **Inventory non-page candidates before extending resources.** Confirm whether `docs/revision-sheets/` or any other artifact is genuinely learner-facing and needs a stable non-page identity. Do not add a resource kind merely for architectural symmetry.
6. **Only if justified, extend `check_resource_registry.py`.** Define the minimal non-page aid fields, target semantics, language and lifecycle behavior; preserve the implementation-resource contract.
7. **Keep sufficiency independent from link integrity.** A typed aid link is not proof that the aid is pedagogically sufficient.
8. **Migrate in reviewed batches.** Preserve all existing content and rationale; do not rewrite the historical inventory snapshot wholesale.
9. **Complete the peer Review route separately under #1541.** Derive it from `guided-route.yml`, `lesson_contracts` and typed revision-aid relations; keep Practice exercises outside the Review route.

## 8. Decisions still open

- The current role vocabulary is `synthesis`, `flashcards`, and `revision_sheet`. Short recall prompts embedded in a lesson are not a separate aid role; they are assessed as integrated support through `revision_support` and explicit section evidence.
- Inspect `docs/revision-sheets/` only if a real reader-facing use case requires a non-page aid identity; otherwise keep non-page revision aids deferred.
- Keep the current structured evidence and anchor rules; add rendered anchor validation only if the current CI/rendered-link checks cannot establish the required guarantee.
- Keep `shared`/multilingual exceptions explicit and evidence-based; do not broaden them by default.
- No further page-based migration is authorized until the current inventory and learner-facing Review gaps are reconciled.

Until these decisions are closed, this remains a proposed contract. No metadata, registry, validator, graph or generated output should be changed on the assumption that these fields already work.
