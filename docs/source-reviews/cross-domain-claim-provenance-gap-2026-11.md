# Cross-domain claim provenance: current model and gap / Provenance des affirmations transversales

**Review date:** 2026-11-18  
**Status:** architecture review only; no new schema, graph or relation vocabulary introduced.

## Executive finding

LLM Lab already has useful evidence-bearing extraction items and a documented target architecture for source lineage. It does **not yet** have a general, implemented first-class record for a scientific claim that connects objects from different project structures while preserving its scope, assumptions, evidence and counterevidence.

The predictive-coding bridge should therefore remain a documented evidence path until the source-lineage migration and a claim-level representation are designed and validated. Adding a generic concept edge now would lose important semantics.

## 1. Existing structures and what they actually mean

| Structure | Current responsibility | Appropriate use | Not a substitute for |
|---|---|---|---|
| `data/sources.yml` | Source identity, bibliography, classification, scan history and artifact references | Identify a versioned external source and its inspection state | An individual scientific claim |
| `data/extractions/<source-id>.yml` | Atomic, source-located paraphrases with evidence kind, confidence, scope, assumptions, limitations and disposition | Preserve what a particular source says at a particular locator | A cross-source synthesis or proof |
| Extraction `provenance` / `verification` | Distinguish embedded voices (e.g. reader comments) and track their independent verification | Attribute and assess community-derived material | General claim provenance; `verification` is narrowly documented for community-derived items |
| `pedagogical_model.source_graph` | Reconstruct an instructional source's own local teaching model | Preserve source-local nodes, edges, route and inferred learning prerequisites | Canonical concepts or a cross-domain scientific graph |
| `data/concepts.yml` | Canonical concepts and semantic concept relations | Stable ontology of reusable technical concepts | A fully qualified evidence record for a theorem or empirical claim |
| `data/computational-graph.yml` | Computational operations and dataflow | Describe implementation-level computations | Scientific equivalence or source-coding theory |
| `data/resources.yml` and page metadata | Project resources and bilingual page navigation/metadata | Locate explanations and learning assets | Evidence lineage |
| `docs/source-lineage-architecture.md` | Target design for distributed source identities, append-only scans and typed source-to-artifact lineage | Guide a future migration | An already implemented schema or validator |

## 2. Implemented contract versus target architecture

The current validator is `site/tools/check_source_catalogue.py`. Its implemented checks include source/extraction identity, controlled source and extraction types, source scan history, extraction locators, evidence-confidence values, concept/page references, and selected community provenance/verification fields.

The following must not be mistaken for implemented functionality:

- `docs/source-lineage-architecture.md` explicitly describes a **target** distributed model. Per-source identity files, append-only scan-event files and source-lineage files are not yet the canonical authoring format.
- The current source-lineage vocabulary (`supports`, `contradicts`, `corroborates`, `derived-from`, etc.) is an architectural proposal, not a validator-enforced live graph.
- There is no separate, general claim registry in the current canonical data model.
- Current extraction evidence records do not provide a general relation object linking one extraction item to a claim that combines several sources and a computational experiment.
- A citation, shared concept ID, tag or source-local pedagogical edge is not proof of a scientific relation.

The validator's current limitations are documented in `docs/source-catalogue-schema.md`; structural validation also does not assess scientific correctness.

## 3. Minimal future claim representation to evaluate

Do not implement this as a new concept graph. First test whether a claim record can be owned by the existing source-to-knowledge lineage layer and projected into existing concept, page, experiment and computational structures.

A future claim record would need, at minimum:

- stable language-neutral claim ID and concise declarative statement;
- claim class: definition, mathematical identity, theorem, empirical result, implementation mapping, analogy, hypothesis, or pedagogical interpretation;
- subject/object references to existing stable entities (concept, computational node, extraction item, experiment result, page), without copying their definitions;
- relation semantics and direction, with no generic unqualified `related-to`;
- explicit scope: source/data/model family, tokenization, distribution, context, units and evaluation protocol where applicable;
- assumptions and preconditions;
- quantification and modality (exact, asymptotic, expected, approximate, empirical, conditional);
- evidence links to exact extraction item IDs and locators, plus experiment run IDs/commit/configuration when applicable;
- evidence role for each link: establishes, derives, operationalizes, tests, corroborates, qualifies, or contradicts;
- limitations, counterexamples and unresolved counterevidence;
- review status, reviewer decision, and history of superseding corrections.

This is a design checklist, not a schema proposal ready for implementation. The next step is to compare it with the in-progress source-lineage migration, avoid duplicating its relation records, and prototype one predictive-coding claim as a fixture.

## 4. Predictive-coding claim fixture (conceptual only)

Candidate statement:

> For a fixed autoregressive distribution (q) and a specified token sequence, the ideal probabilistic cost is (-\sum_i \log_2 q(x_i\mid x_{<i})) bits; a finite lossless arithmetic-coding implementation can approach this cost only under a compatible shared model and coding protocol, with quantization and framing/termination overhead accounted for separately.

This statement is deliberately qualified. It contains at least three distinguishable claims:
1. a mathematical identity for the ideal negative-log probability cost;
2. a coding-theoretic/algorithmic claim about representing that cost with a decodable arithmetic code;
3. an implementation claim about the actual finite bitstream and its overhead.

Shannon, Rissanen–Langdon and Witten–Neal–Cleary play different evidential roles; they should not be attached as an undifferentiated list of citations. The experiment must supply a fourth kind of evidence: a reproducible implementation and exact round-trip.

## 5. Decisions and next steps

- [x] Inspect the source catalogue and extraction data contract.
- [x] Inspect the consolidated source-catalogue validator and identify implemented checks versus documented gaps.
- [x] Inspect the source-lineage target architecture and its migration gates.
- [x] Distinguish source-local pedagogical graphs from the canonical concept graph and computational graph.
- [ ] Implement/validate the distributed source-lineage migration before treating its proposed files and relations as live.
- [ ] Prototype the claim fixture against existing IDs and source-lineage semantics; check whether a first-class claim is genuinely needed.
- [ ] Add valid/invalid fixtures and tests before adopting a schema.
- [ ] Connect the coder experiment run to its exact configuration, code revision and result artifact.
- [ ] Only after those gates, decide which projections (concept, computational, page, experiment) should expose the claim.

No new graph, relation type, claim schema or canonical edge was created in this review.
