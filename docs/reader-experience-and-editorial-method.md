# Reader experience and editorial method

**Purpose:** make LLM Lab a navigable explanation system, not a textbook that must be read from page one to the end. This document is the shared editorial contract for public pages, concepts, learning stages, and contributions. It complements the scientific and implementation criteria in the [full curriculum plan](full-curriculum-plan.md), [roadmap](roadmap.md), and [contributing guide](../CONTRIBUTING.md); it does not replace them.

## 1. The learning model: a graph with progressive depth

The site has an overall direction—from the problem an LLM solves to its mechanisms, mathematical details, implementations, and evidence—but it is **not a single mandatory reading sequence**. Readers arrive with different questions and backgrounds. They must be able to enter at a useful level, understand where they are, and follow only the branches they need.

Each topic should support four complementary reading modes:

- **Orient:** understand the purpose, role, and main idea without mastering every underlying mechanism.
- **Connect:** see how the concept fits into the surrounding LLM or Transformer system.
- **Understand:** follow the mechanism, notation, assumptions, and a worked example.
- **Investigate:** examine derivations, edge cases, counterexamples, implementation details, tests, papers, or experiments.

These are levels of depth, not required steps or a score. A reader may jump directly to a concept, stop after the overview, or return later for the details. The site should provide a graph of meaningful links rather than force every reader through every prerequisite.

### Progressive disclosure in practice

Put the information needed for the current question first. Make deeper material discoverable without making it a prerequisite for the overview.

1. **First screen:** the question being answered, why it matters to an LLM, and a compact mental model or summary.
2. **Core explanation:** the essential mechanism and the minimum terminology needed to understand it.
3. **Technical detail:** equations, derivations, tensor shapes, numerical considerations, and worked examples when relevant.
4. **Further investigation:** implementation and tests, variants, caveats, research references, and related concepts.

Use headings, concise callouts, diagrams, links, and—where it improves usability—collapsible details. Do not hide a caveat that changes the meaning of the main claim, and do not force the reader to open several disclosures to discover the central explanation. A long derivation may be optional; a condition required for the claim to be true is not.

**Example — RoPE:** a reader of the Transformer overview needs to know that attention needs positional information and that RoPE is one way to introduce it. That reader should be able to continue without deriving the rotation identity. The dedicated RoPE page can then offer geometric intuition, the relative-position derivation, implementation conventions, long-context limitations, and references. The overview must link to the deep dive, but it should not reproduce it.

## 2. Page types have different jobs

Do not force every page into an identical chapter template. Choose the page type first and use the relevant contract.

### A. Orientation or system overview

Answer: **What is this system, what problem does it solve, and how do its major parts fit together?**

- Start with the whole system and a small number of meaningful components.
- Explain data flow and causal relationships at the level needed for the overview.
- Introduce unfamiliar terms briefly and link to their concept pages.
- Label which details can be skipped on a first pass.
- Avoid derivations that are not needed to understand the system-level claim.
- End with several purposeful routes: a likely next concept, a relevant deep dive, and evidence/code if available.

### B. Concept page

Answer: **What does this concept mean, why is it used here, and under what conditions does it work?**

Include what is relevant, rather than filling every section mechanically:

- A clear definition and the specific LLM question it answers.
- Intuition before formalism, with notation and shapes defined before use.
- A small worked example that can be checked by hand or with a short calculation.
- The assumptions, conventions, edge cases, and limitations that materially affect interpretation.
- The most likely misconception; add a counterexample when it distinguishes plausible alternatives.
- Connections to upstream concepts, downstream uses, competing approaches, and implementation/tests where they exist.
- Accessible sources, with primary papers or official documentation for technical claims and pedagogical sources for intuition.

A concept page should stand on its own for the LLM-specific learning objective. A link to a private knowledge base is never a substitute for a needed definition or derivation. At the same time, do not expand into a general textbook chapter unrelated to the application.

### C. Implementation or test documentation

Answer: **What exactly has been implemented, what contract does it satisfy, and what evidence checks it?**

- Link the implementation to the concept and equation it realizes.
- State interfaces, shapes, conventions, numerical tolerances, and unsupported cases.
- Distinguish illustrative pseudocode, executable code, tested behavior, and planned work.
- Link tests to the property or failure mode they verify.
- Never treat a passing unit test as proof of general scientific correctness or model quality.

### D. Experiment or evaluation report

Answer: **What question was tested, against what baseline, under which conditions, and what can the result support?**

State the hypothesis, data provenance, split/deduplication policy, configuration, seed, metrics, uncertainty where relevant, compute budget, limitations, and negative or inconclusive results. Keep results reproducible and distinguish observation from interpretation.

### E. Glossary, reference, or exercise page

Keep glossary entries concise and link to the concept page. Organize references by what they establish or help explain. Exercises should test a stated learning objective, use stable IDs across languages, and reveal solutions only on request. A navigation placeholder must not imply that exercises or implementations already exist.

## 3. Link design: a learning graph, not a chain of obligations

Links should answer a reader's likely next question. Prefer a small number of explicit relationships over a long list of generic links.

Where relevant, identify these relationships:

- **Understand first (essential):** a prerequisite without which a specific claim or derivation is genuinely hard to follow.
- **Useful background:** helps but is not required for the page's main conclusion.
- **Go deeper:** optional derivation, variant, implementation detail, or paper.
- **See it in the system:** the overview or downstream use that gives the concept meaning.
- **Verify it:** code, tests, or experiment, only if they exist.
- **Compare / challenge:** alternative methods, limitations, counterexamples, or critical reviews.

Do not label a concept as a prerequisite merely because it is related. Make essential dependencies few and explain why they are essential. A reader following an overview should not have to understand every linked concept before the overview itself makes sense.

## 4. Source synthesis: curate and combine the best explanations

LLM Lab aims to be a **more complete, more teachable synthesis of the strongest existing material**, not a summary of one book and not a pile of links. “Best” is question-dependent: a visual explanation may be best for first intuition, a primary paper for the original claim, official documentation for an API contract, and a controlled experiment for a measured performance claim. No single source is authoritative for every kind of question.

For each important topic, use a lightweight source map when it improves the explanation:

- **Core claim:** what exactly needs to be understood or established?
- **Primary evidence:** which paper, formal derivation, standard, or official documentation supports the technical claim?
- **Pedagogical explanation:** which existing explanation communicates the idea particularly well, and what does it leave implicit?
- **Alternative perspective:** does another source use different notation, assumptions, architecture, or emphasis?
- **Open limitations:** what is simplified, implementation-dependent, disputed, or not demonstrated?
- **LLM-specific bridge:** what must be added so the reader can connect the general idea to an actual language-model mechanism?

Then synthesize rather than concatenate:

1. Identify the reader's question and the minimum correct mental model.
2. Compare the strongest relevant sources for accuracy, scope, clarity, and omissions; do not rank sources by popularity alone.
3. Write an original explanation with consistent notation and a worked example that serves the learning objective.
4. Add the important caveats and counterexamples that a single source may omit.
5. Link to the best complementary source for readers who want a different presentation or more detail.
6. Record provenance for factual claims, figures, and borrowed framing; attribute specific ideas, and never reproduce substantial prose, exercises, code, or illustrations without a clear legal basis.
7. Recheck living sources and version-sensitive claims before treating a coverage item as current.

A source matrix is useful for a major topic or contested claim; it is unnecessary overhead for every small paragraph. Preserve disagreement where sources genuinely differ instead of silently blending incompatible conventions. When an explanation is simplified, state what it abstracts away and link to the fuller treatment.

**The output should be better than any single source for this learning goal** because it combines clear intuition, rigorous definitions, consistent notation, the right depth, counterexamples, current evidence, and links to further reading. It should not claim to be universally superior or exhaustive: define the scope, state what remains uncovered, and keep references inspectable.

## 5. Shared quality contract for every public page

Before a page is considered ready, check the following applicable items:

1. **Purpose:** the page answers a concrete question and states why it matters for LLMs.
2. **Level:** a reader can tell what is essential now and what is optional depth.
3. **Accuracy:** claims are scoped; notation, assumptions, conventions, and important exceptions are explicit.
4. **Pedagogy:** the main idea appears before unnecessary detail; examples actually illustrate the claim.
5. **Connections:** links lead to useful context or depth and distinguish essential from optional prerequisites.
6. **Evidence:** technical claims have suitable public sources; code, tests, experiments, and their status are represented honestly.
7. **Navigation:** the reader can continue, go deeper, compare, or return to the overview without getting trapped in a linear sequence.
8. **Bilingual parity:** French and English preserve the same substantive claims, qualifications, examples, and references. Exact wording need not be literal if meaning is preserved.
9. **Accessibility and rendering:** headings are meaningful, figures have text alternatives, equations and disclosures render, and links work.
10. **Scope discipline:** no page, implementation, or experiment is added simply to make the curriculum look more complete. Follow the roadmap's knowledge-validation gate.

Not every page needs a full derivation, code sample, counterexample, or exercise. It must either include what its purpose requires or link clearly to the relevant material. Do not remove a caveat or a needed explanation merely to make a page shorter.

## 5. Review workflow for a page, concept, or learning stage

Use this workflow for both new material and revisions:

1. **Name the reader question.** What should the reader be able to explain or decide after this page?
2. **Choose the page type and depth.** Is this an overview, a concept deep dive, implementation evidence, an experiment, or a reference/exercise?
3. **Map the minimum concept graph.** Identify essential prerequisites, optional background, downstream uses, and the useful next links. Avoid a full dependency chain when a local explanation is enough.
4. **Draft the high-level explanation first.** Write the answer and mental model before expanding into derivations and edge cases.
5. **Add depth only where it pays for itself.** Include the mathematics, worked examples, misconceptions, limitations, and implementation links needed to support the page's actual claims.
6. **Check sources and scientific scope.** Verify that references support the claims, not just the topic; distinguish established results from hypotheses and project interpretations.
7. **Check French/English equivalence.** Review claims and caveats, not just translation fluency.
8. **Validate the right surface.** Run the relevant tests and Quarto/link checks, then inspect rendered math, figures, mobile layout, and navigation as applicable. CI is necessary evidence, not a substitute for scientific review.
9. **Record status and remaining uncertainty.** Mark content, code, and experiments as planned, illustrative, implemented, tested, or experimentally evaluated as appropriate. Do not imply mastery from publication or CI.
10. **Only then advance the roadmap.** New implementations and experiments remain gated by validated prerequisite knowledge as specified in the roadmap.

## 6. What this method deliberately avoids

- A compulsory, chapter-by-chapter reading order.
- Treating every concept as equally important to every reader.
- Introducing advanced notation before explaining the purpose of the mechanism.
- Duplicating a deep derivation on every overview page.
- Replacing an explanation with a link, especially to a private source.
- Using collapsible sections to hide essential assumptions or limitations.
- Equating a published page, green CI, or a completed exercise with scientific validation or personal mastery.
- Adding pages and code solely to make progress appear larger.

The target experience is simple: **understand the whole at a useful level first; follow a link when a question becomes relevant; return to the whole with a better mental model.**
