---
name: knowledge-and-learning-integration
description: Integrate validated source-extraction records into the LLM Lab knowledge graph and bilingual learning experience, including concepts, relations, existing/new pages, figures, experiments, references, navigation and validation.
---

# Knowledge and learning integration

## Mission and phase boundary

This is **Phase B: integration**. Consume persistent, reviewable records produced by `source-extraction`. Decide which items genuinely improve LLM Lab, then integrate them into the canonical knowledge graph and/or learning experience.

Do not rescan by default. If an extraction is incomplete, stale or tied to a different version, request targeted re-extraction. An extracted item is not automatically accepted. A fully catalogued source can produce no graph or page change.

## 1. Inspect the current architecture

Before changing anything, inspect:
- `docs/knowledge-graph-standards.md` and `docs/knowledge-graph-implementation-audit.md`;
- `data/concepts.yml`, `data/domains.yml`, `data/resources.yml`;
- `site/tools/export_knowledge_graph.py`, schemas, graph validators and tests;
- `docs/learning-path.md`, `docs/content-section-mapping.md`, page inventory and templates;
- editorial principles, reader-experience guidance and page metadata schema;
- relevant pages in both `site/fr/` and `site/en/`, including prerequisites and downstream pages;
- source catalogue, references, resource library, asset register, experiments and open issues/PRs.

The current branch is authoritative. Audits and extraction recommendations are discovery aids, not proof of current state.

## 2. Review and disposition every item

Compare each extraction with actual existing coverage. Record one disposition:
- `integrate`, `correct`, `clarify`, `link`, `cite`, `case-study`, `experiment`, `defer`, or `reject`.

For each, record rationale, evidence/confidence, generality, existing coverage, destination and learner value. State what is genuinely complementary: derivation, mental model, counterexample, evidence, limitation, implementation perspective, failure mode, history or experiment.

Do not add content solely because it is novel or interesting.

## 3. Enrich the knowledge graph deliberately

The graph may be augmented, but only when the extraction changes the conceptual model or useful relationships.

### Concepts
- Reuse existing stable concept IDs.
- Add a concept only for a durable, reusable notion with a distinct definition and meaningful relations.
- Do not create concepts for source titles, source entities, model names, section headings, temporary findings, examples or every extraction item.
- Keep source identity separate from the concept it discusses.
- Never create a second concept registry or independent graph database.

### Relations
- Reuse the established relation vocabulary and direction.
- Add edges only when their semantics are justified. Distinguish prerequisite, part-whole, specialization, dependency, association, contrast and other supported types.
- Do not convert analogy into equivalence, correlation into causation, association into prerequisite, or historical succession into conceptual dependency.
- Preserve evidence/provenance for new or materially changed relations where the schema supports it; otherwise link the extraction through supported provenance fields or record the limitation.
- Check effects on neighbouring concepts, domain membership, page mappings and route prerequisites.

### Sources, extracted items and projections
- Represent sources/extractions using the compatible canonical model established in Phase A.
- Link sources/items to concepts, pages and first-class resources without conflating identities.
- Keep source catalogue, concept registry, learning-resource registry and pedagogical route distinct but cross-linked.
- Update the JSON-LD exporter and tests whenever the canonical graph model changes. JSON-LD is generated, never hand-maintained.
- Update the interactive map only when new nodes/edges materially improve discovery. Graph topology is not the same thing as the pedagogical route.

Report before/after nodes and edges: added, changed, intentionally unchanged and removed (with explicit justification).

## 4. Select the right learning destination

Map accepted items by learner question and page purpose:

| Layer | Appropriate contribution |
|---|---|
| Foundations | Reusable mathematical, statistical, CS, numerical or systems prerequisite |
| Understand / core | General mechanism, definition, mental model, misconception correction |
| Synthesis | Relations among concepts, architecture families, training/inference stages |
| Deepen | Derivation, formal property, complexity, variants, research debate, failure conditions |
| Case study | Named model/family/version, configuration, design choices, results and limits |
| Build | Tensor/data contracts, algorithms, code paths, numerical and engineering trade-offs |
| Practice & experiment | Reproducible activity, ablation, comparison, interactive exploration, test |
| Reference / glossary / history | Stable terminology, bibliography, historical or lookup material |

One source may contribute at several layers. Split by learner question. Do not place model-specific details in general concept pages or force general principles to live only in case studies.

Keep prerequisite vs suggested reading, concept relation vs navigation relation, core vs optional depth, and explanation vs implementation vs practice distinct.

## 5. Extend existing pages before creating new ones

Assess whether an item can clarify a definition, add a bounded analogy, strengthen a derivation, expose an assumption, add a counterexample/misconception/failure mode, improve a figure, add an example, motivate an experiment, improve cross-links or correct stale information.

Before editing, inventory existing claims, caveats, examples, equations, activities and links that must remain. Every moved item needs a working destination and explicit rationale. No silent shortening or loss.

### New-page gate

Create a page only if all conditions hold:
1. a distinct, durable learner question and learning outcome exist;
2. canonical ownership is clear;
3. no existing page can accommodate it through a coherent small extension;
4. it fits a meaningful core, Deepen, case-study or practice location;
5. evidence, examples, references and FR/EN counterparts can be supported;
6. it does not fragment a topic or duplicate an existing concept treatment.

Inspect page inventory, archetypes/templates, content-section mapping, neighbours and open issues/PRs. Document why extending existing pages is inferior. If the idea is immature, retain a structured proposal rather than publishing a speculative page.

## 6. Integrate analogies, visuals, experiments and code responsibly

### Analogies
Use only when structurally sound and useful for a defined learner difficulty. Explain mapping and failure boundary; credit the source; do not copy distinctive wording or illustration. Analogy supplements, never replaces, formal or computational definitions.

### Figures and visualizations
Choose: link original, embed with verified rights, create an independently authored figure, or omit. Never trace/cosmetically alter protected visuals. Preserve useful existing project assets unless replacement is justified. Update `docs/visual-assets-register.md`, references, accessibility text and affected pages.

### Experiments, datasets and benchmarks
Turn ideas into bounded falsifiable protocols only when useful and feasible. Specify hypothesis, variables, controls, dataset, model/version, baseline, metrics, compute and interpretation risks. Reuse canonical code, fixtures and experiment directories. Keep statuses distinct: proposed, protocol implemented, run completed, independently reproduced. Never present source results as project results.

### Code
Use pinned versions, existing project architecture and canonical code locations. Add tests where appropriate. Distinguish conceptual pseudocode from executable code and intended behavior from observed/tested behavior.

## 7. Update references, metadata and bilingual pages

For published changes:
- cite the source next to the claim and update the appropriate canonical source/reference inventory;
- include exact version/date and licence/attribution where relevant;
- update metadata, concept associations, resource references, reciprocal links and route/navigation only when semantics require it;
- inspect both language counterparts and align claims, equations, assumptions, examples, caveats, citations and links substantively;
- use natural language-specific phrasing, not mechanical translation;
- if a counterpart is absent, record the gap and decide whether to create it or defer publication.

Do not create a parallel bibliography. A source reference is not a concept node or pedagogical navigation link.

## 8. Plan, validate and report

For broad changes, prepare a reviewable plan:

| Extraction item | Evidence/confidence | Existing coverage | Disposition | Graph impact | Page/asset/experiment destination | FR/EN |
|---|---|---|---|---|---|---|

Run narrow checks, then broader checks for shared systems:
- source catalogue and extraction schema;
- concept graph and relation validation;
- JSON-LD export and tests;
- metadata, links, IDs, references and asset paths;
- bilingual parity;
- Quarto render/build for affected pages;
- tests for changed code, notebooks and experiments;
- visual inspection of FR/EN pages, equations, figures, mobile layout and navigation.

Inspect diffs for accidental deletions, unrelated formatting churn, generated noise and duplicated explanations. A green build does not prove scientific correctness or pedagogical quality.

Final report:
1. extraction items reviewed and dispositions;
2. graph nodes/edges added, changed, intentionally unchanged or removed;
3. pages/sections/assets/experiments/references updated or proposed;
4. new-page decision and rationale;
5. existing knowledge preserved or moved;
6. FR/EN parity;
7. validation commands/results;
8. unresolved issues and next steps.

## Definition of done

- Each accepted integration links to a source and precise extraction item.
- Graph changes use canonical IDs, relation semantics, schemas and generated projections.
- Every page change has a demonstrated learner benefit and fits page ownership/layer.
- New-page decisions pass the explicit gate.
- Existing useful content is preserved.
- Rights, attribution, versions and experimental status are accurate.
- FR/EN counterparts and navigation are substantively aligned.
- Relevant checks and rendered-page review are reported.
- Deferred/rejected items have explicit reasons.
