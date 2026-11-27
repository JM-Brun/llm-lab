# Foundations: theoretical and mathematical architecture

**Status:** approved architectural direction; implementation not started  
**Decision date:** 2026-11-26  
**Scope:** a first-class, bilingual learning component for the mathematical and theoretical foundations of language models  
**Owner:** project architecture; detailed scientific content remains owned by its canonical learning pages

## 1. Decision

LLM Lab will introduce **Foundations — theoretical and mathematical foundations** as a first-class learning component.

It is not merely a subsection of Deepen and it is not a prerequisite gate that every reader must complete before using Understand or Build. It has its own entry point, coherent learning paths, explanatory pages and exercises, while remaining connected to the rest of the lab.

Mathematics is its central pillar. The scope may also include theoretical models and results needed to explain LLMs rigorously: probabilistic modelling, learning theory, neural-network theory, information theory, numerical analysis and the mathematical properties of Transformer architectures.

The component should let a learner move in both directions:

- from an LLM mechanism to the mathematical objects, assumptions, derivations and properties that explain it;
- from a mathematical concept to the LLM components and operations in which it is used.

The aim is not to turn LLM Lab into a general mathematics textbook. Selection and depth must remain motivated by understanding, reconstructing, implementing, evaluating and researching LLMs.

## 2. Why a separate component

The existing learning experience has several complementary purposes:

- **Understand:** build a conceptual explanation of what a model does and why.
- **Build:** reconstruct mechanisms through inspectable implementations and tests.
- **Deepen:** study advanced mechanisms, variants, limitations and research.
- **Practice & experiment:** exercise knowledge and test claims.

Mathematical development is transversal to all of them, but it has a distinct pedagogical purpose: define objects precisely, state assumptions, derive equations, prove or explain properties, analyse limitations, and verify results numerically.

Placing all this material under Deepen would make mathematics look like optional advanced commentary. Making it a separate component gives it a visible identity and its own progression without imposing it as a universal prerequisite.

## 3. Learning contract

A Foundations page should help the reader answer some or all of these questions:

1. What problem or LLM mechanism motivates this mathematical idea?
2. Which mathematical objects are involved, and what do the symbols mean?
3. What are the formal definitions, assumptions and conventions?
4. How is the relevant equation or result derived?
5. What does it mean geometrically, probabilistically, statistically or computationally?
6. What small numerical example makes it concrete?
7. Where does it appear in an LLM, and what does it enable?
8. What are its limits, edge cases, alternative formulations or deeper results?

Use this as a flexible editorial contract, not a mandatory eight-section page template. A page should include only the depth justified by its learning objective. Distinguish definitions, derivations, propositions, proofs, examples, numerical demonstrations and empirical observations. Never present an illustration or a passing test as a proof.

## 4. Subject landscape

The following is an initial taxonomy for discovery and audit, not yet a new controlled registry or a commitment to create every listed page.

### 4.1 Mathematical disciplines

**Linear algebra and geometry**
- Scalars, vectors, vector spaces, bases and dimensions
- Matrices, linear maps and matrix multiplication
- Inner products, projections, norms and distances
- Rank, low-rank structure, eigenvalues and decompositions
- Tensor notation and shape-aware operations

**Probability and statistics**
- Probability spaces, random variables and distributions
- Joint, marginal and conditional distributions
- Independence, expectation, variance and covariance
- Conditional modelling and sequential factorization
- Likelihood, estimation and maximum likelihood
- Sampling and statistical evaluation

**Calculus and differential analysis**
- Functions, composition, limits and derivatives
- Partial derivatives, gradients and Jacobians
- Chain rule and matrix calculus
- Taylor approximation and local sensitivity
- Convexity and curvature where relevant

**Information theory**
- Entropy and conditional entropy
- Cross-entropy and negative log-likelihood
- KL divergence and information gain
- Mutual information
- Coding, compression and perplexity

**Optimization**
- Objectives, constraints and regularization
- Gradient descent, SGD and mini-batch optimization
- Momentum, adaptive methods, Adam and AdamW
- Conditioning, stability and convergence
- Optimization geometry and generalization connections

**Numerical mathematics and scientific computing**
- Floating-point representation and rounding
- Numerical error, conditioning and stability
- Precision formats, quantization and approximation
- Matrix computation and computational cost
- Reproducibility and numerical verification

### 4.2 Theory and mathematical models of LLM components

The subject landscape should also be indexed by the model mechanisms to which the mathematics applies:

- Text, token IDs, discrete sequences and embeddings
- Positional representations and vector geometry
- Hidden states, projections and linear transformations
- Q/K/V, dot products, attention scores, masking and softmax
- Multi-head attention, residual transformations, normalization and MLPs
- Logits and conditional next-token distributions
- Autoregressive factorization, decoding and sampling
- Observed-target scoring, likelihood, NLL and cross-entropy
- Teacher forcing and sequence-level objectives
- Differentiation, backpropagation, gradients and parameter updates
- Optimizers, regularization, generalization and learning dynamics
- Numerical precision, quantization, scaling and efficiency

This second index is an application view, not a second copy of the mathematical subject taxonomy. One mathematical concept may support several mechanisms; one mechanism may depend on several mathematical concepts.

## 5. Relationship with the canonical LLM computation model

The mathematical component must align with the canonical computational spine documented in [canonical-computational-spine.md](canonical-computational-spine.md).

The shared prediction mechanism is:

\[
z_t = f_\theta(x_{<t}), \qquad
p_\theta(\cdot \mid x_{<t}) = \operatorname{softmax}(z_t).
\]

This supports distinct operational branches:

- **Generation:** a decoding policy selects a token from the conditional distribution and feeds it into a later context.
- **Observed-target scoring:** the probability of an observed target is selected to compute target and sequence log-probabilities.
- **Evaluation:** observed-target scoring is applied to held-out data and aggregated into metrics, without updating parameters.
- **Training:** target log-probabilities produce an objective; differentiation computes gradients and an optimizer updates parameters.

The Foundations component should explain the mathematics underlying these branches without flattening them into one linear execution path. In particular, likelihood and loss are not steps in ordinary generation; training and evaluation are not interchangeable; teacher forcing is a context policy; prefill/decode and KV cache describe inference execution.

The component should also preserve the Transformer computation boundary: Q/K/V projections occur inside each Transformer block from that block's input hidden states. They do not follow the final contextualized representations.

## 6. Relationship with existing knowledge architecture

Reuse existing canonical sources and relation semantics. Do not create a parallel ontology, graph, curriculum or metadata vocabulary.

| Information | Canonical owner | Foundations responsibility |
|---|---|---|
| Stable concepts, bilingual labels/definitions and typed semantic relations | `data/concepts.yml` | Add or refine mathematical concepts only after an inventory and concept-level review |
| Controlled domains and concept-domain membership | `data/domains.yml` | Reuse existing domains initially; propose a domain change only with a demonstrated classification need |
| Published learning content | `site/**/*.qmd` | Own the mathematical explanations and derivations in canonical pages |
| Page identity, language, level, destination and editorial metadata | Page-map metadata, governed by `docs/page-metadata-schema.md` | Classify Foundations pages using existing fields; do not add metadata dimensions casually |
| Curriculum modules and pedagogical prerequisites | `docs/learning-path.md` | Define a Foundations-specific progression only where the curriculum model can represent it without confusing it with computation |
| Reader-facing guided route | `data/guided-route.yml` | Integrate a route only after its scope and ownership are reviewed |
| Computational operations and dataflow | `data/computational-graph.yml` | Link mathematical explanations to the operations they formalize; do not turn mathematical prerequisites into computational edges |
| Implementation artifacts | `data/resources.yml` | Associate concrete notebooks, code and experiments only when they exist and have stable identities |
| Exercises and experiments | Practice & Experiment canonical model and page conventions | Keep substantial exercise collections separate from the main explanatory pages |

The knowledge graph, computational graph, pedagogical curriculum and page-navigation graph remain different models. A mathematical prerequisite is not automatically a computational dependency, semantic generalization or page hierarchy edge.

### Canonical page and concept ownership

A mathematical concept should have one canonical concept identity and one authoritative explanatory home at the appropriate level. Other pages should provide the context-specific derivation or application required by their learning objective and link to the canonical explanation; they should not reproduce the same general exposition.

Do not create a separate concept solely because the same mathematics appears in another LLM component. Conversely, do not overload a broad concept page with every application: keep the general mathematical treatment and the mechanism-specific application distinct but connected.

## 7. Relationship with the other learning components

- **Understand** introduces the mechanism and its intuition. It may link to a mathematical explanation when formal detail is useful, but should not become dependent on completing a Foundations route.
- **Build** uses the mathematical definitions, dimensions, invariants and numerical properties needed to implement and test the mechanism. Build remains implementation-led.
- **Deepen** explores advanced theory, variants, research results and limitations. Foundations supplies the formal tools; Deepen asks what follows from them and what remains unresolved.
- **Practice & experiment** owns growing exercise collections and practical investigations. Main Foundations pages should link to these rather than accumulating unbounded question banks.
- **Editorial collections** may tell independent stories about mathematical ideas, but must reference canonical Foundations concepts and pages rather than creating competing definitions.

## 8. Suggested learning paths

These are candidate paths to validate against the current curriculum and concept registry:

1. **Mathematics essentials for LLMs:** vectors, matrices, products, norms, functions, probability and derivatives needed to follow the core model.
2. **Mathematics of the Transformer:** embeddings, projections, attention, softmax, residual transformations, normalization and MLPs.
3. **Mathematics of probabilistic prediction and learning:** conditional distributions, likelihood, cross-entropy, sequence objectives, gradients, backpropagation and optimization.
4. **Advanced theory of language models:** approximation and expressivity, generalization, overparameterization, learning dynamics, scaling laws, representation geometry, information and compression.

These are not yet approved route definitions. Their prerequisites, overlaps, entry points, optional branches and expected outcomes must be audited before they are added to `docs/learning-path.md` or the guided-route projection. The fourth path is research-oriented and should not be treated as a prerequisite for building or understanding a small GPT.

## 9. Initial pilot

Do not begin with a large page-production effort. First audit current pages, concepts, resources, exercises and code for mathematical coverage, quality and ownership.

A possible small pilot, subject to that audit, is:

- vectors and matrix operations;
- dot products and similarity;
- conditional probability and probability distributions;
- softmax;
- entropy, cross-entropy and negative log-likelihood;
- derivatives, gradients and the chain rule.

The pilot should test the complete learning contract across different kinds of mathematics. It should include at least one worked derivation, one hand-computable numerical example, one implementation or numerical verification, and links to the relevant LLM mechanisms. Avoid creating a new page where an existing page can be upgraded cleanly.

## 10. Page quality and scientific standards

Foundations content must meet the project's scientific and editorial standards:

- Define notation, tensor shapes, index conventions, domains and assumptions.
- Check dimensional consistency and distinguish scalars, vectors, matrices and higher-rank tensors.
- Derive equations step by step where the derivation is pedagogically important.
- State whether a claim is a definition, identity, proposition, theorem, approximation, heuristic or empirical observation.
- Include counterexamples and boundary cases when they prevent common misconceptions.
- Separate mathematical equivalence from numerical equivalence and implementation convention.
- Use small examples that can be checked independently; provide reproducible code only when it adds value.
- Cite primary or authoritative sources for nontrivial claims and preserve provenance and licensing for reused figures, code and explanations.
- Validate rendered LaTeX in both French and English, including mobile layout.
- Keep translations mathematically equivalent: notation, assumptions, caveats and derivation steps must agree.

## 11. Decisions and non-goals

### Adopted

- Foundations is a first-class component, separate from Deepen.
- Its central focus is mathematics; relevant theoretical models and results may be included.
- It has its own entry point and candidate learning paths.
- It is transversal and linked to Understand, Build, Deepen and Practice & Experiment.
- It reuses canonical concepts, resources, computational relations and page metadata rather than creating parallel systems.
- The work begins with an audit and ontology/relationship design, not mass page creation.

### Not decided yet

- The final public-facing label and French/English navigation wording.
- The physical directory and Quarto navigation structure.
- Whether any existing controlled domain needs to be extended or reclassified.
- The exact route definitions, prerequisites and mapping to the existing curriculum.
- The first pages to create or substantially revise.
- Whether dedicated mathematical exercise pages need a separate index or can use existing Practice conventions.

### Explicit non-goals

- A general-purpose mathematics curriculum unrelated to LLM learning.
- A mandatory mathematics gate before Understand or Build.
- A duplicate concept registry, mathematical graph, page taxonomy or computational graph.
- A second optimizer/training explanation copied across several locations.
- A mass migration or page creation before inventory and dependency analysis.
- A heavyweight ontology, database or workflow framework without a demonstrated need.

## 12. Implementation plan and hand-off

Work in the following order. Update this document as decisions become evidence-backed.

### Phase 1 — Audit existing coverage

- Inventory mathematical explanations, equations, derivations, exercises, code and references in the current bilingual site.
- Inspect `data/concepts.yml`, `data/domains.yml`, `data/resources.yml`, `data/computational-graph.yml`, `docs/learning-path.md` and the guided route.
- Map each relevant concept to its canonical page(s), LLM mechanism(s), implementation/resource(s), and existing exercise(s).
- Identify missing concepts, duplicated explanations, incorrect or underspecified mathematics, broken prerequisites and inconsistent notation.
- Record evidence and confidence; do not infer that a concept is absent merely because its label is missing.

### Phase 2 — Mathematical concept model and relations

- Reuse stable concept IDs where they already exist.
- Propose only missing concepts with clear definitions, scope and bilingual labels.
- Distinguish mathematical prerequisite, generalization, application and implementation relations; use the existing relation vocabulary where semantically valid.
- Keep curriculum prerequisites in the curriculum owner and computation edges in the computational registry.
- Review whether the existing domain model can classify this component without introducing a competing taxonomy.

### Phase 3 — Navigation and curriculum design

- Define the component landing page and its relationship to the site's existing Understand/Build/Deepen/Practice navigation.
- Validate the candidate paths against actual prerequisites and learner goals.
- Decide page destinations, level conventions, FR/EN parity and page-to-page orientation using existing metadata contracts.
- Integrate route projections only after the canonical curriculum decisions are stable.

### Phase 4 — Pilot and validation

- Select a small set of existing pages to improve and only the missing pages needed to test the architecture.
- Validate mathematical correctness independently of code tests.
- Check worked examples, numerical verification, references, rendered equations, bilingual parity, accessibility and mobile behavior.
- Gather evidence that a learner can move between intuition, formalism, implementation and application without unnecessary repetition.

### Phase 5 — Progressive extension

- Extend coverage by demonstrated gaps and dependencies, not by filling a predetermined catalogue.
- Add deeper theoretical material when it supports a clear learning or research objective.
- Keep exercise growth in Practice & Experiment and preserve clear links from each Foundations page.

### Acceptance criteria for the component

The component is ready for public navigation when:

1. It has a clear purpose, entry point and scope in both languages.
2. Its initial inventory and concept relationships have been reviewed.
3. Its learning paths have explicit outcomes and justified prerequisites.
4. Each pilot concept has one canonical identity and a clear content owner.
5. Links to Understand, Build, Deepen and Practice are useful and non-duplicative.
6. Mathematical claims, derivations, examples and notation have been reviewed.
7. FR/EN rendering, navigation, mobile layout and accessibility have been checked.
8. The maintenance workflow identifies where future concepts, pages, exercises and resources belong.

## 13. Session hand-off

**Current state (2026-11-26):** the architectural direction is approved by the project owner. This document records the decision and the proposed model. No Foundations pages, navigation entries, route stages, new mathematical domains or registry migrations are claimed to have been implemented by this decision alone.

**Next action:** perform Phase 1 as a read-only audit. Start with the existing concept registry and current bilingual pages, then inspect the computational graph and curriculum. Return an evidence-backed coverage matrix and a proposed canonical concept/relation delta before changing page content or navigation.

The audit should explicitly reconcile this component with [the information architecture](information-architecture.md), [the learning path](learning-path.md), and [the canonical computational spine](canonical-computational-spine.md). Preserve the project's rule: one canonical owner per kind of information, with reader-facing routes and graphs generated as projections rather than competing sources of truth.


## 14. Phase 1 audit hand-off (2026-11-27)

**Audit status:** source-level inventory and structural checks substantially completed; Phase 1 remains open pending rendered-site inspection and owner review. This section records the current evidence and the remaining work. It does not authorize content, registry, route or navigation changes.

### 14.1 Evidence-backed inventory

The following counts were checked against `main`:

| Item | Verified result |
|---|---:|
| Canonical concepts in `data/concepts.yml` | 125 |
| Concept domains in `data/domains.yml` | 6 |
| Concept-to-resource references | 394 |
| Stable page IDs reconstructed from Quarto sources | 315 |
| Unresolved resource references | 0 |
| Published pages in the learning-map projections | 153 FR + 153 EN |

Resource resolution must follow the actual page identity contract. In particular, `site/<lang>/exercises/<slug>.qmd` maps to the stable ID `<lang>/<slug>-exercises`; treating every resource ID as a direct `site/<id>.qmd` path produces false missing-file reports.

A targeted sample of 42 mathematical/theoretical pages (21 FR/EN pairs) was also inspected:

- all 42 pages exist in the generated learning-map projections;
- the compared `topic`, `type`, `destination`, `level` and `domain` metadata agree across the 21 language pairs;
- local file targets checked in the sample resolve;
- representative anchors were checked against source headings or route-generated fragments;
- the 18 pages not listed directly in `concepts.yml.resources` have editorial relationships or optional-route roles. They are not 18 registry errors and must not be associated mechanically.

The 18 pages are: `attention-score-scaling`, `cosine-similarity`, `embedding-linearity` / `linearite-embeddings`, `entropy-synthesis` / `synthese-entropie`, `experience-information-theory`, `mathematical-foundations`, `queries-keys-values-advanced`, `scaling-laws` and `tensors`.

These results are a targeted audit, not a claim that every mathematical statement on every site page has received a scientific review.

### 14.2 Coverage findings to carry into Phase 2

**Already explained in canonical LLM-oriented pages:** embeddings and contextual representations; Q/K/V and attention operations; categorical next-token distributions; likelihood, log-likelihood, NLL, cross-entropy and entropy; loss, gradients, partial derivatives in the loss calculation, chain rule and backpropagation.

**Still implicit, scattered or lacking a reusable general concept identity in the current inventory:**

- Linear algebra: vector, matrix, vector space, linear transformation, dot product and norm.
- Probability: random variable, general probability distribution, expectation, variance and covariance.
- Differential calculus: function/composition, derivative, partial derivative, Jacobian and chain rule as reusable mathematical concepts.
- Numerical analysis: floating-point representation, rounding, conditioning and general numerical stability.

These are candidate coverage gaps, not yet approved additions to the concept registry. The existing probability and gradient lessons explain LLM applications; they should not be mistaken for complete general introductions to probability theory or differential calculus. The tensors page is a technical reference about shapes and axes, not a general linear-algebra course.

**Specific concept candidate:** `scaling-laws` is the strongest candidate for a canonical concept identity: its page is a `concept-lesson` with an autonomous scientific objective, but the concept registry has no corresponding concept. Its scope and relations to model parameters, data, compute and loss still need a precise definition.

**Do not create automatically:** `tensor` and `cosine-similarity` require a granularity decision. The remaining unassociated pages are mainly deep dives, summaries, experiments or optional reading resources, not evidence of one missing concept per page.

The six existing domains appear sufficient for the pilot. No seventh domain is justified by the current evidence.

### 14.3 Architecture constraints confirmed

- The current page destination vocabulary is `orient`, `understand`, `build`, `deepen`, `practice` and `reference`; it has no `foundations` destination.
- Adding a new destination would require a coordinated change to the metadata contract, validator, learning-map builder/renderers and Quarto navigation/render configuration. Adding only a validator value would be incomplete.
- The current page-map `domain` field has a specific role for Deepen pages; it must not be silently repurposed as a general Foundations subject classification.
- `data/guided-route.yml` is the Understand route, not a generic route registry. Foundations must not be inserted as mandatory Understand stages.
- The concept relation model, pedagogical prerequisites, page graph and computational graph have distinct semantics. Only the existing `prerequisite` relation is currently suitable for directed pedagogical dependencies; mathematical objects must not be represented as computational operations.
- Existing ownership remains in force: #1554 for cross-registry inventory, #416 for concept-relation semantics, #575 for the canonical computational spine, and #1512 for the exercise-page model.

### 14.4 Confirmed source anomalies — defer changes until review

1. `site/fr/exercises-foundations.qmd` and `site/en/exercises-foundations.qmd` contain literal backslash-n sequences in the continuation-links paragraph before exercises 8 and 9.
2. `site/en/likelihood.qmd` contains doubled backslashes in `2^{\\bar{\\ell}}`, while the French source uses `2^{\bar{\ell}}`.
3. `attention-score-scaling` describes its derivation as relying on Gaussian assumptions, while the displayed variance derivation requires independence, centering and unit variance; Gaussianity is used for the simulation. The proof assumptions and simulation choice should be distinguished.

These are source-level findings. Fixes are intentionally deferred until the audit is reviewed and the implementation scope is approved.

### 14.5 Remaining work, in execution order

#### A. Close Phase 1 — rendered and scientific verification

- [ ] Inspect the published HTML for the 42-page sample when the Pages deployment is reachable. Record the deployment/version inspected.
- [ ] Verify rendered equations, equation numbering/references, diagrams and figures, captions, code blocks and cross-language notation.
- [ ] Test representative internal links and anchors in a browser, including route-generated anchors.
- [ ] Inspect responsive layouts at desktop and mobile widths; check horizontal overflow, equation clipping and diagram readability.
- [ ] Perform keyboard navigation and a focused screen-reader/accessibility pass on representative page structures.
- [ ] Review the scientific claims and derivations on the proposed pilot pages, distinguishing formal assumptions from illustrative or simulation choices.
- [ ] Review the coverage matrix and candidate gaps with the project owner. Mark each item as covered, partially covered, intentionally out of scope or approved gap, with source evidence and confidence.

**Exit condition:** the audit records both source-level and rendered-page evidence, and the project owner accepts the coverage findings. A successful Quarto build or metadata CI is necessary but does not satisfy this exit condition by itself.

#### B. Phase 2 — decide the minimal concept and relation delta

- [ ] For each candidate, write a scope statement, definition, bilingual labels, boundaries and LLM use cases before assigning an ID.
- [ ] Review the linear-algebra, probability and differential-calculus clusters for useful prerequisite order without forcing them into one linear course.
- [ ] Decide whether `scaling-laws` merits a canonical concept and define its scope and relations.
- [ ] Decide whether `tensor` and `cosine-similarity` deserve concept identities or remain applications/references.
- [ ] Reuse existing concepts and relation types wherever their semantics fit; coordinate any relation-model change with #416.
- [ ] Confirm domain membership using the six existing domains; coordinate cross-registry consequences with #1554.
- [ ] Keep all mathematical prerequisites out of `data/computational-graph.yml`.

**Exit condition:** a reviewed, minimal concept/relation proposal with no page-per-concept assumption and no duplicate registry.

#### C. Phase 3 — resolve the component/navigation representation

- [ ] Compare two explicit options: a coordinated `destination:foundations` extension, or a Foundations navigation projection that preserves existing destination semantics.
- [ ] For either option, enumerate every affected contract, validator, generator, renderer, navigation entry and bilingual page.
- [ ] Decide how subject/domain classification works without overloading the current Deepen-only page-map field.
- [ ] Define Foundations entry points and path objectives, prerequisites, optional branches and expected outcomes.
- [ ] Keep Foundations independent from the Understand guided route; do not make it a gate before Understand or Build.
- [ ] Coordinate any exercise links and collections with #1512.

**Exit condition:** a minimal architecture decision and migration plan accepted before implementation.

#### D. Phase 4 — pilot before broad rollout

- [ ] Select a small representative pilot from existing pages; prefer upgrading a canonical page over creating a duplicate.
- [ ] Test the learning contract with definitions, stated assumptions, derivations, hand-computable examples, numerical verification and explicit LLM applications.
- [ ] Have mathematical correctness reviewed independently from code/tests.
- [ ] Validate French/English equivalence, rendered LaTeX, links, accessibility and mobile behavior.
- [ ] Keep growing exercise banks in Practice & Experiment, linked from the explanatory pages.

**Exit condition:** the pilot demonstrates that a learner can move between intuition, formalism, implementation and LLM application without unnecessary duplication.

#### E. Phase 5 — progressive extension and maintenance

- [ ] Extend only from demonstrated gaps, learner needs and justified prerequisites.
- [ ] Add advanced theory when a specific learning or research objective warrants it.
- [ ] Document where future concepts, pages, exercises, code artifacts and references should be added.
- [ ] Re-run bilingual, metadata, link, rendered-equation and accessibility checks as part of normal content maintenance.

### 14.6 Current implementation boundary

No lesson page, source anomaly, concept, relation, domain, route, destination, renderer or navigation entry was changed by the Phase 1 audit. The documentation above records findings and work still to be done; it is not an implementation approval.

**Immediate next action:** complete the rendered-page and scientific review in section 14.5.A, then obtain explicit owner acceptance of the coverage matrix before starting the concept delta in Phase 2.
