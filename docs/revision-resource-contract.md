# Revision-resource relationship contract

**Status:** proposed architecture contract; not an implemented metadata schema.  
**Date:** 2026-11-19  
**Scope:** explicit associations between a learning page and its revision support (integrated section, companion page or non-page artifact) for synthesis, flashcards and revision sheets.

This document records a candidate model for review. It does **not** authorize edits to the 62-page historical snapshot, changes to `LLM-LAB-PAGE-MAP v1`, changes to `data/resources.yml`, or changes to any validator. Those changes require a separately reviewed implementation plan after this contract and the existing data inventory have been checked.

## 1. Design requirements

1. A learning page may have zero, one or several revision artifacts.
2. A revision artifact may support more than one learning page; do not duplicate a shared artifact to manufacture one-to-one links.
3. Revision support may be either:
   - an integrated section of the learning page itself, identified by an explicit heading anchor;
   - a companion published Quarto page with its existing stable page ID; or
   - a non-page artifact with its own stable resource ID in `data/resources.yml`.
4. The relationship has an explicit pedagogical role. A synthesis, a flashcard set and a revision sheet are not interchangeable.
5. The relation is directional: **learning page → revision artifact**. Reverse lookups are derived indexes, not separately authored links.
6. Missing metadata must not be interpreted as proof that a page has no revision support.
7. The relation must not be inferred from filenames, matching titles, links in the body, tags, topic overlap or proximity in a graph.
8. The relationship is not a reading-order edge, prerequisite, conceptual hierarchy edge, concept-resource association, or evidence/provenance edge.
9. French and English counterparts should link to the corresponding language version of an artifact. A language-neutral artifact may be shared when its content genuinely is language-independent.
10. Existing page, concept and non-page resource identities remain owned by their current canonical sources.

## 2. Terminology and identity

| Term | Meaning | Canonical identity |
|---|---|---|
| Learning page | Published page whose explanation or implementation is supported by revision material | Existing page ID from `LLM-LAB-PAGE-MAP v1` |
| Integrated section | Revision material embedded in the learning page itself | Explicit heading anchor within the source page |
| Page artifact | Revision material published as a separate Quarto page | Existing page ID; it is not copied into `data/resources.yml` |
| Non-page artifact | Revision material not published as a Quarto page (for example, a machine-readable flashcard set) | Stable resource ID in `data/resources.yml` |
| Revision role | The function the artifact serves for the learning page | Controlled value on the relationship |
| Revision relationship | Explicit association from one learning page to one artifact | Derived key from source page, role, target type and target ID |

A page ID and a resource ID are different namespaces. Never resolve a page target by searching the resource registry, or a resource target by searching page metadata. In particular, `concepts[].resources` continues to contain published page IDs; it must not be overloaded with non-page resource IDs or revision links.

## 3. Proposed relationship shape

The preferred candidate is an optional `revision` object in the page's existing `LLM-LAB-PAGE-MAP v1` block. This keeps page-owned relationships beside the page identity and its other page-level relations, while allowing the target to be either a page or a non-page resource.

Illustrative only:

```yaml
revision:
  status: assessed
  resources:
    - role: synthesis
      target:
        type: page
        id: fr/information-theory-synthesis
    - role: flashcards
      target:
        type: resource
        id: information-theory-flashcards-fr
    - role: revision_sheet
      target:
        type: page
        id: fr/information-theory-revision
```

The example IDs and target pages are illustrative, not assertions that these artifacts exist in the current repository.

### 3.1 Status semantics

The `revision` object is optional so existing pages remain valid and untouched until a migration is approved.

| Status | Meaning | Required behavior |
|---|---|---|
| Omitted | Not yet assessed under this contract | Report as unknown / not assessed, never as “no resource” |
| `not_assessed` | Explicitly not reviewed | `resources` must be omitted or empty |
| `assessed` | Reviewed against the declared revision roles | `resources` may be empty or contain validated relationships |
| `not_applicable` | Page is outside the agreed revision-support scope | A non-empty `reason` is required; do not count as a missing resource |

An empty list is meaningful only with `status: assessed`: it means that the page was reviewed and no revision artifact was retained. It does not mean that no artifact could ever be useful.

### 3.2 Controlled roles

The initial proposed vocabulary is deliberately small:

- `synthesis`: a concise, self-contained explanation of the central question, findings, distinctions and limits;
- `flashcards`: retrieval-practice prompts with answers, stored as a set;
- `revision_sheet`: a compact revision aid, structured for later recall or exam preparation.

Do not add a role merely because a file has a particular extension or title. If a resource performs multiple roles, prefer one primary role per relationship and allow multiple relationships only when each role adds a distinct learner-facing function.

### 3.3 Target discrimination

Each relationship must contain exactly one target form:

- `target.type: section` with `target.id` resolving to an explicit, unique heading anchor in the source page itself;
- `target.type: page` with `target.id` resolving to an existing, published companion page ID;
- `target.type: resource` with `target.id` resolving to an existing, published non-page resource ID.

No bare string target is allowed: the explicit type prevents collisions between page and resource namespaces. A section target is local to the source page and does not create a self-relation in the page graph. The relationship role is independent of target type; a synthesis can be an integrated section, a companion page or a non-page artifact.

## 4. Proposed constraints

These constraints are requirements for a future validator implementation, not current validation behavior.

### 4.1 Structural constraints

- `revision`, when present, is a mapping with only `status`, `resources`, and optional `reason`.
- `status` is one of `not_assessed`, `assessed`, or `not_applicable`.
- `resources` is a list; each entry contains exactly `role` and `target`.
- `role` is one of `synthesis`, `flashcards`, or `revision_sheet`.
- `target` contains exactly `type` and `id`; `type` is `section`, `page` or `resource`.
- Duplicate relationships (same source page, role, target type and target ID) are rejected.
- A `page` target cannot be the source page. A `section` target is expected to belong to the source page and is not a page-graph self-edge.
- `not_assessed` has no relationships. `not_applicable` requires a non-empty reason and has no relationships.
- `assessed` may have an empty list; that is the only state in which an empty list means “reviewed, no retained artifact”.

### 4.2 Referential and lifecycle constraints

For a section target:

- the anchor must be explicitly declared on a heading in the source page;
- the anchor must be unique within that page;
- the section must contain the claimed revision role rather than merely being a generic heading;
- the section link is rendered as the source page URL plus its fragment;
- it does not count as a separate page or non-page resource.

For a page target:

- the page ID must resolve uniquely in the published-page index;
- the target must have `status:published`;
- the target must not be the source page;
- the target language must match the source page language, or be `shared` where the page contract permits it.

For a non-page target:

- the resource ID must resolve uniquely in `data/resources.yml`;
- the resource must be in a published lifecycle state;
- its language must match the source page language, or be language-neutral;
- its location must pass the existing resource-location checks;
- it must not be confused with an implementation module merely because both are non-page resources.

The current resource registry only admits `kind: implementation`. If real revision artifacts require non-page records, the future change must define and validate the smallest additional resource kind(s); it must not silently broaden the current vocabulary.

### 4.3 Bilingual and cardinality constraints

- French and English learning-page counterparts should have semantically equivalent revision coverage.
- Where both language-specific artifacts exist, each page should point to its matching language version.
- A shared resource is permitted only when the artifact is genuinely language-neutral.
- Multiple flashcard sets may be associated with one page if they have distinct, documented scopes; duplicate copies of the same set are not allowed.
- The contract does not require every page to have every role. Coverage policy and eligibility rules belong in the later metric register, not in this relationship schema.

### 4.4 Semantics that must remain separate

Do not encode revision support through:

- `suggested_route`, `hierarchy` or `related`;
- concept `resources` lists;
- resource `referenced_by` alone (that field records which pages reference a non-page resource, not the role of a revision relationship);
- Quarto sidebar position, exercise links or filename conventions;
- source/evidence lineage.

A revision relationship does not prove that the artifact is accurate, complete, pedagogically effective, or up to date. Those require separate review evidence.

## 5. Compatibility audit against current validators

This section records what the current code actually validates on the inspected `main` snapshot. It is not a claim that the proposed contract is already supported.

### 5.1 `site/tools/check_page_metadata.py`

The current page validator:

- parses the `LLM-LAB-PAGE-MAP v1` YAML comment;
- requires `id`, `scope`, `purpose`, `suggested_route`, `hierarchy`, `related` and `tags`;
- validates the known page relation fields, tag dimensions, Quarto `keywords` parity, route/hierarchy reciprocity and acyclicity, bilingual parity, and render-list coverage;
- returns a normalized page record containing only its currently recognized fields.

It does **not** currently parse, normalize, validate or return a `revision` object, and it does not resolve revision anchors against page-body headings. An extra `revision` key is therefore not covered by the current page contract; its presence could be silently ignored by downstream consumers. The proposed relationship is consequently **not validator-compatible as an implemented feature**, even though the current parser does not reject unknown page-map keys.

### 5.2 `site/tools/check_resource_registry.py`

The current resource validator:

- requires `schema_version: 1`;
- rejects unknown resource fields;
- accepts only `kind: implementation`;
- validates bilingual labels/descriptions, BCP 47 language, status, local/external location, published-page references, concept references and optional provenance.

It does not currently admit a revision-resource kind or validate the relationship role of a resource. Do not add revision artifacts to `data/resources.yml` until the resource-kind decision and validator change have been reviewed.

### 5.3 Existing concept registry

`data/concepts.yml` uses `concepts[].resources` for published page IDs. That contract is distinct and must remain unchanged. Adding non-page resource IDs or revision roles to that list would violate the current identity boundary and create ambiguous consumers.

### 5.4 Compatibility conclusion

| Area | Current state | Consequence |
|---|---|---|
| Page-map syntax | YAML comment parser accepts mappings but extracts only known fields | A revision field would currently be ignored, not validated |
| Page relation validation | Only route, hierarchy and related-page relations are checked | No revision target resolution, lifecycle or language checks |
| Non-page resource registry | Strict allow-list; only implementation kind | Revision artifacts are not currently representable as a supported resource kind |
| Concept-to-page associations | Page IDs only | Must not be reused for non-page revision targets |
| Generated learning map | Current page graph and concept graph have distinct projections | Revision relations must not be injected into route/hierarchy edges |

**Decision:** the proposal is compatible with the repository's identity boundaries and can be implemented without changing the meaning of existing fields, but it is **not compatible with the current validators as a functioning, validated feature**. A future implementation must extend the page validator and, only if non-page revision artifacts are confirmed by the inventory, the resource validator. The extension must be additive, explicitly tested, and introduced only after this contract is accepted.

## 6. Migration and rollout boundary

No migration is authorized by this document.

After review and approval:

1. inventory the actual revision artifacts and their page associations on the real Understand and Build corpus;
2. classify each candidate as an integrated section, companion page artifact or non-page resource, and identify its language and role;
3. test the proposed shape against representative existing cases without editing the historical snapshot;
4. define a versioned migration and validator compatibility strategy;
5. implement the validator and focused fixtures before migrating page metadata;
6. migrate only reviewed pages in bounded batches, preserving an auditable before/after report.

The 62-page historical snapshot must remain unchanged until the contract, its constraints, and the migration plan have been explicitly validated.

## 7. Decisions still requiring review

- Is the optional page-map `revision` object the right canonical owner, or should the relation live in a separate relation registry?
- Which explicit heading-anchor convention should identify integrated revision sections, and how should the validator prove that the anchor exists?\n- Should integrated sections be targeted by explicit heading anchors, and what exact heading/block syntax should the validator recognize?
- Are the three proposed roles sufficiently distinct for the artifacts actually present?
- Does the resource registry need a generic `revision` kind, or do concrete non-page artifacts justify narrower kinds?
- What is the precise eligibility rule for `not_applicable`?
- What bilingual-parity exceptions are legitimate for shared or language-neutral resources?
- Should a page have one preferred synthesis/revision sheet per language, or may several coexist with explicit scope?

Until these decisions are settled, this remains an architectural proposal. Do not implement the sample YAML or change any page, registry, schema, validator, route, graph or generated output.
