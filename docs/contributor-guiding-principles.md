# Contributor guiding principles

These principles are the short version of the project's editorial and engineering contract. Use them when proposing a page, figure, implementation, experiment, or design change. For detailed procedures, see the [contributing guide](../CONTRIBUTING.md), the [reader-experience and editorial method](reader-experience-and-editorial-method.md), the [flexible page-template system](page-template-system.md), the [page patterns](page-patterns.md), and the [implementation-page patterns](implementation-page-patterns.md).

## 1. Teach understanding, not just content

**Editorial economy is mandatory.** Do not add generic meta-discourse that describes the page instead of teaching its subject. Keep an introduction, transition, or signpost only when it states a concrete problem, distinction, assumption, result, prerequisite, or useful reading choice. Cross-links must explain the specific question they answer here; do not announce vaguely that more detail is available elsewhere. Avoid end-of-page lists that duplicate menus or the learning path. Link to a concept where it is introduced or used. When in doubt, remove the sentence and check whether scientific meaning or useful navigation is lost. Apply this check to titles, leads, callouts, summaries, conclusions, and next steps in both languages.

1. **Start from a learner question.** Every change should help a reader answer a concrete question or perform a defined investigation.
2. **Use a soft page pattern.** Choose the dominant learner question, then select only the modules that improve understanding. Combine, reorder, or omit sections freely; never add empty headings to satisfy a template.
3. **Make each page useful on its own.** Do not replace necessary explanations with links or require access to private repositories.
4. **Synthesize, do not concatenate.** Integrate primary evidence, pedagogical explanations, implementation details, and critical perspectives into a coherent account.
5. **Separate conceptual teaching from implementation teaching.** Concept pages explain mechanisms and formal ideas; implementation pages explain executable representations, contracts, verification, and trade-offs. Link them rather than duplicating large explanations.
6. **Keep overviews at the right level.** Explain organising relationships and link to dedicated pages for derivations, detailed algorithms, or code. Do not move essential definitions out of context merely to reduce page length.
7. **State learning outcomes only when they help.** Outcomes must be observable and page-specific, not generic promises.
8. **Maintain a useful glossary and use French equivalents without erasing established technical usage.** Define unfamiliar terms when first needed and preserve French/English terminology parity. In French pages, introduce the accepted French term alongside a widely used English term at first mention (for example, *embedding* / *plongement*). Keep the English term where it is standard in code, APIs, model names, or established expressions, and reuse the French equivalent naturally in explanatory prose. Do not alternate mechanically or imply that related concepts (such as an initial embedding and a contextualized representation) are interchangeable.

## 2. Prefer scientific precision over apparent certainty

9. **Scope every important claim.** State relevant assumptions, conventions, conditions, and limitations.
10. **Separate intuition from evidence.** Analogies and diagrams build intuition; they do not prove mathematical, implementation, or empirical claims.
11. **Challenge misconceptions.** Use counterexamples, boundary cases, or alternative methods to expose false equivalences and overgeneralizations.
12. **Use mathematical notation consistently.** Define symbols, dimensions, domains, reductions, axes, and conventions. Distinguish definitions, assumptions, theorems, hypotheses, and empirical observations.
13. **Cite sources for what they support.** Prefer primary papers and official documentation for technical claims; verify that a source supports the actual statement.
14. **Make uncertainty and status visible.** Distinguish planned, illustrative, implemented, tested, benchmarked, and experimentally observed work.

## 3. Connect explanations to inspectable practice

15. **Keep one source of truth.** Reusable code belongs in `src/`, tests in `tests/`, experiment runners/configurations in `experiments/`, and evidence-backed reports in `reports/`. A notebook or page may teach from these artifacts but should not become an unmaintained competing implementation.
16. **Specify the execution contract.** For runnable examples, state required dependencies, runtime assumptions, setup, command, inputs, outputs, shapes, dtypes, units, and conventions when relevant.
17. **Test meaningful properties.** Check invariants, hand-computed cases, edge conditions, numerical stability, gradients, and reference equivalence where appropriate—not only the happy path.
18. **Bound correctness claims.** Explain what tests establish and what they do not. Passing CI is not proof of general correctness or production suitability.
19. **Make experiments reproducible.** Record the question, baseline, data provenance, preprocessing, split/deduplication policy, configuration, seed, metrics, hardware, software versions, compute budget, and limitations as applicable.
20. **Support performance claims with comparable measurements.** Define workload and baseline; report relevant latency, throughput, memory, precision/error, and measurement conditions. Do not generalize beyond the tested setup.
21. **Explain simplifications and failure modes.** Distinguish pedagogical code from robust or optimized code; document unsupported cases and regression tests for discovered bugs.
22. **Prefer small, inspectable changes.** Avoid unnecessary dependencies, duplicated implementations, and opaque abstractions.

## 4. Design for navigation, accessibility, and visual learning

23. **Choose the medium to fit the question.** Figures, plots, animations, and interactive experiments should clarify structure, geometry, data flow, or change—not decorate.
24. **Use external resources responsibly.** Verify licences and attribution conditions for reused images, datasets, and code. A public URL is not a reuse licence.
25. **Make visuals accessible and honest.** Provide captions and meaningful alt text, contrast, keyboard access, labelled axes/units, and clear distinction between conceptual illustrations and measured results.
26. **Keep the interface coherent.** Reuse the visual design system; a new page pattern does not automatically justify a new component or page-specific styling.
27. **Validate the rendered experience.** Check links, equations, diagrams, navigation, responsive layouts, and keyboard behavior where relevant. Source inspection and a green build are not substitutes for rendered review.

## 5. Preserve bilingual and open learning

28. **Keep French and English substantively equivalent.** Claims, qualifications, examples, exercises, references, and implementation instructions must agree.
29. **Keep public learning self-contained.** Public pages must not depend on private notes, URLs, files, or build inputs.
30. **Respect provenance and reuse rights.** Attribute ideas and assets, verify licences, and do not copy substantial material without a clear legal basis.
31. **Prefer useful completeness over volume.** Add a page, dependency, visual, exercise, or experiment only when it solves a real learning or verification need.

## 6. Extract reusable knowledge from every model, method, and source

Studying a new model, architecture, training or inference method, research paper, technical article, or implementation is also an opportunity to improve the **general LLM knowledge base**. Do not treat the resulting case study as an isolated destination, and do not turn every source into a new page. Extract and place reusable scientific knowledge where it best serves the existing learning graph.

Use this editorial workflow:

1. **Decompose the source into claims and mechanisms.** Identify what is genuinely new, what is an instance of an established concept, what is a measured result, what is a design choice, and what is a vendor or author claim. Record the source and the evidence supporting each important claim.
2. **Test generality.** Ask whether the mechanism, mathematical result, systems constraint, trade-off, or evaluation method applies beyond the studied model or article. Separate general principles from model-specific configurations, names, benchmark results, and implementation details.
3. **Find the canonical destination before creating content.** Inspect existing concept pages, overviews, implementation guides, deep dives, glossary entries, and references. Extend the best existing page when the new material belongs to its scope. Create a new conceptual page only when it answers a distinct, durable learner question that cannot be integrated coherently without overloading or distorting an existing page.
4. **Choose the right pedagogical depth.**
   - **Core learning path:** include only the minimum general mechanism needed to understand LLMs and the system-level relationships. Give the reader a correct mental model, define necessary terms, and link to deeper treatment. Do not put specialist optimizations or research-specific details in the core merely because they are interesting.
   - **Advanced / deep-dive pages:** place derivations, complexity analysis, architectural variants, optimization techniques, systems trade-offs, detailed empirical evidence, and specialist implementation details here when they are useful but not prerequisites for the core mental model.
   - **Case study:** retain model-specific architecture choices, recipes, configuration, training details, reported benchmarks, limitations, and source-specific claims. Link these to the generic concepts they instantiate; do not present one model's choices as universal practice.
5. **Synthesize and connect.** Explain the mechanism in the project's own notation and pedagogical style. Add the relevant links in both directions where useful: generic concept to case study, and case study to generic explanation. Preserve French/English parity. Avoid copying the source's narrative or merely accumulating quotations and links.
6. **Verify and maintain.** Prefer primary papers and official technical documentation for scientific claims; use secondary articles as discovery aids or pedagogical perspectives, not as sole evidence for specialist claims. Check equations, assumptions, complexity bounds, benchmark conditions, implementation behavior, and known limitations. Update references and tests/examples where appropriate.

A useful classification test is: **Would this claim remain true, with the same conditions, if the named model or article disappeared?** If yes, it may belong in a generic concept page. If it depends on a particular model, dataset, hardware, training recipe, benchmark protocol, or source interpretation, keep that dependency explicit in the case study or experiment report. Some material legitimately belongs in both places at different levels: a concise general principle in the core, its rigorous treatment in a deep dive, and the concrete instantiation in the case study.

This is a recurring editorial responsibility, not a mandatory page-production quota. Reuse existing pages where possible; do not create duplicate concepts, force every source into the curriculum, or promote a detail to the core path without a clear learner need.

## The practical review question

> Will this change help a reader understand a specific LLM mechanism, inspect or verify its implementation, identify limitations, and navigate between explanation, code, tests, and evidence—without hiding assumptions or overstating the results?

If the answer is unclear, narrow the scope or explain the trade-off in the pull request.


## 7. Classify and place advanced knowledge consistently

The Deepen destination uses a stable six-domain taxonomy: (1) architectures and mechanisms, (2) text and tokenization, (3) mathematical tools and geometry, (4) probabilistic foundations and training, (5) inference and efficiency, and (6) scale and research questions. The bilingual Deepen map explains the learner-facing questions and lists the canonical current entries.

When adding material:

1. Identify the reader question and primary learning outcome before choosing a page title or category.
2. Check the canonical content owner. Extend an existing page when the material fits its scope; create a new page only for a distinct, durable question.
3. Decide whether the minimum mechanism is required by the core mental model. If it is, retain a concise, accurate explanation in Understand and place only the derivation, variant, research discussion, or specialist implementation in Deepen.
4. Assign exactly one primary sidebar category by learning objective. Use contextual links and metadata relations for legitimate cross-domain connections rather than duplicating the entry in several categories.
5. Keep graph semantics precise: parent/child means conceptual containment or decomposition; related means a useful non-hierarchical connection; suggested_route means a recommended reading transition.
6. Update the bilingual map, both sidebars, the Quarto render list, the page audit inventory, and metadata in the same change. Preserve FR/EN scope, level, status, and relations.
7. Create a new category only when multiple pages justify it or when a durable domain has a credible expansion path. Do not create one-page buckets around individual models or papers.

The Deepen taxonomy is for discovery, not a prerequisite sequence. Sidebar order must never be interpreted as conceptual dependency.
