# Source lineage architecture

**Status:** target architecture; migration is staged and must preserve the current catalogue until the compatibility gate passes.  
**Scope:** scalable identity, inspection history, evidence extraction and traceability between external sources and LLM Lab artifacts.

## 1. Problem and decision

`data/sources.yml` currently combines source identity, bibliographic metadata, classification, scan history and links to project artifacts. It is a useful canonical catalogue, but every new source and every re-inspection increases the size and merge-conflict surface of one file.

Adopt a **distributed YAML authoring model with generated indexes and graph projections**. Keep the repository's existing distinction between sources, extractions, concepts, pages and resources. Do not create a competing concept ontology, page graph or resource registry.

The target layout is:

```text
data/
  sources/
    <source-id>.yml             # one durable identity record per source/version
  source-scans/
    <source-id>/
      <event-id>.yml            # append-only inspection events
  source-lineage/
    <source-id>.yml             # typed edges owned by their originating record
  extractions/
    <source-id>.yml             # atomic, located evidence and editorial disposition
  sources.yml                   # generated compatibility/discovery index
  source-taxonomy.yml           # controlled values
```

The exact directory layout is a contract: do not add a second central edge registry. A generated graph/index may aggregate local records for querying, reports or visualization, but generated output is never hand-authored.

## 2. Ownership and identity

| Information | Canonical owner | Rule |
|---|---|---|
| Source identity and bibliographic metadata | `data/sources/<source-id>.yml` | One stable ID per meaningful source/version |
| Inspection history | `data/source-scans/<source-id>/<event-id>.yml` | Append-only events; never overwrite earlier evidence |
| Source-to-artifact provenance edges | `data/source-lineage/<source-id>.yml` | Edges are typed, directional and owned by the source record |
| Atomic extracted knowledge | `data/extractions/<source-id>.yml` | Every retained item has a locator and evidence boundary |
| Discovery/compatibility index | `data/sources.yml` | Generated projection only after migration; never edit by hand |
| Concepts, domains, pages and resources | Existing canonical registries | Reference stable IDs; do not copy their definitions |

A source identity is not a scan, extraction, claim, concept, page or experiment. These entities have separate IDs and lifecycle states. A source may have many scan events, extraction items and lineage edges.

Deduplicate sources using DOI, normalized canonical URL, repository plus pinned revision, or another stable external identifier—not title similarity alone. Preserve distinct editions, mirrors and revisions when they materially differ; connect them with explicit relations.

## 3. Inspection events are immutable evidence

Each scan event records at least:

- stable event ID and source ID;
- event type and ISO 8601 timestamp;
- inspected source version/revision when available;
- exact inspected scope and locators;
- access method and outcome;
- limitations, inaccessible sections and unresolved rights;
- optional tool/agent and processing version when reproducibility requires it.

A new inspection creates a new event. Correct an erroneous event by adding a superseding/correction event with an explicit link; do not silently rewrite historical evidence. The source-level `scan_status` is a derived summary of the latest relevant inspection, not a replacement for event history. Integration status remains a separate axis.

## 4. Typed lineage edges

Each edge has a stable local ID, relation type, target kind and target ID. Add a precise evidence pointer whenever the relation is based on a particular extracted item.

Initial relation vocabulary:

| Relation | Meaning |
|---|---|
| `derived-from` | Target artifact was produced using this source or item |
| `summarizes` | Target is a summary of the source |
| `translated-from` | Target is a translation |
| `reproduces` | Target reproduces a method, result or artifact |
| `supports` | Source evidence supports a specific claim or concept assertion |
| `contradicts` | Source evidence conflicts with a specific claim |
| `corroborates` | Independent evidence supports a claim already made elsewhere |
| `supersedes` | A source/version replaces an earlier one |
| `cites` | The source explicitly cites another source |

Do not conflate bibliographic citation with scientific corroboration. A source that cites another source is not independent evidence for the cited claim. `supports`, `contradicts` and `corroborates` should target a claim/extraction item where possible, not a whole topic label.

Relations are directional. Do not store reciprocal duplicates unless a consumer explicitly requires them; generate inverse views. Validate relation types, target kinds, target existence and evidence pointers. Apply cycle checks only to relation types whose semantics require acyclicity; do not impose a blanket DAG constraint on the whole graph.

## 5. Example records

Source identity:

```yaml
schema_version: 1
id: example-source
title: "Example article"
canonical_url: "https://example.org/article"
source_type: blog
version: null
revision: null
```

Inspection event:

```yaml
schema_version: 1
id: scan-2026-11-16-001
source_id: example-source
event_type: inspection
occurred_at: "2026-11-16T10:30:00Z"
status: partially-scanned
inspected_scope:
  - "Article body, sections 1–4"
limitations:
  - "Linked experiments were not reproduced"
```

Lineage edges:

```yaml
schema_version: 1
source_id: example-source
relations:
  - id: supports-entropy-definition
    type: supports
    target:
      kind: extraction-item
      source_id: example-source
      id: entropy-definition
    evidence:
      extraction_id: example-source
      item_id: entropy-definition
```

The examples are intentionally minimal. The detailed schemas, allowed values and validation rules must be maintained in `docs/source-catalogue-schema.md` and `data/source-taxonomy.yml`. Do not introduce unvalidated free-form relation names.

## 6. Generated projections and compatibility

Generate `data/sources.yml` deterministically from per-source records during the migration's compatibility phase. It must contain only fields needed by existing consumers and must be clearly marked generated. A generated global lineage JSON/YAML projection may be added only when a real consumer needs it.

The generator must:
- sort records and edges deterministically;
- fail on duplicate IDs, missing targets, invalid schemas or ambiguous source identities;
- preserve stable IDs and all existing metadata;
- never infer scan completeness, licence, evidence confidence or scientific corroboration;
- support a check mode that exits non-zero when committed generated output is stale.

Do not switch writers until all readers, tests, workflows and skills use the new canonical paths. Remove the legacy authoring path only in a later change after compatibility and migration checks pass.

## 7. Migration sequence and acceptance gates

1. **Inventory:** enumerate all readers/writers of `data/sources.yml`, scan history, extraction references and source IDs in docs, tests, workflows and agent skills.
2. **Schema and fixtures:** define schemas for source, scan event and lineage edge; add valid/invalid fixtures and relation semantics.
3. **Migration tool:** transform existing records losslessly, preserving ordering where meaningful, timestamps, scopes, limitations, IDs and null/unknown rights.
4. **Shadow validation:** compare the generated compatibility index against the current catalogue and verify every extraction still resolves.
5. **Consumer migration:** update validators, ingestion tooling, documentation and skills to read/write per-source records.
6. **CI enforcement:** validate local records, referential integrity, deterministic generation and stale projections.
7. **Cutover:** make the distributed records canonical; retain the generated index only for compatibility/discovery. Remove legacy writes only after all consumers are migrated.

Acceptance requires zero lost records, zero unresolved source/extraction IDs, deterministic generated output, passing tests and CI, and documented rollback. A passing structural validator does not prove scientific correctness or rights clearance.

## 8. Operating rules for contributors and agents

- Before adding a source, search existing source IDs, DOI, canonical URL, aliases and pinned repository revisions.
- Create or update only that source's identity file; add each inspection as a new event file.
- Keep extracted claims atomic and source-located in `data/extractions/<source-id>.yml`.
- Add lineage edges only when the relation is meaningful and evidenced; do not create an edge for every mention or keyword overlap.
- Link to existing concept/page/resource IDs; never copy their definitions into source records.
- Distinguish author claims, community comments, editorial interpretation and independent verification.
- Record unknown access, version, licence and evidence states explicitly; never fill gaps by inference.
- Update schemas, validator fixtures, tests, documentation and relevant agent skills together when the contract changes.
