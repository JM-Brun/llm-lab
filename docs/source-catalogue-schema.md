# Source catalogue and extraction data contract

**Status:** initial versioned contract (schema version 1).  
**Canonical source:** this document defines external-source and extraction records.  
**Scope:** research traceability and discovery; not page metadata, the concept graph, or the pedagogical route.

## 1. Ownership and separation

| Data | Canonical owner | Meaning |
|---|---|---|
| External source identity and scan history | `data/sources.yml` | What source exists, what was actually inspected, when, and with what access/reuse constraints |
| Controlled source facets | `data/source-taxonomy.yml` | Allowed source types, levels, contributions, audiences, statuses, extraction kinds, and tag policy |
| Atomic extracted knowledge | `data/extractions/<source-id>.yml` | What a source contributes at a precise locator, with evidence and limitations |
| Knowledge domains | `data/domains.yml` | The six canonical subject domains |
| Scientific concepts and typed relations | `data/concepts.yml` | Durable concepts and semantic relationships |
| Published and implementation resources | `data/resources.yml` and page metadata | Existing resource model; do not overload it with source records |
| Bibliographic presentation | `docs/references.md` | Human-readable annotated bibliography, not proof of scanning |

A source, an extracted item, a concept, a page and a learning resource have different identities. Link them; never collapse them into one registry. YAML is canonical authoring data. JSON-LD remains a generated projection.

## 2. Classification: theme, tags and metadata

Every source has one primary theme once it is selected for substantive inspection. It may have zero or more secondary themes.

- `classification.primary_theme`: exactly one ID from `data/domains.yml`; the best overall subject classification.
- `classification.secondary_themes`: zero or more distinct IDs from the same registry; use only when a second domain is materially covered.
- `classification.tags`: zero or more namespaced, lowercase-kebab-case retrieval facets, such as `topic:attention`, `method:contrastive-learning`, `modality:video`, `application:code-generation`, or `ecosystem:pytorch`.
- `classification.concept_ids`: optional references to existing canonical concepts in `data/concepts.yml`. These are not tags and must not be guessed from keyword overlap.

The primary theme is a classification, not a claim that the source belongs exclusively to that domain. A cross-disciplinary source may have several secondary themes. Do not duplicate the same ID in primary and secondary themes.

### Tags are not concepts

Tags support search and aggregation. They do not assert a scientific definition, semantic relation, prerequisite or ontology membership. Before creating a tag, check whether it duplicates:
- a domain ID (use the domain field);
- a canonical concept ID (use concept_ids);
- a source metadata field (use the typed field);
- an existing tag or its alias (reuse the canonical tag).

Tags are normalized and namespaced to limit collisions. The initial namespaces are `topic`, `method`, `modality`, `application`, and `ecosystem`. Add a namespace only for a demonstrated query use case. Do not create a tag for every named entity or every extracted phrase.

### Metadata are typed fields, not tags

Use explicit fields for information that needs reliable filtering or validation:

| Field | Controlled values / format | Purpose |
|---|---|---|
| `source_type` | `data/source-taxonomy.yml` | Paper, book, blog, documentation, repository, dataset, etc. |
| `language` | BCP 47 language tag | Language of the source/version inspected |
| `technical_level` | Controlled level | Introductory, intermediate, advanced, mixed, unspecified |
| `contribution_types` | Controlled list | Theory, derivation, implementation, experiment, visualization, pedagogy, etc. |
| `audiences` | Controlled list | Learner, practitioner, researcher, educator, maintainer |
| `scan_status` | Controlled lifecycle | What has actually been inspected |
| `integration_status` | Controlled lifecycle | Whether extraction items have been reviewed/integrated |
| `publication_date`, `updated_date`, `accessed_at` | ISO 8601 date/date-time | Source chronology and inspection time |
| `version`, `revision` | Source-native strings | Edition, release, commit, or version inspected |
| `licence` and reuse fields | SPDX identifier when known; otherwise explicit unknown | Rights and reuse constraints |

Do not invent a generic `meta_tags` field. Typed metadata is easier to validate, query and evolve than encoded key-value strings. If a future use case requires an additional facet, add a documented typed field or a controlled tag namespace rather than hiding it in free-form metadata.

## 3. Source record

A source record in `data/sources.yml` uses this shape:

    schema_version: 1
    sources:
      - id: example-attention-paper
        title: "Example paper title"
        creators:
          - "Author One"
        source_type: paper
        identifiers:
          doi: "10.xxxx/example"
        canonical_url: "https://example.org/paper"
        publisher: "Example venue"
        publication_date: "2024-01-15"
        updated_date: null
        language: en
        version: "published version"
        revision: null
        licence:
          identifier: null
          url: null
          status: unknown
        reuse:
          text: link-only
          figures: unknown
          code: unknown
          data: unknown
        classification:
          primary_theme: architectures-mechanisms
          secondary_themes:
            - mathematical-tools-geometry
          tags:
            - topic:attention
            - method:scaled-dot-product
          concept_ids:
            - self-attention
        metadata:
          technical_level: advanced
          contribution_types:
            - theory
            - architecture
          audiences:
            - practitioner
            - researcher
        scan_status: partially-scanned
        integration_status: not-reviewed
        scan_history:
          - accessed_at: "2026-11-04T10:00:00Z"
            status: partially-scanned
            inspected_scope:
              - "Sections 1–3"
              - "Figure 2"
            limitations:
              - "Supplementary material not inspected"
        related:
          pages: []
          concepts:
            - self-attention
          audit_records: []

### Identity and provenance

- Use a stable language-independent kebab-case ID. Never derive identity from a translated title.
- Deduplicate by DOI, normalized canonical URL, or repository plus pinned revision—not title alone.
- Preserve distinct editions, versions, mirrors and aliases when they matter; connect them explicitly.
- Prefer canonical publisher, author, DOI or repository URLs. Record redirects/mirrors as aliases when useful.
- Record exact version, commit or release for mutable sources.
- Use explicit unknown values for rights; an accessible URL or public repository does not imply a licence.

### Scan status and history

The current `scan_status` is a summary. Each inspection event belongs in `scan_history`, with date, status, exact scope and limitations. A source may be rescanned at a later version; do not overwrite the earlier inspection evidence.

Allowed statuses are in `data/source-taxonomy.yml`. A source is `scanned` only when the declared intended scope has been inspected; otherwise use `partially-scanned`. A citation or link alone is `discovered` or `selected`, not scanned.

A source can be classified before scanning. For unclassified discovered records, `primary_theme` may be null; it must be assigned before substantive extraction is marked complete.

## 4. Extraction records and source pedagogical models

Store one file per source in `data/extractions/<source-id>.yml`. Each item is atomic and carries:

For instructional sources (tutorials, blog articles, courses and book chapters), the extraction file also carries a top-level `pedagogical_model`. This is the source's own reconstructed model, not an extension of the canonical LLM Lab concept registry:

- `reconstruction`: completeness status, evidence basis and explicitly inferred elements;
- `source_graph.nodes`: source-local node IDs, kinds, descriptions and source locators; IDs must use a `src-` prefix so they cannot be mistaken for canonical concept IDs;
- `source_graph.edges`: typed source-local relations whose endpoints must resolve to nodes in that same graph;
- `source_graph.interpretation`: an explicit statement that reconstructed relations are interpretations unless the source itself defines them formally;
- `learning_outcomes` and `assumed_prerequisites`: each marked `declared` or `inferred`, with its basis;
- `teaching_route`: ordered source sections, their pedagogical function and teaching moves; order must be unique and contiguous;
- `pedagogical_strengths` and `pedagogical_limits`;
- `comparison`: links to the comparison dossier, canonical graph and route references, decision, and structures deliberately kept separate.

Source-local graph IDs are not canonical concept IDs. Never copy them into `data/concepts.yml` automatically. Do not infer a prerequisite edge from section order, an analogy mapping, or a motivational example. A source graph can contain pedagogical anchors as well as technical entities, but those node kinds must remain distinguishable. If the source is only partially accessible, record a partial reconstruction and its evidence boundary rather than filling gaps by guesswork.


Store one file per source in `data/extractions/<source-id>.yml`. Each item is atomic and carries:

- stable item ID and controlled `kind`;
- concise paraphrased summary, not copied source prose;
- exact locator and locator type;
- optional `provenance` when the item's voice differs from the parent source (for example, a reader comment quoted on an article page): `voice` (`primary-author`, `reader-comment`, `editorial-note`, `maintainer`, or `other`), `speaker` when explicitly available, `parent_source_id`, `locator`, and `captured_at`. This identifies who made the statement and where it appeared; it does not validate the content.
- optional `verification` for community-derived claims: status (`unverified`, `corroborated`, `contradicted`, `not-assessed`), independent source IDs/URLs, and a concise technical assessment. Keep the original comment claim separate from the verifier's interpretation.
- evidence kind, confidence, scope, assumptions and limitations. Evidence confidence uses `evidence_confidence_levels` in `data/source-taxonomy.yml` (`established`, `well-supported`, `context-dependent`, `disputed`, `speculative`, `unverified`). This is distinct from pedagogical assessment levels (`low`, `moderate`, `high`, `uncertain`), defined by `assessment_levels`;
- optional item-level classification, which can refine but not silently overwrite source classification;
- existing canonical concept IDs, if justified;
- candidate page/concept/resource destinations, explicitly marked as proposals;
- optional item-level `disposition` and rationale after Phase B review, using `item_dispositions` in `data/source-taxonomy.yml`. The validator rejects unknown disposition and evidence-confidence values. Source-level `integration_status` is a summary and must not replace item-level decisions.

The extraction taxonomy is in `data/source-taxonomy.yml`. Use the sample and record rules in `data/extractions/README.md`.

### Optional pedagogical assessment

An extraction item may include a compact perspective profile when the contribution is pedagogical or intended for later synthesis:

    pedagogical_profile:
      learner_question: "What learner difficulty does this explanation address?"
      explanatory_lens: linguistic
      teaching_form: [worked-example, mental-model]
      abstraction_level: introductory
      prerequisites: [tokenization, contextualized-representation]
      distinctive_value: "Shows a cross-position dependency not illustrated by the existing lexical-ambiguity example."
      limitations:
        - "Illustrative motivation; not evidence that one attention head resolves coreference."

Use concise source-grounded values. The lens and teaching-form values are descriptive facets, not concept IDs or graph relations. Do not invent a unique perspective when sources share one. This field is optional for general factual or technical items, but expected for newly extracted pedagogical contributions that are candidates for cross-source synthesis.

An extraction item may also include:

    pedagogical_assessment:
      novelty: {level: low, rationale: "The mechanism is already explained in the project."}
      complementarity: {level: high, rationale: "The source offers a distinct learner-facing mental model."}
      pedagogical_value: {level: moderate, rationale: "It may help learners who struggle with the formal role distinction."}
      applicability: {level: moderate, rationale: "Could fit as an optional note in the existing lesson."}
      redundancy: {level: low, rationale: "The analogy illuminates a different aspect from the canonical example."}
      evidence_quality: {level: moderate, rationale: "The explanation is inspectable but is a secondary tutorial."}

Allowed levels are low, moderate, high and uncertain. Every dimension must have a rationale; use uncertain when the evidence or comparison is insufficient. These are independent editorial judgements, not numerical scores and not a ranking. The assessment is optional for older records, but expected for newly extracted pedagogical contributions (analogy, mental-model, teaching-sequence, question, misconception, page-improvement) and any item proposed as a learning improvement.

An extraction item may carry a different primary theme from its source only when its specific contribution genuinely belongs elsewhere. This does not reclassify the source. Item-level tags should be sparse and more specific than source-level tags where possible.

## 5. Inheritance and query behavior

For discovery, an item may inherit the source's primary/secondary themes and source-level tags when it has no item-level override. Do not copy inherited values into every item by default; this creates duplication and drift.

When displaying or filtering:
1. use item-level classification when explicitly present;
2. otherwise fall back to source classification;
3. keep source metadata (language, source type, version, scan status) distinct from item evidence and integration disposition;
4. never infer concept membership or semantic graph edges from tags.

## 6. Historical backfill and bibliography reconciliation

Backfill in evidence-aware passes:
1. collect source mentions from references, source audits, page citations, asset registers, experiment records, notebooks, code and issue/PR discussions;
2. normalize identity and deduplicate;
3. classify evidence of use: scanned, partially scanned, linked/cited only, recommended/discovered, inaccessible, or unknown;
4. record the exact known inspected scope and dates; do not infer them from a citation;
5. add extraction items only where an auditable locator and useful content are available;
6. report counts, duplicates, missing provenance/licences and unresolved statuses.

Keep `docs/references.md` as a readable bibliography. It may link to source IDs, but must not become a second canonical machine-readable catalogue. A source catalogue entry does not require a published page change.

## 7. Validation and evolution

The consolidated initial validator is `site/tools/check_source_catalogue.py`; it runs in CI after the YAML validation dependency is installed. Its current scope is deliberately explicit:

- YAML syntax and schema version for source, taxonomy, domain, concept and extraction files;
- unique source and extraction-item IDs, and extraction-to-source referential integrity;
- controlled source types, scan/integration statuses, extraction kinds and item dispositions;
- valid domain, concept and bilingual page references;
- namespaced tag syntax and duplicate detection;
- scan-history dates, statuses, inspected scopes and limitations;
- exact item locators and supported evidence-confidence values;
- community-item voice, parent-source provenance, capture date, verification status and independent source references.
- instructional-source pedagogical-model status, source-local node identity, edge endpoint integrity, explicit graph interpretation, declared/inferred outcomes and prerequisites, contiguous teaching-route order, strengths/limits and comparison pointers.

The initial validator does **not yet** validate BCP 47 language tags, publication/version chronology, licence identifiers or rights/status consistency, alias resolution, resource references, all optional item-level pedagogical fields, or the scientific validity of reconstructed source-graph relations. Keep these as explicit follow-up work; extend the consolidated validator and its tests rather than creating one script per data file. Do not treat a passing initial validator as proof that rights or scientific claims are valid.

Source scan status, source integration status and item disposition are independent lifecycle axes: partial inspection can coexist with accepted item integrations, and a fully scanned source can produce no learner-facing change. Never infer scan completeness from integration status.

Any schema change must update this contract, examples, taxonomy, validator fixtures, tests, skills and migration notes together. Keep JSON-LD and visualizations as derived projections; never hand-edit generated output.

## 8. Standards alignment

Use stable URI-like identifiers and ISO 8601 dates. Use BCP 47 for language tags and SPDX identifiers only when the licence is known and correctly identified. The source catalogue can later be projected to Schema.org `CreativeWork` and PROV-O where useful, but do not introduce a second RDF store or an ontology toolchain for the current static project. SKOS domains/concepts remain owned by their existing registries; source tags are not a substitute for SKOS concepts.
