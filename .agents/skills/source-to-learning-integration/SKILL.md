---
name: source-to-learning-integration
description: Extract, verify, classify, and integrate reusable knowledge from an external article, blog post, paper, documentation page, tutorial, repository, or website into the most appropriate existing LLM Lab pages and learning layers. Use when a new source should enrich the site, complement existing explanations, update a case study, add evidence, or reveal a content gap.
---

# Source-to-learning integration

## Mission

Turn an external source into a **traceable improvement of the existing LLM Lab learning experience**. Extract its useful ideas, verify what they establish, distinguish general knowledge from source-specific material, and integrate each contribution at the right pedagogical level and canonical destination.

The objective is not to summarize every source, collect links, or create a page for every interesting article. It is to improve the existing learning graph with complementary explanations, evidence, examples, counterexamples, implementation insight, or practice—without duplication, loss of existing knowledge, unsupported claims, or damage to the bilingual site.

This skill complements, rather than replaces:
- `editorial-boundary-audit`: use it when the work primarily concerns page ownership, overlap, or scope conflicts.
- `knowledge-architecture-audit`: use it when the work changes graph schemas, concept identities, relation vocabularies, projections, or curriculum architecture.
- `docs/contributor-guiding-principles.md`: authoritative editorial and scientific constraints.
- `docs/reader-experience-and-editorial-method.md`, `docs/page-metadata-schema.md`, `docs/learning-path.md`, `docs/content-section-mapping.md`, and relevant page templates: authoritative reader, metadata, route, and page-pattern contracts.

## When to use

Use this skill when the input is one or more:
- technical blog posts, articles, tutorials, explainers, or websites;
- scientific papers, preprints, books, lecture notes, or research reports;
- official documentation, API references, engineering reports, or benchmark reports;
- public source-code repositories, notebooks, demos, visualizations, or interactive tools;
- a named model, architecture, method, implementation, experiment, or case study whose reusable lessons should improve the general site.

A URL is an input lead, not proof that the page is accessible, authoritative, current, or reusable. If a source cannot be accessed, record the limitation and do not infer its contents from its title or snippets.

## Non-negotiable principles

1. **Improve the learning graph, not the source collection.** Every retained contribution must answer a learner question, resolve a misconception, add evidence, enable an activity, or improve navigation.
2. **Synthesize; do not concatenate.** Re-express verified ideas in the site's own coherent pedagogical narrative. Do not paste or closely paraphrase substantial source passages.
3. **One source can yield several contributions.** A source may contain a general mechanism, an advanced derivation, a model-specific example, an implementation detail, and an experiment. Route these separately instead of forcing them into one page.
4. **One idea has one appropriate canonical home.** Extend an existing page when possible. Reuse short explanations in context when needed, but do not duplicate a full treatment.
5. **Complementarity is more valuable than repetition.** Explicitly identify what the source adds beyond the current site: a different mental model, formal derivation, alternative formulation, counterexample, empirical evidence, implementation perspective, failure mode, historical context, or teaching activity.
6. **Generalize cautiously.** Separate established general principles from hypotheses, author interpretations, one-model design choices, vendor claims, benchmark-specific observations, and implementation accidents.
7. **Evidence must match the claim.** A source supports only what it actually demonstrates. Distinguish theorem/proof, measured result, empirical association, illustrative example, opinion, proposal, and undocumented assertion.
8. **Preserve provenance.** Keep bibliographic identity, stable URL/DOI/repository reference, author/organization, publication or update date where available, access date, relevant section/figure/code location, and licence/reuse status.
9. **No silent content loss.** Before changing a page, identify existing claims, explanations, examples, caveats, links, and activities that must remain. A source integration is additive or a justified replacement—not an excuse to shorten away useful material.
10. **Maintain French/English parity.** Update both language counterparts substantively. Preserve technical terminology and accepted French equivalents; do not treat literal translation as parity.
11. **Respect source and asset rights.** A public URL does not grant reuse rights. Prefer original synthesis and independently authored diagrams. Record attribution and licence constraints for any reused figure, image, code, dataset, or substantial text.
12. **Do not distort the learning route.** Core prerequisites belong in the core path; optional derivations and specialist details remain optional. A source's own order is not the site's teaching order.

## Required context inspection

Before extracting or editing, inspect the current repository state and read the relevant current versions of:
- `docs/contributor-guiding-principles.md`
- `docs/reader-experience-and-editorial-method.md`
- `docs/page-metadata-schema.md`
- `docs/learning-path.md`
- `docs/content-section-mapping.md`
- `docs/pedagogical-resource-library.md` and `docs/references.md`, where present and relevant
- relevant page templates, page inventory, concept registry, and existing source audits.

Then inspect the actual source pages in `site/fr/` and `site/en/`, including metadata, rendered/navigation relationships, and relevant linked implementations, tests, experiments, figures, and references. Treat the current branch as authoritative; prior audits are discovery aids, not proof of current state.

For a bounded topic, inspect a coherent cluster of adjacent/canonical pages rather than searching only for an exact keyword. Check both likely destination pages and their neighbours to understand prerequisites, downstream use, and existing explanations.

## Workflow

### 1. Establish source identity and access

Create a source record with:
- title and source type;
- author(s) or responsible organization;
- canonical URL and DOI/repository identifier if available;
- publication date, last-updated date, and access date (distinguish these);
- source version, commit, release, or archived version where relevant;
- licence and reuse conditions for text, figures, code, and data;
- access status and any limitations (paywall, inaccessible sections, dynamic content, missing supplementary material).

For a website with multiple relevant pages, record the exact pages examined. Do not describe a whole site as reviewed when only a subset was accessed.

Assess source quality according to source type:
- research claims: primary paper, methods, data, supplementary material, replication, and later critique where relevant;
- API or implementation behavior: official documentation and source code at a pinned version;
- empirical claims: protocol, dataset, baselines, metrics, uncertainty, and reproducibility;
- educational explanations: technical correctness, scope, clarity, and references behind the explanation.

Use primary sources to verify important claims when the supplied article is secondary. Preserve disagreements and uncertainty instead of manufacturing consensus.

### 2. Extract a structured claim and idea inventory

Read the source beyond its introduction and conclusion. Inspect relevant sections, equations, tables, figures, appendices, code, and linked primary sources.

Build an extraction ledger. Each entry should be atomic enough to route independently:

| Field | Required content |
|---|---|
| ID | Stable local identifier within the analysis (e.g. S1, S2) |
| Idea / claim | Concise statement in original wording only when a short technical term is necessary; otherwise synthesize |
| Kind | Definition, mechanism, derivation, assumption, theorem, hypothesis, empirical result, design choice, implementation detail, example, misconception, limitation, recommendation, historical fact, or open question |
| Evidence | Exact section, equation, figure, table, code path, experiment, or cited primary source |
| Confidence | Established / well-supported / context-dependent / disputed / speculative / unverified |
| Scope | General LLM principle, model family, named model/version, task, dataset, hardware, software stack, or source-specific context |
| Preconditions | Assumptions, conditions, data, architecture, precision, workload, or evaluation protocol |
| Contribution | What this adds that the current site does not already explain |
| Candidate destination | Existing page(s), page layer, glossary, reference, activity, or proposed gap |
| Action | Integrate, link, cite only, retain as case study, create activity, investigate, or reject |
| Rights | Reuse constraints for associated assets/code/data |

Do not collapse a paper's reported observation into a universal fact. Capture negative results, caveats, trade-offs, and limitations—not only the headline contribution.

For code repositories, inspect versioned source and tests. Distinguish intended behavior, observed behavior, and behavior guaranteed by tests. Do not infer algorithmic properties from names or README claims alone.

### 3. Separate generalizable knowledge from source-specific material

Classify every retained idea into one or more of these layers:

| Layer | What belongs here | Typical destination |
|---|---|---|
| **Foundations / prerequisites** | Reusable mathematics, statistics, computer science, numerical or systems concepts needed by several topics | Existing foundation or Deepen page; do not create a parallel textbook |
| **Core conceptual understanding** | General mechanism and mental model required to understand LLM behavior | Canonical Understand page and core route |
| **Cross-cutting synthesis** | Relationships among concepts, architecture families, training/inference stages, or system components | Existing overview, map, or synthesis page |
| **Advanced theory / Deepen** | Detailed derivation, formal properties, complexity, variants, research debate, failure conditions | Existing Deepen page |
| **Architecture or model case study** | Named model, family, version, design choices, configuration, reported results, limitations | Existing case-study page or a narrowly justified new one |
| **Build / implementation** | Tensor/data contracts, algorithms, software interfaces, code paths, numerical and engineering trade-offs | Existing Build walkthrough and canonical `src/` implementation |
| **Practice / experiment** | Reproducible activity, comparison, ablation, interactive exploration, exercise, or falsifiable test | Practice & experiment page, `experiments/`, `tests/`, and `reports/` as appropriate |
| **Reference / glossary / history** | Stable definitions, terminology, source bibliography, historical facts, lookup material | Existing glossary, reference, history, or resource library |

A single source may contribute at several layers. Split the contribution by learner question and evidence. Do not force a general principle to live only in a case study; do not move model-specific details into a general concept page.

### 4. Determine complementarity against the existing site

For each candidate contribution, compare it with the current canonical destination and neighbouring pages. Record:
- what is already covered and at what depth;
- what is missing, weak, ambiguous, outdated, or insufficiently evidenced;
- what the source adds that is genuinely distinct;
- whether the new material changes a conclusion, refines a boundary, supplies evidence, or merely restates the same point;
- whether it belongs in the body, a compact callout, a worked example, an optional deep dive, a case study, a reference entry, or an activity;
- what existing content must be preserved.

Use these dispositions:
- **Complementary addition** — a meaningful new perspective, proof, evidence, example, caveat, or activity.
- **Correction/update** — current content is wrong, stale, or overgeneralized; retain a traceable account of the correction.
- **Clarification** — a distinction, assumption, or limitation needs to be made explicit.
- **Cross-link only** — source is useful, but its content does not justify reproduction.
- **Reference only** — useful bibliographic resource with no necessary content integration.
- **Case-study only** — relevant only to a particular model/version/system.
- **No action** — duplicate, weakly supported, irrelevant, inaccessible, or not worth the added complexity.

Never add material solely because it is novel or interesting. Explain its learning value.

### 5. Map to canonical pages and learning routes

Choose the destination by the learner's question and the page's declared purpose—not by keyword match, source structure, or convenience.

For each proposed integration, record:
- stable page ID and FR/EN source paths;
- destination layer and page archetype;
- exact target section or proposed section;
- prerequisite and downstream relationships;
- related concept IDs and relation semantics, if the current registry supports them;
- references and source attribution to add;
- page metadata fields or navigation relations that may need updating;
- implementation, test, experiment, figure, or glossary dependencies;
- pages that need reciprocal links or short local explanations.

Prefer the existing canonical page. Create a new page only if the contribution answers a distinct, durable learner question and cannot be integrated coherently into an existing page without overloading it or violating scope. Before proposing a new concept, inspect `data/concepts.yml`; use existing stable IDs and relation vocabularies. Do not create a second concept registry or treat tags/headings as concepts.

Keep these distinctions explicit:
- prerequisite vs suggested next reading;
- concept relation vs page-navigation relation;
- core vs optional advanced content;
- general mechanism vs case-specific instantiation;
- explanation vs implementation vs practice.

### 6. Design the integration before editing

Prepare a concise integration plan with one row per contribution:

| Source idea | Evidence / confidence | Generality | Existing coverage | Destination and section | Change type | Related pages / assets | Parity |
|---|---|---|---|---|---|---|---|

The plan must state:
- which source ideas will be integrated and which will not;
- why each destination is the best fit;
- what new learner value is added;
- what existing information will be retained;
- whether a new page, figure, code example, exercise, or experiment is justified;
- the exact bilingual and metadata/navigation scope.

For a small, unambiguous addition, proceed directly while keeping this mapping in the change description. For broad, cross-cutting, disputed, or destructive changes, stop at a reviewable plan or open a focused issue/PR before applying the wider restructuring. Do not silently widen the scope.

### 7. Integrate with scientific and pedagogical discipline

When editing:
- write an original synthesis in the site's terminology and voice;
- explain the mechanism, not just the source's conclusion;
- state assumptions, notation, dimensions, units, and scope where relevant;
- distinguish definitions, mathematical results, hypotheses, empirical observations, and engineering choices;
- include a worked example, counterexample, failure mode, or limitation when it improves discrimination;
- keep the core explanation concise and move optional derivations or specialist material to Deepen;
- add a concrete link at the point where it answers a reader's next question;
- cite the source next to the supported claim and add it to the relevant reference/source inventory;
- pin versioned behavior for code, models, and APIs;
- create original visuals when they materially improve comprehension; do not reuse third-party visuals without verified permission and attribution;
- keep source code in canonical project locations and use existing tests/experiments rather than creating duplicate implementations;
- avoid generic meta-introductions, repetitive summaries, and link lists that do not help the learner.

Do not add raw article summaries to concept pages. A case-study page may summarize the source's contribution, but it must connect the case to reusable concepts and clearly delimit what is specific to that case.

### 8. Preserve and update bilingual counterparts

For every published content change:
- inspect both French and English counterparts;
- apply equivalent claims, equations, assumptions, examples, caveats, source citations, and links;
- preserve language-appropriate terminology and natural phrasing;
- update page IDs, metadata, tags, route relations, and references consistently where needed;
- verify that the counterpart exists and is substantively aligned; if it does not, record the gap rather than silently publishing a one-language change.

Do not mechanically translate source terminology. Follow the site's terminology conventions, including paired French/English technical terms where useful.

### 9. Validate the integration

Run the narrowest relevant checks, then broader checks when the change affects shared systems:
- page metadata/schema and concept-registry validation;
- local links, IDs, references, and asset paths;
- bilingual counterpart and semantic parity checks;
- Quarto render/build for affected pages and site navigation;
- existing tests for any code, notebook, experiment, or generated artifact changed;
- visual inspection of rendered FR and EN pages, equations, figures, mobile layout, and navigation;
- source/licence attribution checks for external assets.

Inspect the diff for accidental deletions, unrelated formatting churn, generated-file noise, and duplicated explanations. Compare the before/after content inventory: every prior substantive claim, caveat, example, and useful link must either remain, be moved with a working link, or have an explicit evidence-based reason for removal.

A green build is necessary where applicable but does not establish scientific correctness, source fidelity, or pedagogical quality.

### 10. Record provenance and close the loop

Update the appropriate source/reference inventory with:
- canonical citation and access date;
- source type and version/date;
- relevant claims or sections used;
- destination pages and the nature of the contribution;
- confidence and caveats;
- licence/attribution status;
- validation status and follow-up questions.

Do not create a second bibliography or source registry if an existing authoritative location fits. If a new source record structure is needed, first inspect the current reference model and propose a compatible extension.

Conclude with a compact integration report:
1. source(s) examined and access limitations;
2. extracted ideas grouped by kind and confidence;
3. generalizable versus source-specific contributions;
4. exact pages/sections updated or proposed;
5. complementary value added relative to existing coverage;
6. existing information preserved or moved;
7. FR/EN parity status;
8. references/assets/licence status;
9. checks run and results;
10. unresolved issues and next steps.

## Definition of done

The task is complete only when:
- source identity and access limits are recorded;
- important claims are traceable to precise evidence;
- general principles and source-specific claims are separated;
- each accepted contribution has a justified destination in the existing learning graph;
- complementarity is demonstrated against actual current page content;
- existing useful knowledge has not been silently lost;
- references, versions, and reuse rights are handled correctly;
- French and English pages remain substantively aligned;
- affected metadata, links, routes, and supporting artifacts are consistent;
- relevant checks and rendered-page review are reported;
- rejected or deferred ideas have an explicit disposition.

The final deliverable is an improved, coherent learning experience—not a pile of extracted notes.
