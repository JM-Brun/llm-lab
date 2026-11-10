# Pilot audit: pedagogical page patterns and existing content

**Status:** source-level pilot completed; rendered review and implementation remain open.  
**Audit date:** 2026-11-03  
**Scope:** representative bilingual pages from concept, mathematical-objective, algorithmic mechanism, architecture comparison, and system-overview families.  
**Research basis:** evidence review in PR #283 (pending merge).

## 1. Executive summary

The sampled pages already show several strong pedagogical practices: precise page scope, explicit distinctions between commonly conflated quantities, worked examples, assumptions and failure cases, source provenance, implementation boundaries, and bilingual semantic alignment.

The main problem is **not that every page lacks the same sections**. The more important issue is that the repository has several overlapping layers of template guidance and page classification:

- the existing archetype guide and its separate overview, concept, reference, practice, and guided-build templates;
- the existing page metadata taxonomy (type tags) and LLM-LAB-PAGE-MAP;
- the new flexible composition model and scientific page-pattern families proposed in PR #278;
- Diátaxis documentation genres identified in the evidence review.

These layers can coexist, but their responsibilities and mapping are not yet explicit. Without a clear hierarchy, contributors may not know whether to choose a documentation genre, an existing page archetype, a scientific pattern, or all three. This is a maintainability and editorial-consistency risk.

**Recommendation:** do not rewrite sampled pages to match the new patterns. First consolidate the guidance architecture: distinguish the page's user-facing documentation job from its subject-specific explanatory pattern, and treat shared orientation / explanatory modules / optional depth as composition guidance. Then run a rendered pilot on one page from each distinct family.

## 2. Method and evidence boundary

### Sample selection

| Pair | Page family | Why selected |
|---|---|---|
| site/en/entropy.qmd / site/fr/entropy.qmd | Concept / mathematical quantity | Compact concept page with clear distinctions and a numerical example |
| site/en/cross-entropy.qmd / site/fr/cross-entropy.qmd | Mathematical objective | Dense page combining definition, derivation, implementation scope, training conventions, and checks |
| site/en/scaled-dot-product-attention.qmd / site/fr/scaled-dot-product-attention.qmd | Algorithmic mechanism | Worked matrix computation, diagram, numerical workbench, misconception checks, implementation and tests |
| site/en/transformer-architectures.qmd / site/fr/transformer-architectures.qmd | Architecture comparison / reference | Comparative taxonomy with scope boundaries and architecture/objective/task distinctions |
| site/en/transformer.qmd / site/fr/transformer.qmd | System overview | End-to-end explanation connecting components and routing to deeper pages |

This is a purposive pilot, not a statistically representative sample of the whole site.

### What was inspected

- Source QMD for the five FR/EN page pairs listed above.
- Existing guidance: docs/page-template-guide.md, docs/overview-page-template.md, docs/practice-page-template.md, docs/reference-page-template.md, docs/guided-build-page-template.md, and docs/page-metadata-schema.md.
- The proposed soft-target model and pattern families on the branch for PR #278.
- Existing ownership boundaries in issues #61 and #130.

### What was not verified

- The published site could not be opened through the available page-inspection route during this pass. No claim is made about actual rendered layout, mobile behavior, keyboard interaction, screen-reader behavior, or WCAG conformance.
- Quarto rendering, local-link validation, automated tests, and CI were not run as part of this source audit.
- No learner study or usability test was performed.

Keep these evidence types separate in subsequent updates. A source-level inspection is not a rendered-page audit.

## 3. Cross-cutting findings

### Finding A — Multiple template systems need an explicit hierarchy

The existing docs/page-template-guide.md already calls templates reusable starting points, but links to five separate archetype templates. Those documents contain numbered suggested structures. PR #278 adds a new flexible composition model and scientific page-pattern families, but does not yet fully explain how contributors should relate the new model to all existing archetypes.

The page metadata contract separately says that type is the stable editorial classification and points to docs/site-page-design-system.md as the implementation map. This is an important invariant: the new patterns should not silently create a second metadata taxonomy or an extra archetype field.

**Risk:** a contributor may infer that algorithm, concept, mathematical concept, overview, and tutorial/reference/explanation are competing categories. They answer different questions.

**Recommendation:**
1. Use one stable page metadata type for the page's primary editorial/delivery role, as already defined by the metadata contract.
2. Treat tutorial / how-to / reference / explanation as a user-need or documentation-genre lens, not as a new mandatory metadata field.
3. Treat algorithm / mathematical object / architecture / technology / overview as scientific explanatory patterns that select relevant modules.
4. Treat shared orientation, optional modules, and optional depth as the composition layer.
5. Map the existing overview, concept, guided-build, practice, and reference templates to this model; retire or simplify duplicated skeletons only after the mapping is agreed.

### Finding B — The strongest pages are not the ones with the most sections

Entropy is compact yet does its job: it defines the distribution, states bounds and assumptions, gives a numerical comparison, distinguishes predictive entropy from observed-token surprisal, explains temperature, states limitations, and provides a small self-check. It does not need a large diagram or an implementation section.

Cross-entropy and attention need more space because their mathematical and computational dependencies are more involved. Their length is justified by the distinct reasoning tasks they support, although each still needs a redundancy and rendered-density review.

**Recommendation:** assess page completeness against the learner task and the claims actually made, not against a count of template modules or page length.

### Finding C — Worked examples are valuable when they expose a nontrivial transformation

The sample includes useful numerical traces:
- entropy compares two distributions and their entropy values;
- cross-entropy connects a target probability to loss and derives the KL identity and logit gradient;
- attention traces Q/K scores through scaling, softmax, and value aggregation.

These examples make intermediate states inspectable. They are not generic filler. In contrast, a short concept page may need only one small example and a clear boundary.

**Recommendation:** preserve worked examples when they expose a calculation, algorithmic state transition, or causal mechanism. Where a page targets advanced readers, avoid repeating prerequisite arithmetic without a clear reason. Consider completion prompts or transfer questions after a worked trace.

### Finding D — Verification quality varies more than verification presence

The sampled pages use self-checks, but the best questions ask for interpretation or calculation:
- entropy asks the reader to distinguish distributional uncertainty from correctness and observed surprisal;
- attention asks the reader to calculate weights and reason about masking;
- cross-entropy asks about the averaging denominator and limits of perplexity.

This is preferable to generic recall. However, a self-check alone does not constitute spaced practice, and a page-level question should not be used as a proxy for a dedicated exercise set.

**Recommendation:** retain the existing distinction between a compact in-page self-check and a full practice page. Use a small progression where appropriate: interpret → calculate/trace → diagnose → transfer. Ensure the answer reveals reasoning and assumptions, not only the result.

### Finding E — Figures and code workbenches should be evaluated by their explanatory contribution

The attention page's diagram and numerical workbench have specific explanatory roles: the diagram separates scores, weights, and outputs; the code experiment tests the scale of random dot products. The cross-entropy figure isolates the effect of target probability on loss. The Transformer overview diagrams provide a system-level map.

**Recommendation:** for each visual or interactive element, record the question it answers and what it adds beyond adjacent prose. For complex diagrams, source-level fig-alt should convey the key relationship, but rendered accessibility still needs testing. A short generic alt string is not a sufficient equivalent for a dense scientific diagram.

### Finding F — Bilingual parity is substantive, not necessarily literal

The sampled FR/EN pairs largely preserve the same scope, mathematical assumptions, example logic, caveats, and learning checks while using natural language-specific phrasing. This is the correct target; literal sentence-by-sentence translation is not necessary.

Potential differences in localized asset names, links, decimal notation, or labels should be reviewed as semantic parity questions, not automatically treated as defects.

**Recommendation:** audit bilingual parity against claims, examples, notation, caveats, and learner outcomes. Do not require identical section counts if a language-specific wording change improves clarity.

## 4. Page-level findings

### 4.1 Entropy — compact concept pattern

**Strengths**
- The opening establishes the context and explicitly rejects the inference from low entropy to truth/reliability.
- The formal definition, finite-vocabulary bounds, logarithm base, and zero-probability convention are stated.
- The two-token example supports interpretation rather than merely repeating the equation.
- The distinction between predictive entropy, observed-token surprisal, and sequence negative log-likelihood is explicit.
- Temperature and calibration are treated with appropriate caveats.
- The self-check tests conceptual distinctions; the answers explain the reasoning.
- The FR/EN pages are closely aligned in scope and example.

**Potential refinements**
- The page does not need an additional learning-outcomes box, a diagram, or an implementation section by default; adding them would likely increase noise.
- The connection to cross-entropy and likelihood is useful, but should remain contextual rather than expand into a second derivation here.
- Verify the rendered equation spacing and narrow-screen line wrapping.

**Pattern fit:** concept / mathematical quantity, primarily an explanation.

### 4.2 Cross-entropy — mathematical objective with implementation boundary

**Strengths**
- The page distinguishes target distribution, predicted distribution, one-hot target, and batch-level reduction.
- The derivation of H(q,p) = H(q) + D_KL(q || p) includes assumptions and the infinite-value edge case.
- Token shift, padding masks, reduction, weighting, and tokenizer comparison are surfaced as distinct implementation concerns.
- The NumPy reference implementation's scope is explicitly bounded; the page does not imply that a row-wise classification loss is a complete sequence-training objective.
- The gradient derivation and numerical examples connect the local loss to optimization.
- FR/EN content preserves the same mathematical and implementation caveats.

**Potential refinements**
- This page combines several legitimate but substantial learning jobs: mathematical definition/identity, token-level language-modeling conventions, implementation scope, gradient interpretation, and perplexity. It may be near the threshold where a dedicated companion on token-level loss aggregation or gradients would reduce cognitive load. Existing canonical pages should be checked before splitting; do not split simply to shorten it.
- The self-check and the Further practice block both point toward exercises. The latter explicitly says detailed exercises are not yet written; verify whether this navigation placeholder is still useful or is redundant with the in-page self-check and site navigation.
- Check whether the Further practice wording accurately reflects the current exercise-page status at merge time.
- Rendered review should inspect the long derivations, figure, and nested disclosures together.

**Pattern fit:** mathematical concept + algorithm/training interface; primarily explanation, with reference-like implementation scope.

### 4.3 Scaled dot-product attention — mechanism and worked computational trace

**Strengths**
- The opening gives a concise mental model and explicitly states what softmax does not establish.
- The page separates scores, scaling, masking, normalization, and aggregation.
- Matrix shapes and a hand-checkable numerical example are provided.
- The scaling rationale states its simplifying distributional assumptions.
- The NumPy workbench tests the variance argument instead of presenting code as decoration.
- Misconceptions and a counterexample distinguish relative weights from semantic relevance and softmax from causality.
- Implementation and tests are linked with an explicit statement of what they verify.
- The French and English explanations are substantively aligned.

**Potential refinements**
- There are several navigation/signposting devices on one page: an epistemic badge strip, pipeline stepper, one-minute callout, concept connections, route cards, and language switch. Some may be useful, but the rendered page should be checked for repeated orientation and competing navigation hierarchies.
- The current editorial guidance discourages generic further-reading blocks and duplicated navigation. Prefer contextual links where they answer a specific question; check whether the stepper and route cards both add distinct value.
- The micro-workbench is a good example of an optional explanatory module, but its visual prominence and collapse behavior should be assessed against the page's intended first-pass reader.
- The mathematical statement about variance is explicitly conditional on independent, zero-mean, unit-variance components; preserve this qualification if the text is shortened.
- Check rendered syntax and keyboard behavior for custom HTML badges, stepper, workbench, and details disclosure.

**Pattern fit:** algorithmic mechanism / mathematical operation, with a tutorial-like worked trace; not a full tutorial because it does not guide the reader through building a complete artifact.

### 4.4 Transformer architectures — comparison/reference pattern

**Strengths**
- The opening differentiates the three major Transformer configurations without claiming they exhaust all sequence architectures.
- The comparison table exposes consistent dimensions: information flow, masking/attention, typical objectives, common uses, examples.
- Separate sections explain why each architecture fits particular kinds of tasks.
- A dedicated section distinguishes architecture, training objective, and use task, preventing a common category error.
- The scope boundary explicitly notes that Transformer is not synonymous with LLM.
- FR/EN versions use corresponding comparison logic and caveats.

**Potential refinements**
- The page has a reference/comparison function as well as an explanatory one. Keep the comparison table scannable and ensure each row's claims remain qualified as typical associations, not necessary pairings.
- A visual diagram may help if it reveals the information-flow difference more clearly than the table; do not add one unless it provides a genuinely different representation.
- Inspect table behavior at mobile widths and ensure meaning is not conveyed by color alone.

**Pattern fit:** architecture comparison; documentation genre is explanation/reference hybrid.

### 4.5 GPT/Transformer overview — system explanation

**Strengths**
- The scope is explicit: it traces the forward computation from tokens to logits and distinguishes the generation loop and parameter learning.
- The first diagram provides a system-level map; a second diagram compares attention and MLP roles.
- The page distinguishes token embeddings from contextualized representations and describes positional information.
- The learning outcomes align with the core explanation.
- It links to canonical concept pages where detail belongs, instead of deriving everything inline.
- FR/EN pages preserve the same conceptual distinctions.

**Potential refinements**
- The page has many potential onward links and several diagrams. Review the first-screen density and whether each link is anchored to a concrete learner question.
- The overview should not absorb detailed derivations or implementation details that have canonical deep-dive destinations.
- Keep parameter learning separate from the forward pass and generation loop; the opening already signals this distinction and should remain consistent throughout the page.
- The source's figure alternatives should be checked for equivalent information, especially where diagrams carry component relationships.

**Pattern fit:** system overview / explanation, with contextual links to component-level concept pages.

## 5. Guidance architecture: proposed responsibility map

| Layer | Question it answers | Existing or proposed owner | Should it create mandatory sections? |
|---|---|---|---|
| Documentation/user need | What is the reader trying to do: learn, perform, look up, understand? | Diátaxis lens; current page archetype guide | No |
| Stable editorial role | What kind of page is this in the site taxonomy? | page-metadata-schema.md and site-page-design-system.md | Metadata classification only; not an outline |
| Scientific explanatory pattern | What is the dominant subject-specific learner question? | Proposed page-patterns.md | No |
| Composition | Which orientation, explanation modules, and depth layers are useful? | Proposed page-template-system.md | No |
| Visual implementation | How are headings, callouts, figures, disclosures, and interactions presented? | design-system.md and shared SCSS | Reusable visual rules, not content quotas |
| Practice and evidence | How is the claimed understanding or behavior checked? | Practice template, exercises, tests, experiment protocol | Depends on page purpose; not every page needs an assessment |
| Accessibility | Can all readers perceive and operate the rendered content? | WCAG 2.2 and WAI guidance | Applicable requirements must be met; not a pedagogical outline |

## 6. Prioritized recommendations

### P0 — Resolve the guidance hierarchy before broader adoption

- [ ] Add an explicit mapping between documentation genres, current metadata/page archetypes, and scientific page-pattern families.
- [ ] State that the metadata type remains authoritative; do not add a second archetype field.
- [ ] Make the new flexible composition document the canonical explanation of how to choose and combine modules.
- [ ] Review existing overview-page-template.md, practice-page-template.md, reference-page-template.md, and guided-build-page-template.md so they become concise genre-specific supplements rather than competing full systems.
- [ ] Ensure page-template-guide.md points to one clear entry point and does not duplicate the same review checklist in multiple places.

### P1 — Pilot improvements on pages with clear evidence of benefit

- [ ] Use the entropy pair as the compact concept example: demonstrate that a short page can be complete without every module.
- [ ] Use the attention pair as the rich mechanism example: demonstrate a worked trace, conditional mathematical depth, meaningful visual, and implementation boundary.
- [ ] Use the cross-entropy pair to decide whether one page has too many distinct jobs or whether its current integrated structure is coherent.
- [ ] Keep the architecture comparison and GPT overview distinct: one compares model families, the other traces one selected model's computation.
- [ ] Make only changes that resolve a specific observed problem.

### P2 — Complete validation

- [ ] Run Quarto render and existing metadata/local-link checks after any changes.
- [ ] Inspect FR/EN rendered pages at desktop and mobile widths.
- [ ] Check heading order, table overflow, equations, diagram scaling and alternative text, disclosures, keyboard operation, visible focus, and text zoom.
- [ ] Record accessibility evidence separately; do not claim WCAG conformance from source inspection.
- [ ] If learner outcomes are to be claimed, conduct a small usability/learning evaluation rather than infer effectiveness from editorial review.

## 7. Non-goals and guardrails

- Do not bulk-rewrite all pages to match the new patterns.
- Do not add a visible learning-outcomes callout to every page.
- Do not add diagrams or interactive workbenches as a quota.
- Do not collapse essential assumptions, mathematical hypotheses, or limitations.
- Do not create a new metadata field unless the current schema demonstrably cannot express the need.
- Do not duplicate the broader navigation/curriculum audits in #61 and #130.
- Do not interpret source-level review or CI as rendered accessibility evidence.

## 8. Conclusion

The pilot supports the direction of the soft-target system, but also exposes a governance issue: **the project needs one clear hierarchy between metadata, documentation genre, scientific page pattern, composition guidance, visual design, and practice/verification**.

The best existing pages already converge in reader experience while differing in structure. The next improvement should therefore be to clarify and consolidate authoring guidance, then test it on a small bilingual pilot. Page-level refactoring should follow only when a concrete comprehension, navigation, accessibility, or maintenance benefit is demonstrated.
