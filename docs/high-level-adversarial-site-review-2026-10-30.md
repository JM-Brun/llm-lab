# High-level adversarial review of the published site

**Review date:** 2026-10-30  
**Scope:** external-reader review of the published LLM Lab website  
**Review type:** strategic, editorial, pedagogical, information architecture, and UX  
**Status:** recommendations; this report does not imply that site changes have been implemented.

## 1. Purpose and review stance

This review considers the published experience from the perspective of a visitor who does not know the author's intentions or the repository's internal history. It asks whether the site makes it easy to understand:

1. what an LLM is and what problem it solves;
2. how data, representations, architecture, prediction, and learning fit together;
3. how to follow a coherent path from concepts to a working GPT implementation;
4. how to distinguish explanations, executable implementations, experiments, and planned work.

The review is deliberately adversarial: it looks for mismatches between the project's ambition and the experience communicated by navigation, titles, page boundaries, and learning paths.

This is a high-level review, not a page-by-page scientific verification, source audit, accessibility conformance assessment, or pixel-level visual inspection. Those require separate evidence-based passes.

## 2. Executive assessment

LLM Lab has a strong and differentiated educational premise: connect intuition, mathematics, implementation, and experimentation while distinguishing explanation from evidence. Its scientific caution and attention to assumptions, counterexamples, and limitations should be preserved.

The main strategic concern is that the site can still be perceived as a collection of Transformer/LLM topics rather than as an integrated learning environment that helps a reader understand, build, and investigate a language model.

The highest-leverage improvement is not to add more content. It is to make the existing content legible as a coherent system: clarify the conceptual map, expose the build-from-scratch spine, distinguish the model lifecycle from cross-cutting topics, and make content maturity visible.

| Dimension | Assessment | Main concern |
|---|---|---|
| Scientific positioning | Strong | Preserve the critical, evidence-aware approach |
| Educational ambition | Strong | Make learning outcomes visible |
| Information architecture | Needs review | Different conceptual roles can appear at the same level |
| Learning progression | Needs strengthening | The complete build path is not tangible enough |
| Titles and editorial hierarchy | Needs normalization | Overview, concept, implementation, and reference pages can be hard to distinguish |
| Navigation | Needs strengthening | Topic discovery is more visible than guided progression |
| Breadth of LLM coverage | Needs explicit framing | A GPT decoder-only path can be mistaken for the whole LLM landscape |
| Visual identity | Not fully assessed | Browser-based desktop/mobile inspection remains necessary |
| Accessibility and responsive UX | Not assessed conclusively | Requires a dedicated technical pass |

## 3. Information architecture

### 3.1 Finding: the navigation risks mixing unlike conceptual objects

A navigation tree becomes difficult to understand when it places architectural components, data transformations, mathematical quantities, learning mechanisms, and reference resources at the same hierarchical level.

Examples of different conceptual roles:

- **Architecture:** Transformer, decoder-only model, Transformer block.
- **Data pipeline:** corpus preparation, tokenization, sequence construction.
- **Representations:** token IDs, embeddings, positional information, hidden states.
- **Mechanisms:** attention, causal masking, feed-forward networks.
- **Prediction outputs:** logits, probabilities, decoding.
- **Learning objective:** likelihood, entropy, cross-entropy, loss.
- **Optimization:** gradients, backpropagation, optimizer.
- **Scientific practice:** evaluation, experimental design, error analysis.
- **Reference resources:** glossary, bibliography, exercises.

These elements are related, but they do not answer the same kind of question. A flat or weakly grouped list can obscure the system's causal structure.

### 3.2 Recommended conceptual map

Use this as a **high-level map**, not as a mandatory linear syllabus and not as an instruction to create ten new sections immediately:

1. **Understanding language models** — next-token prediction, autoregressive generation, model families, historical context.
2. **From data to tokens** — corpora, Unicode, preprocessing, tokenization, vocabulary, sequence windows, training examples.
3. **Representing language** — tensors, token embeddings, positional information, RoPE, contextual representations.
4. **Computing with a Transformer** — Q/K/V, attention, causal masks, multi-head attention, MLP, residual paths, normalization, blocks.
5. **Producing predictions** — hidden states, output projection, logits, softmax, probability distributions, decoding.
6. **Learning from data** — targets, likelihood, entropy, cross-entropy, loss, backpropagation, gradients, optimization, regularization.
7. **Building and training a GPT** — initialization, implementation, batching, training loop, validation, checkpoints, reproducibility, generation.
8. **Using and adapting pretrained models** — inference, prompting, supervised fine-tuning, instruction tuning, LoRA/QLoRA.
9. **Evaluating models and understanding limitations** — metrics, protocol design, leakage, calibration, robustness, interpretability, bias, limitations.
10. **Efficiency and advanced topics** — compute and memory, architectural variants, quantization, scaling, research directions.

Cross-cutting resources should remain discoverable without being forced into the main sequence: glossary, references, exercises, interactive labs, code, and historical material.

### 3.3 Qualification: a learning graph, not a compulsory sequence

The conceptual map must remain consistent with the project's existing editorial principle: LLM Lab is a navigable knowledge graph with progressive depth, not a textbook every reader must follow from page one.

Support three complementary routes:

- **Orientation route:** understand the system and its major parts without mastering every derivation.
- **Guided build route:** follow the dependencies required to implement and train a small GPT.
- **Reference/deep-dive route:** enter through a concept, implementation, experiment, or research question.

The global menu should answer “what is covered here?” The guided path should answer “what should I study or build next, and why?” These functions should be related but not conflated.

## 4. Make the model lifecycle explicit

A central improvement is to distinguish three processes that are often confused.

### 4.1 Construction and training

**Question:** how are model parameters obtained?

Data and targets → numerical representations → architecture → forward computation → loss → gradients → optimizer updates → learned parameters.

### 4.2 Inference and generation

**Question:** how are learned parameters used?

Context → tokenization → representations → Transformer computation → logits → probability distribution → decoding → next token → updated context.

### 4.3 Adaptation and evaluation

**Question:** how is a pretrained model specialized and assessed?

Pretrained model → optional adaptation → evaluation protocol → measurements → error analysis → conclusions and limitations.

These processes share components but have different goals, data flows, and validation requirements. Fine-tuning should not be presented as merely another name for inference or as an obligatory stage of every from-scratch build.

## 5. Titles and editorial structure

### 5.1 Finding: technical precision is necessary but not sufficient

Specialized titles should retain correct terminology. However, a title that names a component without explaining its role can be difficult to place in the larger system.

A useful editorial pattern is:

- **Title:** the question or mechanism in reader-oriented language.
- **Subtitle:** the exact technical scope.
- **Learning objective:** what the reader should understand or be able to do.
- **Context:** where the concept appears in the model lifecycle.
- **Navigation:** essential prerequisites, useful background, deeper material, and a return link to the system overview.

Illustrative title patterns:

| Reader-oriented title | Technical scope |
|---|---|
| How does an LLM represent text? | Unicode, tokens, IDs, and embeddings |
| How do tokens become vectors? | Embedding tables, dimensions, and lookup |
| How does a Transformer use context? | Queries, keys, values, and attention |
| How does a model predict the next token? | Hidden states, logits, softmax, and decoding |
| How does a model learn from its errors? | Likelihood, cross-entropy, gradients, and optimization |

These are editorial examples, not a directive to rename every existing page.

### 5.2 Make page roles explicit

Distinguish the following content roles:

- **System overview:** explains the whole mechanism and relationships among its parts.
- **Canonical concept page:** owns the definition, mechanism, assumptions, example, limitations, and core references for one concept.
- **Question lesson or companion:** answers a distinct, bounded learner question without duplicating the canonical explanation.
- **Implementation/test page:** documents actual code, interfaces, shapes, conventions, and the properties verified by tests.
- **Experiment/report:** states the question, hypothesis, data, baseline, protocol, measurements, uncertainty, and limitations.
- **Reference resource:** glossary, bibliography, exercise index, or lookup resource.

Do not split pages merely to increase page count. Create a separate companion only when it has a distinct learning objective or explanatory method. Prefer concise inline explanations when sufficient.

### 5.3 Page granularity

Small pages help with linking, maintenance, and targeted study. Excessive fragmentation forces readers to navigate repeatedly between concepts that form one continuous explanation.

The appropriate unit is a coherent learning objective, not simply one term or equation. A page should be independently useful while remaining connected to its parent system and downstream applications.

## 6. Build-from-scratch path

The ambition to build an autoregressive GPT from random initialization should be represented as an explicit, inspectable path.

A complete learning/build path should make these milestones discoverable:

1. Define next-token prediction and autoregressive factorization.
2. Prepare a corpus and document data provenance and splits.
3. Train or select a tokenizer and encode text.
4. Construct input windows and shifted targets.
5. Define tensor shapes and model configuration.
6. Implement token embeddings and positional information.
7. Implement attention and causal masking.
8. Implement the remaining Transformer block components.
9. Initialize parameters and run a forward pass.
10. Compute the objective with correct target alignment and masking.
11. Backpropagate and update parameters.
12. Validate, checkpoint, and reproduce training.
13. Generate text autoregressively and inspect failure modes.

This list describes an educational completeness criterion. It does **not** assert that these implementations currently exist.

For each milestone, distinguish:
- explanation available;
- implementation available;
- tests available;
- experiment/report available;
- planned or not yet demonstrated.

A passing test is evidence for a specified software property, not proof of general scientific correctness or model quality.

## 7. Scope: GPT as a concrete case, LLMs as a broader field

A decoder-only autoregressive GPT is a sensible concrete construction target. It should not silently stand for every LLM architecture or training objective.

**Concrete build target**
- decoder-only Transformer;
- causal next-token prediction;
- pretraining from random initialization;
- autoregressive generation.

**Broader landscape**
- encoder-only and encoder-decoder architectures;
- masked and autoregressive objectives;
- alternative architectural designs;
- pretraining and post-training;
- instruction tuning and parameter-efficient adaptation;
- multimodal models;
- evaluation and limitations.

Keep the main build path focused. A concise architecture/family map and contextual links can explain what the GPT example does and does not represent.

## 8. Scientific and mathematical quality

### 8.1 Preserve the project's differentiator

The following characteristics should remain central:

- distinguish intuition from formal definition;
- state assumptions and conventions;
- define tensor shapes and dimensions;
- provide checkable numerical examples;
- connect equations to implementations;
- distinguish code behavior from scientific claims;
- use tests to verify explicit properties;
- include counterexamples and limitations where they clarify scope;
- distinguish empirical observations from interpretations;
- cite sources that support the actual claim.

The project should not trade this rigor for superficial simplification.

### 8.2 Standard for technical concept pages

Where relevant, a technical page should provide:

1. Definition and role in an LLM.
2. Intuition and system context.
3. Mathematical formulation with notation defined.
4. Tensor shapes and conventions.
5. Worked numerical example.
6. Implementation link, if implementation exists.
7. Tests and the exact properties they establish, if tests exist.
8. Assumptions, edge cases, and numerical considerations.
9. Likely misconception and discriminating counterexample.
10. Limitations and accessible references.

This is a quality checklist, not a compulsory template to fill mechanically on every page.

### 8.3 Cross-cutting concepts

Generalization, bias/variance, regularization, numerical stability, optimization, model capacity, calibration, interpretability, and robustness span multiple lifecycle stages.

Make them discoverable as cross-cutting concepts rather than assigning them artificially to one chapter. This supports a learning graph and avoids duplicating the same concept across multiple pages.

## 9. Reader journeys and navigation

The site should make four journeys obvious:

### Journey A — Understand what an LLM is

Start with the problem and system overview; follow the data flow and prediction loop; inspect major components; optionally open mathematical or implementation deep dives.

### Journey B — Build a GPT

Follow the dependency-aware build milestones from data preparation to generation. At each milestone, show the objective, prerequisites, available explanation, implementation/test status, and next step.

### Journey C — Look up a concept

Use search, glossary, or direct navigation; land on a canonical page; see its role, assumptions, related concepts, and links to code/evidence where available.

### Journey D — Investigate a claim

Move from the claim to its assumptions, cited source, implementation, test, or experiment. Make clear which kind of evidence is available and what it can establish.

Navigation recommendations:

- keep the global menu hierarchical and concise;
- show the active location and useful parent context;
- limit local table-of-contents depth;
- provide contextual prerequisite and follow-on links;
- avoid generic link dumps;
- make search and glossary useful as lookup tools;
- ensure mobile navigation and long mathematical pages remain usable;
- preserve non-linear entry points.

## 10. Visual identity and presentation

The intended visual direction should combine three qualities:

- **Scientific textbook:** readable typography, disciplined notation, carefully composed diagrams.
- **Technical documentation:** predictable hierarchy, precise labels, stable navigation, code readability.
- **Educational laboratory:** meaningful visualizations, interactive controls, inspectable intermediate values, and experiments.

The visual system should reinforce distinctions between overview and detail; intuition and formalism; mathematical derivation and empirical result; implementation and planned work; central content and optional deep dives.

Avoid decorative cards, excessive color categories, redundant diagrams, and callouts that add no semantic value. Illustrations should explain structure, data flow, geometry, or behavior.

Existing external illustrations should not be removed merely because their reuse rights have not yet been checked. Record their provenance and maintain explicit license/copyright verification tasks. Do not infer that an illustration is free to reuse.

### 10.1 Required visual/technical follow-up

This high-level review does not establish pixel-level visual quality. A separate browser-based review should inspect:

- desktop and mobile layouts;
- typography and line length;
- math rendering and overflow;
- code block readability and horizontal scrolling;
- contrast and focus states;
- keyboard navigation;
- image alternative text and attribution;
- responsive diagrams and SVGs;
- table and callout behavior;
- loading performance and interactive behavior.

## 11. Priority recommendations

| Priority | Workstream | Expected outcome |
|---|---|---|
| P0 | Reconcile the conceptual map with existing architecture and curriculum documents | One coherent target model, without a competing curriculum |
| P0 | Make build-from-scratch milestones explicit | A reader can see the route from corpus to generation and what is actually implemented |
| P0 | Clarify training, inference, and adaptation/evaluation | Lifecycle distinctions are visible throughout navigation and explanations |
| P1 | Improve homepage orientation | Visitors can identify purpose, audience routes, and content maturity |
| P1 | Normalize page roles and titles | Overview, concept, implementation, experiment, and reference content are distinguishable |
| P1 | Map existing pages to the conceptual structure | No content is lost; gaps and duplicates are evidenced |
| P1 | Clarify content status | Planned work is not mistaken for available material or implementation |
| P2 | Refine visual hierarchy | Consistent treatment of diagrams, equations, code, examples, and caveats |
| P2 | Conduct responsive/accessibility review | Browser-verified usability across devices and input modes |

## 12. Recommended execution order

1. **Inventory before restructuring.** Map every existing EN/FR page, navigation entry, code module, test, and experiment to the conceptual map.
2. **Reconcile existing project documents.** Compare this review with the reader-experience/editorial method, full curriculum plan, learning path, roadmap, page audit inventory, and editorial audits. Update or cross-reference canonical documents rather than creating parallel sources of truth.
3. **Define the target information architecture.** Agree on hierarchy, page roles, cross-cutting resources, and the three lifecycle processes.
4. **Define the build path and status model.** Identify what is documented, implemented, tested, experimentally demonstrated, planned, or missing.
5. **Prototype navigation and homepage changes.** Validate representative reader journeys before editing many content pages.
6. **Migrate incrementally.** Preserve useful content, stable URLs where practical, bilingual parity, and links. Avoid mass renaming or deletion without a verified redirect/cross-reference plan.
7. **Run scientific and technical validation.** Render both languages, check local links, review external references, and inspect actual browser output.
8. **Repeat the adversarial reader test.** Check whether an unfamiliar reader can find an entry point, understand where they are, choose the next step, and distinguish evidence from explanation.

## 13. Acceptance criteria

- [ ] A new visitor can explain the site's purpose and identify an appropriate entry route.
- [ ] Global navigation reflects conceptual relationships rather than a flat inventory of terms.
- [ ] The build-from-scratch route is explicit from data preparation to generation.
- [ ] Training, inference, and adaptation/evaluation are clearly distinguished.
- [ ] The GPT build target is framed as a concrete case within the broader LLM landscape.
- [ ] Overview, concept, implementation, experiment, and reference pages have distinct roles.
- [ ] Existing useful content, links, and illustrations are preserved unless a specific, documented reason justifies a change.
- [ ] Planned, available, implemented, tested, and experimentally demonstrated work are not conflated.
- [ ] The learning experience remains non-linear; optional depth does not become a mandatory prerequisite.
- [ ] French and English versions preserve equivalent scope, qualifications, and navigation.
- [ ] Desktop/mobile rendering, mathematics, keyboard navigation, contrast, and image alternatives have been checked in a browser.
- [ ] The final information architecture is consistent with existing curriculum and editorial guidance rather than introducing a competing source of truth.

## 14. Evidence limits and related project documents

This report records a high-level external assessment of the published experience on 2026-10-30. It does not claim that every page, link, illustration, responsive state, or interactive element has been exhaustively inspected. Visual statements are therefore framed as design recommendations and follow-up checks, not as measured defects.

Use this report alongside the existing canonical project documents:

- [Reader experience and editorial method](reader-experience-and-editorial-method.md)
- [Full curriculum plan](full-curriculum-plan.md)
- [Learning path](learning-path.md)
- [Repository roadmap](roadmap.md)
- [Page audit inventory](page-audit-inventory.md)
- [Editorial boundary audit](editorial-boundary-audit.md)
- [Visual assets register](visual-assets-register.md)

**Relationship to those documents:** this report captures the external strategic diagnosis and recommendations. The editorial method remains the contract for reader experience and page design; the curriculum and learning path remain the source of truth for educational dependencies; the roadmap remains the implementation-priority record; page-level inventories and audits remain the evidence for individual content decisions. If recommendations here conflict with a more detailed, already validated project rule, reconcile the documents explicitly before changing the site.


## 15. Reconciliation with the existing project architecture (2026-10-30)

This section records the comparison with the repository's existing editorial, curriculum, learning-path, roadmap, and audit documents. It resolves the main risk raised by the first version of this review: accidentally introducing a second information architecture or a parallel roadmap.

### 15.1 Finding: the repository already has the right strategic model

The existing documents already establish the central design principles:

- [Reader experience and editorial method](reader-experience-and-editorial-method.md) defines a **non-linear learning graph with progressive depth**, four reading modes (Orient, Connect, Understand, Investigate), page roles, contextual links, and criteria for question-led companion lessons.
- [Full curriculum and coverage plan](full-curriculum-plan.md) defines the scope, conceptual dependencies, the three learning depths (big-picture overview, guided model-building path, deep dives), and a laboratory layer for diagrams, interactions, experiments, and tests.
- [Learning path](learning-path.md) operationalizes the curriculum through a reader-facing crosswalk, guided modules, page links, evidence gates, and explicit distinctions between available and planned work.
- [Repository roadmap](roadmap.md) owns priorities, current implementation status, sequencing, and the rule that existing knowledge must be validated before new implementation or experiment work.
- [Public page audit inventory](page-audit-inventory.md) records page-level evidence and remaining checks; it is explicitly partial and does not certify every page.
- [Editorial boundary audit](editorial-boundary-audit.md) defines what belongs in LLM Lab versus the general mathematical knowledge base and protects the public pages' self-contained explanations.

**Conclusion:** no new curriculum document, top-level navigation taxonomy, or parallel roadmap is needed. The audit's role is to challenge and refine the existing system, not replace it.

### 15.2 Existing coordination issues are the source of truth for this work

Two open issues already coordinate the relevant work:

- [Issue #130 — Coordinate the high-level learning-design audit](https://github.com/JM-Brun/llm-lab/issues/130) owns the lifecycle-oriented navigation proposal and the coordination of the high-level design review. Its proposed flow is: understand an LLM; text to model input; inside the model; representations to prediction; learning; generation; adaptation to useful assistant; build and inspect; optional deep dives and references.
- [Issue #87 — Turn the three learning depths into a traceable curriculum map](https://github.com/JM-Brun/llm-lab/issues/87) owns the traceability between the panorama, guided build path, and deep dives, including learning questions, prerequisites, outcomes, next steps, optional detours, and evidence.

The present audit should feed findings into #130. The curriculum crosswalk and milestone evidence belong in #87 and `docs/learning-path.md`; page-level findings belong in the page audit inventory and relevant focused issues.

### 15.3 How the audit recommendations map to canonical documents

| Audit recommendation | Canonical owner | Reconciliation decision |
|---|---|---|
| Global navigation should follow the system's causal/lifecycle flow | Issue #130; full curriculum plan | Refine the existing lifecycle proposal; do not introduce a second sidebar taxonomy |
| Three reader routes/depths | Reader-experience method; issue #87 | Preserve Panorama / Guided build / Deep dives as complementary routes, not separate content silos |
| Explicit from-scratch GPT milestones | Learning path; full curriculum plan; roadmap | Keep the existing modules and evidence gates; do not imply that the complete GPT implementation or training run exists |
| Training vs inference vs adaptation/evaluation | Full curriculum plan; learning path; issue #130 | Treat these as distinct lifecycle processes that cross-link, not as three new mandatory chapters |
| Page types and title conventions | Reader-experience method | Apply its existing page contracts; do not impose a universal template or mass-renaming exercise |
| Concept coverage and dependencies | Full curriculum plan | Use the curriculum graph and source baseline; do not mirror Raschka chapter-for-chapter |
| Implementation/test/experiment status | Learning path; roadmap; page audit inventory | Keep evidence states separate: documented, implemented, tested, rendered, experimentally demonstrated, and learner mastery |
| General mathematics vs LLM-specific application | Editorial boundary audit | Preserve self-contained public explanations; do not move or remove prerequisite mathematics based solely on overlap |
| Visual and accessibility review | Roadmap; page audit inventory; visual assets register | Record concrete browser findings in the existing audit/asset records; this report does not claim a pixel-level review |

### 15.4 Lifecycle distinction: clarify the model without creating duplicate chapters

The three processes highlighted in this audit—training, inference/generation, and adaptation/evaluation—are useful as a cross-cutting explanatory lens:

- **Training:** data/targets → representations → forward pass → objective → gradients → parameter updates → validation.
- **Inference/generation:** context → tokenization → forward pass → next-token distribution → decoding → appended token → repeated forward pass.
- **Adaptation/evaluation:** pretrained checkpoint → optional adaptation/post-training → evaluation protocol → measurements → error analysis and limitations.

These processes should be shown in overview diagrams and used to disambiguate explanations. They are not a replacement for issue #130's lifecycle-oriented navigation, and they should not become three new top-level chapters by default. In particular, evaluation applies to base models and adapted models; it is not a phase that only follows fine-tuning.

### 15.5 Scope and sequencing constraints retained

The reconciliation does not authorize a broad rewrite or new implementation work.

1. Inventory and map existing pages, navigation entries, code, tests, and experiments before changing the sidebar.
2. Reuse the current six-question homepage crosswalk and guided modules in `docs/learning-path.md`; update them only where a concrete mismatch or missing dependency is demonstrated.
3. Preserve the existing three-depth model and progressive disclosure. Do not make optional deep dives such as RoPE mandatory prerequisites for the overview.
4. Respect the active learning/implementation gate recorded in the roadmap and learning path, including issue #82. Do not jump ahead to later implementation stages merely because the high-level map lists them.
5. Preserve existing content, URLs, bilingual scope, and external illustrations. Do not delete illustrations as a precaution; record provenance and verify license/copyright status through the existing visual-assets process.
6. Do not conflate a page's existence, code presence, passing tests, a successful render, an experiment, and learner mastery.
7. Prototype and validate representative reader journeys before making broad navigation or homepage changes.

### 15.6 Revised decision

The target is **one coherent learning system**, not a new taxonomy:

- **Navigation:** use issue #130's lifecycle-oriented proposal, reconciled against the real page inventory.
- **Learning depths:** preserve the Panorama / Guided build / Deep dives model in issue #87 and the full curriculum plan.
- **Page design:** follow the reader-experience and editorial method.
- **Build progression and evidence:** maintain `docs/learning-path.md` and the roadmap.
- **Validation:** extend the page audit inventory and visual asset register with observed evidence.

The audit's ten thematic groupings in §3.2 are retained only as a coverage lens. They are not a menu specification. The next concrete action is to complete the crosswalk/inventory under #130 and #87, identify genuine gaps or contradictions, and only then prototype the sidebar and homepage. No mass renaming, page splitting, content deletion, or implementation expansion is justified by this audit alone.
