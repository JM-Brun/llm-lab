# Contributing

**Start here:** [Contributor guiding principles](docs/contributor-guiding-principles.md) — the short decision-making rules for teaching quality, scientific rigour, code, experiments, accessibility, design, and bilingual parity. For the repository's source-of-truth map, metadata ownership, graph semantics, and maintenance responsibilities, use [Information architecture and metadata governance](docs/information-architecture.md).

Use the [page-template guide](docs/page-template-guide.md) and [page archetype implementation map](docs/site-page-design-system.md) when creating or substantially restructuring a page. They connect reusable starting structures to the existing metadata taxonomy, editorial method, and visual design system; they are soft targets, not mandatory section checklists.

This is a learning and experimentation repository. Prefer small, testable changes that make the reasoning, implementation, and evidence inspectable. Follow the shared [reader-experience and editorial method](docs/reader-experience-and-editorial-method.md): the site is a navigable learning graph with progressive depth, not a mandatory linear book. The Wiki is the canonical home for reusable, domain-general concepts; LLM Lab is a separate public, bilingual learning site whose explanations must be complete without access to the private Wiki. The repositories have different purposes, not a shared runtime or reading dependency. Reusing a concept in both is intentional when LLM Lab needs to teach it to explain language models. Public readers must never need a Wiki URL, private definition, or private file to understand a page or render the site. Cite accessible public sources and include all definitions, assumptions, derivations, examples, caveats, and exercises needed by the LLM Lab learning experience—even when that creates deliberate overlap with the Wiki.

## Choose the right source before editing

Use this routing sequence; do not create a second registry or copy a rule into a neighbouring guide.

1. **Reader-facing page and destination:** consult [Content-section mapping](docs/content-section-mapping.md) for Understand / Build / Deepen / Practice & experiment, and [Learning path](docs/learning-path.md) for sequence, prerequisites, milestones, and evidence.
2. **Page identity and graph metadata:** consult [Page metadata schema](docs/page-metadata-schema.md). The page map owns page IDs, page roles, destinations, tags, and page-to-page navigation relations.
3. **Concepts, domains, and non-page resources:** consult [Information architecture](docs/information-architecture.md) for ownership boundaries, then edit only the canonical source it identifies: `data/concepts.yml`, `data/domains.yml`, or `data/resources.yml`. Do not infer concepts from headings or resources from every code file.
4. **Page composition:** start with the [Page-template guide](docs/page-template-guide.md); use the [site page-design map](docs/site-page-design-system.md) to select an archetype and the [soft template system](docs/page-template-system.md) for composition. These are guidance, not mandatory section checklists.
5. **Visual treatment:** use the [design system](docs/design-system.md); do not create page-specific styling when a shared component is appropriate.
6. **Experiments and evidence:** use the [experiment protocol](docs/experiment-protocol.md), and keep configurations, reports, and source artifacts in their designated locations.

## Maintenance and validation workflow

For a change that affects page metadata, concepts, resources, curriculum, templates, or generated maps:

1. Update the canonical source only; update its owning documentation only when its contract or maintenance procedure changes.
2. Run the validator for the changed registry and the relevant unit/integration tests. The [information-architecture index](docs/information-architecture.md) links each source to its validator and generated projection.
3. Regenerate derived outputs using the documented generator. Never hand-edit generated JSON, route fragments, or graph projections.
4. Render the bilingual site when Quarto sources, navigation, metadata, or generated includes change: `quarto render site`.
5. Check rendered local links and the affected FR/EN pages. For interactive maps, also check keyboard, touch, responsive behavior, empty/error states, and the textual alternative.
6. In the PR, distinguish source review, automated tests, Quarto rendering, browser inspection, accessibility checks, and learner evidence. Do not claim one as proof of another.

For routine prose-only edits, run proportionate checks; do not run unrelated graph migrations. When a schema or controlled vocabulary changes, document compatibility/migration implications and update fixtures and validators in the same change. See [information architecture §8](docs/information-architecture.md#8-scalability-and-maintenance-requirements) for the governing maintenance principles.

## Contribution modes

Choose the mode that matches the change and identify it in the PR.

### Editorial economy: remove generic meta-discourse

Do not pad reader-facing pages with sentences that merely announce what the page, section, chapter, or learning path does. Avoid generic formulations such as “This page provides an overview”, “the following sections explore…”, “each step links to a dedicated explanation”, “to continue your learning journey…”, or equivalent wording in French. These statements are usually reusable on almost any page and therefore tell the reader little about the specific concept.

Before keeping an orienting or transitional sentence, ask:

- Does it state a page-specific problem, claim, distinction, assumption, result, or useful reading decision?
- Does it explain why a linked concept is needed at this exact point, and what question that link answers?
- Would removing it make the scientific explanation, scope, or navigation materially harder to understand?

If the sentence only describes the document, repeats the heading, advertises that more detail exists elsewhere, or announces an obvious transition, delete it. Do not replace deleted filler with another generic sentence. Replace it only when a concrete learner need is left unmet—for example, explain the actual dependency, define the boundary of the current argument, or state the conceptual consequence.

Use links contextually and sparingly. A link should identify the specific unresolved question or prerequisite it addresses; a list of related pages or a promise that “more detail” exists is not an explanation. Keep meaningful scope notes, learning outcomes, warnings, and transitions when they prevent a real misconception or help the reader make a useful choice.

Do not add end-of-page navigation sections such as “Pour continuer”, “Pour poursuivre”, “Continue learning”, or “Where to go next” when they merely repeat the site's menus, learning path, or links already present in the page. Put a link on the relevant concept at the point where it is introduced or used, and explain the specific connection only when that context helps the reader. Keep genuinely useful external references, primary sources, and tools in a references/resources section; do not discard them just because a redundant navigation section is being removed.

Apply this review to introductions, chapter leads, callouts, section endings, summaries, “next steps”, and navigation text in both French and English. During review, remove generic meta-discourse rather than merely shortening it. Prefer a page-specific scientific statement over a statement about the page.

1. **Concept teaching page or synthesis** — first identify the reader question and page type. Use the [page-template guide](docs/page-template-guide.md) to select an archetype, then the [concept-page template](docs/concept-page-template.md) as a flexible guide, not a rigid form. Lead with the high-level purpose and mental model, then offer optional depth through meaningful links. Explain an LLM-specific concept, connect it to essential (not merely related) prerequisites, cite sources, state assumptions and limits, and include counterexamples where they clarify likely misconceptions. Do not put private Wiki URLs or concept IDs in public lesson content. If maintainers need cross-repository traceability, record it in the private `career-knowledge` repository; it must never be a reader or build dependency. Teach enough of the general mathematics locally for the page to stand alone; include the derivations and worked examples required by the LLM learning objective. Focus the selection, notation, examples, counterexamples, and interpretation on LLMs. **Every substantive concept page must include a clearly identifiable implementation/code section when the concept is computationally implementable.** For LLM topics, prefer a small, runnable Python/PyTorch example tied directly to the mathematics, with shape comments, explicit axis/mask/target conventions, and assertions or tests for key invariants. Link to maintained `src/llm_lab` code when it exists; do not let a long page snippet become a second untested implementation. For concepts that are genuinely theoretical or not meaningfully executable, state that boundary and provide an algorithm, symbolic derivation, or precise pseudocode instead. Do not add decorative or unrelated code merely to satisfy a checklist. It is acceptable—and sometimes necessary—to repeat a definition or derivation also present in the Wiki. Do not shorten or remove material solely to eliminate overlap.
2. **French/English parity and navigation** — improve translations, glossary, cross-links, learning sequence, accessibility, or site structure. Keep substantive claims, caveats, examples, and references equivalent in both languages; do not translate a claim into a stronger one.
3. **Reference implementation and numerical tests** — add or revise reusable code under `src/llm_lab`, with typed interfaces and tests for shapes, masks, gradients, numerical edge cases, or known values. Notebooks may explain the code but must not be its only implementation.
4. **Controlled experiment and evaluation** — define a hypothesis, baseline, data provenance, configuration, seed, split strategy, metrics, compute budget, and limitations. Preserve runnable entry points/configuration and report negative or inconclusive results as well as positive ones.
5. **Critical review or correction** — challenge a claim, implementation, illustration, or interpretation with a source, counterexample, reproducible check, or explicit uncertainty. Separate a documented source claim from the project's own analysis.
6. **Figures and external references** — add or revise visual material with source/author attribution and a checked licence. Prefer original visuals or linking to an authorized original source instead of copying external assets; record provenance in the reference page.
   **Preservation rule:** do not remove, replace, hide, or disable an existing external illustration solely because its licence or permission is unknown, unclear, or restrictive. Record the exact asset and unresolved status in `docs/visual-assets-register.md` and keep the illustration in place while the rights and intended use are investigated. Do not remove, replace, hide, or disable existing external illustrations as an audit outcome. If a potential legal or contractual issue is identified, document it and escalate it; take no action on the illustration unless the user explicitly instructs it.
7. **Build, dependencies, and developer tooling** — update Quarto, Python packaging, CI, linting, or reproducibility tooling. Explain material dependency changes and keep the core exercises runnable on CPU with small inputs.

## Pedagogical resource discovery

Use the curated [Pedagogical Resource Library](docs/pedagogical-resource-library.md) when creating or substantially revising a concept, overview, mathematical explanation, or learning sequence. It includes visual explainers, animations, interactive tools, science communication, and primary/official references.

Actively look for ideas on how to explain the topic—not just sources that mention it. Consider whether an original diagram, figure, animation, interactive experiment, analogy, or step-by-step visual sequence would make the mechanism clearer. Compare sources when the concept is important or easily misunderstood; identify what each source simplifies or omits, then produce an original synthesis with consistent notation, worked examples, counterexamples, limitations, and links to implementation/tests. Use primary papers and official documentation to verify technical claims; popularity or visual polish is not evidence.

This is a quality prompt, not a requirement to add a figure to every page or to cite a fixed number of resources. A visual should answer a concrete learner question and remain useful alongside the text. Do not copy prose, exercises, code, diagrams, or animations without a clear legal basis. Check the specific licence and attribution requirements, record provenance in `site/references.qmd`, and provide captions and alt text. A publicly accessible asset is not automatically reusable.

For substantial revisions, use the library's [repeatable improvement loop](docs/pedagogical-resource-library.md#a-repeatable-improvement-loop). Record the learner problem, source roles, design decision, limitations, checks actually run, and remaining work in docs/page-audit-inventory.md or the PR description. Start with a small number of complementary sources rather than collecting links indefinitely. A decision to retain an existing explanation or not add a visual is acceptable when supported by the learner need and evidence. Do not report source inspection as rendered review, and do not report planned validation as completed.

For a substantial visual or explanatory revision, also state:
- the second perspective it adds (e.g. numeric example, counterexample, geometric view, algorithm steps), not just the source it came from;
- the analogy's useful mapping and where it breaks;
- why the selected medium is better than a simpler alternative for this specific learner question;
- how the figure is grounded, referenced, captioned, described with alt text, and distinguished from empirical evidence.

## Local setup

Install Python 3.12 and uv, then run:

```bash
uv sync --locked --dev
uv run pre-commit install
uv run pre-commit run --all-files
```

Commit `uv.lock` whenever dependency metadata changes. Use `uv lock --check` to check that the lockfile matches `pyproject.toml`, and use `uv sync --locked --dev` to reproduce the locked environment.

## Before opening a pull request

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy src
uv run pytest
uv run --no-project --with-requirements docs/requirements-history-validation.txt --python 3.12 python scripts/render_history_pilot.py
quarto render site
```

Run the relevant checks for the changed surface and state clearly if a tool or optional dependency is unavailable. Review the rendered page, including the other language version for bilingual changes.

## Engineering and research conventions

- Put reusable code in `src/llm_lab`; notebooks and lesson snippets are explanatory, not the sole home of core logic.
- Each computational concept page should connect the explanation to an implementation and a verifiable invariant (assertion, test, known value, or finite-difference check). Keep page snippets minimal and runnable; put reusable logic in `src/llm_lab` and test it there.
- Keep functions focused, typed, and small enough to reason about; document tensor shapes and numerical conventions.
- For numerical implementations, test known values and/or finite differences.
- For model or training changes, document hypothesis, baseline, data provenance, split/deduplication policy, configuration, seed, hardware, metrics, costs, and limitations.
- Keep experiments reproducible; do not commit secrets, raw datasets, model weights, or large generated outputs.
- Pin dependencies through `pyproject.toml` constraints and the committed `uv.lock`.
- Explain deviations from upstream implementations and cite the source.
- Separate verified, planned, illustrative, and experimentally observed results. Passing CI verifies configured checks, not scientific claims or visual quality.
- Follow [LICENSE.md](LICENSE.md) for project-owned code and prose; third-party materials and images with unestablished provenance have separate or unresolved terms.


### Page learning outcomes: one shared component

When a page needs an explicit statement of expected capabilities, use the bilingual **Objectifs d’apprentissage / Learning outcomes** component with the shared `.callout-note.learning-outcomes` classes and `collapse="true"`, so it is collapsed by default like comprehension checks. Its appearance must be controlled centrally in `site/styles.scss`; do not create one-off styles or ad hoc “À la fin de cette page” notes. Place it after the chapter lead, keep it to two to four observable, page-specific capabilities, and omit it when it adds no useful target. Outcomes are not summaries or comprehension checks. Follow section 11 of the [reader-experience method](docs/reader-experience-and-editorial-method.md#11-standardize-page-learning-outcomes).

### Learning checks: one recognizable pattern, increasing cognitive demand

All reader-facing self-checks must use the shared pattern documented in [the reader-experience method](docs/reader-experience-and-editorial-method.md#10-standardize-embedded-learning-checks). Do not create ad hoc headings such as “Questions de contrôle”, “Vérifier votre compréhension”, “Self-check”, or “Check your understanding”: use the canonical language-specific heading and the shared `.self-check` container. Keep the visual treatment, question numbering, answer disclosure, and exercise-space link consistent across French and English pages.

Design a short progression where the topic supports it: (1) retrieve or identify the key concept, (2) explain or calculate a mechanism, (3) apply it under changed conditions or diagnose a misconception, and (4) transfer or critique the result. Difficulty should increase through reasoning demand, not obscure wording. Each question must test a stated learning outcome and require an explanation, intermediate step, calculation, prediction, or justified choice where appropriate. Avoid recall-only quizzes, questions answered by copying one sentence, artificial trick questions, and questions whose answer depends on an unstated convention.

Reveal solutions only on request. A useful solution explains the reasoning, names assumptions, and diagnoses a plausible wrong answer; it is not merely a letter or final number. Do not invent questions to fill a fixed count: a concise, topic-appropriate check is better than a padded sequence. Link to the relevant collection in the bilingual exercise hub when available, using a topic-specific anchor. Clearly distinguish short embedded checks from substantial exercise collections, and never imply that planned exercises already exist.
