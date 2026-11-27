# Knowledge-change workflow

**Status:** normative workflow · **Version:** 1.1 · **Scope:** adding knowledge, integrating sources, creating or restructuring learning pages, and updating the canonical knowledge graph.

**Related canonical workflows:** [Source-to-learning system integration](source-to-learning-system-integration.md), [Source-to-knowledge validation](source-to-knowledge-validation.md), [Project-level learning resource audit](project-learning-resource-audit.md), [Page metadata schema](../page-metadata-schema.md), [Information architecture](../information-architecture.md).

## 1. Purpose

This workflow makes every knowledge change an explicit, traceable change to the existing LLM Lab learning system. It is an entry point and decision protocol, not a replacement for the specialist workflows, registries, schemas, templates or validators.

The desired outcome is not a larger corpus. It is a more coherent bilingual knowledge system in which:
- each durable concept has a clear definition, owner and meaningful typed relations;
- each page answers a distinct learner question at an appropriate depth;
- each source's contribution can be traced to the claims or teaching choices it informs;
- connections across domains are discoverable without being mistaken for prerequisites;
- new material improves existing explanations where possible, rather than multiplying near-duplicate pages;
- every change preserves useful prior knowledge and can be validated independently.

## 2. Choose the change mode

Start by identifying what is being added. A single request may combine modes, but each mode keeps its own evidence and completion state.

| Change mode | Typical input | Primary workflow / skill | Output |
|---|---|---|---|
| External source intake | Article, paper, book, course, repository, video, dataset | `source-to-learning-integration` (coordinates `source-extraction` then `knowledge-and-learning-integration`) | Source record, extraction, item decisions, justified project changes or explicit no-op |
| New project knowledge | A derived insight, corrected explanation, new relation, cross-domain synthesis | `knowledge-change-workflow` + `knowledge-and-learning-integration` | Evidence-backed page/graph/resource delta and provenance |
| New learning page | A durable learner question not served adequately by current pages | `new-learning-page` + `knowledge-and-learning-integration` when graph/source integration is involved | Page contract, bilingual page(s), metadata/navigation, links and tests |
| Existing page improvement | Missing explanation, better example, correction, scope/ownership issue | `page-content-audit` or `editorial-boundary-audit`, then integration | Bounded content change and preservation record |
| Knowledge-graph evolution | New concept, semantic relation, domain impact or knowledge-map projection | `knowledge-architecture-audit` | Canonical concept/domain/resource changes and regenerated projections |
| Computational-graph evolution | New operation, data representation, dataflow relation, execution branch, feedback/repetition rule or computational view | `knowledge-architecture-audit` | Canonical `data/computational-graph.yml` change, schema/validator/tests and regenerated computational views |
| Page-navigation evolution | Page identity, suggested route, hierarchy, related links or page-map projection | `knowledge-architecture-audit` | Canonical page metadata change and regenerated page-map projection |
| External learning project | Coherent course/site/book/repository ecosystem | `project-learning-resource-audit` first | Project model, source map, comparative integration decisions |

Do not invoke every skill. Use the smallest combination that covers distinct decisions. The [skill routing matrix](../../.agents/skills/audit-skill-routing/SKILL.md) is the operational index.

### Cross-workflow ownership and hand-off matrix

Use this compact matrix to choose the workflow boundary and preserve distinct completion evidence. Specialist skills provide the detailed procedures; this table is the shared routing crosswalk, not a second checklist.

| Work unit / trigger | Entry skill or workflow | Specialist owner(s) | Canonical owner(s) | Validation / hand-off |
|---|---|---|---|---|
| Review an individual lesson | `audit-skill-routing` → `page-content-audit` | `scientific-content-audit` only for disputed claims; `rendered-site-audit` for observed UI | Page source, page metadata, relevant concepts/resources | Page audit findings, relevant tests, render/accessibility evidence kept separate |
| Review a page group or route | `audit-skill-routing` → `page-group-audit` / `understand-path-audit` / `build-path-audit` | `editorial-boundary-audit`, `scientific-content-audit`, `knowledge-architecture-audit` only for their distinct questions | `docs/learning-path.md`, `data/guided-route.yml`, page metadata | Group/route transitions, prerequisite evidence, FR/EN parity; no inferred curriculum from sidebar |
| Review formal architecture or metadata | `audit-skill-routing` → `knowledge-architecture-audit` | `scientific-content-audit` for semantic correctness | `data/concepts.yml`, `data/domains.yml`, `data/resources.yml`, page-map metadata and their schemas | Existing registry/page validators and graph tests |
| Discover or inspect an external source | `source-to-learning-integration` → Phase A | `source-extraction`; `visual-asset-audit` for asset-specific provenance/rights | Current `data/sources.yml`, `data/source-taxonomy.yml`, scan history | Exact scan scope, retrieval route, version, rights and limitations |
| Extract source contributions | `source-extraction` | Technical review only where needed | `data/extractions/<source-id>.yml` | Atomic items, exact locators, evidence/confidence, source-local pedagogical model; no page/graph mutation |
| Compare sources and synthesize | `source-to-learning-integration` / source-to-knowledge validation protocol | `knowledge-and-learning-integration` for accepted Phase B decisions | Existing source reviews/syntheses and extraction records | Contribution comparison, convergence/disagreement, dispositions and rationale |
| Integrate validated knowledge | `knowledge-change-workflow` → `knowledge-and-learning-integration` | `new-learning-page`, page/group/editorial/scientific specialists only as needed | Concepts, domains, resources, page sources, references and existing route owners | Canonical diffs, preservation ledger, bilingual parity, tests and rendered checks |
| Model computation/dataflow | `knowledge-change-workflow` → `knowledge-architecture-audit` | `scientific-content-audit` when operation semantics are disputed | `data/computational-graph.yml`, `docs/computational-graph-schema.md` | `site/tools/check_computational_graph.py`, `tests/site/test_computational_graph.py`, generated views |
| Change page metadata/navigation | `knowledge-change-workflow` → `knowledge-architecture-audit` | `page-group-audit` for learner consequences; `rendered-site-audit` for rendered behavior | `LLM-LAB-PAGE-MAP v1` in page source | `site/tools/check_page_metadata.py`, map generator/tests, FR/EN route/link checks |
| Validate actual learner experience | `audit-skill-routing` → `rendered-site-audit` or relevant route/page skill | `page-content-audit`, `page-group-audit` as appropriate | Rendered Quarto site and its canonical sources | Browser, keyboard, responsive and accessibility evidence; learner tasks are a separate validation state |

The hand-off states are independent: **source inspected → extraction complete → synthesis complete → integration decision → implementation complete → structural/technical validation → rendered validation → learner validation**. A later state does not retroactively prove an earlier one, and no single `done` flag should collapse them.

## 3. Gate 0 — establish the current baseline

Before editing:

1. Identify the repository, current base/head branch and commit. Work on a focused branch.
2. Search open and recently closed issues/PRs, existing source reviews, extractions, pages and graph records. Reuse the existing owner; do not create duplicate tracking work.
3. Read `AGENTS.md`, `CONTRIBUTING.md`, and the canonical documentation relevant to the change.
4. Locate the authoritative source, schema, generator, consumer and validator for every field or artifact to be changed.
5. Record what is observed, what is inferred and what remains unknown. Old audit reports and prior agent summaries are discovery aids, not current-state evidence.

**Pass condition:** the change has one clear owner and does not create a competing registry, graph, taxonomy, template contract or learning route.

## 4. Gate 1 — state the learner problem before choosing an artifact

Write one concise statement:

> A learner/researcher needs to [observable capability or resolve a precise question] because [specific difficulty or gap]; current LLM Lab coverage at [exact page/section/concept] does not yet do this adequately because [evidence].

Then test the smallest candidate intervention, in this order:

1. correct or clarify an existing claim;
2. improve an existing section, worked example, diagram, exercise or experiment;
3. add a complementary perspective or bounded subsection;
4. add a contextual link or optional reference;
5. create a new page only when the learner question is distinct, durable and cannot be served cleanly by an existing owner.

A different source, label, analogy or topic tag is not by itself a new learner question. A graph concept is not automatically a page. A new page is not automatically a new route step.

**Pass condition:** the proposed artifact is justified by a concrete learner benefit and its maintenance cost is understood.

## 5. Gate 2 — resolve ownership and model boundaries

Use the existing canonical ownership model. Do not infer ownership from filenames or headings.

| Information | Canonical owner / rule |
|---|---|
| Source identity and bibliographic metadata | `data/sources.yml` and its documented source model |
| Atomic source evidence and item dispositions | `data/extractions/<source-id>.yml`, controlled by `data/source-taxonomy.yml` |
| Stable concepts and typed semantic relations | `data/concepts.yml` |
| Controlled knowledge domains | `data/domains.yml` |
| Computational graph | `data/computational-graph.yml`, governed by `docs/computational-graph-schema.md` and `docs/canonical-computational-spine.md` | Computational nodes, operations, dataflow edges, operational branches and named graph views | The concept graph, pedagogical route, Build dependencies or page navigation |
| Non-page implementation resources | `data/resources.yml` |
| Page identity, editorial role, destination, tags, hierarchy, related and suggested navigation | `LLM-LAB-PAGE-MAP` metadata in page source |
| Reader-facing nine-stage Understand route | `data/guided-route.yml` (machine-readable stages); `docs/learning-path.md` explains the route |
| Overall curriculum and Build order/status | `docs/learning-path.md`, `docs/full-curriculum-plan.md` and existing Build lesson/code evidence |
| Build route and deliverables | Existing Build route definitions and docs |
| Source-to-project synthesis and provenance | Existing `docs/source-reviews/`, `docs/source-syntheses/`, extraction records and references |
| Computational graph | `data/computational-graph.yml`, governed by `docs/computational-graph-schema.md` and `docs/canonical-computational-spine.md` |
| Generated knowledge/page/computational graph, map, route and navigation projections | Existing generators; never hand-edit generated outputs |

Keep these structures distinct:
- concept graph relations are semantic, not reading instructions;
- page hierarchy expresses containment/organization, not necessarily prerequisites;
- `related` expresses useful discovery links, not a route;
- `suggested_route` is page-level local navigation, not a second global curriculum;
- domain membership is classification, not causality or dependency;
- source citations are provenance, not proof that sources independently corroborate one another.

Use only existing controlled values. Propose a schema, relation type, tag namespace or domain change only when several real cases require it; document migration and validator implications before adoption.

## 6. Gate 3 — evidence and synthesis

For source-backed changes, complete Phase A extraction before Phase B integration unless a trustworthy, current extraction already exists. Follow the canonical source-to-knowledge protocol.

For project-derived knowledge that is not tied to one external source:
- record the derivation, implementation/test, dataset or observation that supports it;
- separate established facts, project-specific results, hypotheses and design choices;
- include assumptions, scope, uncertainty, counterexamples and failure conditions;
- cite the exact primary/official source or local artifact where the claim depends on it;
- do not create a synthetic citation or imply independent corroboration from derivative sources.

For each candidate contribution, compare its learner question, explanatory lens, mental model, example phenomenon, teaching move, abstraction level, evidence and caveats with the exact existing coverage. Assess novelty and complementarity separately. A low-novelty complementary perspective can be valuable; a novel detail can still be noise.

Use only item dispositions defined by `data/source-taxonomy.yml`. Keep source scan status, extraction completeness, synthesis, integration and validation as independent states.

**Pass condition:** each accepted contribution has a precise evidence boundary, a decision and a canonical destination. Useful rejected/deferred material remains traceable where appropriate.

### Page-level production sequence: seven connected stages

For a reader-facing learning page—whether new or substantially improved—use the following sequence as the operational view of the gates above. It is a crosswalk, not a second workflow: source extraction, graph governance, page metadata, curriculum, templates and validation remain owned by their canonical documents.

| Stage | Work to perform | Required working output / exit condition | Canonical owner |
|---|---|---|---|
| **1. Ingest or reuse sources** | First audit the existing catalogue, extraction records, source reviews and syntheses. Reuse adequate, current evidence; ingest new primary, official or pedagogical sources only when a coverage, freshness, provenance or quality gap justifies it. Inspect relevant text, equations, figures, code, data and linked evidence; record versions, access limits and rights. | Existing sources are reused or new sources registered with explicit inspection scope; uninspected modalities and evidence gaps remain visible. | `source-extraction`; `data/sources.yml`; existing source reviews/syntheses |
| **2. Model source metadata and extracted knowledge** | Classify sources using controlled metadata; extract atomic claims, definitions, mechanisms, derivations, examples, teaching sequences, visuals, code and limitations with precise locators and evidence confidence. Reconstruct source-local semantic and pedagogical models where useful. | Traceable extraction records distinguish what the source says, what it demonstrates and what remains uncertain. | `docs/source-catalogue-schema.md`; `data/source-taxonomy.yml`; `data/extractions/` |
| **3. Compile and synthesize** | Compare sources against the learner question and existing LLM Lab coverage. Identify convergence, complementary explanatory lenses, disagreements, contradictions, unsupported claims and unique teaching contributions. Decide what to integrate, cite, link, defer or reject. | A source synthesis / review and item-level dispositions explain what each retained contribution adds and where it belongs. | `docs/source-synthesis-method.md`; `docs/source-syntheses/`; `knowledge-and-learning-integration` |
| **4. Model the page and its place in learning** | Decide whether to improve an existing owner or create a page. Define its learner contract and pre-draft blueprint. Map canonical concepts, page ownership, semantic relations, prerequisites, route position, neighboring pages and the distinct Understand / Build / Deepen / Practice roles. Align hidden `purpose` metadata with the observable outcome the core lesson itself teaches; do not encode an exercise delegated to Practice as the lesson's sole purpose. | A reviewed page contract and pedagogical blueprint explain the page's learner purpose, scope, sequence, examples, metadata and links before prose production. | This workflow; [page-template system](../page-template-system.md); [new-learning-page skill](../../.agents/skills/new-learning-page/SKILL.md); [page metadata schema](../page-metadata-schema.md); curriculum contracts |
| **5. Write the explanation** | Compose an original, self-contained explanation from the validated synthesis and blueprint. Develop intuition, formal definitions, mathematics, figures, worked examples, code and caveats in an order that supports the learner outcome. Use a coherent worked thread where it improves understanding. | The core explanation is technically defensible, pedagogically coherent and substantively equivalent in FR/EN. | [Page-template system](../page-template-system.md); [reader-experience method](../reader-experience-and-editorial-method.md) |
| **6. Derive pedagogical companions** | Decide which outputs are justified: revision synthesis, flashcards, optional deep dives, dedicated exercises, experiments and Build references. Derive each from validated concepts and outcomes; do not create every format mechanically. Link the core lesson to its dedicated Practice companion; let that companion route learners to broader exercise collections or existing activities rather than bypassing the separation. | Companion resources have explicit purpose, canonical links and equivalent language coverage, or a reasoned not-applicable decision; Practice navigation follows the dedicated companion. | Existing revision, Deepen, Build and Practice structures; [Practice separation issue #1512](https://github.com/JM-Brun/llm-lab/issues/1512) |
| **7. Validate and close** | Review science, reasoning, source traceability, page/graph/route metadata, links, bilingual parity, rendered accessibility, Quarto output and relevant full-build/CI checks. Record what was and was not tested. | Validation evidence, residual risks and follow-up work are recorded; no unsupported claim of browser or learner validation. | This workflow; specialist validators and CI; [source-to-knowledge validation](source-to-knowledge-validation.md) |

**The page blueprint is the hand-off between synthesis and drafting.** It is a design brief, not another registry or mandatory file. For a bounded edit to an existing page, update only the affected parts of its existing contract and blueprint; do not recreate a dossier for every correction.

### When the change concerns a series or coherent multi-page group

Before drafting individual pages, write a provisional group contract: shared learner question and outcome, intended audience, page inventory and roles, intended order, transitions, dependencies, coverage boundaries and expected navigation. Review that contract and the existing pages with the [page-group-audit skill](../../.agents/skills/page-group-audit/SKILL.md), whose group map and transition analysis test purpose, membership, coherence, overlap/gaps and bilingual parity. Then apply the seven page-level stages and the page blueprint to each page that is created or substantially changed. Reuse the existing source reviews and synthesis records across the group; map each contribution to its canonical page rather than copying the same explanation into every page. A series plan is an editorial coordination aid, not a new registry, concept graph, page hierarchy or global learning route. Only the canonical `data/guided-route.yml` defines the Understand sequence.

Keep these distinctions explicit throughout the sequence:

- The **source model** describes what a resource contains and how it teaches; it does not define LLM Lab's canonical knowledge.
- The **concept graph** models stable semantic knowledge; the **computational graph** models objects and operations; neither specifies the reading order.
- The **Understand route** is a conceptual progression; **Build** is an independent implementation progression. Links between them are useful references, not automatic prerequisites.
- **Deepen** is optional depth. **Practice & experiment** is the activity destination. Learning pages teach; their dedicated practice companions assess and exercise that knowledge.
- The stages are ordered for planning but iterative in practice. A contradiction, technical error or failed validation may send work back to source inspection, synthesis, modelling or drafting.

Do not require a new synthesis dossier for a single-source correction, a new page for every concept, a flashcard set for every lesson, or a single narrative example where the subject is better taught through several contrasting cases.

## 7. Gate 4 — create or update the learning artifact

### Existing page
- Preserve its declared purpose and canonical scope, or document why that contract must change.
- Add only the explanation needed for the learner question.
- Link to the canonical owner for details rather than duplicating a second full explanation.
- Keep examples, figures, equations, exercises and references consistent with the updated text.
- Record a source-to-destination conservation map for every move, merge, shortening or replacement.

### New page
Use [New learning page skill](../../.agents/skills/new-learning-page/SKILL.md) and the existing [page-template guide](../page-template-guide.md), page archetype and metadata schema. Before implementation, define:
- one durable learner question and observable outcome;
- intended audience, prerequisites, scope and exclusions;
- canonical concepts and source evidence;
- why existing pages cannot own the material;
- destination (Understand, Build, Deepen, Practice & experiment or reference);
- language counterparts and any justified exception;
- links and graph/navigation implications;
- preservation, validation and maintenance plan.

Do not invent a new Understand route. If the sequential route genuinely needs changing, update `data/guided-route.yml` and its documentation/tests as a separate, explicit curriculum decision. Optional Deepen pages remain optional and must not acquire implied order from sibling links or hierarchy.

### Graph update
Add a concept only if it is stable, reusable, clearly distinguishable and useful beyond one page/source. Reuse existing IDs and relations. Every new relation must have a precise meaning, direction and evidence. Do not turn examples, transient claims, section headings, tools or source-local nodes into canonical concepts automatically.

A new concept should have bilingual labels/definitions and useful page-resource associations. Update the concept registry and its validator fixtures/tests; regenerate graph projections through their canonical generator.

A computational-graph change is a separate decision, not a side effect of adding a concept or page. Update `data/computational-graph.yml` only when the computation/dataflow model itself needs correction or extension. Follow `docs/computational-graph-schema.md` and `docs/canonical-computational-spine.md`; preserve node/edge identity, branch membership, abstraction level and the explicit semantics of feedback, repeated and optional edges. Update the graph validator/tests and regenerate its bilingual views through the existing generator. Never translate a computational edge automatically into a concept relation, page hierarchy or pedagogical prerequisite.

## 8. Gate 5 — connect the knowledge, not just the files

For each accepted change, inspect relevant neighboring concepts and pages. Consider cross-domain relations when they reveal a real shared mechanism, causal link, analogy, constraint, application or contrast.

Use typed relations, not generic `related-to`. For example, distinguish:
- shared mechanism from superficial vocabulary overlap;
- causal contribution from correlation;
- analogy from identity;
- prerequisite from application;
- contradiction from mere difference;
- independent corroboration from shared citation lineage.

Cross-domain connections should help explain one subject through another without flattening either field. Keep separate definitions and evidence boundaries where disciplines use similar terms differently. Record the bridge's value and limits.

Update page `related` links only when they answer a useful next question. Do not create a complete clique among all related pages. Update concept-resource associations only where the page actually supports the concept.

**Pass condition:** a reader can understand why each important link exists and what question it helps answer.

## 9. Gate 6 — bilingual and preservation checks

For every published bilingual change:
- update the French and English counterparts substantively, not necessarily literally;
- preserve intentional language-specific narrative, examples, references and cultural cues;
- compare scope, learning outcomes, technical claims, equations, caveats, examples, exercises and navigation;
- use language-matched links and illustrations;
- record an explicit exception when no counterpart is appropriate.

For every move, split, merge or shortening, maintain a conservation ledger:

| Source block | Information/learner function | Decision | Destination/anchor | Verification |
|---|---|---|---|---|
| Exact source heading/anchor | Definition, derivation, caveat, example, figure, exercise, citation, link, etc. | keep / move / merge / summarize / retire with rationale | Exact path and target anchor | Present, rendered, tested |

Do not remove a source block until its replacement or destination exists and has been checked. Keep distinctive examples and caveats even when a general explanation is consolidated.

## 10. Gate 7 — validate at the right layers

Run checks proportionate to the changed system. Expand scope when shared schemas, registries, generators, templates or routes change.

| Layer | Examples | What it establishes (and does not) |
|---|---|---|
| Source/provenance | exact locators, scan scope, rights, external reference spot-check | Traceability; not scientific truth by itself |
| Technical | primary-source review, derivation, code tests, experiment reproduction | Scoped correctness; not pedagogical effectiveness |
| Data/schema | YAML/schema and source/concept/resource/page metadata validators | Structural contract; not semantic quality |
| Graph/navigation | concept endpoints/relations, page links, route membership, generated projection freshness | Structural coherence; not learner comprehension |
| Bilingual | FR/EN structure and semantic comparison | Parity; not independent translation review unless performed |
| Build/render | relevant unit tests, full Quarto render when applicable, rendered local-link check | Buildability and local link integrity; not accessibility |
| Rendered/accessibility | desktop/mobile, theme, keyboard, screen-reader/text alternative, interaction/error states | Observed usability for tested cases only |
| Learner | formative tasks, transfer questions, independent observation | Evidence for tested learners/tasks only; not broad efficacy |

Report each layer as **passed**, **failed**, **pending**, **not run** or **not applicable**, with the exact command/commit where possible. Do not imply a browser or learner check from a passing CI run.

## 11. Gate 8 — close the loop

The change is ready for review when:
- the issue/PR ownership is clear and linked;
- the problem statement and scope are explicit;
- source and knowledge decisions are traceable;
- all accepted material has one canonical owner;
- prior useful knowledge is preserved;
- graph/page/route semantics remain distinct;
- bilingual counterparts and language-specific editorial choices are respected;
- generated artifacts are regenerated, never hand-edited;
- relevant tests and renders are reported honestly;
- unresolved work is recorded in the existing issue rather than silently left in prose.

The completion report should include:
1. learner problem and change mode;
2. canonical files/artifacts changed;
3. sources and evidence boundaries;
4. concepts/relations/pages/resources added, changed or intentionally unchanged;
5. cross-domain links considered and why retained/rejected;
6. preservation map;
7. FR/EN parity and intentional differences;
8. validation matrix;
9. remaining risks and revisit triggers.

A task can be complete with an explicit no-change decision. It is not complete merely because a page, source record, graph node, issue or PR was created.

## 12. Maintenance and improvement

Update this workflow only when canonical ownership, gate semantics or validation responsibilities change. Keep detailed page composition in page templates, source procedures in source workflows, and graph semantics in information-architecture documentation. Do not copy their full checklists here.

When a repeated failure appears, add a targeted test or validator before adding another prose checklist. Review the workflow against real additions and page changes; record case-specific lessons in dated audits, not as permanent universal rules.
