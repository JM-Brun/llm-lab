# Contributor guiding principles

These principles are the short version of the project's editorial and engineering contract. Use them when proposing a page, figure, implementation, experiment, or design change. For detailed procedures, see the [contributing guide](../CONTRIBUTING.md) and the [reader-experience and editorial method](reader-experience-and-editorial-method.md).

## 1. Teach understanding, not just content

1. **Start from a learner question.** Every change should help a reader answer a concrete question or perform a defined investigation.
2. **Explain the whole before the details.** Give the reader a useful mental model first, then provide optional depth through meaningful links.
3. **Build a learning graph, not a compulsory sequence.** Make relationships between concepts explicit; distinguish essential prerequisites from helpful background and optional deep dives.
4. **Make each page useful on its own.** Do not replace explanations with links, and never require access to private repositories or notes to understand public content.
5. **Synthesize, do not concatenate.** Combine the strongest pedagogical explanations, primary evidence, implementation details, and critical perspectives into one coherent account with consistent notation.

## 2. Prefer scientific precision over apparent certainty

6. **Scope every important claim.** State relevant assumptions, conventions, conditions, and limitations.
7. **Separate intuition from evidence.** Analogies and diagrams can build intuition; they do not prove mathematical, implementation, or empirical claims.
8. **Challenge plausible misconceptions.** Use worked examples, counterexamples, edge cases, or alternative methods when they clarify what a claim does—and does not—mean.
9. **Cite sources for what they support.** Prefer primary papers and official documentation for technical claims; use pedagogical resources for teaching ideas. Check that a source supports the actual statement, not merely the general topic.
10. **Make uncertainty and status visible.** Distinguish planned, illustrative, implemented, tested, and experimentally observed work. Do not overstate results or hide negative and inconclusive findings.

## 3. Connect explanations to inspectable practice

11. **Connect concepts to computation when meaningful.** For computational concepts, link equations and conventions to a small runnable example, maintained implementation, or precise pseudocode.
12. **Test properties, not just happy paths.** Where appropriate, verify shapes, masks, numerical values, gradients, invariants, edge cases, and failure modes.
13. **Keep experiments reproducible.** Record the question, baseline, data provenance, split and deduplication policy, configuration, seed, metrics, compute budget, and limitations.
14. **Treat tests as bounded evidence.** Passing CI shows that configured checks passed; it does not by itself establish scientific correctness, general model quality, or pedagogical clarity.
15. **Prefer small, inspectable changes.** Keep reusable code in the package, avoid duplicate implementations, and explain deviations from upstream references.

## 4. Design for navigation, accessibility, and visual learning

16. **Make the first screen readable.** Prioritize the page's purpose and main idea; keep secondary navigation and advanced details from overwhelming the initial view.
17. **Use visuals to explain a mechanism.** A diagram, animation, or interaction should answer a specific learner question better than plain text alone. Avoid decoration that adds complexity without insight.
18. **Make visuals accessible and honest.** Provide captions and text alternatives, maintain contrast and keyboard access, and distinguish conceptual illustrations from measured results.
19. **Keep the interface coherent.** Use consistent visual hierarchy, spacing, navigation, and interaction patterns. The site's green, restrained retro-computing identity should support readability rather than compete with it.
20. **Validate the rendered experience.** Check links, equations, diagrams, navigation, responsive layouts, and keyboard behavior where relevant. Source inspection and a green build are not substitutes for reviewing the actual page.

## 5. Preserve bilingual and open learning

21. **Keep French and English substantively equivalent.** Definitions, examples, caveats, references, and conclusions must agree; wording may differ naturally.
22. **Keep public learning self-contained.** Public pages must not depend on private notes, private URLs, or private build inputs. Overlap with the separate knowledge base is acceptable when needed to teach the LLM-specific application.
23. **Respect provenance and reuse rights.** Attribute ideas and assets, verify licences, and do not copy substantial prose, code, exercises, or figures without a clear legal basis.
24. **Prefer useful completeness over volume.** Add a page, dependency, visual, or experiment only when it solves a real learning or verification need. Do not optimize for page count or apparent progress.

## The practical review question

Before submitting a contribution, ask:

> Will this change help a reader understand a specific LLM mechanism more clearly, verify important claims more reliably, and find the right next level of detail—without hiding assumptions or overstating the evidence?

If the answer is unclear, narrow the scope or explain the trade-off in the pull request.
