# External-source to learning-system integration workflow

**Status:** normative project workflow · **Version:** 1.0 · **Last reviewed:** 2026-11-04  
**Related collection:** [Q/K/V source collection](../source-reviews/qkv-source-collection.md)

## 1. Objective

Convert external learning resources into a traceable, critically assessed contribution to LLM Lab. The goal is not to summarize every source or maximize page edits. It is to identify what the source adds to the project's knowledge, pedagogy, experimentation, implementation or visual communication, then integrate only what improves the learning system.

The unit of work is the **atomic contribution**, not the article.

## 2. Keep six models separate

Never collapse these structures into one graph or one sequence:

1. **Source record:** provenance, version, access method, rights and scan history.
2. **Source knowledge extraction:** atomic claims, definitions, equations, examples, code and evidence.
3. **Source-local semantic/process graph:** concepts and computational relations reconstructed from the source.
4. **Source-local pedagogical route:** the source's order, motivations, prerequisites and learning outcomes.
5. **Canonical project knowledge graph:** stable concepts and typed semantic relations shared across LLM Lab.
6. **Canonical learning routes and site navigation:** intended learner progression, page ownership, optional depth and implementation route.

A seventh cross-cutting record tracks visual assets and reuse rights. The source's teaching order is not automatically a prerequisite graph; a semantic relation is not automatically a pedagogical dependency.

## 3. Workflow stages and gates

### Stage 0 — Register and scope

Create or update a canonical source entry before extraction.

Capture:
- stable source ID and canonical URL;
- title, author/creator, publisher, source type, language;
- publication/update date and version/revision where verifiable;
- licence and reuse status (unknown unless verified);
- topic tags and candidate concept IDs;
- intended audience and technical level;
- related canonical pages, concepts and review records.

Record retrieval method and access date. Define separate scan components: author text, figures/media, code/data, comments, outbound links, metadata, and rights. Use `not-inspected`, `unavailable` or `unknown` rather than silently treating inaccessible material as absent.

**Gate:** a source is registered and its scope/limitations are explicit. Do not claim a complete scan.

### Stage 1 — Scan and preserve provenance

Inspect the canonical source first. If direct access fails, use an author-controlled mirror or indexed result only as a clearly identified fallback.

For each access event record:
- exact component inspected;
- retrieval route (direct page, API, indexed text, mirror, repository);
- whether content was directly visible or reconstructed;
- content coverage and missing sections;
- discrepancies between snapshots;
- comments and linked materials separately;
- media placeholders versus actual image bytes;
- unresolved rights and metadata.

Do not merge comments into author-authored prose. Do not infer missing content from snippets. Keep historical scan events; append corrections rather than erasing provenance.

**Gate:** evidence boundary is explicit and reproducible enough for the next reviewer.

### Stage 2 — Extract atomic contributions

Create one extraction item per independently assessable contribution. Suitable item types include:
- definition or distinction;
- equation, derivation or assumption;
- computational step or data-flow relation;
- analogy, example or counterexample;
- misconception or qualification;
- experiment, benchmark or implementation pattern;
- visualization or accessibility feature;
- learning outcome, prerequisite or teaching move;
- community suggestion (with separate provenance).

Each item should include:
- stable source-scoped ID;
- concise paraphrase, not copied prose;
- source locator (section, heading, timestamp, code symbol, comment);
- evidence basis and confidence;
- technical assessment and assumptions;
- pedagogical function and target learner difficulty;
- novelty, complementarity and likely learner value;
- candidate canonical concept IDs;
- disposition and rationale.

Use confidence labels consistently:
- **High:** directly supported by an explicit source passage/equation and technically checked.
- **Medium:** source supports the interpretation but assumptions or scope need qualification.
- **Low:** inferred, ambiguous, weakly evidenced or not independently checked.

Learning outcomes, prerequisites, graph edges and teaching intent not explicitly stated by the author must be marked **inferred**.

**Gate:** all meaningful source contributions are represented, including redundant and rejected items. Do not extract only the items that are convenient to integrate.

### Stage 3 — Reconstruct the source's pedagogical model

Build a source-local graph with typed nodes and relations. Separate:
- domain concepts and representations;
- parameters and computational objects;
- operations and intermediate results;
- constraints/masks;
- examples and analogies;
- applications and claims.

Then reconstruct the source's teaching route:
- opening motivation;
- conceptual introduction;
- formalization;
- worked example;
- practice or checks;
- generalization/application;
- conclusion.

Infer prerequisites and outcomes conservatively. Record omissions: e.g. no tensor shapes, no derivation, no exercises, no implementation, no error analysis.

Do not claim that the source author supplied a formal graph or curriculum unless they actually did.

**Gate:** the source can be compared as both a knowledge model and a teaching experience.

### Stage 4 — Differential comparison against LLM Lab

Inspect the actual canonical artifacts, not only memory or earlier reviews:
- bilingual page content and metadata;
- canonical concept registry and typed relations;
- guided route and learning-path documentation;
- navigation and cross-links;
- exercises, quizzes and workbenches;
- Build implementation, tests and benchmarks;
- visual asset register and citations.

Compare at three scales:
1. **Concept-level:** is the information or relation missing, imprecise or misleading?
2. **Page-level:** does the contribution solve a learner difficulty better than the existing explanation?
3. **Curriculum-level:** does it change prerequisites, order, depth, optional branches or implementation hand-off?

Also compare the source route with the corresponding *local page route* and the *whole project route*. Do not compare a six-section article directly with a site navigation list without a route crosswalk.

For each candidate, answer:
- Is it genuinely new, or merely differently worded?
- Is it complementary even if not novel?
- Does it improve intuition, precision, transfer, practice or implementation?
- Does it expose a missing canonical concept/edge?
- Does it warrant a page edit, cross-link, optional deep dive, exercise, figure or Build task?
- Would integration create duplication, overload or a false implication?
- Is the source sufficiently reliable for the intended use?

**Gate:** each item has an explicit disposition, including a reason for no change.

### Stage 5 — Make bounded integration decisions

Use these dispositions:

| Disposition | Meaning | Typical action |
|---|---|---|
| `integrate` | Clear gap and meaningful benefit | Edit canonical page, graph, exercise, figure or implementation |
| `integrate-by-reference` | Useful alternative but not worth duplicating | Link as optional perspective; preserve extraction |
| `already-covered` | Canonical treatment is equal or stronger | No page change; point to canonical location |
| `defer` | Potential value, insufficient evidence or wrong timing | Add scoped follow-up with trigger/owner if appropriate |
| `reject` | Incorrect, unsupported, misleading or low value | Preserve rejection rationale; do not integrate |

A source may produce zero page edits and still improve the concept graph, evidence quality, source map or future research queue. Conversely, a small example may justify one targeted edit even if most of the article is redundant.

Do not add concepts just to reflect every noun in a source. Add canonical nodes only for durable, reusable concepts that the project itself needs to distinguish. Do not change the curriculum route unless there is evidence of a better learning dependency or cognitive progression.

### Stage 6 — Implement and preserve bilingual parity

Implement the smallest coherent set of changes:
- update canonical concept IDs and typed relations only when justified;
- update both EN and FR pages for learner-facing content;
- preserve page ownership (e.g. Q/K/V roles on Q/K/V page; score/softmax/aggregation derivation on attention page);
- link to adjacent lessons instead of copying their explanations;
- keep optional perspectives visibly optional;
- update exercises, visual asset records, references and navigation only when warranted;
- keep Build work separate from conceptual explanation unless the user explicitly wants implementation.

Never remove existing knowledge during restructuring without a traceable migration. Avoid speculative numerical claims and unsupported empirical language.

### Stage 7 — Validate

Validation should match the changed artifacts:
- YAML/schema validation for source catalogue and extraction;
- concept registry IDs, relations and generated projections;
- page metadata, bilingual parity and local links;
- Quarto render in both languages;
- lint, type checks and tests for changed code;
- accessibility, figure attribution and rights checks;
- visual inspection of rendered pages and any third-party media;
- review of claims against primary papers or official technical documentation.

Record actual CI run status and commit/PR head. A passing early run does not validate later commits. API write success is not content or build validation.

### Stage 8 — Publish a source comparison and update the collection index

For a topic with multiple sources, maintain:
- one source-specific extraction per source;
- one source-specific review per source;
- one living cross-source comparison dossier;
- one concise collection index;
- one canonical concept graph and learner route.

The cross-source matrix should compare the same dimensions across sources, identify convergence versus genuine complementarity, and state what LLM Lab already does better. Preserve disagreement rather than averaging it away. Distinguish shared repetition from independent corroboration.

When adding another source, append a new column/row and revisit prior synthesis only where the new evidence changes a decision. Do not rewrite old source provenance or attribute community comments to article authors.

## 4. Contribution evaluation rubric

Assess each atomic item independently. Do not reduce the decision to a single novelty score.

| Dimension | Guiding question |
|---|---|
| Technical validity | Is it correct under stated assumptions? |
| Evidence strength | Is it explicit, reproducible and independently corroborated where needed? |
| Novelty | Is a concept, relation, distinction or method absent from the project? |
| Complementarity | Does it explain an existing concept from a meaningfully different angle? |
| Pedagogical value | Does it reduce a specific learner difficulty or improve transfer? |
| Mathematical value | Does it add a derivation, assumptions, counterexample or precision? |
| Experimental value | Does it enable a test, benchmark, visualization or falsifiable investigation? |
| Implementation value | Does it add useful tensor, code, performance or engineering insight? |
| Visual value | Does it improve explanatory quality, accessibility or interaction? |
| Integration cost | Does the benefit justify page complexity, maintenance and duplication? |

Use qualitative ratings (high / medium / low / unknown) with short rationales. Keep **novelty** and **complementarity** separate: a repeated idea may still be pedagogically valuable, and a novel detail may be too weak to publish.

## 5. Source status is multidimensional

Do not use a single `complete` flag to imply every component is complete. At minimum track:
- author-text reconstruction;
- figures/media inspection;
- code/data inspection;
- comments/community contributions;
- linked resources;
- metadata/version verification;
- rights/reuse verification;
- technical validation;
- integration state.

The overall scan status should remain partial while any in-scope component is unresolved. The extraction can say author-text reconstruction is complete while the source remains partially scanned.

## 6. Required deliverables for a multi-source topic

- [ ] Canonical source catalogue entries with scan history
- [ ] One structured extraction per source
- [ ] One source-specific technical/pedagogical review per source
- [ ] Source-local graph and teaching route per source (where applicable)
- [ ] Cross-source comparison matrix and route crosswalk
- [ ] Explicit integration/rejection/defer decisions
- [ ] Updated canonical graph/pages/routes only where justified
- [ ] Bilingual parity for learner-facing edits
- [ ] Visual/media and rights audit
- [ ] Validation evidence tied to the final commit
- [ ] Topic collection index with open follow-ups



## 7. Standard deliverable templates

Use the templates in [`docs/workflows/templates/`](templates/) as starting points. They are deliberately separate because each artifact has a different responsibility:

| Template | Use | Canonical destination |
|---|---|---|
| [Source registration](templates/source-registration-template.yml) | Register provenance, metadata, licence, scan history and project relations | One entry in `data/sources.yml` |
| [Structured source extraction](templates/source-extraction-template.yml) | Record scan coverage, source-local graph/route and atomic evidence-backed contributions | One file under `data/extractions/` |
| [Source review](templates/source-review-template.md) | Human-readable technical and pedagogical audit with bounded integration decision | One file under `docs/source-reviews/` |
| [Multi-source comparison](templates/multi-source-comparison-template.md) | Compare sources consistently and explain aggregate impact on the learning system | One living topic dossier under `docs/source-reviews/` |
| [Visual asset audit](templates/visual-asset-audit-template.md) | Inspect exact figure assets, provenance, accessibility and reuse rights | One audit per source or figure set |

### Template use rules

- Copy a template and replace every placeholder; do not leave template placeholders in a published record.
- Keep the structured extraction as the evidence-oriented record and the Markdown review as its human-readable interpretation. Avoid maintaining two competing copies of the same facts.
- The source register is the canonical bibliographic/provenance inventory; do not duplicate the full extraction into `data/sources.yml`.
- Use one cross-source dossier per topic, not one comparison file per pair of sources.
- Use the visual audit only when the source actually contains relevant media; unresolved figures remain explicitly unknown/link-only.
- Template files are examples, not schemas. Run the repository's actual validators against completed records and update templates when the canonical data model changes.
- Preserve unknown values as null/unknown and distinguish `not-inspected`, `unavailable`, `not-applicable` and `not-verified` where relevant.

## 8. Q/K/V worked application

The Q/K/V comparison is the initial worked application of this workflow:
- DEV / Nishanthan provides a compact end-to-end sequence and a multi-head summary; the comparison exposed four canonical concepts already taught but absent from the registry.
- Medium / Neha KK foregrounds why matching and payload should be separated and offers a pronoun-context illustration; it improves the explanation without justifying another page or route.
- The KV-cache comment is separately attributed to a reader and checked against Hugging Face documentation.
- The canonical route and detailed attention derivation remain unchanged.
- Actual original figures and rights remain unresolved; both tutorial records remain partially scanned.

See the [Q/K/V collection dossier](../source-reviews/qkv-source-collection.md) and the [cross-source graph/route comparison](../source-reviews/qkv-learning-graph-comparison-2026-11.md).
