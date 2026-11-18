# Source contract: validation matrix

**Status:** implementation plan for validator v1; this document does not claim that every rule below is enforced today.
**Canonical implementation:** `site/tools/check_source_catalogue.py`.
**Canonical vocabularies:** `data/source-taxonomy.yml`.
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
