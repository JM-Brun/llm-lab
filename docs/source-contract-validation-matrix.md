# Source contract: validation matrix

**Status:** implementation plan for validator v1; this document does not claim that every rule below is enforced today.
**Canonical implementation:** `site/tools/check_source_catalogue.py`.
**Canonical vocabularies:** `data/source-taxonomy.yml` and `data/source-collections.yml`.
**Parent contract:** [Source catalogue and extraction data contract](source-catalogue-schema.md).
**Related architecture:** [Source lineage architecture](source-lineage-architecture.md).

This matrix separates structural invariants from evidence-dependent editorial requirements. It is intended to guide incremental validator changes without turning unknown metadata into false errors or breaking historical records.

## Severity model

- **Error:** malformed data, broken identity/reference, invalid controlled value, or a record that cannot be interpreted safely. CI should fail.
- **Warning/report:** suspicious inconsistency or missing information that may be legitimate for a historical, partial, inaccessible, or mutable source. CI should report it, but should not silently reject the record.
- **Editorial gate:** a human decision requiring evidence or review. A structural validator must not infer the answer.

A missing value is not automatically an error. Rules marked conditional apply only when the field or relevant claim is present, or when the record declares a state that makes the field necessary.

## Validation matrix

| Area | Field / invariant | Condition | Severity | Current v1 coverage | Required fixture |
|---|---|---|---|---|---|
| Source identity | `id` stable kebab-case and unique | Every source | Error | Implemented | valid ID; malformed ID; duplicate |
| Source identity | `source_type`, scan and integration states | Every source | Error | Implemented | each allowed value; unknown value |
| Source collections | Registry schema, unique stable IDs, title, dossier path and lifecycle status | Registry required; every declared collection | Error | Implemented in PR #1313; CI pending | valid registry; duplicate/invalid ID; missing dossier; invalid status |
| Source collections | Optional source `collections` list, unique IDs and registry references | When field is present; legacy absence remains valid | Error | Implemented in PR #1313; CI pending | absent, empty, single/multiple memberships, unknown ID, duplicate ID, malformed list |
| Extraction collections | No duplicated collection membership; resolve through `source_id` only | Every extraction | Error | Implemented in PR #1313; CI pending | no extraction field; duplicate field rejected; source-ID join |
| Bibliography | `title` non-empty; `creators` list of non-empty strings | When present; required for substantive sources after policy decision | Warning initially | Not fully enforced | absent, empty, malformed, multiple creators |
| Bibliography | `canonical_url` absolute HTTP(S); DOI/other identifiers normalized | When present | Error for malformed supplied value; absence is not universally fatal | Not enforced | HTTP, HTTPS, relative URL, malformed DOI |
| Bibliography | `language` BCP 47 | When present | Error for malformed supplied value; unknown remains explicit | Not enforced | en, fr, zh-Hans, invalid tag, null |
| Bibliography | publication/update dates and chronology | When present | Error for unparsable date; warning for implausible ordering | Date parser currently used for scan events only | date, datetime, null, invalid, update-before-publication |
| Versioning | `version` and `revision` | Mutable sources (repositories, living docs, datasets) | Warning if absent; editorial gate for reproducibility | Not enforced | pinned commit, release tag, mutable main, null |
| Rights | licence identifier, URL, status | When rights metadata supplied | Error for malformed structure/invalid status; unknown is valid | Not enforced | SPDX-like ID, URL, unknown, conflicting status |
| Rights | reuse permissions for text/figures/code/data | Every declared reuse decision | Error for unknown controlled value; editorial gate for legal interpretation | Not enforced | link-only, permitted, unknown, unsupported |
| Classification | primary/secondary themes and concept references | When supplied; selected/substantive sources require a primary theme by policy | Error for unresolved IDs, duplicates and overlap | Implemented for supplied values | valid, unknown ID, duplicate, overlap, null |
| Tags | namespaced syntax and uniqueness | When supplied | Error | Implemented | valid namespaces, malformed, duplicate |
| Scan history | event date, status, scope, limitations | Every event | Error for malformed date/status/list shape; warning if scope is empty | Date/status/list shape implemented; non-empty scope policy not enforced | valid, empty scope, invalid date/status |
| Scan summary | source `scan_status` agrees with latest relevant event | When history exists | Warning/report; never rewrite history automatically | Report detects mismatches separately | aligned, stale summary, superseding event |
| Extraction identity | source reference resolves; item ID is unique and source-prefixed | Every extraction/item | Error | Implemented | valid, unknown source, duplicate ID, wrong prefix |
| Extraction content | kind controlled; summary non-empty | Every item | Error | Implemented | valid, unknown kind, blank summary |
| Locator | type-specific syntax and stable resolution | Every retained evidence item | Error when malformed; editorial gate when locator cannot be externally resolved | Only type/value presence is checked | URL, section, PDF page, figure, timestamp, commit/path/line, dataset field; malformed values |
| Evidence | kind, confidence, scope, assumptions, limitations | Every item; exact requiredness depends on item kind | Error for malformed supplied structures/unknown confidence; policy decision for omissions | Partial controlled-value checks | each confidence, missing scope, malformed lists |
| Provenance | voice, parent source, locator, capture date | When item represents a voice distinct from parent source | Error | Implemented | valid reader comment; missing parent; invalid locator/date |
| Verification | status, independent references and assessment | When a claim is explicitly checked | Error for invalid status/reference shape; editorial gate for independence and adequacy | Status and reference syntax partially implemented | internal source ID, URL, unknown ID, self-reference, no evidence |
| Disposition | controlled value and rationale | When a disposition is set | Error for unknown value; warning when rationale absent | Value checked; rationale policy not enforced | valid, unknown, missing rationale |
| Pedagogical assessment | separate qualitative levels and per-dimension rationale | New pedagogical contribution or proposed learning improvement | Error for malformed supplied assessment; editorial gate for whether required | Implemented for supplied assessment | valid, wrong scale, missing rationale, uncertain |
| Pedagogical source graph | local IDs, edge endpoints, declared/inferred status, route order | Instructional sources | Error for structural defects; editorial gate for scientific validity | Structural subset implemented | unknown endpoint, duplicate local ID, inferred edge, non-contiguous route |
| Destinations | page/concept/resource IDs resolve | When supplied | Error for broken references; candidate destinations remain proposals | Pages/concepts partially implemented; resource refs incomplete | valid and unknown IDs |
| Lineage | relation type, direction, target and evidence pointer | Once distributed lineage records are introduced | Error | Not implemented in v1 | supported, contradicts, cites, missing target, missing extraction pointer |

## Non-negotiable interpretation rules

1. **Unknown is data, not failure.** Unknown publication dates, licences, revisions or access states must remain explicit and must not be guessed.
2. **A link is not an inspection.** Bibliographic presence does not justify a scanned status, extraction, corroboration or licence claim.
3. **A source citation is not independent corroboration.** Independence and claim-level support require human/evidence review.
4. **A locator is not merely a non-empty string.** Its grammar depends on its type; implement type-specific validation only after inventorying actual locator types in the corpus.
5. **Do not force one universal schema onto unlike sources.** A paper page, repository commit, video timestamp and dataset field need different locator rules.
6. **Do not turn warnings into hard errors without a measured migration plan.** First report the affected records, classify legitimate exceptions, then migrate with fixtures and a compatibility gate.
7. **Keep editorial and scientific judgement outside structural validation.** A valid graph shape does not prove a relation, causal claim, or pedagogical interpretation is true.

## Incremental implementation sequence

1. Inventory actual field shapes and locator types in all extraction records; publish counts and representative examples.
2. Add pure validators for URL, BCP 47, dates, licence/reuse enums and type-specific locators. Unit-test each without coupling tests to the live corpus.
3. Add conditional cross-field rules (for example, a verified licence requires an identifier or evidence URL; a pinned repository revision requires a stable revision locator).
4. Add warning/report output for source-summary versus latest scan event, missing extraction coverage, unknown rights and unpinned mutable sources.
5. Run the validator against the full corpus in report-only mode; classify every new warning before promoting any rule to error.
6. Add migration fixtures for legacy nulls, partial scans, inaccessible sources, community provenance and instructional source graphs.
7. Only then consider a schema-version increment. Keep v1 readable until migration and generated projections are verified.

## Scale and performance constraints

- Validate each changed source/extraction locally for fast feedback, but retain periodic full-corpus validation for global uniqueness and referential integrity.
- Build ID sets and indexes once per validation run; avoid rescanning page trees or reparsing registries per item.
- Keep deterministic ordering in reports and generated projections.
- Measure wall time, peak memory and error counts against synthetic fixtures at increasing source/item counts before selecting incremental caches or a database.
- Any cache must be invalidated by all relevant registry and taxonomy inputs; stale validation is worse than a slower full check.
- Do not shard canonical IDs or relation vocabularies by domain. Stable global identity is essential for cross-domain discovery.

## Acceptance criteria for the validator work

- Every row above is marked implemented, deliberately deferred, or not applicable with a reason.
- Tests cover valid, invalid, null/unknown, conditional and legacy cases for every implemented rule.
- The current corpus passes without silently changing source status, confidence, rights or scientific claims.
- Report-only warnings are reviewed and documented before severity is raised.
- Full-corpus and synthetic scale measurements are recorded; no scalability claim is based only on schema design.

## As-built contract snapshot — 2026-11-18

**Audited source revision:** `b32663df12166ad0bbffaff7e948a79c551a429c` (`main`).  
**Implementation:** `site/tools/check_source_catalogue.py`.  
**Direct regression tests:** `tests/test_source_catalogue_validator.py`.  
**Purpose:** distinguish rules that the current validator actually enforces from the broader v1 design above. This is a code-and-fixture audit, not a claim that every historical record has been semantically reviewed.

### Current enforcement by record family

**Collection-contract implementation under review:** PR #1313 adds the three collection-registry and source-membership checks below. Until CI passes on the final PR head and review is complete, these checks are implementation-in-review, not an accepted baseline.

| Record family | Field / condition | Current enforced behavior | Direct regression evidence | Not established by this check |
|---|---|---|---|---|
| Catalogue envelope | Schema versions for taxonomy, domains, concepts, sources and extraction files | Exact supported versions are required | Existing validator tests and full-catalogue CI | Semantic compatibility of every future schema revision |
| Source identity | Source `id` | Stable kebab-case syntax and uniqueness | Duplicate source-ID test; other ID behavior is implemented | Identity equivalence across mirrors, editions or aliases |
| Source classification | `source_type`, `scan_status`, `integration_status` | Values must occur in the taxonomy | Minimal valid source fixture; malformed status fixture | Whether the chosen status truthfully describes the inspected source |
| Source classification | `classification.primary_theme`, `secondary_themes`, `concept_ids` | Supplied IDs must resolve; secondary themes cannot duplicate or overlap primary | Unknown domain/concept references test | Whether the classification is substantively appropriate |
| Source tags | `classification.tags` | Supplied tags must be unique and match the five allowed namespaces and kebab-case syntax | Duplicate and malformed source-tag tests | Retrieval usefulness or semantic correctness of a tag |
| Source inspection | `scan_history` | At least one event; each event must be a mapping with parseable ISO date/date-time, known status, and string-list scope/limitations | Invalid date/status test; empty-history test | Scope completeness, accuracy of the scan summary, or truth of the reported inspection |
| Source relationships | `related.pages`, `related.concepts` | Supplied page and concept IDs must resolve; `related` must be a mapping | Unknown page/concept references test | Whether a page genuinely uses or is supported by the source |
| Bibliography and rights | `title`, `creators`, `identifiers`, `canonical_url`, `publisher`, `publication_date`, `updated_date`, `language`, `version`, `revision`, `licence`, `reuse`, `metadata` | No comprehensive field-level validation in the current validator | No direct fixture coverage | URL validity, BCP 47 conformance, chronology, SPDX correctness, reuse permission or rights interpretation |
| Extraction envelope | `source_id`, `items` | Source reference must resolve; items must be a list | Valid extraction fixture and unknown source reference behavior in implementation | Whether every source ought to have an extraction |
| Extraction item | `id`, `kind`, `summary` | ID must be unique and prefixed by source ID; kind must be in taxonomy; summary must be non-empty text | Duplicate ID, wrong prefix and valid extraction fixtures | Atomicity or fidelity of the paraphrase |
| Extraction locator | `locator.type`, `locator.value` | Mapping with non-empty string `type` and `value`; no type-specific grammar | Missing-field and malformed-type/value fixtures; corpus inventory in `docs/extraction-locator-inventory.md` | URL resolution, source inspection, precision, or claim support |
| Evidence | `evidence.confidence` | Evidence must be a mapping and confidence must be a controlled value | Unknown confidence test | Adequacy of evidence, truth of claim, or calibration of confidence |
| Item classification | `classification` | Optional mapping; supplied primary domain, concept IDs and tags are checked | Extraction tag duplicate test; source-level reference tests cover adjacent logic | Whether item classification should override or inherit source classification in a given case |
| Item disposition | `disposition` | Optional; if present, must be a taxonomy value | Valid and invalid disposition tests | Requiredness of a disposition or rationale quality |
| Pedagogical assessment | `pedagogical_assessment` | Optional mapping; each supplied supported dimension requires a known level and non-empty rationale | Valid, invalid-level and empty-rationale tests | Whether assessment is required for a particular contribution; quality of the human judgement |
| Community provenance | `provenance` | Optional mapping; checks voice, resolvable parent source ID, locator mapping with non-empty string `type`/`value`, capture date, and non-empty `speaker` when supplied | Valid/invalid provenance tests plus malformed locator/speaker fixtures | Speaker identity/authenticity or correctness of the quoted statement; locator resolution |
| Verification | `verification` | Optional mapping; checks status, sources list shape, and that each reference is a known source ID or begins with HTTP(S) | Valid and invalid verification tests | URL validity/retrieval, independence, self-corroboration, evidence quality or actual claim support |
| Candidate destinations | `candidate_destinations.pages` | Supplied page IDs must resolve | Implemented; no dedicated focused fixture identified in this batch | Whether the destination is editorially appropriate |
| Pedagogical model | Required for source types `blog`, `tutorial`, `course`, `book-chapter`; optional for other source types | Structural checks for reconstruction, source-local graph nodes/edges, interpretation, declared/inferred outcomes and prerequisites, route order, strengths/limits and comparison fields | Existing corpus validation; focused positive/negative fixtures are not yet comprehensive | Whether the reconstructed graph, teaching sequence or inferred prerequisite is scientifically/pedagogically correct |

### Important implementation details and boundaries

- The validator requires extraction locator `type` and `value` to be non-empty strings. It deliberately does not impose type-specific grammar. The full-corpus inventory found 432 mapping locators with non-empty required fields; it did not establish URL resolution or claim support.
- The locator inventory observed 14 types. The 354 `section` values are heterogeneous; do not impose a universal grammar or make `label` mandatory. Unknown types and extra keys remain report-only.
- `scan_history` must be a non-empty list, but an event's `inspected_scope` and `limitations` may currently be empty lists. A syntactically valid event does not prove that its stated scope was actually inspected.
- Source bibliography, language, version and rights fields are represented in canonical records but are not comprehensively validated. Explicit `null` and `unknown` values are legitimate and must not be converted to fabricated metadata.
- A provenance locator follows the same minimal structural contract as an extraction locator: mapping plus non-empty string `type` and `value`. This still does not establish that the locator resolves.
- Verification references beginning with `http://` or `https://` pass the current syntactic prefix check. The validator does not fetch them or establish that they identify an independent source. A source ID in the list can refer to the parent source itself; independence is not checked.
- The validator checks graph endpoint identity and route numbering, not semantic validity of source-local relations or truth of reconstructed learning outcomes.
- The inventory report's timestamp classification is heuristic. It describes observed value shapes and does not validate locator resolution.

### Regression coverage present on the audited revision

The direct test module includes temporary-corpus cases for:
- minimal source and unknown optional metadata accepted;
- valid extraction accepted;
- malformed scan-history date/status and empty scan history rejected;
- missing locator and unknown evidence confidence rejected;
- instructional source missing its pedagogical model rejected;
- duplicate source IDs and extraction-item IDs rejected;
- extraction item ID with the wrong source prefix rejected;
- unresolved source domain, concept and page references rejected;
- duplicate and malformed source tags rejected;
- valid and invalid item dispositions and pedagogical assessments;
- duplicate extraction tags;
- non-string extraction locator fields and empty provenance locator/speaker values;
- valid and invalid community provenance and verification structures.

This list describes direct fixtures in the test module, not exhaustive coverage of every row in the matrix. In particular, there are not yet focused fixtures for malformed bibliography/rights fields, URL semantics, provenance locator internals, verification URL validity or independence, every pedagogical-model branch, and all conditional/legacy combinations.

### Next bounded work

1. Add this as-built matrix to review and keep it synchronized with validator changes.
2. Audit the actual source/extraction corpus for the unvalidated bibliography, rights, language and version fields before proposing constraints. Preserve unknowns and distinguish malformed supplied values from absent values.
3. Add isolated fixtures only for rules whose semantics are clear and whose compatibility has been checked against the corpus. Prefer report-only diagnostics for uncertain historical patterns.
4. Review scan-summary/history consistency as a report first; do not rewrite append-only inspection history.
5. Keep locator resolution, source inspection, claim support and independent corroboration as separate evidence questions.
6. Add focused pedagogical-model fixtures only after checking representative instructional records and distinguishing declared source content from project reconstruction.

This focused follow-up strengthens only the structural locator contract (non-empty string `type`/`value`, plus non-empty optional provenance `speaker`). It does not add type-specific locator grammars, fetch URLs, change canonical records/taxonomy, or alter CI policy.

