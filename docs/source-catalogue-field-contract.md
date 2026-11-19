# Source catalogue field contract — as built

**Status:** implementation inventory, 2026-11-19  
**Authority:** the executable rules are in `site/tools/check_source_catalogue.py`; the broader authoring contract remains in [source-catalogue-schema.md](source-catalogue-schema.md) and [data/extractions/README.md](../data/extractions/README.md). This page distinguishes CI-enforced structure from documented authoring expectations. It does not silently upgrade recommendations into validation rules.

## 1. Ownership and join keys

| Record | Current canonical location | Identity / join |
|---|---|---|
| Source identity, bibliography, classification, rights and scan summary/history | `data/sources.yml` | `sources[].id` |
| Collection dossier identity | `data/source-collections.yml` | `collections[].id` |
| Atomic extraction | `data/extractions/*.yml` | `source_id` joins to exactly one source ID; filename is not the join key |
| Controlled values | `data/source-taxonomy.yml` | taxonomy lists |
| Domains / concepts / pages | Existing canonical registries and bilingual page-map comments | Stable IDs |

The source record owns collection membership. Extraction records must not repeat it. The distributed source-lineage architecture may move source identity to `data/sources/<source-id>.yml` later; that migration is not implied by this contract inventory.

## 2. Source identity record

| Field | Meaning | CI contract today | Compatibility / review note |
|---|---|---|---|
| `id` | Stable source identity | Required; lowercase kebab-case; unique across catalogue | Do not derive from translated titles or extraction filenames |
| `title` | Display title | Not independently type/emptiness-checked by this validator | Required by the authoring model; preserve source title |
| `creators` | Author/creator names | Not independently validated here | Record only attributable creators |
| `source_type` | Controlled source kind | Required; member of `source_types` | Taxonomy-owned |
| `identifiers` | DOI, arXiv, repository identifiers, etc. | No field-level validation here | Preserve unknowns; identifiers are not interchangeable |
| `canonical_url` | Preferred source URL | No URL resolution or syntax validation here | A stored URL does not establish accessibility |
| `publisher`, `publication_date`, `updated_date`, `language`, `version`, `revision` | Bibliographic/version metadata | No field-level validation here | Unknown date/version remains unknown |
| `licence`, `reuse` | Rights and reuse status | No licence inference or rights validation here | Public accessibility is not permission |
| `scan_status` | Current scan summary | Required; member of `scan_statuses` | Must reflect actual inspected scope |
| `integration_status` | Project integration lifecycle | Required; member of `integration_statuses` | Separate axis from scan status |
| `classification` | Subject classification and facets | If present, must be a mapping; references and tags are checked | `primary_theme` may be null; themes resolve to domains |
| `classification.primary_theme` | Main domain | Optional/null; if non-null, must resolve | Classification, not collection membership |
| `classification.secondary_themes` | Additional domains | Optional list of strings; unique; cannot repeat primary; each resolves | No inference from keywords |
| `classification.tags` | Retrieval facets | Optional list; unique namespaced tags matching controlled syntax | Tags are not concepts or collections |
| `classification.concept_ids` | Canonical concept references | Optional list of strings; each resolves | Do not infer from lexical overlap |
| `scan_history` | Append-only inspection events | Required non-empty list; each event must be a mapping with ISO date/datetime `accessed_at`, controlled `status`; `inspected_scope` and `limitations` are checked as lists of strings | Event contents are evidence boundaries, not a guarantee of completeness |
| `related` | Project artifact associations | Optional mapping (absence defaults to an empty mapping); supplied `pages` and `concepts` must resolve | `audit_records` is documented as navigation, not proof of review |

### Transitional collection contract

The registry `data/source-collections.yml` is required and must have `schema_version: 1` plus a `collections` list. Each entry requires:
- unique kebab-case `id`;
- non-empty `title`;
- non-empty repository-relative `dossier_path`, without absolute paths or `..`, resolving to an existing file;
- `status` exactly `active` or `archived`.

On a source record, `collections` is currently optional for migration compatibility. If supplied, it must be a list of strings, contain no duplicates, and every ID must resolve to the registry. An absent field is not equivalent to an approved empty membership decision; an explicit empty list means no membership is declared. Do not require backfill until identities are approved and source-by-source review is complete.

## 3. Extraction record and item

| Field | Meaning | CI contract today | Compatibility / review note |
|---|---|---|---|
| `schema_version` | Extraction schema version | Required; exactly `1` | |
| `source_id` | Parent source identity | Must resolve to a source ID | The filename is deliberately not used for joining |
| `collections` | Forbidden duplicate membership | Rejected if present | Membership belongs on the canonical source record |
| `items` | Atomic evidence items | Required list | Empty-list policy is not a substitute for useful evidence |
| `items[].id` | Stable item identity | Required; unique across loaded extractions and prefixed by `<source_id>:` | |
| `items[].kind` | Extraction kind | Required; controlled by `extraction_kinds` | |
| `items[].summary` | Concise paraphrase | Required non-empty string | Avoid copied source prose |
| `items[].locator` | Exact inspected anchor | Required mapping; `type` and `value` must be non-empty strings | `label` is optional; no universal type-specific grammar or URL resolution |
| `items[].evidence` | Evidence description | Required mapping; `confidence` must be a controlled value | The validator does not prove the assessment or source support |
| `items[].disposition` | Editorial decision | Optional; if supplied, controlled by `item_dispositions` | Rationale is authoring guidance, not a fully enforced schema |
| `items[].classification` | Item-level refinement | Optional mapping; supplied tags and concept references are checked | Must not silently rewrite source-level classification |
| `items[].provenance` | Attribution where item voice differs from parent source | Optional mapping; controlled `voice`, known `parent_source_id`, valid locator; optional `speaker` must be non-empty; `captured_at` must be ISO date/datetime | Attribution does not verify truth |
| `items[].verification` | Separate assessment of community-derived claims | Optional mapping; controlled status; each source reference must resolve or be HTTP(S) | Verification is not merged into original speaker's claim |
| `items[].candidate_destinations` | Proposed page/concept destinations | If supplied as a mapping, `pages` is checked; a non-mapping value is not explicitly rejected by this validator | A proposal is not an integrated link; concept IDs are not validated in this branch |
| `items[].pedagogical_assessment` | Qualitative editorial assessment | Optional mapping; supplied dimensions require a controlled level and non-empty rationale | Not a scientific confidence score |

The current validator also checks source-local pedagogical models. For source types `blog`, `tutorial`, `course`, and `book-chapter`, the top-level model is required. Its reconstruction, graph nodes/edges, learning outcomes, assumed prerequisites, teaching route and comparison block have structural checks. Source-local graph IDs must be namespaced; edge endpoints must resolve within that graph. These local labels are not canonical concept relations.

## 4. Evidence and epistemic boundaries

Keep these axes distinct:

1. **Source identity/version** — what external object is being referenced.
2. **Inspection event** — what was actually opened or inspected, when, and with what limitations.
3. **Extraction item** — what claim, definition, method, result or limitation was retained, at an exact locator.
4. **Attribution** — who made a statement when the voice is not the source author.
5. **Verification** — whether the statement was independently checked, contradicted or not assessed.
6. **Editorial disposition** — what LLM Lab chooses to do with the item.
7. **Confidence** — the current assessment of evidence strength, not a proof certificate.

A valid YAML record, a non-empty locator, multiple citations, or a high confidence label does not establish that the source supports a claim or that corroborating sources are independent.

## 5. Known enforcement gaps and next validation work

The validator is a structural/referential guard, not a complete semantic schema. The following remain intentionally unclaimed until implemented and tested:

- field-level type/format validation for much bibliographic and rights metadata;
- append-only enforcement and reconciliation between the last scan event and source-level scan summary;
- closed vocabularies for locator types and source-local pedagogical edge types;
- type-specific locator grammars, URL reachability and proof that a locator resolves to the intended passage;
- full field-level validation of evidence basis, scope, assumptions, limitations and provenance semantics;
- epistemic relation and independence semantics for supports/contradicts/corroborates;
- source-version identity and lineage consistency across a future distributed migration;
- exhaustive corpus compatibility for every optional/conditional branch, especially provenance and pedagogical models.

Before tightening any rule, add representative valid, invalid, unknown, legacy and conditional fixtures, then run the validator and tests against the complete corpus. Structural errors and quality warnings must remain separate. Unknown dates, licences, source independence and scientific claims must not become fabricated values to satisfy CI.

## 6. Validation entry points

- Validator: `site/tools/check_source_catalogue.py`
- Validator tests: `tests/test_source_catalogue_validator.py`
- Coverage report: `site/tools/report_source_coverage.py`
- Coverage report tests: `tests/test_source_catalogue_report.py`
- Collection registry: `data/source-collections.yml`
- Collection membership owner: source identity record in `data/sources.yml` during the legacy phase

This is a documentation inventory based on the current validator implementation. It does not claim a local test run, a new CI result, a full-corpus semantic audit, or a scientific reproduction.
