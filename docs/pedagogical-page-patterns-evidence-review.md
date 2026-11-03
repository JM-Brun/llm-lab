# Evidence review: pedagogical page patterns for LLM Lab

**Status:** research synthesis; recommendations are provisional until tested against representative pages.  
**Reviewed:** 2026-11-03  
**Scope:** page-level explanations in a bilingual, web-published scientific and technical learning resource.

## Executive finding

There is **no generally accepted standard that prescribes one universal structure for a pedagogical page**. The relevant literature and guidance operate at different levels:

1. **Documentation architecture** distinguishes user needs and content genres (notably Diátaxis).
2. **Instructional design** aligns intended learning, learner activity, and evidence of learning (constructive alignment).
3. **Cognitive and educational psychology** provides conditional evidence about worked examples, retrieval practice, spacing, cognitive load, and learner expertise.
4. **Multimedia learning research** informs the relationship between prose, diagrams, labels, and visual attention.
5. **Accessibility standards** specify testable requirements for the rendered web content (WCAG 2.2), complemented by WAI authoring guidance and mathematical markup standards.

These are complementary, not interchangeable. A documentation taxonomy is not an experimentally validated learning theory; an empirical learning effect is not a page template; and an accessibility standard is not a pedagogy.

**Recommendation:** keep LLM Lab's page template as a soft composition model. Add evidence-informed decision prompts and validation criteria, not a mandatory sequence of headings. The most useful unit of consistency is the reader's ability to identify the page's purpose, follow its explanation, inspect the relevant evidence, and navigate to the right depth—not identical page outlines.

## 1. Evidence and authority taxonomy

Use the following labels when interpreting recommendations:

- **Normative standard:** a formal specification with testable conformance criteria (e.g. WCAG 2.2). It can justify requirements, not claims that a page teaches effectively.
- **Empirical finding:** an effect observed in experiments, reviews, or meta-analyses. Its strength, population, task, and boundary conditions matter.
- **Theoretical framework:** an explanatory model that generates useful design hypotheses (e.g. cognitive load theory or multimedia learning theory). Do not convert every principle into an unconditional rule.
- **Professional framework / heuristic:** a practical method for organizing work (e.g. Diátaxis). It can improve consistency and diagnosis without being a universal empirical standard.
- **Project convention:** a local decision adopted because it fits LLM Lab's goals and architecture. Keep it explicitly revisable.

## 2. Relevant frameworks and research

### 2.1 Diátaxis — classify the reader's need before choosing a page form

Diátaxis distinguishes four documentation needs and corresponding forms:

- **Tutorial:** learning-oriented, guided experience.
- **How-to:** goal-oriented instructions to accomplish a task.
- **Reference:** information-oriented, precise description.
- **Explanation:** understanding-oriented discussion of concepts, context, and reasons.

This is highly applicable to LLM Lab because a concept explanation, executable guided build, API-like reference, and practice activity should not be forced into the same page structure. The distinction also helps diagnose mixed-purpose pages.

**Evidence status:** mature professional documentation framework, not a controlled, empirically validated instructional-design standard. Use it as an information-architecture and editorial heuristic, not proof of learning gains.

**Project implication:** first classify the page's dominant job. LLM Lab's patterns (concept, algorithm, mathematical object, architecture, technique, overview, etc.) are useful scientific subtypes within that larger distinction. They should not compete with or replace the distinction between tutorial, how-to, reference, and explanation.

Sources: [Diátaxis](https://diataxis.fr/) · [Start here](https://diataxis.fr/start-here/) · [Applying Diátaxis](https://diataxis.fr/application/).

### 2.2 Constructive alignment — align the page's claim, activity, and check

Biggs' constructive alignment connects intended learning outcomes, learning/teaching activities, and assessment. The central idea is that learners must perform activities that elicit the intended understanding, and assessment should examine that same performance.

The original framework is designed primarily for courses and teaching units, not as a required micro-template for every web page. Its page-level adaptation should therefore be lightweight:

1. What should the reader be able to explain, calculate, distinguish, implement, or critique?
2. What part of the page gives them the concepts and worked reasoning needed?
3. What prompt or exercise would reveal whether they can do it?

A page does not need a visible “Learning outcomes” callout or a quiz in every case. If the page is a short reference entry, its purpose may be accurate retrieval rather than instruction. If a page makes several distinct claims, one generic self-check may not adequately assess them.

**Evidence status:** influential instructional-design framework grounded in constructivist learning and alignment principles. It is a design model, not evidence that adding outcomes boxes or quizzes mechanically improves every page.

Source: Biggs (1996), [Enhancing teaching through constructive alignment](https://doi.org/10.1007/BF00138871). See also [Monash's practical explanation](https://www.monash.edu/learning-teaching/teachhq/Teaching-practices/learning-outcomes/how-to/constructive-alignment).

### 2.3 Cognitive load, worked examples, and guidance fading

Cognitive load theory explains why the same explanation can help a novice and hinder an experienced learner. Working-memory demands depend on task complexity and prior knowledge. Research reviews identify several relevant effects:

- **Worked-example effect:** novices can learn more effectively from a complete worked solution than from immediately solving an equivalent unfamiliar problem.
- **Split-attention effect:** learners can be burdened when they must mentally integrate information separated across a page or display.
- **Guidance fading:** support that helps novices can become redundant as expertise grows.
- **Expertise-reversal effect:** an instructional treatment beneficial to less experienced learners can lose its benefit or become counterproductive for more experienced learners.

A 2023 meta-analysis of mathematics studies reported a medium average effect for worked examples (g = 0.48; 43 articles, 55 studies, 181 effect sizes). This result is promising but must not be generalized without qualification to every scientific topic, learner population, or online reading context.

**Project implication:**
- Include a worked example when it exposes a nontrivial procedure, derivation, numerical consequence, or implementation trace.
- Keep examples small enough to inspect and annotate intermediate steps.
- Where useful, follow a worked example with a completion prompt, prediction, or transfer question.
- Do not require a worked example for every conceptual or reference page.
- Do not keep repeating elementary scaffolding when the target audience is expected to know it.
- Integrate labels and explanations near the equation, diagram element, or code they explain; avoid forcing readers to shuttle between distant blocks.

Sources:
- Paas & van Merriënboer (2020), [Cognitive-Load Theory: Methods to Manage Working Memory Load in the Learning of Complex Tasks](https://doi.org/10.1177/0963721420922183).
- Kalyuga et al. (2003), [The Expertise Reversal Effect](https://doi.org/10.1207/S15326985EP3801_4).
- Kalyuga (2007), [Expertise Reversal Effect and Its Implications for Learner-Tailored Instruction](https://doi.org/10.1007/s10648-007-9054-3).
- Barbieri et al. (2023), [A Meta-Analysis of the Worked Examples Effect on Mathematics Performance](https://doi.org/10.1007/s10648-023-09745-1).

### 2.4 Retrieval practice and spacing — make verification cognitively meaningful

Dunlosky et al.'s review rates practice testing and distributed practice as high-utility techniques across a range of learning conditions and outcomes. Roediger and Karpicke's experiments show that retrieval can improve delayed retention more than repeated study, even when immediate restudy produces better short-term performance.

This supports active recall and problem-solving prompts, but it does not support adding a decorative quiz to every page. A question should require the reader to retrieve or use the intended idea, and its answer or feedback should resolve the reasoning rather than merely expose a letter.

A single self-check at the end of one page is **not** spaced practice. Spacing requires revisiting knowledge across time or later learning contexts; this belongs to the wider exercise/curriculum system, not just the page template.

**Project implication:**
- Use progressive questions where the content supports them: interpret → calculate/trace → diagnose a misconception → transfer to a new context.
- Prefer prompts that reveal a specific misconception or reasoning step over generic “Did you understand?” questions.
- Provide feedback or a worked rationale when an incorrect response could reinforce a misconception.
- Link to a dedicated exercise when practice needs multiple items, cumulative retrieval, or spaced revisiting.
- Treat self-checks as optional modules selected by the learning objective, not mandatory page furniture.

Sources:
- Dunlosky et al. (2013), [Improving Students' Learning With Effective Learning Techniques](https://doi.org/10.1177/1529100612453266).
- Roediger & Karpicke (2006), [Test-Enhanced Learning](https://doi.org/10.1111/j.1467-9280.2006.01693.x).

### 2.5 Multimedia learning — diagrams should reduce work, not add decoration

Mayer's research program and subsequent reviews distinguish ways to reduce extraneous processing (coherence, signaling, contiguity), manage essential processing (segmenting, pre-training), and support generative processing. A review of multimedia e-learning principles reports positive average effects for several principles, but effects vary with prior knowledge, material, and design conditions.

Useful design implications for technical pages:

- **Coherence:** remove decorative or tangential elements that compete with the explanation.
- **Signaling:** visually identify the step, variable, component, or relationship currently being explained.
- **Spatial contiguity:** place labels and explanatory text close to the diagram elements they describe.
- **Segmenting:** break a complex mechanism into meaningful steps rather than presenting an undifferentiated wall of detail.
- **Pre-training:** define essential component names and roles before asking readers to understand a dense system diagram.
- **Generative processing:** ask readers to predict, annotate, compare, or explain a visual relationship rather than merely view it.

Do not turn these into absolute rules such as “always add an image” or “always remove text.” In scientific content, a diagram may be indispensable; in other cases, a precise equation or prose explanation is clearer. The design should serve the learning objective.

Sources:
- Mayer (2017), [Using multimedia for e-learning](https://doi.org/10.1111/jcal.12197).
- Fiorella & Mayer (2021), [Principles for Reducing Extraneous Processing in Multimedia Learning](https://doi.org/10.1017/9781108894333.019).
- Mayer (2022), [Multimedia Learning](https://doi.org/10.1093/oxfordhb/9780199841332.013.18).

### 2.6 UDL — prompts for access and learner variability, not a rigid page recipe

CAST's Universal Design for Learning Guidelines 3.0 organize design considerations around engagement, representation, and action/expression. They encourage multiple ways to access information, build understanding, interact, and communicate.

This is useful as a lens for identifying barriers in a technical learning resource: dense notation without explanation, diagrams with no equivalent, interaction available only by pointer, or a concept conveyed through one representation only.

**Evidence status:** a research-informed design framework and set of prompts. It is not a web conformance standard, nor a reason to provide multiple redundant formats for every item. The relevant question is whether learners can access the essential information and perform the intended activity through supported means.

**Project implication:** preserve semantic HTML, text alternatives, keyboard support, and static/text equivalents for essential interactive information. Use multiple representations when they clarify a difficult concept or remove a barrier, not as a quota.

Source: [CAST UDL Guidelines 3.0](https://udlguidelines.cast.org/) and [About the 3.0 update](https://udlguidelines.cast.org/more/about-guidelines-3-0/).

### 2.7 WCAG 2.2 — normative requirements for the rendered page

WCAG 2.2 is a W3C Recommendation. It provides testable, technology-independent success criteria for accessible web content. It is the strongest normative reference in this review, but it governs accessibility, not pedagogical effectiveness.

Relevant criteria for LLM Lab include:
- text alternatives for non-text content (1.1.1);
- information and relationships, meaningful sequence, and sensory characteristics (1.3.1–1.3.3);
- use of color and contrast (1.4.1, 1.4.3, 1.4.11);
- text resize and reflow (1.4.4, 1.4.10);
- keyboard access and no keyboard trap (2.1.1–2.1.2);
- page titles, focus order, link purpose, headings/labels, visible and unobscured focus (2.4.x);
- language of page and parts (3.1.1–3.1.2);
- name, role, and value for UI components (4.1.2).

For complex scientific diagrams, WAI guidance recommends a short identification plus a longer text equivalent that conveys the essential information, data, or relationships. A generic alt string such as “diagram of attention” is not sufficient when the diagram itself carries a substantial part of the explanation.

For mathematical content, MathML is a W3C technology for representing mathematical structure and content. MathML Core is currently a Candidate Recommendation Snapshot (24 June 2025), not a W3C Recommendation; do not mislabel its current status. Quarto/MathJax output should be tested with actual browser and assistive-technology combinations rather than assumed accessible from source syntax alone.

**Project implication:** keep WCAG conformance checks separate from editorial review. Passing a Quarto build does not establish WCAG conformance; an alt attribute's presence does not establish that its text is equivalent; and source-level semantics do not prove keyboard or screen-reader behavior.

Sources:
- [W3C WCAG 2.2 Recommendation](https://www.w3.org/TR/WCAG22/).
- [WAI Images Tutorial](https://www.w3.org/WAI/tutorials/images/), including [complex images](https://www.w3.org/WAI/tutorials/images/complex/).
- [WAI Writing for Web Accessibility](https://www.w3.org/WAI/tips/writing/).
- [W3C MathML Core](https://www.w3.org/TR/mathml-core/).
- [Section 508: Accessible equations and formulas](https://www.section508.gov/create/accessible-equations-formulas/).

## 3. What this means for LLM Lab's current soft-target model

The existing model's three layers remain a sound editorial architecture:

- **Shared orientation:** supports page purpose and reader orientation. Keep it concise; do not force a separate learning-outcomes box or scope section where the opening already does the job.
- **Optional explanatory modules:** choose by the page's dominant learner question and the type of reasoning required. Worked examples, derivations, diagrams, implementation, limitations, and exercises are conditional modules.
- **Optional depth:** use progressive disclosure for genuinely secondary detail. Do not hide assumptions, definitions, or caveats required to interpret the main claim.

The page-pattern families are not a replacement for documentation genres. A mathematical concept page can be an explanation; a guided implementation can be a tutorial or how-to; an API contract is reference; a synthesis page may be explanation or orientation. The dominant page job should determine the form before the topic-specific pattern determines which explanatory modules are useful.

## 4. Recommended lightweight decision protocol

For each new or substantially revised page, ask:

1. **Reader need:** Is this a tutorial, how-to, reference, explanation, or a deliberate hybrid? What question brought the reader here?
2. **Outcome:** What should the reader be able to do or distinguish after the core explanation?
3. **Prior knowledge:** Which terms and operations can be assumed? Which must be introduced? Could a worked example help a novice, or would it repeat material for the intended audience?
4. **Explanation:** What is the minimum causal/mechanical chain that makes the main claim understandable? Which representation (prose, equation, diagram, code, table) carries it most clearly?
5. **Practice:** What question would expose a likely misconception or demonstrate transfer? If no meaningful check fits, omit it or link to a better exercise.
6. **Depth:** Which details are optional, and which assumptions or caveats must remain visible?
7. **Accessibility:** Can the essential information be perceived and operated without relying on color, pointer-only interaction, or an image without an equivalent?
8. **Evidence:** Which claims need primary/official sources, tests, or experimental context? What validation has actually been performed?

Use these as prompts, not a score. Record a reason when a page intentionally departs from the usual pattern; do not demand a justification for every omitted module.

## 5. Practices to avoid

- A universal fixed sequence of headings applied to every page.
- Learning-outcome callouts that restate the title or cannot be assessed from the page.
- Decorative diagrams, stock illustrations, or image quotas disconnected from a learning question.
- Generic “check your understanding” questions that test only wording recall or repeat the exposition.
- Hiding essential assumptions, definitions, limitations, or caveats inside collapsed disclosures.
- Treating a page-level self-check as spaced practice.
- Applying novice scaffolding indiscriminately to advanced readers (expertise reversal).
- Claiming that a framework is “scientifically proven” as a whole when only selected principles have empirical support.
- Treating WCAG as a pedagogical quality score or treating a successful build as an accessibility audit.
- Treating all principles as universally beneficial regardless of subject, learner knowledge, and task.

## 6. Suggested changes to project documentation

1. Keep the current template as a soft target and make its non-prescriptive status explicit.
2. Add the distinction between **documentation purpose** (tutorial/how-to/reference/explanation) and **scientific page pattern** (algorithm, mathematical concept, architecture, etc.).
3. Add a compact alignment prompt: reader outcome → explanatory activity → meaningful check, without requiring visible outcome boxes or quizzes.
4. Add conditional guidance for worked examples and progressive fading based on prior knowledge.
5. Strengthen diagram guidance: every informative visual should answer a question; complex diagrams need an equivalent conveying their essential relationships, not just a generic caption.
6. Keep accessibility validation as a separate, evidence-recorded track (WCAG 2.2 AA target already adopted in the design system).
7. Pilot these prompts against representative bilingual pages before changing the template system or refactoring content.

## 7. Limits of this review

This is a targeted literature and standards scan, not a systematic review. Search coverage is not exhaustive; no protocol, dual screening, or formal risk-of-bias assessment was performed. Some sources are behind publisher access controls and were assessed from abstracts or institutional records. Effect sizes reported by individual reviews are context-specific and are not predictions of LLM Lab's own learning outcomes.

The next step is a representative audit of actual LLM Lab pages, including rendered FR/EN pages. That audit should test whether the principles above identify real problems and useful changes; it should not assume that every recommendation will apply.

---

## Bibliography and authoritative resources

- Barbieri, C. A., Miller-Cotto, D., Clerjuste, S. N., & Chawla, K. (2023). [A Meta-Analysis of the Worked Examples Effect on Mathematics Performance](https://doi.org/10.1007/s10648-023-09745-1). *Educational Psychology Review*, 35, 35.
- Biggs, J. (1996). [Enhancing teaching through constructive alignment](https://doi.org/10.1007/BF00138871). *Higher Education*, 32, 347–364.
- CAST. (2024). [Universal Design for Learning Guidelines 3.0](https://udlguidelines.cast.org/).
- Diátaxis. [A systematic approach to technical documentation](https://diataxis.fr/).
- Dunlosky, J., Rawson, K. A., Marsh, E. J., Nathan, M. J., & Willingham, D. T. (2013). [Improving Students' Learning With Effective Learning Techniques](https://doi.org/10.1177/1529100612453266). *Psychological Science in the Public Interest*, 14(1), 4–58.
- Fiorella, L., & Mayer, R. E. (2021). [Principles for Reducing Extraneous Processing in Multimedia Learning](https://doi.org/10.1017/9781108894333.019). In *The Cambridge Handbook of Multimedia Learning*, 185–198.
- Kalyuga, S. (2007). [Expertise Reversal Effect and Its Implications for Learner-Tailored Instruction](https://doi.org/10.1007/s10648-007-9054-3). *Educational Psychology Review*, 19, 509–539.
- Kalyuga, S., Ayres, P., Chandler, P., & Sweller, J. (2003). [The Expertise Reversal Effect](https://doi.org/10.1207/S15326985EP3801_4). *Educational Psychologist*, 38(1), 23–31.
- Mayer, R. E. (2017). [Using multimedia for e-learning](https://doi.org/10.1111/jcal.12197). *Journal of Computer Assisted Learning*, 33(5), 403–423.
- Mayer, R. E. (2022). [Multimedia Learning](https://doi.org/10.1093/oxfordhb/9780199841332.013.18). In *The Oxford Handbook of Educational Psychology*.
- Paas, F., & van Merriënboer, J. J. G. (2020). [Cognitive-Load Theory: Methods to Manage Working Memory Load in the Learning of Complex Tasks](https://doi.org/10.1177/0963721420922183). *Current Directions in Psychological Science*.
- Roediger, H. L., & Karpicke, J. D. (2006). [Test-Enhanced Learning](https://doi.org/10.1111/j.1467-9280.2006.01693.x). *Psychological Science*, 17(3), 249–255.
- W3C. (2024). [Web Content Accessibility Guidelines (WCAG) 2.2](https://www.w3.org/TR/WCAG22/).
- W3C WAI. [Images Tutorial](https://www.w3.org/WAI/tutorials/images/) and [Writing for Web Accessibility](https://www.w3.org/WAI/tips/writing/).
- W3C Math Working Group. (2025). [MathML Core — Candidate Recommendation Snapshot](https://www.w3.org/TR/mathml-core/).
