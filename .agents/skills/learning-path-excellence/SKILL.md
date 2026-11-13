---
name: learning-path-excellence
description: >
  Design, audit and improve LLM Lab's conceptual learning path so that every page
  serves both newcomers and experienced readers. Use when shaping page-level
  learning value, strengthening the whole route, benchmarking the best educational
  resources, adding high-level perspective or complementary insight, or avoiding
  a merely redesigned copy of existing LLM courses. Complements understand-path-audit:
  this skill defines the editorial ambition and value test; the audit skill checks
  the concrete reader journey, coherence and implementation.
---

# Learning Path Excellence

## Mission

Help make LLM Lab a genuinely distinctive, high-quality synthesis of the best ways
to understand large language models—not another course that repeats a familiar
table of contents with a different visual identity.

The path has two audiences at once:

1. **The newcomer or returning learner** needs a clear, accurate, welcoming route
   from first principles to a working mental model. No unexplained prerequisite,
   acronym, equation or hidden dependency should block the main explanation.
2. **The reader who already knows LLMs** should still discover something worth
   their time on every page: a sharper mental model, a useful abstraction, a
   non-obvious connection, a trade-off, a failure mode, a historical or systems
   perspective, a careful qualification, or a synthesis they are unlikely to get
   from a routine introductory explanation.

These are not two separate courses and not two competing layers of jargon. Build
one coherent explanation with progressive depth: an accessible core that is
substantive in its own right, plus meaningful perspective that rewards deeper
attention without obstructing the beginner.

## Activation contract

Use this skill when the task involves one or more of the following:

- Defining or revising the editorial ambition of the Understand / Theory path.
- Auditing whether individual pages offer distinctive value to both audiences.
- Improving a page beyond correctness and basic clarity.
- Comparing the best explanations, courses, visualizations, papers or tools for a
  topic and distilling their strongest pedagogical ideas.
- Deciding what belongs on a page, what should be deferred, and what should connect
  across the route.
- Reviewing the path as a whole for depth, coverage, narrative, cumulative insight
  and differentiation from existing learning resources.

For implementation-path dependencies, code correctness and build milestones, defer
to `.agents/skills/build-path-audit/SKILL.md`. For a detailed reader-journey,
transition, readability and rendered-experience audit, combine this skill with
`.agents/skills/understand-path-audit/SKILL.md`.

## Hard rules

### 1. One page, two levels of reward

Every substantive page must pass both tests:

- **Beginner test:** Can a motivated newcomer understand the central idea, why it
  matters to an LLM, how it works at the promised level, and what they should now
  be able to explain?
- **Experienced-reader test:** After reading the page, can someone who already
  knows the standard explanation name at least one useful new insight, sharper
  distinction, connection, caveat, trade-off or perspective they gained?

Do not satisfy the second test with an isolated "for experts" box containing
unrelated advanced facts. The deeper insight must illuminate the page's actual
subject and be connected to its core explanation.

### 2. Distinctive value, not novelty theatre

A page does not need an obscure fact or cutting-edge research result to be valuable.
A precise reframing, an elegant derivation, a well-chosen counterexample, an
important boundary condition or a connection between levels of abstraction can be
more valuable than novelty.

Do not add advanced material merely to look sophisticated. Every addition must
improve understanding, decision-making, transfer, or intellectual perspective.

### 3. Synthesize; do not imitate

Use external resources as a landscape of ideas, not as templates to copy.

- Identify what each strong source does particularly well: intuition, sequencing,
  visual explanation, mathematical treatment, implementation, experiment, critique,
  historical context or systems perspective.
- Extract the pedagogical principle and rebuild it in LLM Lab's own explanatory
  structure, language, examples and evidence.
- Attribute borrowed claims, ideas, figures, code and quotations appropriately.
- Check licences and reuse conditions before incorporating assets or code.
- Never imply that one source is definitive or that a collection of links is itself
  a synthesis.

The goal is a curated synthesis of complementary strengths, not a collage and not
a ranking exercise.

### 4. Preserve a coherent conceptual spine

Respect the canonical route, page ownership and project architecture. Do not
reorder stages, invent prerequisites, duplicate canonical explanations or create
new pages simply to accommodate every interesting idea. First ask whether an
insight belongs in the current page, an existing neighboring page, an optional
deep dive, a cross-cutting synthesis, or nowhere.

A page must explain the context needed for its own main argument. Links enrich the
journey; they do not substitute for essential definitions or reasoning.

### 5. Depth must be progressive and honest

Keep the main line readable. Introduce deeper content after the core mechanism is
understood, or make it clearly optional. Label approximations, assumptions,
idealizations, model-family differences, empirical evidence and open questions.
Do not present a teaching simplification as a universal property of all LLMs.

### 6. No page is exempt

Apply the dual-audience value test to every page, including overview, introductory,
mathematical, historical, synthesis and concluding pages. Introductory pages can
offer high-level perspective; technical pages can offer intuition and relevance.
Do not reserve all interesting insight for the end of the route.

## What counts as an experienced-reader contribution?

Choose the contribution that genuinely fits the topic. Examples include:

- **A higher-level model:** explain the role a mechanism plays in the whole system,
  not just its local operation.
- **A useful distinction:** separate concepts often conflated in popular
  explanations (for example, token identity versus contextual representation,
  logits versus probabilities, training-time versus inference-time behavior).
- **A trade-off:** show what a design choice buys, what it costs, and under which
  constraints it makes sense.
- **A boundary or failure mode:** show where the simple mental model stops working.
- **A connection:** relate the topic to optimization, information theory, geometry,
  statistics, systems engineering, cognitive science or another relevant field,
  without forcing analogies.
- **A derivation or invariant:** reveal why a formula or implementation behaves as
  it does, and what can be checked.
- **A historical perspective:** explain which problem a design addressed and what
  changed afterward, without turning the page into a chronology.
- **A family-level perspective:** distinguish what is specific to decoder-only
  Transformers, autoregressive language modeling, a particular training recipe or
  an implementation choice from what is more general.
- **An empirical perspective:** identify what experiments measure, what evidence
  supports a claim, what remains uncertain, and what a counterexample would look
  like.
- **A synthesis:** connect this page to several earlier mechanisms and show the
  larger pattern that emerges.

These are options, not a checklist. A page should usually develop one or two
strong contributions rather than mention all of them superficially.

## Decision gates

### Is the proposed addition worth keeping?

| Question | Keep it when… | Otherwise… |
|---|---|---|
| Does it answer a real learner question? | It resolves confusion or enables a new inference. | Remove or defer it. |
| Does it add value beyond a standard explanation? | It changes the reader's mental model or understanding. | Improve the framing or omit it. |
| Is it correctly scoped? | Assumptions and applicability are explicit. | Qualify or narrow the claim. |
| Is it placed well? | It follows the knowledge needed to understand it. | Move it or make it optional. |
| Is it supported? | Sources, derivations, tests or experiments support it. | Research or label uncertainty. |
| Does it belong here? | It strengthens this page's canonical purpose. | Link to the proper owner or defer. |

### How much depth should be exposed?

- **Core:** essential to understand the page's main claim; explain locally.
- **Enrichment:** valuable perspective that most readers can follow after the
  central explanation; integrate where it improves the narrative.
- **Deep dive:** mathematically, historically or technically demanding detail that
  is useful but not necessary for the route's main progression; disclose clearly.
- **Further exploration:** external resources, papers, implementations or
  experiments that invite independent study; explain why each is worth opening.

Do not use these labels mechanically. Use the project's established page patterns
and progressive-disclosure components where appropriate.

## Execution workflow

### 1. Establish the editorial and architectural context

Before proposing content:

1. Read the current canonical curriculum and route data.
2. Read the page's canonical purpose, audience, destination and concept ownership.
3. Read the relevant neighboring pages and existing deep dives.
4. Read the current editorial, template, design and source-attribution contracts.
5. Determine what is already implemented versus planned.

Use the current owners identified by the information architecture. At minimum, consult
the relevant parts of:

- `docs/learning-path.md`
- `data/guided-route.yml`
- `docs/content-section-mapping.md`
- `docs/information-architecture.md`
- `docs/reader-experience-and-editorial-method.md`
- `docs/page-template-system.md` and `docs/page-template-guide.md`
- `docs/annotated-references.md` and the relevant source audits
- `docs/roadmap.md` and `docs/project-status.md`

If a path has moved, find its current canonical owner. Do not create a parallel
editorial contract.

### 2. Define the page's unique learning promise

Write down, before editing:

- **Learner question:** What question brings a reader to this page?
- **Core understanding:** What should a newcomer understand after reading it?
- **Prior knowledge:** What may reasonably be assumed, and what must be recalled
  or explained locally?
- **Distinctive contribution:** What can an experienced reader gain here?
- **Exit capability:** What can the reader now explain, calculate, predict,
  compare or critically assess?
- **Handoff:** What question does this answer create for the next page?

If the distinctive contribution cannot be stated in one concrete sentence, the
page probably needs more than cosmetic editing.

### 3. Research the best available explanations

When external benchmarking is relevant, identify a small, topic-specific set of
high-quality resources. Prefer complementary sources over many near-duplicates:

- An intuitive or visual explanation.
- A rigorous mathematical or primary-source treatment.
- A clear implementation or worked example.
- An empirical, critical or systems-oriented perspective.

Not every page needs all four. Select based on the page's learning promise.

For each source, record:

- What it explains unusually well.
- Which learner difficulty it resolves.
- What assumption, limitation or blind spot it has.
- What pedagogical idea can be adapted.
- What must not be copied (expression, structure, protected asset or unsupported
  claim).

Prefer primary papers, official technical documentation and inspectable
implementations for factual verification. Use educational resources for teaching
ideas, not as the sole authority for contested technical claims. Verify freshness
when the subject changes quickly.

Do not claim to have reviewed a source that was not actually inspected. Distinguish
source-level reading from a quick search-result scan.

### 4. Build the explanation from the learner's question

A strong page will usually make the following journey possible, in a form suited to
its topic:

1. Orient the reader: why this question matters in an LLM.
2. Establish intuition: give a simple but non-misleading mental model.
3. Define the mechanism: explain the entities, operations and assumptions.
4. Make it inspectable: use a worked example, figure, equation, code fragment or
   experiment where it materially helps.
5. Interpret the result: explain what the mechanism enables and what it does not.
6. Add the distinctive perspective: connect, compare, qualify or challenge the
   simple model.
7. Check understanding: ask the reader to predict, derive, diagnose or compare
   something meaningful.
8. Hand off: make the next conceptual question feel earned.

This is a reasoning sequence, not a mandatory page template. Omit steps that do not
serve the page and use the project's established composition patterns.

### 5. Test both audiences explicitly

Run two short reading simulations.

**Newcomer simulation**

- Can the reader state the question being answered?
- Are terms and notation introduced before use?
- Can they follow the mechanism without opening several prerequisite links?
- Does the example actually demonstrate the claim?
- Can they explain the idea in their own words after the page?

**Experienced-reader simulation**

- What did the page add beyond a standard overview?
- Is the insight precise and non-trivial rather than merely more jargon?
- Does it reveal a connection, limitation, trade-off or implication?
- Does it sharpen an existing understanding or enable a new prediction?
- Is the advanced contribution supported and worth the reader's attention?

If either simulation fails, revise the page's content or framing—not just its
visual design.

### 6. Evaluate the whole path as a cumulative argument

Do not judge pages only as independent articles. Across the route, ask:

- Does each page make a necessary or clearly worthwhile contribution?
- Does the route progressively build a system-level model rather than a glossary
  of disconnected mechanisms?
- Are recurring ideas revisited with increased precision rather than repeated?
- Do later pages connect mechanisms that earlier pages introduced separately?
- Are there explicit moments of synthesis, comparison and reflection?
- Does the path distinguish core concepts from model variants and implementation
  choices?
- Are uncertainty, limitations, evaluation and failure modes part of the story,
  rather than an afterthought?
- Can a returning reader refresh their mental model efficiently?
- Can an experienced reader follow optional depth without being forced through
  elementary repetition?

Identify both local gaps and global gaps. A missing insight may be best addressed
by a small addition to an existing page, not a new chapter.

### 7. Make changes conservatively and validate them

When editing is requested:

- Prefer a small, high-leverage change to broad rewrites.
- Preserve useful examples, caveats, references, figures and exercises.
- Keep French and English versions substantively equivalent.
- Maintain canonical concept ownership and cross-page boundaries.
- Update canonical sources, not generated projections.
- Check citations, asset licences and attribution.
- Re-read the affected page in its neighboring context.
- Run relevant validators and render checks; state exactly what was run.
- Do not claim comprehension has been validated without learner testing.

## Page-level value record

For each audited page, maintain a concise record:

| Field | Required content |
|---|---|
| Page and role | Stable page ID, language paths and place in the route |
| Learner question | The question the page answers |
| Beginner outcome | The mental model or capability gained |
| Experienced-reader value | The specific deeper insight or perspective |
| Best-source contribution | What the strongest consulted resources teach well |
| LLM Lab synthesis | What is combined, clarified or improved here |
| Missing or weak element | Evidence and reader consequence |
| Proposed change | Smallest effective action and its canonical owner |
| Depth placement | Core, enrichment, deep dive or further exploration |
| Validation | Checks actually performed and remaining uncertainty |

A page is not complete merely because every field is filled. The record is a
diagnostic tool; quality comes from the explanation itself.

## Whole-path review matrix

Use a compact matrix to detect gaps and repetition across the route:

| Dimension | What to look for |
|---|---|
| Accessibility | Clear entry, defined terms, manageable cognitive load |
| Conceptual rigor | Correct mechanisms, assumptions, notation and caveats |
| Distinctive depth | Useful perspective beyond the standard introductory account |
| Synthesis | Connections across mechanisms and levels of abstraction |
| Evidence | Primary sources, derivations, reproducible examples or experiments |
| Transfer | Ability to predict, compare, diagnose and apply ideas |
| Narrative | Motivated progression and meaningful handoffs |
| Economy | No redundant explanations or decorative advanced material |
| Bilingual parity | Equivalent meaning, precision, examples and depth |
| Differentiation | A clear reason to read LLM Lab rather than a generic alternative |

## Output contract

Adapt the output to the task, but make the dual-audience goal explicit. For a page
review, report:

1. **Verdict:** whether the page serves both audiences.
2. **Beginner experience:** what works and what blocks understanding.
3. **Experienced-reader value:** what is genuinely enriching, what is missing, and
   why it matters.
4. **Best-of synthesis:** the strongest pedagogical ideas found in relevant
   resources, with sources and reuse boundaries.
5. **Concrete improvements:** prioritized edits, their placement and expected gain.
6. **Validation and uncertainty:** what was inspected, tested or not verified.

For a whole-path review, additionally report:

- The path's distinctive educational proposition.
- Which pages already provide strong dual-audience value.
- Pages that are clear but too conventional, or rich but too difficult.
- Missing cross-page connections and repeated material.
- The best opportunities for synthesis and high-level perspective.
- A prioritized, bounded improvement roadmap.

Avoid generic scores, claims of uniqueness without comparison, and praise that is
not tied to evidence. Separate observed strengths, hypotheses and recommendations.

## Completion criteria

A page meets this skill's ambition when:

- A newcomer can follow its core explanation without avoidable prerequisites.
- An experienced reader can identify a concrete, worthwhile gain.
- The deeper contribution is integrated with the topic, not bolted on.
- Claims, examples and sources are accurate and appropriately qualified.
- The page has a clear role in the cumulative route.
- Its depth is proportionate and progressively disclosed.
- It contributes to a distinctive synthesis rather than imitating one source.
- The French and English experiences preserve equivalent substance.

The whole path meets the ambition when every page passes the dual-audience test and
the route forms a coherent, cumulative explanation with meaningful synthesis,
without sacrificing accessibility, rigor or editorial economy.
