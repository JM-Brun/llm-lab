# Project-level learning resource audit workflow

**Status:** normative workflow · **Version:** 1.0 · **Introduced:** 2026-11-09  
**Coordinator:** [#756 — project-by-project pedagogical value audit](https://github.com/JM-Brun/llm-lab/issues/756)  
**Related workflows:** [source-to-learning-system integration](source-to-learning-system-integration.md) · [source-to-knowledge validation](source-to-knowledge-validation.md) · [project audit template](templates/project-learning-resource-audit-template.md)

## 1. Purpose and boundary

Audit a coherent external learning project as a **learning system**, not merely as a list of pages or isolated sources. Examples include a book and companion repository, a course, an educational website, a tutorial series, or an interactive learning environment.

The audit asks:
1. What does this project teach, how does it teach it, and what evidence supports its technical and pedagogical claims?
2. Which specific contributions would improve LLM Lab when compared with its existing concepts, pages, routes, Build path, exercises and experiments?

This is a higher-level comparison layer over the existing source workflow. It does **not** replace source registration, extraction, source-specific review, topic synthesis, asset review, or canonical LLM Lab architecture.

Reuse the existing system:
- data/sources.yml remains the only source catalogue.
- data/source-taxonomy.yml and docs/source-catalogue-schema.md remain the classification and data contracts.
- data/extractions/<source-id>.yml remains the structured evidence record.
- docs/source-reviews/ remains the home for source reviews and comparative dossiers.
- Existing source-review and multi-source-comparison templates remain authoritative at their respective levels.
- #756 coordinates the portfolio; one project-specific issue owns each project audit.

Do not create a second project registry, source format, extraction schema, controlled vocabulary, graph database, automation, or issue per individual page.

## 2. Units and levels of comparison

| Level | Unit | Main question | Canonical artifact |
|---|---|---|---|
| Source | Article, paper, video, repository, course module, visualizer | What does this exact source contain? | Source record + extraction |
| Topic collection | Several sources addressing one concept or learner question | What is convergent, complementary or disputed? | Living topic dossier |
| Learning project | Coherent book/course/site/series/tool ecosystem | What is the project's instructional and technical design? | Project audit dossier + owner issue |
| Project portfolio | Several comparable learning projects | Which patterns and contributions complement one another? | Cross-project synthesis, only when evidence exists |
| LLM Lab | Canonical learning system | What should change, and what should remain unchanged? | Canonical graph, pages, routes, exercises and Build artifacts |

A project may contain multiple sources. Do not force them into one extraction. Conversely, do not split a coherent project into many project-owner issues merely because it has multiple pages, chapters or repository files.

## 3. Reconcile existing work before scanning

1. Read #756 and identify the existing project owner.
2. Search existing issues, PRs, source reviews, extraction records and the source catalogue for prior work.
3. Reuse relevant work such as #86, #95, #114, #147, #458, #472, #742 and focused project owners where applicable. Verify their current scope/status.
4. Resolve project identity and boundaries: canonical URL, author/organization, related works, course/repository companions, versions and aliases.
5. Map constituent source records to the existing owner issue. Keep individual source records and provenance intact.
6. Create a new project issue only if no existing issue owns the coherent project family. Link it to #756 and state which previous tasks remain authoritative for narrower work.

**Gate A — ownership:** exactly one clear project-level owner exists; existing source-level work remains reusable and independently traceable.

## 4. Define a bounded audit scope

Record the declared learner audience and prerequisites (and reviewer inference), intended outcomes, included modules/pages/code/notebooks/exercises/demos/media, excluded or inaccessible components, inspected versions/revisions and access dates, audit depth, and selection rationale/coverage bias.

Do not claim to have audited an entire course or website after reading its landing page or a few representative lessons. Distinguish discovered, selected, inspected, extracted, compared, integrated and validated states. These are descriptive progress states, not new taxonomy values.

**Gate B — scope:** another maintainer can tell what the audit covers and what it does not.

## 5. Reconstruct the project model

Build a compact, evidence-linked model of the external project. Do not assume it has a formal graph or curriculum; label reviewer reconstruction as inferred.

### 5.1 Instructional architecture
Inspect declared audience, prerequisites and outcomes; entry points and assumed background; progression, modules, chapters and optional branches; conceptual explanations versus implementation tasks; scaffolding, worked examples, retrieval practice and formative assessment; advanced depth and variants; navigation and continuity across languages/devices.

Separate author-declared prerequisites from inferred dependencies. A chapter order is evidence of teaching sequence, not automatically a technical prerequisite graph.

### 5.2 Conceptual and computational model
Reconstruct key concepts/distinctions; objects, representations, operations, intermediate results and constraints; computational/data-flow narrative; mathematical definitions, derivations, assumptions and boundary cases; abstractions, hidden steps and simplifications.

Keep the source model distinct from LLM Lab's canonical knowledge graph and computational architecture. Do not convert every term into a proposed canonical concept.

### 5.3 Explanatory and visual model
Assess analogies and their limits; examples/counterexamples and the phenomena they actually illustrate; diagrams, animations and interactive visualizations; what learners can manipulate, observe, predict or compare; accessibility and technical fidelity; media provenance and reuse rights.

A visual asset must be inspected as an asset. A title, thumbnail, caption or alt text is not evidence that the visual itself was examined. Preserve existing LLM Lab illustrations during rights audits.

### 5.4 Practice and implementation model
Inspect exercises, quizzes, prediction tasks and feedback; experiments, datasets, notebooks, code examples and tests; implementation abstractions, dependencies, reproducibility and version pinning; what learners construct versus merely use; how practice checks understanding or transfer.

A repository's existence, passing code test or completed notebook is not evidence of learner mastery.

**Gate C — project model:** the dossier describes the inspected learning experience, distinguishing observed facts, source claims and reviewer inferences.

## 6. Differential comparison with LLM Lab

Compare against current LLM Lab artifacts, not memory or a stale audit: canonical FR/EN pages; concept registry and typed relations; computational architecture; guided route and Deepen branches; Build milestones and tests; Practice & experiment activities; navigation; references and visual assets.

Use a **learner-question crosswalk**. For each major project module or contribution, identify:
1. the learner question or capability it addresses;
2. the project's explanatory lens and teaching move;
3. the corresponding LLM Lab page, graph concept, route stage or activity;
4. differences in scope, level, assumptions and evidence;
5. what LLM Lab already explains more clearly or rigorously;
6. the precise gap or complementary value, if any.

Compare projects on common dimensions where applicable:

| Dimension | Comparison questions |
|---|---|
| Audience and prerequisites | Who can start, and what background is assumed? |
| Learning outcomes | What can learners explain, derive, implement or evaluate? |
| Curriculum architecture | What organizes progression: concepts, implementation, tasks, tools or projects? |
| Conceptual model | Which abstractions and relations are explicit? |
| Mathematical treatment | Are definitions, derivations, dimensions, assumptions and counterexamples supplied? |
| Explanatory pedagogy | Which mental models, examples, analogies and misconceptions are addressed? |
| Visual/interactive pedagogy | What becomes visible or manipulable, and what is simplified or hidden? |
| Practice and feedback | What does the learner do, predict, explain or test? |
| Implementation | What is built, with which abstractions, tests and reproducibility guarantees? |
| Scope and maintenance | What is omitted, version-sensitive, stale or costly to maintain? |
| Evidence and attribution | Are claims traceable to primary/official sources? Are assets reusable? |
| Accessibility and language | Are navigation, keyboard, mobile, language and accessibility addressed? |

Do not assign a global project score or popularity ranking. A project can be excellent in one dimension and weak in another.

### Required complementarity test

Do not stop at topic presence. For every plausible contribution compare the learner question/cognitive difficulty, explanatory lens/mental model, example phenomenon, abstraction level/prerequisites, teaching move/learner action, assumptions, omissions and failure boundaries.

A low-novelty contribution may still be valuable if it offers a meaningfully different route to understanding. A novel detail is not automatically worth integrating. Record benefit and cost: duplication, cognitive load, page ownership, maintenance and bilingual effort.

**Gate D — comparison:** each high-potential contribution has a specific LLM Lab counterpart and an explicit decision. Use canonical item dispositions for extraction items; project-level conclusions remain descriptive and must not create a second controlled vocabulary.

## 7. Cross-project synthesis

Cross-project synthesis is not required to complete an individual audit. Build it only after at least two project audits have comparable evidence.

Compare shared learner questions and instructional functions; trace citation/derivation lineage before calling claims independent corroboration; preserve contradictions and audience assumptions; identify complementary explanations, diagrams, exercises and implementation patterns; state where LLM Lab already provides a stronger treatment; test one concrete synthesis opportunity before broad redesign.

Use the existing multi-source comparison template as the matrix scaffold, extending its columns to projects and adding the project-model dimensions above. Do not create pairwise reports. Maintain one portfolio synthesis under docs/source-reviews/ only when it contains durable cross-project conclusions.

The existing [2026-11-05 learning-path comparison](../source-reviews/learning-path-comparison-2026-11-05.md) is a dated baseline for Raschka, Hugging Face and LLM Lab. Reuse and extend it rather than recreating its work.

## 8. Integration decisions

For extraction items, use only canonical item_dispositions from data/source-taxonomy.yml. Keep project-level conclusions descriptive and link them to underlying item IDs.

Prefer a precise improvement to an existing page/exercise; then a contextual link or optional perspective; then justified graph/route/implementation reference changes. Create a new page only for a distinct, durable learner question. Create an experiment or interactive feature only when it enables a specific learner action not already supported.

Keep Understand, Build, Deepen, and Practice & experiment responsibilities distinct. Every proposal states source evidence/locator, learner difficulty, exact target, why current treatment is insufficient, alternatives including link/no-op, validation, preservation implications, maintenance cost and FR/EN impact.

## 9. Validation and completion

| Validation layer | Evidence |
|---|---|
| Project inspection | Exact versions, inspected modules/assets/code and access limits |
| Extraction | Source locators, structured records, scan status and extraction checks |
| Technical | Primary evidence, independent derivations, API/code/tests as applicable |
| Pedagogical reconstruction | Observed sequence, declared/inferred outcomes, examples and practice |
| LLM Lab integration | Item decisions, bounded diff, preserved knowledge, graph/route/page checks |
| Site quality | Schema, tests, Quarto EN/FR render, links, visual/browser and accessibility checks |
| Learner outcomes | Formative observations or controlled evaluation only if actually conducted |

A successful issue update, API write, passing CI or complete source extraction does not validate the whole learning project. Record CI against the final commit/PR head. Do not claim learner efficacy from expert review or automated tests.

## 10. Maintenance and revisit triggers

Revisit only after a material event: major edition/course redesign, significant new modules/exercises/interactions/implementation, material correction/deprecation, relevant LLM Lab architecture change, or a concrete integration candidate. Do not schedule recurring scans solely to keep source lists fresh. Keep the owner issue as the maintenance entry point and append dated evidence.

## 11. Required deliverables

- [ ] Existing owner issue and prior evidence reconciled.
- [ ] Scope, versions, access and inspection coverage stated.
- [ ] Source/extraction records reused or added through canonical contracts.
- [ ] Project-local instructional, conceptual, visual and implementation models reconstructed where applicable.
- [ ] Differential learner-question crosswalk with LLM Lab.
- [ ] Complementarity pass and explicit no-change decisions.
- [ ] Contribution-level dispositions and exact target artifacts.
- [ ] Validation evidence and unresolved limitations.
- [ ] Revisit trigger and maintenance implications.
- [ ] Portfolio synthesis updated only when cross-project evidence warrants it.
