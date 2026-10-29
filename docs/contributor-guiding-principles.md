# Contributor guiding principles

These principles are the short version of the project's editorial and engineering contract. Use them when proposing a page, figure, implementation, experiment, or design change. For detailed procedures, see the [contributing guide](../CONTRIBUTING.md), the [reader-experience and editorial method](reader-experience-and-editorial-method.md), and the [concept-page template](concept-page-template.md).

## 1. Teach understanding, not just content

1. **Start from a learner question.** Every change should help a reader answer a concrete question or perform a defined investigation.
2. **Explain the whole before the details.** Give the reader a useful mental model first, then provide optional depth through meaningful links.
3. **Build a learning graph, not a compulsory sequence.** Make relationships between concepts explicit; distinguish essential prerequisites from helpful background and optional deep dives.
4. **Make each page useful on its own.** Do not replace explanations with links, and never require access to private repositories or notes to understand public content.
5. **Synthesize, do not concatenate.** Combine strong pedagogical explanations, primary evidence, implementation details, and critical perspectives into one coherent account with consistent notation.
6. **Use a flexible concept-page pattern.** Where relevant, move from intuition and motivation to definition, notation, assumptions, examples, applications, limitations, exercises, and implementation. Adapt the structure to the concept; do not force empty sections onto every page.
7. **Maintain a useful glossary.** Define terms when first needed and link them to canonical concept explanations. Keep glossary entries concise, disambiguate overloaded terms, and maintain French/English terminology parity.

## 2. Prefer scientific precision over apparent certainty

8. **Scope every important claim.** State relevant assumptions, conventions, conditions, and limitations.
9. **Separate intuition from evidence.** Analogies and diagrams can build intuition; they do not prove mathematical, implementation, or empirical claims.
10. **Actively challenge misconceptions.** Identify common false equivalences and overgeneralizations, then use counterexamples, boundary cases, or alternative methods to show exactly where they fail. For example, cosine similarity measures angular alignment under a chosen representation; it is not, by itself, a measure of semantic similarity or human-perceived meaning.
11. **Use mathematical notation consistently and correctly.** Define symbols, dimensions, domains, reductions, axes, and conventions. Check derivations and edge cases; distinguish definitions, assumptions, theorems, hypotheses, and empirical observations.
12. **Cite sources for what they support.** Prefer primary papers and official documentation for technical claims; use pedagogical resources for teaching ideas. Check that a source supports the actual statement, not merely the general topic.
13. **Make uncertainty and status visible.** Distinguish planned, illustrative, implemented, tested, and experimentally observed work. Do not overstate results or hide negative and inconclusive findings.

## 3. Connect explanations to inspectable practice

14. **Connect the learning graph end to end.** Link overview → concept → worked example → implementation → tests/experiments where these exist, and provide return links so readers can move in both directions. Avoid orphaned pages and dead-end code references.
15. **Connect concepts to computation when meaningful.** Link equations and conventions to a small runnable example, maintained implementation, or precise pseudocode.
16. **Test properties, not just happy paths.** Where appropriate, verify shapes, masks, numerical values, gradients, invariants, edge cases, and failure modes.
17. **Use exercises for active recall.** Add questions that test understanding, calculation, interpretation, or transfer. Hide solutions by default using an accessible progressive-disclosure pattern; include reasoning and feedback in the revealed answer, not just a letter or final number.
18. **Keep experiments reproducible.** Record the question, baseline, data provenance, split and deduplication policy, configuration, seed, metrics, compute budget, and limitations.
19. **Treat tests as bounded evidence.** Passing CI shows that configured checks passed; it does not by itself establish scientific correctness, general model quality, or pedagogical clarity.
20. **Prefer small, inspectable changes.** Keep reusable code in the package, avoid duplicate implementations, and explain deviations from upstream references.

## 4. Design for navigation, accessibility, and visual learning

21. **Make the first screen readable.** Prioritize the page's purpose and main idea; keep secondary navigation and advanced details from overwhelming the initial view.
22. **Choose the medium to fit the question.** Consider original figures, diagrams, plots, animations, and interactive experiments when they clarify structure, geometry, data flow, or change over time. Each visual should answer a learner question, not merely decorate the page.
23. **Use external resources responsibly.** Search for high-quality explanations and complementary perspectives. For every reused image, figure, animation, dataset, or code sample, verify the specific licence and attribution conditions, record provenance, and cite the source. A public URL is not a reuse licence. Prefer original visuals when practical.
24. **Make visuals accessible and honest.** Provide captions and meaningful alt text, maintain contrast and keyboard access, label axes/units, and distinguish conceptual illustrations from measured results.
25. **Keep the interface coherent.** Use consistent visual hierarchy, spacing, navigation, and interaction patterns. The site's green, restrained retro-computing identity should support readability rather than compete with it.
26. **Validate the rendered experience.** Check links, equations, diagrams, navigation, responsive layouts, and keyboard behavior where relevant. Source inspection and a green build are not substitutes for reviewing the actual page.

## 5. Preserve bilingual and open learning

27. **Keep French and English substantively equivalent.** Definitions, examples, caveats, exercises, references, and conclusions must agree; wording may differ naturally.
28. **Keep public learning self-contained.** Public pages must not depend on private notes, private URLs, or private build inputs. Overlap with the separate knowledge base is acceptable when needed to teach the LLM-specific application.
29. **Respect provenance and reuse rights.** Attribute ideas and assets, verify licences, and do not copy substantial prose, code, exercises, or figures without a clear legal basis.
30. **Prefer useful completeness over volume.** Add a page, dependency, visual, exercise, or experiment only when it solves a real learning or verification need. Do not optimize for page count or apparent progress.

## The practical review question

Before submitting a contribution, ask:

> Will this change help a reader understand a specific LLM mechanism more clearly, identify and correct a likely misconception, verify important claims more reliably, and navigate from explanation to concept to implementation—without hiding assumptions or overstating the evidence?

If the answer is unclear, narrow the scope or explain the trade-off in the pull request.
