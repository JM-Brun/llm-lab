---
name: llm-learning-explorer
description: >
  Discover, evaluate and translate external ideas, projects, visual explanations,
  analogies, research perspectives and learning experiences into evidence-based
  opportunities for LLM Lab. Use when asked to find inspiration, complementary
  projects, visual references, teaching approaches, conceptual connections,
  researchers or authors, or to enrich the LLM learning experience without
  duplicating or bloating the existing curriculum. Distinct from understand-path-audit,
  which audits the current reader journey, and build-path-audit, which audits
  implementation dependencies and evidence.
---

# LLM Learning Explorer

## Mission

Find useful ways to help a learner understand large language models more deeply, intuitively and memorably.

Explore beyond conventional LLM courses. Search for ideas, perspectives, visual explanations, interactive demonstrations, analogies, historical context, mathematical intuition, research tools, experiments, teaching techniques and connections to other disciplines.

The goal is **not to collect links** or maximize the number of pages. It is to discover a small number of high-value contributions that improve the learner's mental models, reveal a missing perspective, make an abstract mechanism observable, or connect concepts that currently feel isolated.

Work from the actual LLM Lab experience, not from an imagined generic LLM curriculum.

## Activation contract

Use this skill when the user asks to:
- find new ideas, inspiration, projects, courses, explainers, figures, authors or researchers;
- identify visual resources, diagrams, animations, interactive tools or demonstrations;
- discover analogies, thought experiments, examples or alternative explanations;
- connect LLM concepts to mathematics, statistics, computer science, linguistics, cognitive science, neuroscience, physics, information theory, philosophy, history or other fields;
- identify gaps or complementary perspectives in the public learning journey;
- enrich a page, pathway or learning experience with external inspiration.

Do not use it as a substitute for:
- a focused scientific correctness audit of existing lessons;
- a full reader-journey audit (use understand-path-audit);
- an implementation/dependency audit (use build-path-audit);
- a routine source ingestion whose contribution is already specified;
- a generic bibliography with no integration analysis.

## Canonical project contracts

Read the current versions relevant to the requested scope. Locate the canonical owner if a path has moved.

- `README.md`: project purpose, scope, learning philosophy and evidence boundaries.
- `docs/learning-path.md`: authoritative distinction between Theory / Understand and Build, canonical route and objectives.
- `data/guided-route.yml`: eight-stage Understand route; do not create or reorder stages casually.
- `docs/content-section-mapping.md`: ownership boundaries for Understand, Build, Deepen and Practice & experiment.
- `docs/information-architecture.md`: canonical ownership of pages, concepts, sources, resources and graph projections.
- `docs/design-system.md`: visual language, accessibility and interaction conventions.
- `docs/reader-experience-and-editorial-method.md`: progressive disclosure, editorial economy and reader experience.
- `docs/source-catalogue-schema.md`, `data/sources.yml`, `data/source-taxonomy.yml`: source identity, provenance, facets and status.
- `docs/experiment-protocol.md`: requirements for experiments and claims based on observations.
- `docs/visual-assets-register.md`: provenance, rights and status of visual assets.
- `data/concepts.yml`, `data/domains.yml`, `data/resources.yml`: canonical concepts, domains and first-class resources.
- `.agents/skills/understand-path-audit/SKILL.md` and `.agents/skills/build-path-audit/SKILL.md`: complementary audit boundaries.

Inspect the live French and English pages for the requested topic, including their links and existing visuals. For a broad exploration, start with `site/fr/llm-overview.qmd` and its English counterpart, then follow the relevant canonical pages and route metadata. The overview is a map, not the owner of every detailed explanation.

## Non-negotiable principles

### 1. Start from the learner and the existing project

- Identify the learner question, the relevant point in the journey and what the learner is expected to understand before and after it.
- Inspect existing content before proposing additions. Search both French and English, including Deepen and Practice & experiment.
- Reuse existing concepts, pages, domains, resources and source records. Do not create a parallel taxonomy, graph, index or source catalogue.
- Distinguish a true content gap from a discoverability, explanation, visual-design or navigation gap.
- A resource being excellent in isolation does not make it appropriate for LLM Lab.

### 2. Search widely, select narrowly

Explore both LLM-specific and cross-disciplinary sources. Useful source families include:
- Open-source educational projects, courses, notebooks and explainers.
- Interactive visualizations, simulators, demos and browser-based experiments.
- Research papers, surveys, historical papers and technical reports.
- University teaching material, lecture notes and recorded lectures.
- Books, essays, technical blogs and carefully documented tutorials.
- Visual communication, scientific illustration, data visualization and animation.
- Analogies and explanatory models from other scientific or technical fields.
- Tools that expose model behavior, representations, attention, tokenization, uncertainty or failure modes.

Search for the underlying idea, not just the phrase "LLM tutorial". Explore adjacent concepts and disciplines when they can illuminate an LLM mechanism. Use primary sources to verify important technical claims and original creators' pages to verify provenance and rights.

Search in English and French where useful. Follow references and links from promising sources, but avoid endless link collection.

### 3. Explore complementary perspectives

For each topic, deliberately consider more than one explanatory lens where relevant:
- **Mechanistic:** what computation is performed, in what order?
- **Mathematical:** what equation, geometry, probability or invariant explains it?
- **Visual:** what can be seen, animated, manipulated or compared?
- **Intuitive:** what analogy or concrete scenario gives a first mental model?
- **Historical:** what problem led to the idea and how did it evolve?
- **Empirical:** what experiment, observation or counterexample tests the explanation?
- **Critical:** what does the model not establish; what are the limits or competing interpretations?
- **Systems:** how does the mechanism interact with data, hardware, software or an application?
- **Human and linguistic:** what do language, communication and cognition illuminate—and where do comparisons break down?

Do not force all lenses into every topic. Select those that reveal something genuinely new.

### 4. Treat analogies as scaffolds, not explanations

For every proposed analogy:
- State exactly which part of the mechanism it illuminates.
- Map the analogy's elements to the actual LLM components or operations.
- State where the mapping stops working.
- Identify misconceptions it could create.
- Prefer analogies that support a prediction or a small test, not just a memorable slogan.

Never imply that an LLM literally thinks, remembers, understands, attends or reasons in the same way a human does merely because a metaphor uses those words. Explain technical meanings and limits.

### 5. Treat visuals as teaching instruments

Evaluate a visual by the learning task it enables, not by attractiveness or novelty.

Look for process diagrams, geometric views, token-by-token or layer-by-layer animations, interactive controls, comparative diagrams, timelines, failure visualizations and small numerical visualizations that can be checked by hand.

For each candidate visual, record:
- The exact learner question it answers.
- The concept and canonical page it supports.
- What the learner should notice or manipulate.
- Whether it is static, animated, interactive or a runnable experiment.
- Whether the source is accessible, stable and usable on mobile.
- Creator, original URL, licence/permission status and attribution requirements.
- Whether it can be linked, recreated, adapted or only used as inspiration.

Never assume an image, diagram, animation, screenshot, font or dataset is reusable because it is publicly visible. Do not copy or redraw distinctive third-party artwork without checking rights. Record unresolved assets in the visual asset register and escalate; do not silently replace useful existing figures.

### 6. Preserve the four destinations

Classify every proposed contribution by its primary learning objective:

| Destination | Put it here when it primarily… | Typical contribution |
|---|---|---|
| **Understand (Apprentissage)** | establishes the essential mental model needed to understand what an LLM does and why | concise intuition, essential diagram, small worked example, key distinction |
| **Build (Construire)** | helps implement, integrate or verify a working component | implementation guide, interface contract, code, tests, reproducible milestone |
| **Deepen (Approfondir)** | explains why a mechanism has its properties, assumptions, variants or limitations | derivation, alternative formulation, research discussion, advanced visualization |
| **Practice & experiment (Exercer / pratiquer)** | lets learners calculate, manipulate, implement, test or challenge a claim | exercise, interactive workbench, controlled experiment, falsifiable hypothesis |

Understand and Build are independent pathways. Do not make one a prerequisite for the other. Deepen and Practice & experiment support either pathway.

Keep the core Understand path concise. A fascinating derivation, long history, advanced architecture comparison or extensive interactive playground usually belongs in Deepen or Practice, with a well-placed link from the core page. Do not add content to Understand merely because it is relevant.

### 7. Evidence and provenance

- Open and inspect the original source; do not rely solely on search snippets, reposts or generated summaries.
- Verify authorship, date/version, scope, technical claims, dependencies and whether the resource still works.
- Prefer original papers, official documentation, source code and creator-maintained demos for factual verification.
- Distinguish a paper's claim, a tutorial's explanation, a demo's behavior and your own inference.
- Record publication/update dates where relevant. Mark unstable or abandoned projects.
- Do not invent authors, titles, links, licences, benchmark results or capabilities.
- Note when an analogy or visualization is pedagogically useful but technically incomplete.
- Do not infer that a visualization proves a scientific claim.
- For experiments, require a question, hypothesis, baseline, controlled variables, configuration, seed where applicable, measurements and limitations, following the experiment protocol.

### 8. Avoid duplication and curriculum bloat

Before recommending a new page or module, ask in this order:
1. Can an existing page explain the idea with one concise paragraph or figure?
2. Would a contextual link to an existing Deepen page be enough?
3. Would an exercise or experiment provide more value than another explanation?
4. Could the resource be added to the existing source catalogue or resource registry without changing the curriculum?
5. Is a new page justified by a distinct learner outcome that has no suitable canonical home?

Do not create new Understand stages or change the eight-stage route based on one interesting source. Do not duplicate canonical explanations. Do not turn every discovered project into a required reading.

## Workflow

### Step 1 — Define the exploration question

Translate the request into topic/scope, learner audience and prior knowledge, relevant route stage/page/concept, requested contribution types, and whether the task is discovery only, recommendation, ingestion or implementation.

If the request is broad, choose a balanced exploration scope and state it. Ask one clarification only if the target cannot be inferred.

### Step 2 — Build a current-state snapshot

1. Read the relevant canonical page(s) in French and English.
2. Inspect the preceding and following pages when route continuity matters.
3. Search existing Deepen, Practice & experiment, source catalogue and resource records.
4. Inspect current figures, diagrams, interactive elements and links.
5. Note existing explanations, known gaps, duplicate candidates and content that must remain out of scope.

Produce a short gap map: already explained well; explained but hard to visualize; missing complementary perspective; existing resource that is hard to discover; genuinely missing learner activity or explanation.

### Step 3 — Explore source landscapes

For a broad exploration, search across at least three relevant source families. Include cross-disciplinary sources when the subject allows it. Search for projects and repositories; interactive and visual explainers; educators, researchers and authors; papers, lecture notes and courses; analogies and conceptual frameworks; experiments and tools.

Use targeted queries derived from the gap map. Search result volume is not a quality measure. Follow primary-source links for the strongest candidates.

### Step 4 — Extract candidate contributions

For each promising source, separate:
- **Source:** what the resource actually contains.
- **Idea:** the transferable concept or teaching approach.
- **Contribution:** what LLM Lab could gain.
- **Evidence:** what supports the interpretation.
- **Limit:** what should not be copied or generalized.
- **Integration:** the smallest useful way to incorporate it.

A source may yield several distinct ideas; several sources may support one idea. Avoid treating each source as a separate curriculum item.

### Step 5 — Evaluate and rank

Assess pedagogical value, complementarity, LLM relevance, evidence quality, visual/experiential value, integration cost and reuse feasibility.

Use qualitative priority:
- **P1 — High-value opportunity:** clear learner benefit and a concrete integration point.
- **P2 — Worth exploring:** promising, but needs verification, design or a small prototype.
- **P3 — Inspiration / watchlist:** interesting but not currently worth integrating.

Do not use false numerical precision. A candidate with unclear rights or weak evidence cannot be P1 for direct asset reuse, even if it is pedagogically excellent as inspiration.

### Step 6 — Design an integration proposal

For each P1/P2 candidate, specify:
- target page ID and canonical owner, or existing registry;
- destination: Understand, Build, Deepen or Practice & experiment;
- learner question and intended outcome;
- proposed format: paragraph, figure, animation, interactive, exercise, experiment, external link or optional reading;
- exact content to add and what it replaces or links to;
- source attribution and licence status;
- French/English parity implications;
- accessibility and responsive requirements;
- validation required;
- maintenance cost and dependencies.

Prefer an incremental contribution to an existing page or asset over a new page. If a new page is proposed, justify its distinct outcome and show why existing destinations cannot accommodate it.

### Step 7 — Act only within the requested scope

- If asked to explore, deliver findings and proposals; do not edit pages.
- If asked to enrich content, implement only well-supported, bounded improvements.
- If asked to ingest sources, follow existing source-ingestion and extraction conventions; do not invent a parallel pipeline.
- If asked to create issues, create focused issues with evidence, destination, acceptance criteria, provenance and validation.
- Do not claim an issue, page, asset, experiment or implementation exists until the corresponding write or validation succeeds.

When editing, preserve useful existing content and references; update canonical sources, not generated projections; maintain French/English substantive parity; reuse the design system; keep the core route concise; validate links, figures, alt text, licences, build/render and relevant tests.

### Step 8 — Re-evaluate the learner experience

After an implemented change, revisit the target page and its context:
- Does the contribution answer a real learner question?
- Is the new idea distinguishable from the established mechanism?
- Does the visual agree with the prose, equations and code?
- Does it create a misleading analogy or unsupported claim?
- Does it duplicate another canonical explanation?
- Does it preserve the route's entry and exit transitions?
- Is the FR/EN experience equivalent?
- Can the learner use it with keyboard, screen reader and mobile viewport where applicable?

## Output contract

For a discovery or exploration task, use this structure:

1. **Exploration scope** — topic, pages/stages inspected, languages and evidence level.
2. **Current-state gap map** — what is already covered and what remains underserved.
3. **Best discoveries** — curated table with source, idea, contribution, destination and priority.
4. **Visual and experiential opportunities** — concrete diagrams, animations, interactives or experiments, including provenance and rights status.
5. **Complementary perspectives** — analogies, disciplinary connections, historical context, researchers/authors and alternative viewpoints, with limits.
6. **Integration proposals** — exact page/resource, smallest change, learner outcome, FR/EN implications and validation.
7. **Do not add yet** — interesting candidates rejected or deferred, with concise reasons.
8. **Next actions** — bounded issues or edits only when requested.

For a focused task, omit empty sections. Keep the result curated and decision-oriented. Every recommendation must answer: **what does the learner gain, where does it belong, and why is it not already covered?**

## Completion criteria

The exploration is complete when:
- the existing learning experience was inspected before external discovery;
- relevant source families and complementary perspectives were searched;
- original sources and important claims were checked;
- ideas are distinguished from source summaries and integration proposals;
- each recommendation has a destination and a learner outcome;
- visual rights, provenance and accessibility are addressed;
- duplicates and curriculum bloat are actively filtered;
- uncertainty and evidence limitations are explicit;
- the output is actionable without implying that unimplemented work is already available.
