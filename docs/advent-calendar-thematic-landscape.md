# LLM calendar — thematic landscape and future story candidates

**Status:** editorial exploration; candidate reservoir, not an approved calendar  
**Scope:** thematic directions that may complement future LLM Lab calendar editions  
**Related decisions:** [2026 advent-calendar editorial redesign](advent-calendar-editorial-redesign.md) and [production handoff](advent-calendar-next-steps.md)

> This document extends the editorial strategy; it does not replace the approved 2026 slate, change the chronological production order, or authorize additional days. The current edition remains governed by the editorial redesign and its per-day acceptance gates.

## 1. Why maintain a thematic landscape?

The calendar is not a second, shortened version of the LLM Lab course. Its purpose is to make the scientific and intellectual territory around LLMs more visible: where their ideas came from, what phenomena they exhibit, which disciplines help us interpret them, what remains unexplained, and what consequences follow when they are used in real systems.

The main LLM Lab pathways answer questions such as:

- What does a language model compute?
- How are its components connected?
- How can a small model be implemented, trained, evaluated and experimented with?

A calendar story should instead open a question that benefits from a different lens: historical, linguistic, mathematical, statistical, experimental, philosophical, or sociotechnical.

The reader should leave with a reusable idea, not merely an anecdote or a simplified definition.

## 2. Relationship to the approved 2026 edition

The [2026 editorial redesign](advent-calendar-editorial-redesign.md) already defines an approved collection of 24 independent stories and chronological production. That decision remains authoritative.

The thematic families below are a **long-term discovery framework**. They help identify missing perspectives and future candidates; they are not a new taxonomy that every edition must fill.

Some current 2026 stories deliberately revisit concepts that also have canonical lessons (for example attention, normalization, cross-entropy, decoding or backpropagation). Their inclusion is justified only by a genuinely different question and treatment: a retrieval analogy, a statistical-mechanics connection, an information-theoretic interpretation, a numerical issue, or a worked mathematical derivation. The canonical lesson remains the technical reference; the story must not paraphrase it.

Therefore:
- do not remove or silently replace an approved 2026 story because a candidate appears in this document;
- do not add a twenty-fifth day or expand the current scope;
- do not infer a prerequisite from a story's day number or thematic family;
- use the candidate reservoir when planning a later edition, a standalone article, or a future replacement proposal that goes through explicit review.

## 3. Thematic families

### A. Origins and intellectual history

**Question:** Which earlier problems, theories and inventions made modern language models possible?

Possible directions:
- Shannon and the mathematical theory of information;
- Zipf and statistical regularities in language;
- Markov models and early probabilistic language modelling;
- prediction, coding and compression;
- Turing, early machine intelligence and the history of language processing;
- neural networks, perceptrons and the revival of backpropagation;
- the history of machine translation and statistical NLP;
- the evolution of attention mechanisms before the Transformer.

**Editorial value:** reconstruct the problem that motivated an idea, the alternatives available at the time, the evidence that changed the field and the limits of the historical analogy. Avoid a chronology that merely lists milestones.

### B. Language as a difficult object

**Question:** What makes human language irregular, ambiguous, culturally situated and difficult to represent?

Possible directions:
- polysemy, ambiguity and context;
- idioms, metaphor, pragmatics and indirect meaning;
- Zipf-like frequency distributions and the long tail;
- rare words, names, spelling variation and morphological richness;
- low-resource languages and uneven data coverage;
- code-switching, dialects and domain shift;
- what is lost when meaning is reduced to observable text.

**Editorial value:** use concrete linguistic cases to expose assumptions in data collection, representation and evaluation. Do not turn the story into a basic tokenization or embedding lesson.

### C. Mathematical and statistical phenomena

**Question:** Which mathematical ideas explain surprising behaviour in high-dimensional models and their data?

Possible directions:
- concentration of measure and high-dimensional geometry;
- the birthday paradox, collisions and finite representation spaces;
- heavy-tailed distributions, rare events and extreme values;
- Simpson's paradox and aggregation effects;
- double descent and the limits of simple bias–variance narratives;
- grokking and delayed generalization;
- scaling laws and the uncertainty of extrapolation;
- phase transitions and abrupt behavioural changes, where evidence supports the comparison.

**Editorial value:** make a phenomenon observable through a derivation, simulation or counterexample. State assumptions and distinguish mathematical results from empirical regularities and proposed explanations.

### D. Experimental discoveries inside trained networks

**Question:** What can experiments reveal about computations that are not obvious from the model's architecture?

Possible directions:
- mechanistic interpretability and circuit-level analysis;
- induction heads and copying/retrieval-like behaviours;
- superposition and polysemantic neurons;
- feature representations and sparse autoencoders;
- in-context learning as an empirical phenomenon;
- grokking and changes in internal representations;
- causal interventions, ablations and activation patching;
- the gap between a plausible explanation and a causally supported mechanism.

**Editorial value:** tell the story of an experiment: what was measured, what intervention was made, what alternative explanations remain and how far the result generalizes. Avoid presenting a visualization as proof of a complete explanation.

### E. Limits, paradoxes and philosophy

**Question:** What do LLM behaviours tell us — and not tell us — about intelligence, meaning, knowledge and understanding?

Possible directions:
- the Chinese Room argument and its critiques;
- the symbol-grounding problem;
- Moravec's paradox;
- competence versus robust performance;
- hallucination, truth and epistemic uncertainty;
- memorization versus generalization;
- compositionality, systematicity and out-of-distribution reasoning;
- whether benchmark success supports a claim about understanding.

**Editorial value:** distinguish philosophical arguments, behavioural evidence and empirical claims. Present positions in proportion to their arguments and evidence; do not manufacture a false scientific consensus.

### F. System design, tools and external information

**Question:** What changes when a language model is embedded in a larger system?

Possible directions:
- retrieval-augmented generation and external knowledge;
- memory architectures and information persistence;
- tool use, function calling and agent loops;
- planning, delegation and control;
- verification, execution feedback and self-correction;
- local models and constraints on deployment;
- latency, throughput, batching and serving trade-offs.

**Editorial value:** move beyond the isolated neural network and study interfaces, control flow, failure propagation and system-level reliability. Link to technical LLM Lab material where useful, without turning a story into a system implementation tutorial.

### G. Social, economic, legal and environmental consequences

**Question:** What happens when LLMs are trained, deployed and used at scale?

Possible directions:
- energy, water, hardware and inference costs;
- data provenance, copyright and consent;
- bias, representation and unequal error costs;
- automation, labour and changes in expertise;
- accountability and auditability;
- privacy, security and prompt injection;
- accessibility, language inclusion and public-interest applications.

**Editorial value:** use documented cases, public data, legal texts and empirical studies. Separate technical facts, legal interpretation, policy choices and value judgments. Avoid generic opinion pieces detached from evidence.

## 4. Initial candidate reservoir

The following candidates are deliberately **not assigned to days**. They are starting points for future research, not a commitment to publish every topic.

| Candidate question | Family | Distinct contribution to investigate | Main caution |
|---|---|---|---|
| Can a system manipulate symbols without understanding them? | Limits and philosophy | Reconstruct the Chinese Room argument and the strongest objections | Do not present a thought experiment as an empirical test of LLMs |
| How can symbols acquire meaning beyond their relations to other symbols? | Limits and philosophy | Examine grounding, embodiment and multimodal evidence | Avoid treating one definition of meaning as universally accepted |
| Why are some tasks trivial for humans but difficult for machines? | Limits and philosophy | Explain Moravec's paradox and its historical context | Avoid implying a fixed hierarchy of human and machine abilities |
| Why can a fluent answer be false? | Limits and philosophy | Separate hallucination mechanisms, uncertainty, verification and user reliance | "Hallucination" covers several failure modes; define the scope |
| Can we identify a small computational circuit inside a large network? | Experimental discoveries | Follow a mechanistic-interpretability experiment from hypothesis to intervention | A circuit found in one model or task may not generalize |
| Why can one neuron participate in representing several features? | Experimental discoveries | Explain superposition and polysemanticity with a controlled toy model | Avoid equating individual neurons with human-readable concepts |
| Can a model learn an algorithm from examples in its prompt? | Experimental discoveries | Study in-context learning and competing explanations | Distinguish observed behaviour from claims about the model's internal algorithm |
| What does a model's ability to use a tool actually demonstrate? | System design | Separate language generation, action selection, execution and feedback | Do not conflate a tool call with reliable agency |
| Does external memory make a model know more? | System design | Compare parameter knowledge, retrieval, provenance and freshness | Retrieval success does not guarantee correct synthesis |
| What does one generated answer cost in compute and energy? | Consequences | Trace system boundaries and compare measurement methods | Report workload, hardware, utilization and allocation assumptions |
| Can a benchmark measure reasoning rather than familiarity with its examples? | Limits and evaluation | Study contamination, construct validity, robustness and alternative tests | Avoid claiming that all benchmarks are invalid |
| Why do rare cases dominate some deployment failures? | Language and statistics | Connect long tails, coverage gaps and risk-weighted evaluation | Do not assume frequency alone determines impact |
| How does language-resource inequality propagate into model quality? | Language and society | Connect corpus coverage, annotation, evaluation and downstream use | Avoid reducing language quality to corpus size alone |
| When does a scaling curve stop being a useful forecast? | Mathematics and statistics | Examine extrapolation, regime changes and uncertainty | No empirical scaling law is universal |
| How can a model appear to improve suddenly after long training? | Mathematics and statistics | Reconstruct grokking experiments and proposed explanations | Separate the original setup from later generalizations |
| What can a causal intervention tell us about a neural network? | Experimental discoveries | Contrast correlation, ablation and activation patching | Interventions can introduce distribution shifts or artifacts |

## 5. Candidate qualification: a decision, not a popularity contest

Before a candidate is selected, create a short dossier answering:

1. **Narrative question:** what precise question will the story answer?
2. **Disciplinary origin:** where does the idea come from?
3. **Evidence-bearing event:** what discovery, experiment, controversy or counterexample carries the story?
4. **Conceptual payload:** what should the reader be able to explain or apply afterward?
5. **LLM connection:** which concrete model behaviour, design choice or deployment question is illuminated?
6. **Canonical overlap:** which LLM Lab pages already cover nearby concepts?
7. **Complementary delta:** what will the story add that those pages do not?
8. **Demonstration:** what calculation, simulation, intervention, dataset or primary-source analysis makes the idea inspectable?
9. **Limits:** what does the evidence not establish?
10. **Sources and rights:** are primary/authoritative sources and reusable media available?
11. **Audience and prerequisites:** can the story stand alone for the intended reader?
12. **Decision:** explore, select, merge, defer or reject — with a short reason.

### Hard rejection or reformulation conditions

Reject or reformulate a candidate when:
- its only contribution is to restate a canonical lesson in simpler language;
- its link to LLMs is decorative rather than explanatory;
- its central claim has no adequate evidence or is too contested to present responsibly;
- it depends on unexplained specialist prerequisites that cannot reasonably be introduced;
- it repeats another story without a distinct question or demonstration;
- its proposed visual or analogy carries the argument but cannot be validated.

## 6. Composition principles for future editions

- Select a coherent set of questions, not one story from every family.
- Mix disciplines and narrative forms: historical reconstruction, mathematical puzzle, empirical experiment, case study, critical debate and system investigation.
- Avoid long runs of stories that reproduce the order of the LLM Lab curriculum.
- Preserve independence for readers. Numerical order may guide production and browsing, but it does not create prerequisites.
- Prefer a small number of well-evidenced stories over filling a quota with weak topics.
- Keep the story's scientific or intellectual question central; the LLM connection should be substantive but need not dominate every section.
- Make the transfer explicit: what new question can the reader now ask in another context?
- Reassess the candidate reservoir when the canonical curriculum or the state of LLM research changes.

## 7. A practical overlap audit

Use the following classification when comparing a candidate with LLM Lab:

| Overlap class | Meaning | Editorial response |
|---|---|---|
| Direct duplication | Same question, same concepts, same explanation and same example | Do not select as a calendar story |
| Same concept, new lens | A canonical concept is examined through a different discipline, historical episode or mathematical derivation | Potentially valid; make the new lens the actual subject |
| Adjacent phenomenon | The story examines a related behaviour, failure or consequence not taught in the canonical page | Usually promising; link to the canonical page only as optional further reading |
| Outside the core model | The story concerns history, language, society, evaluation or deployed systems beyond the internal computation | Strong candidate if the LLM connection is meaningful |
| Research frontier | The story concerns active research with unsettled explanations | Select only with careful evidence grading and explicit uncertainty |

The audit should compare actual learning outcomes and examples, not just page titles or shared keywords. A story may reuse the same concept identifier without duplicating the canonical lesson.

## 8. Maintenance

This is a living editorial reservoir, not a frozen syllabus.

Review it when:
- a new calendar edition is planned;
- a candidate becomes outdated or its evidence changes;
- a canonical LLM Lab page changes enough to alter the overlap assessment;
- a published story already covers the proposed question;
- a major research result changes the interpretation of a topic.

For each selected candidate, retain the decision and its rationale so that future editors do not repeatedly reconsider rejected or already-covered topics.

## 9. Next step

Do not start drafting all candidates. First:

1. preserve the 2026 edition's approved slate and current Day 01 → Day 24 production sequence;
2. use this landscape to identify which perspectives are absent from that edition;
3. keep future candidates in a backlog with explicit overlap and evidence assessments;
4. after the current edition is stable, select a small, diverse set for the next editorial cycle;
5. review the selected set against the then-current LLM Lab curriculum and published stories.

**Editorial invariant:** the calendar must remain complementary to LLM Lab. It is a place to explore the scientific world around language models, not another way of traversing the same technical curriculum.
