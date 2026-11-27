# The "why" and the "how" in the learning experience

**Status:** pedagogical and metadata design decision  
**Date:** 2026-11-27  
**Scope:** Theory / Understand route, concept metadata, source ingestion, page-level explanations, and reader-facing learning-map projections.

## 1. Decision

LLM Lab must teach both:

- **How:** how a concept, mechanism, mathematical operation, or architecture works.
- **Why:** what problem or need makes it useful, what motivates its introduction, and what it contributes to the larger understanding of an LLM.

The "why" is a complementary dimension of the existing learning experience. It is **not** a new mandatory section on every page, a replacement for technical explanations, or the organizing principle of every lesson.

The required invariant is more modest and more useful:

> For every important concept and every core learning step, the learner must be able to identify both how it works and why it matters, with the explanation placed where it best serves the learning task.

The existing technical explanation remains central where the lesson is about a mechanism, derivation, implementation, or experiment. The motivation should give the learner enough perspective to understand the problem being addressed and the role of the concept in the wider system.

## 2. What "why" means

The word "why" can refer to several different questions. They must not be collapsed into one generic field or one generic paragraph.

| Dimension | Question | Typical location |
|---|---|---|
| Problem motivation | What problem or limitation makes this concept useful? | Concept model; concise page introduction when useful |
| Design rationale | Why does this mechanism or design have these properties, rather than those of an alternative? | Concept explanation, comparison, or Deepen material |
| Architectural role | What does the concept contribute to the larger LLM computation or system? | Learning route, architecture overview, cross-concept explanation |
| Learning rationale | Why is this concept introduced at this point in the route? What gap does it address? | Learning route and transitions |
| Practical purpose | When does this concept matter in implementation, evaluation, or use? | Build, Practice, or application material |

Not every concept needs every dimension. Record and explain only the dimensions that are meaningful and supported by the sources or by a technically sound explanation.

In particular, do not confuse:

- why a mechanism is useful with a historical claim about why researchers originally invented it;
- why a learner studies a concept now with a computational prerequisite;
- why a component exists with a claim that it is universally necessary in every architecture.

Historical attribution requires evidence. Architectural motivations should be stated with appropriate qualifications and alternatives.

## 3. Relationship between "why" and "how"

The two dimensions complement one another; neither should mechanically dominate the other.

### How: mechanism and evidence

Depending on the page, the "how" may include:

- definitions, assumptions, and mathematical formulation;
- operations and data flow;
- diagrams and worked examples;
- implementation and code;
- experiments, tests, and observable consequences;
- limitations and edge cases.

### Why: motivation and perspective

The "why" may include:

- the problem being addressed;
- a limitation of a simpler or preceding approach;
- the property or capability the mechanism provides;
- its role in the architecture;
- relevant alternatives and trade-offs;
- the reason it appears at this point in the learning route.

The amount of explanation depends on the lesson. A short, precise sentence may be enough. A foundational architectural choice may deserve a deeper comparison. A page devoted to deriving a formula may keep the derivation as its main content and provide the motivation in a short introduction or in the route.

**Editorial rule:** explain the problem before or alongside the solution when doing so improves comprehension. Do not force a fixed "Why / How" template when another narrative structure is clearer.

## 4. Reader-facing learning route

The learning route must make the "why" identifiable even when the corresponding explanation is not repeated on the page itself.

For each important stage or core lesson, the route should help the learner answer:

1. What question or problem does this step address?
2. What will I understand or be able to explain after it?
3. Why does this step come here, given what I have already learned?
4. What does it prepare me to understand next?

A route entry may express this in a compact narrative, a question, a transition, or a short motivation. It need not display four separate labels or paragraphs.

A useful transition has the form:

problem or open question → concept introduced → new understanding or capability

This is an explanatory pattern, not a required sentence template.

The route must remain a coherent conceptual progression rather than a catalogue of isolated "why" statements. It must also preserve the existing distinction between:

- Theory / Understand: conceptual and scientific progression;
- Build: implementation dependency order;
- Deepen: optional advanced theory and technical detail;
- Practice & experiment: activities and evidence of understanding.

A "why" statement in the Theory route must not silently turn into a Build prerequisite or make optional Deepen material mandatory.

## 5. Concept metadata: enrich the existing model, do not create another ontology

The existing concept registry in data/concepts.yml remains the canonical source for stable concept identities, bilingual labels and definitions, domains, importance, resources, and typed semantic relations.

The motivation dimension should enrich this model only where it adds durable, reusable knowledge. It must not create:

- a parallel concept registry;
- a second general-purpose graph;
- duplicated page-level metadata;
- a large set of mandatory empty fields;
- a second curriculum model alongside docs/learning-path.md and data/guided-route.yml.

### 5.1 Candidate information to capture

The following is a **design vocabulary**, not a declaration that all fields must be added to the current YAML schema.

| Information | Meaning | Expected use |
|---|---|---|
| Problem / need | The problem the concept addresses | Motivation and source synthesis |
| Motivation | Why the concept is useful in the stated context | Route and page orientation |
| Rationale / trade-off | Why a design has particular properties or is preferred in a context | Deeper explanation and comparison |
| Contribution | What the concept makes possible or contributes | Architectural overview and transitions |
| Limitation | What it does not solve, or what trade-off it introduces | Scientific precision and comparison |
| Alternatives | Relevant alternative approaches | Only when comparison improves understanding |
| Evidence / provenance | Sources or reasoning supporting the statement | Traceability and editorial review |

Keep information concise, language-independent where possible, and attached to the stable concept identity. Localized reader-facing prose belongs in the appropriate localized projection or page, not in duplicated copies of the same fact scattered throughout the repository.

### 5.2 Learning-stage information

The rationale for learning a concept at a particular point belongs to the curriculum model, not to the concept definition itself.

The existing curriculum authority is docs/learning-path.md; the bilingual reader-facing route is projected through data/guided-route.yml. Stage-level or lesson-level motivation should be added to the existing structures after auditing their current schemas and generation path.

Potential information includes:

- the question addressed by the stage;
- the knowledge gap it resolves;
- why the stage follows the previous one;
- the understanding it makes possible next.

Do not duplicate concept motivation in every route entry. A route entry may refer to a concept's established motivation and add only the local reason for studying it at that point.

## 6. Relation semantics: keep the graph boundaries intact

The project already separates computational operations, semantic concept relations, curriculum dependencies, and editorial navigation. This decision preserves those ownership boundaries.

| Relationship | Meaning | Canonical owner |
|---|---|---|
| Computational data flow | An operation consumes, produces, transforms, or constrains computational values | data/computational-graph.yml |
| Semantic relation | A conceptual relationship between stable concepts | data/concepts.yml |
| Learning prerequisite / curriculum order | What knowledge is needed, and how the course is organized | docs/learning-path.md and its route projection |
| Editorial navigation | Page hierarchy and suggested reading transitions | Existing page-map metadata |

Motivation and enablement can be useful semantic interpretations, but they must not be added mechanically as new edge types. First check whether the existing concept-relation vocabulary can express the intended meaning accurately. If a genuinely new relation is required, document its semantics, direction, validation rules, and examples before using it.

In particular:

- a concept motivating another concept is not necessarily a computational predecessor;
- a concept enabling a capability does not automatically make that capability a mandatory learning step;
- page order does not establish computational order;
- computational order does not establish the best pedagogical order.

The "why" can often be expressed as structured concept properties and a short route explanation without introducing any new graph edge.

## 7. Source ingestion and knowledge modelling

Motivations should be captured as part of source ingestion and concept modelling, not reconstructed only after pages have been written.

The existing source workflow should progressively identify, where supported:

1. the problem or question addressed by a source;
2. the limitation or gap it identifies;
3. the proposed mechanism or approach;
4. the claimed benefits and the conditions under which they hold;
5. alternatives, trade-offs, and limitations;
6. evidence, citations, and the source's own framing.

During synthesis and concept modelling:

- compare how different sources motivate the same concept;
- distinguish shared explanations from source-specific claims;
- preserve disagreements and differences in scope;
- separate historical evidence, technical explanation, and editorial inference;
- retain provenance for claims that are carried into concept metadata or pages;
- avoid promoting an author's motivation into a universal explanation without corroboration.

A source may explain how a method works without explaining why it was chosen. In that case, record the missing motivation as unknown or requiring further research; do not invent it to complete a template.

## 8. Reader-facing editorial guidance

Use the least intrusive presentation that makes the motivation understandable.

Possible forms include:

- a sentence in the introduction that names the problem;
- a transition explaining what the previous concept could not yet explain;
- a short "Why it matters" subsection when the motivation deserves explicit treatment;
- a comparison with an alternative approach;
- a route-level explanation, with the page focused on the mechanism;
- a diagram showing the problem, the mechanism, and its contribution;
- a practical example showing when the concept changes an outcome.

Do not add a visible "Why" callout to every page. Do not repeat the same motivation in the route, introduction, callout, summary, and diagram. The route should provide orientation; the page should provide the explanation at the depth appropriate to its role.

### Illustrative examples

These examples show the intended distinction, not mandatory page copy.

**Embeddings**

- Why: token IDs are discrete identifiers and do not by themselves provide the vector representations used by neural-network operations. An embedding lookup supplies learned numerical representations.
- How: embedding matrix, token-ID lookup, vector dimensions, parameter learning, and the relationship to positional information.

Avoid saying that embeddings directly encode a complete or fixed semantic meaning. Their representations are learned and acquire their role through the model and training process.

**Self-attention**

- Why: a token's useful representation can depend on other positions in its accessible context. Attention provides content-dependent weighting and aggregation of information.
- How: Q/K/V projections, compatibility scores, scaling, masking where applicable, softmax, and weighted aggregation.

Avoid implying that attention alone explains all contextualization or that every Transformer architecture uses the same attention pattern.

**Causal masking**

- Why: an autoregressive next-token prediction at a position must not use future target tokens that would be unavailable at generation time.
- How: restrict future positions in the attention scores before normalization.

Distinguish the causal constraint from padding masks and other attention constraints.

**Cross-entropy / training loss**

- Why: the model's predictive distribution needs a quantitative objective that penalizes probability assigned away from the observed target and can be differentiated for learning.
- How: target log-probability, negative log-likelihood, token loss, masking/reduction, gradients, and parameter updates.

Keep observed-target scoring, evaluation, and training distinct; scoring a target does not itself update parameters.

## 9. Proportionality and quality criteria

The "why" should be proportional to pedagogical importance and to the role of the material.

| Material role | Expected treatment |
|---|---|
| Core concept or major architectural mechanism | A clear, accurate motivation must be identifiable in the concept model, the route, or the page; often more than one location is appropriate when each serves a distinct purpose |
| Core lesson / route stage | The learner can identify the question addressed and why the step belongs in the progression |
| Supporting concept | A concise motivation when it improves understanding; no forced paragraph |
| Deepen / reference page | Motivation may be brief or assumed from linked core material when the page's purpose is technical depth |
| Build milestone | Explain the practical or implementation purpose where it is not self-evident |
| Practice / exercise | State the skill or distinction being tested; do not repeat the full concept motivation |

A review should ask:

- Can the learner identify the problem or need behind each important concept?
- Is the explanation technically accurate and appropriately qualified?
- Does the route explain why the learner encounters the concept at this point?
- Does the explanation complement, rather than repeat, the "how"?
- Is the amount of motivation proportionate to the page's role?
- Are claims traceable to sources or clearly identified as synthesis?
- Are alternatives and limitations included when they materially affect the explanation?
- Does the presentation preserve the separate Theory, Build, Deepen, and Practice destinations?

Completeness does not mean every optional field is populated. It means the learner is not left with a major unexplained architectural choice or an unexplained transition in the core route.

## 10. Non-goals and safeguards

- Do not make "why" the dominant section on every page.
- Do not require a fixed "Why / How" page template.
- Do not reduce technical depth, mathematical rigor, implementation detail, or experiments to make room for motivation.
- Do not duplicate explanations across concept metadata, route entries, and pages.
- Do not invent historical explanations or universal design rationales.
- Do not add a parallel ontology, route registry, computational graph, or workflow.
- Do not turn motivation into a new prerequisite relation by default.
- Do not make optional alternatives or Deepen material mandatory.
- Do not infer that a concept is unimportant because its motivation is concise or located elsewhere.

## 11. Adoption and implementation sequence

This document establishes the editorial and modelling principle. It does not by itself change the current YAML schemas or generated pages.

Recommended implementation:

1. Audit the existing concept registry, relation vocabulary, curriculum model, guided-route schema, source metadata, and validators.
2. Identify the smallest compatible place for reusable concept motivation and route-specific learning rationale.
3. Define field semantics and validation only after confirming that existing structures cannot already represent the information.
4. Pilot the approach on a bounded set spanning different kinds of concepts: embeddings, self-attention, MLP, logits, cross-entropy, and teacher forcing.
5. For each pilot concept, trace the motivation from source ingestion through concept modelling to the route and the relevant page.
6. Review whether the motivation is discoverable, accurate, concise, and non-redundant in both French and English.
7. Only then extend the approach to the rest of the core route and decide whether tooling or automated checks are warranted.

**Acceptance condition:** a learner following the core route can explain both how its important mechanisms work and why they are useful or introduced at that point, without encountering repetitive mandatory "why" blocks or a second competing knowledge model.
