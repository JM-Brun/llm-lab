# Reader experience and editorial method

**Purpose:** make LLM Lab a navigable explanation system, not a textbook that must be read from page one to the end. This document is the shared editorial contract for public pages, concepts, learning stages, and contributions. It complements the scientific and implementation criteria in the [full curriculum plan](full-curriculum-plan.md), [roadmap](roadmap.md), and [contributing guide](../CONTRIBUTING.md); it does not replace them. The source-level page map and controlled tag vocabulary are specified in the [page metadata contract](page-metadata-schema.md); keep suggested reading order distinct from conceptual parent/child relations.

## Editorial economy: page-specific information only

Reader-facing prose must teach, orient through a real decision, or establish a meaningful conceptual connection. Do not add generic meta-discourse that merely describes the document or the learning platform. Avoid statements such as “this page provides an overview”, “the following sections explore…”, “each step links to a dedicated explanation”, “to continue the learning journey…”, and their French equivalents. These formulations can be pasted into almost any page without changing their meaning; that is a strong signal that they carry no useful information.

A sentence about page structure is justified only when it conveys something specific that the reader needs: the precise question answered here, a genuine prerequisite, a scope boundary, a deliberate simplification, a reason to choose one branch over another, or the distinct purpose of a linked resource. A cross-link should say what question it resolves or what concept it supplies—not simply promise more detail.

Use this deletion test during drafting and review:

1. Remove the sentence temporarily.
2. Ask whether the reader loses a scientific claim, definition, assumption, interpretation, useful warning, or actionable navigation choice.
3. If not, leave it out. Do not replace it with a synonym or another generic transition.
4. If something important is lost, rewrite the sentence to name that exact information.

Apply the test especially to chapter leads, introductory paragraphs, callouts, section transitions, recaps, conclusions, and “next step” blocks. This is not a demand for terse prose: retain explanations, examples, and caveats that carry knowledge, even when they take space. The goal is higher information density, not shorter pages. Keep French and English versions equivalent in substance and apply the same standard to both.

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

## 4. Question-led complementary lessons

A canonical concept page does not need to answer every interesting question in equal depth. Keep one stable, authoritative explanation for each concept, then add **complementary learning units** only when a distinct learner question deserves its own treatment.

This extends the four reading modes (Orient, Connect, Understand, Investigate); it does not create a competing curriculum or replace the guided build-from-scratch route.

### 4.1 Distinguish content roles

- **Main lesson (canonical concept or system page):** explains what the mechanism is, why an LLM needs it, how it fits into the data/model/training/generation lifecycle, and the minimum correct mechanism. It owns the core definitions, notation, and scope.
- **Question lesson (focused companion):** answers one bounded question that would otherwise overload the main lesson, such as “Why scale dot products by sqrt(d_k)?”, “Why is the causal mask applied before softmax?”, or “What exactly changes when the context window grows?”. It must provide enough local context to stand alone, state its prerequisites, and link back to the canonical explanation.
- **Worked example or exercise:** asks the learner to calculate, predict, diagnose, or explain something. It tests a learning objective; it is not automatically a separate lesson.
- **Interactive experiment:** lets the learner manipulate a meaningful variable or inspect an intermediate result. It must state the question, controls, expected observation, interpretation, and limitations. An animation without a testable learning purpose is decoration, not a lab.
- **Deep dive / research note:** develops derivations, variants, implementation details, evidence, controversies, or limitations beyond the main lesson.

These are roles, not mandatory sections or a requirement to create one artifact of every type for every concept. A short concept may need only one main lesson and a worked example.

### 4.2 Let learner questions determine whether a companion is warranted

Create a separate question lesson only when at least one condition holds:

1. The question has a distinct learning objective and can be answered coherently on its own.
2. It requires a different explanatory mode (for example a geometric intuition, a derivation, a counterexample, or a controlled comparison).
3. It is a recurring misconception or a conceptual obstacle that appears in multiple parts of the course.
4. It connects multiple canonical concepts and is better explained as a cross-cutting bridge than repeated in each page.

Do **not** create a companion merely to split a long page, restate a definition, add a quiz, or imitate a micro-learning platform. Prefer, in order: a concise inline explanation; a worked example or disclosure; a contextual question/answer; then a separate companion page when the objective justifies it.

### 4.3 Connect lessons as a graph

Every companion must identify:
- the learner question it answers;
- its canonical concept owner(s);
- essential prerequisites (few, with a reason) and optional background;
- the specific point at which it should be discovered from the main lesson;
- at least one return link to the main lesson or guided-path milestone;
- related code/tests/experiments and references, when they exist;
- EN/FR counterpart and a stable shared identifier when it is an exercise or question.

A companion may be linked from multiple lessons, but it must have one canonical home. Do not duplicate its full content across chapters. Main lessons should link to the most useful companions at the point where the question naturally arises, not through a generic “related pages” dump. Do not automatically add every companion to the global sidebar: contextual links should remain the primary discovery mechanism unless a companion becomes a major, independently navigable curriculum stage.

The guided build remains the spine: companion material must clarify or deepen a milestone, never obscure the next construction step or make optional theory appear mandatory. The panorama remains an entry point; deep dives remain non-linear.

### 4.4 Use questions to drive a coherent teaching sequence

For a major mechanism, consider this progression where useful:

1. **Need:** what problem appears if this mechanism is absent?
2. **Intuition:** what mental model predicts its behavior?
3. **Mechanism:** what operation is actually computed?
4. **Why this formulation:** why this equation, scaling, mask, parameterization, or design choice?
5. **Inspect:** what intermediate values, shapes, or geometry can we observe?
6. **Challenge:** which plausible alternative or edge case exposes a misconception?
7. **Build:** how is the mechanism implemented and tested in the small GPT?
8. **Limits:** what does this mechanism not guarantee?

This is a question bank, not a compulsory eight-page sequence. Combine adjacent questions when one explanation serves them better; separate them when the learning objective or method genuinely differs.

### 4.5 Example: attention as a family of connected learning units

- **Main lesson — Self-attention in a GPT:** purpose, Q/K/V data flow, causal context, output, and its place inside a Transformer block.
- **Question companion — Why divide attention scores by sqrt(d_k)?** variance intuition, assumptions, softmax saturation, and a small numerical comparison.
- **Question companion — Why mask future positions before softmax?** causal semantics, a counterexample when masking after softmax, and the no-future-information invariant.
- **Worked example — Compute one attention head by hand:** small Q/K/V matrices, scores, mask, normalized weights, and weighted sum.
- **Interactive lab — Change score scale and inspect softmax:** compare entropy/concentration and gradients where executable; do not imply that one plot proves training quality.
- **Deep dive — Multi-head attention and tensor transformations:** split/reshape/transpose/concatenate, projection matrices, and implementation conventions.
- **Build checkpoint — Implement and test causal self-attention:** link to the actual code and property tests only when they exist and have been reviewed.

The companions answer different questions. They should not repeat the entire attention lesson, and their existence/status must not be claimed before implementation and validation.

### 4.6 Acceptance criteria for a companion

A proposed companion is justified when:
- [ ] its question and learning outcome are explicit and non-duplicative;
- [ ] its canonical owner and entry/return links are identified;
- [ ] it is locally understandable with clearly stated prerequisites;
- [ ] its explanation uses an appropriate mode (visual, derivation, example, experiment, or critique);
- [ ] assumptions, caveats, and evidence are accurate;
- [ ] it has EN/FR parity where published in both languages;
- [ ] it improves a real learner transition or resolves a documented misconception;
- [ ] it does not create a second source of truth for definitions or implementation status.

## 5. Source synthesis: curate and combine the best explanations

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

## 6. Shared quality contract for every public page

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

## 7. Review workflow for a page, concept, or learning stage

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

## 8. What this method deliberately avoids

- A compulsory, chapter-by-chapter reading order.
- Treating every concept as equally important to every reader.
- Introducing advanced notation before explaining the purpose of the mechanism.
- Duplicating a deep derivation on every overview page.
- Replacing an explanation with a link, especially to a private source.
- Using collapsible sections to hide essential assumptions or limitations.
- Equating a published page, green CI, or a completed exercise with scientific validation or personal mastery.
- Adding pages and code solely to make progress appear larger.

The target experience is simple: **understand the whole at a useful level first; follow a link when a question becomes relevant; return to the whole with a better mental model.**


## 9. Operationalize learning science without turning lessons into templates

The editorial method should support durable understanding and transfer, not only clear first reading. Use the following evidence-informed strategies where they serve the learning objective. They are design options, not a mandatory checklist for every page; their effects depend on prior knowledge, task complexity, timing, and learner context.

### 9.1 Define observable learning outcomes

State what a learner should be able to do after the activity. Prefer verbs that produce inspectable evidence:

- **Recognize:** identify a component, quantity, convention, or failure mode.
- **Explain:** describe a mechanism and why it is used.
- **Predict:** anticipate the effect of changing an input, parameter, or assumption.
- **Calculate:** derive or compute a result from stated inputs.
- **Implement and verify:** translate a formulation into code and test a stated property.
- **Diagnose:** locate an error in reasoning, notation, code, or experimental design.
- **Transfer and critique:** apply the concept in a new setting and state where the analogy or method stops working.

Do not equate these levels with a universal ranking of difficulty. A learner may explain a concept well but make an arithmetic error; an exercise should make clear which capability it assesses.

### 9.2 Move from worked examples to independent reasoning

For a new or mathematically demanding procedure, consider a progression:

1. A fully worked example with every important step and assumption visible.
2. A completion problem in which the learner supplies one or more missing steps.
3. An independent problem with different values or a changed condition.
4. A transfer or counterexample task that tests whether the learner understands the underlying rule rather than memorizing the example.

Use this progression when it reduces unnecessary search during initial learning. Do not keep learners on worked examples after they can already solve the target task independently. For an established concept, begin with retrieval or diagnosis instead.

### 9.3 Prefer retrieval and explanation over repeated passive rereading

Use short, low-stakes prompts that require learners to reconstruct an idea before seeing the answer: explain a mechanism from memory, reproduce a key equation and define its symbols, predict a tensor shape, or identify which assumption makes a claim valid.

- Ask for a reason or intermediate step when the objective is conceptual understanding.
- Give feedback that explains the correct reasoning and diagnoses common alternatives; a score or “correct/incorrect” marker alone is insufficient for difficult concepts.
- Let learners attempt an answer before revealing a worked solution. Do not hide essential caveats in the answer key.
- Revisit important ideas after a delay and mix earlier topics into later practice when the learner has enough initial fluency to make comparisons useful.
- Use confidence judgements selectively to help learners notice when fluency is mistaken for understanding; do not treat self-reported confidence as evidence of competence.

Retrieval practice, spaced practice, elaboration, concrete examples, and interleaving have substantial research support, but no single schedule or exercise format is optimal for every topic. Avoid prescribing exact spacing intervals without a defined retention goal and learner context.

### 9.4 Make mathematical understanding observable

For mathematical and computational topics, exercises should distinguish at least the relevant parts of the following:

- **Representation:** identify variables, dimensions, axes, units, domains, and conventions.
- **Procedure:** perform the algebraic or numerical operation correctly.
- **Interpretation:** explain what the result means in the LLM computation.
- **Conditions:** state assumptions and conditions under which the result holds.
- **Boundary:** provide a counterexample, limiting case, or failure condition.
- **Verification:** select an appropriate check and explain what it establishes—and what it does not establish.

A numerical check can catch an arithmetic or implementation error; it does not replace a derivation. A unit test establishes behavior for the cases and properties it covers; it does not prove a general theorem. A visual pattern does not establish causality. Preserve these distinctions in exercise instructions and feedback.

### 9.5 Specify an exercise before authoring it

For each substantial exercise, record the fields that are relevant:

- stable exercise ID shared by the French and English versions;
- learning outcome and target capability;
- essential prerequisites, with a reason for each;
- prompt, expected response format, and available tools;
- hints that reveal progressively more information;
- worked solution, including intermediate reasoning and assumptions;
- likely misconceptions and why tempting alternatives fail;
- assessment criteria or rubric, including numerical tolerance where appropriate;
- a changed-condition or transfer variant when it adds value;
- references or implementation/tests needed to verify the answer.

Do not add all fields mechanically to a one-line recall check. Keep the learner-facing activity concise while retaining enough information for another reviewer to validate its correctness.

### 9.6 Evaluate learning claims separately from content quality

Distinguish these evidence levels:

1. **Content review:** the explanation is scientifically and pedagogically coherent.
2. **Exercise validation:** prompts, solutions, distractors, and expected outputs have been checked.
3. **Immediate performance:** a learner can answer directly after instruction.
4. **Retention:** the learner can retrieve or apply the idea after a meaningful delay.
5. **Transfer:** the learner can use the concept in a materially different problem.
6. **Instructional effectiveness:** comparative evidence supports the claim that a teaching design improves outcomes for a defined population and context.

A published page, completed exercise, immediate quiz score, or positive impression does not establish durable mastery or instructional effectiveness. Do not claim that a strategy works for all learners based on general literature; state the scope of evidence and keep learner data collection proportionate, transparent, and privacy-conscious.

### Research grounding

- Weinstein, Y., Madan, C. R., & Sumeracki, M. A. (2018). [Teaching the science of learning](https://doi.org/10.1186/s41235-017-0087-y). *Cognitive Research: Principles and Implications*, 3, 2. A tutorial review of spaced practice, interleaving, retrieval practice, elaboration, concrete examples, and dual coding.
- Roediger, H. L., & Karpicke, J. D. (2006). [The Power of Testing Memory: Basic Research and Implications for Educational Practice](https://doi.org/10.1111/j.1745-6916.2006.00012.x). *Perspectives on Psychological Science*, 1(3), 181–210. Review of retrieval/testing effects and their educational implications.
- Dunlosky, J., et al. (2013). [Improving Students' Learning With Effective Learning Techniques](https://doi.org/10.1111/j.1539-6053.2013.01002.x). *Psychological Science in the Public Interest*, 14(1), 4–58. Comparative review of learning techniques and the conditions that affect their utility.


## 10. Standardize embedded learning checks

Every lesson page that includes a learner-facing comprehension check must use one recognizable structure in both languages. The check is a distinct instructional component—not an ordinary paragraph, a miscellaneous list, or a second conclusion.

### Shared presentation contract

- Use the canonical heading **“Vérifier sa compréhension”** in French and **“Check your understanding”** in English. Avoid competing variants such as “Questions de contrôle”, “Self-check”, or “Vérifier votre compréhension”.
- Wrap the complete activity in the `.self-check` Quarto div so the shared site stylesheet can give it a consistent visual boundary, spacing, and accessible contrast.
- Number questions consistently. Keep each prompt visually separate from its answer; use native `<details>` / `<summary>` disclosure for solutions, collapsed by default.
- Place a concise link near the start or end of the activity to the matching topic collection in the exercise hub (`exercises.qmd` / `../en/exercises.qmd`), using the collection's stable anchor. The link must be relevant to the topic, not a generic invitation to browse unrelated material.
- Do not add the component to a page when it would repeat an existing interactive investigation or when no meaningful check can be written. Do not confuse implementation verification, research checklists, or operational acceptance criteria with learner comprehension questions.

### Cognitive progression

Choose questions according to the learning objective, normally progressing from simpler retrieval to more demanding reasoning:

1. **Identify / retrieve:** define, distinguish, locate a quantity, or recall a condition essential to the concept. Use only when retrieval itself is useful.
2. **Explain / calculate:** reconstruct a mechanism, derive a step, calculate a small example, or predict a shape or output.
3. **Apply / diagnose:** change an input or assumption, compare alternatives, diagnose an error, or explain why a tempting answer fails.
4. **Transfer / critique:** apply the principle to a new context, identify a boundary case, challenge an overclaim, or state what evidence would be needed.

This is a progression of cognitive demand, not a mandatory four-question quota. Use two or three questions when that is sufficient; omit levels that do not fit the topic. Avoid artificial difficulty, trivia, ambiguous prompts, and questions that can be answered by copying a nearby sentence. Increase reasoning demand rather than linguistic complexity.

### Answer and feedback contract

- Keep answer keys collapsed by default and make each disclosure label identify which question it answers.
- Explain the reasoning and relevant intermediate steps; include units, tensor axes, conventions, assumptions, or numerical tolerances where relevant.
- Explain why a plausible misconception is wrong when it helps distinguish neighboring concepts.
- A correct numeric result without interpretation is insufficient when the learning objective includes interpretation.
- Distinguish what a hand calculation, numerical check, unit test, or thought experiment establishes—and what it does not establish.
- Keep embedded checks short and immediate. The exercise hub is for longer calculations, multi-step problems, transfer tasks, and integrated practice. Its status must remain honest: planned collections are not published exercises.

### Bilingual parity and review

French and English versions must test the same learning outcomes at comparable difficulty, with equivalent assumptions, data, answer reasoning, and links to the corresponding exercise collection. Wording may differ naturally. During review, check that every check is scientifically answerable, its solution is correct, all disclosures are closed by default, and the exercise link resolves to the intended anchor.
