# Pedagogical visual design and review process

**Scope:** figures, diagrams, schematics, plots, annotated examples and other authored visual explanations across LLM Lab.  
**Primary audience:** Theory / Understand; the same principles apply to Build and Deepen.  
**Companion contracts:** [Visual asset register](visual-assets-register.md), [design system](design-system.md), [page template system](page-template-system.md), [reader experience and editorial method](reader-experience-and-editorial-method.md), [Understand path audit skill](../.agents/skills/understand-path-audit/SKILL.md).  
**Architectural reference:** [#575 — Provide one persistent computational spine across inference, scoring and learning](https://github.com/JM-Brun/llm-lab/issues/575).  
**Status:** process contract. The route audit below is a source-level baseline, not a claim that every figure has passed browser inspection.

## Applied audit records


  - [Third Understand visual audit pilot (2026-11-26)](visual-audit-third-pilot-2026-11-26.md): embedding lookup, contextualized representations and Transformer architecture, including mobile variants and removal of a redundant hidden pipeline figure.
  - [Four-page Understand visual audit pilot (2026-11-26)](visual-audit-priority-pages-2026-11-26.md): concrete design decisions, placement, captions, caveats and remaining validation for likelihood, loss, gradients and context engineering.

## 1. Purpose and governing rule

A visual is part of the explanation, not decoration added after the prose. It should make a concept, relationship, transformation, constraint, comparison, geometry or empirical result easier to understand, inspect or remember.

The project must not optimize for the number of images per page. It must optimize for explanatory value, scientific fidelity and reader effort.

**No visual is added merely to make a page look illustrated, fill whitespace, imitate another resource or repeat the prose in boxes and arrows.** A concise equation, table, worked example or paragraph may be the better representation. “No new figure” is a valid audit decision.

## 2. Match the visual form to the learning task

These forms have different jobs and must not be treated as interchangeable.

| Form | What it should make visible | Typical use |
|---|---|---|
| Conceptual map | Concepts and typed relationships | System context vs input sequence vs accessible context |
| Computational/data-flow diagram | Operations, dependencies, inputs and outputs | Q/K/V projections, attention, logits-to-distribution |
| Architecture diagram | Components, nesting, repeated blocks and residual paths | Decoder-only GPT stack and Transformer block |
| Sequence/timeline | Order, iteration, state changes and phases | Prefill/decode; observed vs generated tokens |
| Matrix/heatmap | Pairwise relations, masking, positions, dimensions | Causal mask; attention matrices; positional encodings |
| Mathematical/geometric figure | Function, transformation, gradient or geometry | Softmax invariance; cross-entropy curve |
| Worked visual example | A small example traced across steps | Token → ID → embedding; conditional probabilities |
| Empirical plot | Measured behavior, uncertainty and trade-offs | Train/validation loss; benchmarks |
| Comparison figure | Alternatives compared on shared dimensions | Absolute position vs RoPE; SGD vs AdamW |

A learning-path diagram is not a computation diagram. A knowledge graph is not an architecture diagram. A sequence of headings connected by arrows is not automatically an explanation.

## 3. Start from the learner's question

Before drawing, define:

1. **Page and section:** where will the visual live?
2. **Learner question:** what precise question should it answer?
3. **Learning objective:** what should the reader be able to explain, calculate, compare or predict afterwards?
4. **Current obstacle:** what is difficult to infer from the existing prose, equations or example?
5. **Visual takeaway:** what should become immediately visible?
6. **Scope and exclusions:** what is deliberately not represented?
7. **Evidence:** which equations, examples, sources, experiments or implementation behavior ground it?
8. **Success test:** what should a reader be able to point to or explain after inspecting it?

Write the intended takeaway in one sentence. If it cannot be stated precisely, the design is not ready.

## 4. Find and develop visual ideas

### 4.1 Inspect the local teaching context first

Before searching externally:

- Read the target section and relevant neighbouring sections.
- Inspect existing figures, examples, equations and callouts on the page.
- Inspect the previous and next pages in the canonical route.
- Search the visual asset register and image directory for reusable assets.
- Check whether a related figure already exists elsewhere.
- Check the canonical computational model and notation when representing execution.

This reveals duplication risks and opportunities to reuse a stable example across pages.

### 4.2 Search for explanatory ideas in sources

When a genuine visual gap remains, inspect suitable sources:

- Original papers and appendices for mathematical and algorithmic fidelity.
- Author-maintained documentation for API and implementation semantics.
- Textbooks and carefully selected tutorials for explanatory framing.
- Technical talks and lecture slides for alternative representations.
- Reproducible experiments and notebooks for quantitative plots.

For each useful source, record the exact source, author, relevant section or figure, the explanatory idea it contributes, what it does not establish, and whether the figure itself may legally be reused.

A source can inspire an original diagram without granting permission to copy its figure. Do not assume that an attractive visual is scientifically accurate, accessible, reusable or suitable for this learner level. Inspect and verify the underlying explanation. Preserve provenance and licence uncertainty in the source and asset records.

### 4.3 Compare candidate representations when needed

For a high-impact or conceptually difficult visual, sketch at least two materially different candidates: for example, a flow diagram versus annotated states; a matrix versus a token trace; a geometric view versus a function plot; or a system architecture versus a zoomed-in operation.

Choose against the learner question, not visual attractiveness. Select the representation with the lowest interpretation burden that preserves the important distinctions. Do not force multiple candidates for a trivial figure.

## 5. Decide whether a visual earns its place

### Positive contribution

A candidate should satisfy at least one substantial purpose:

- expose a relationship difficult to infer from prose;
- make a multi-step transformation or dependency explicit;
- make tensor dimensions, axes, masking or data movement inspectable;
- let the reader follow a numerical example at a glance;
- compare alternatives on a common basis;
- reveal a geometric, probabilistic or optimization property;
- communicate an empirical result better than a table or sentence;
- prevent a likely misconception by making the distinction visible.

### Redundancy and harm checks

Reject or redesign a candidate if it:

- repeats a paragraph or heading without adding a new view;
- duplicates another figure on the same or neighbouring page;
- uses arrows without specifying what flows or what the arrow means;
- mixes conceptual relationships with execution order or curriculum order;
- hides important caveats in tiny labels or a long caption;
- uses a metaphor that implies a false mechanism;
- introduces more unexplained notation than it resolves;
- cannot be read at the intended page width;
- misleads through scale, colour, omitted cases or selective examples.

### Record an explicit decision

- **Add:** resolves a specific gap and has a clear role.
- **Reuse:** an existing project figure already does the job.
- **Revise existing:** the current visual is close but incomplete or misleading.
- **Keep prose/math/table:** a new visual would not materially improve understanding.
- **Defer:** evidence or the underlying explanation is not ready.

Do not treat “no new figure” as an audit failure.

## 6. Place the visual at the point of need

A figure's location is part of its design.

- Place it after the first paragraph or equation that establishes the objects it depicts, and before prose that relies on the reader understanding it, unless a short motivating example must come first.
- Introduce it in the prose. Explain what to inspect and why it matters.
- Keep it close to the equations and numerical example it illustrates.
- Put advanced variants and implementation details in optional sections when they are not required for the core objective.
- Do not hide a core explanatory figure inside a collapsed disclosure.
- Keep the figure close to its legend, assumptions and essential caveat.
- Do not put a figure at the end merely because that was easiest.
- If a figure is reused across pages, explain its local purpose; do not assume the reader remembers the previous page.

The page must remain intelligible if the image fails to load. Prose, caption and alternative text should preserve the essential claim.

## 7. Design before polishing

### 7.1 Define the visual grammar

Specify before authoring:

- entities/nodes and what each represents;
- operations and transformations;
- arrow semantics: data flow, dependency, feedback, comparison, containment or time;
- direction and reading order;
- grouping and hierarchy;
- units, dimensions, axes and indexing conventions;
- colour, shape, line and pattern semantics;
- what is observed, learned, computed, generated or merely illustrative.

Every arrow needs an interpretable meaning. Use labels or a legend where line styles or colours encode distinctions. Never rely on colour alone.

### 7.2 Scientific and mathematical fidelity

Check the diagram against the actual equations and mechanism:

- preserve operation order and causal direction;
- distinguish tensors, vectors, scalars, token IDs, probabilities, logits and parameters;
- label shapes and axes when they matter;
- distinguish scores from normalized probabilities;
- distinguish conceptual dense attention from what an optimized kernel materializes in memory;
- distinguish attention masks from loss/target masks;
- distinguish gradient calculation from optimizer parameter update;
- distinguish observed tokens used for scoring/training from generated tokens used for inference;
- distinguish fixed parameters at inference from updated parameters during training;
- show optional operations as optional, not mandatory;
- state when a figure is schematic, not to scale, or based on a toy example.

For the shared predictive model, preserve the distinction in [#575](https://github.com/JM-Brun/llm-lab/issues/575): a context is processed by the forward pass to produce logits and a conditional distribution; generation, observed-token scoring and learning are distinct uses of that distribution. Do not turn these branches into one fictitious execution loop. Q/K/V projections belong inside each Transformer attention block, not after the final contextualized representations.

### 7.3 Cognitive load and visual hierarchy

- Make the main claim visible first; secondary detail should be quieter.
- Use short labels, consistent terminology and enough whitespace.
- Keep a clear reading direction and avoid crossing connectors where possible.
- Split a complex mechanism into panels only when the panels correspond to a real conceptual decomposition.
- Avoid tiny text, dense legends and unexplained abbreviations.
- Prefer one focused figure over a poster containing every detail of the chapter.
- Use colour consistently across related pages; check contrast and colour-blind accessibility.
- Use line patterns, labels or shapes as redundant encodings.
- Keep decoration subordinate to the explanation.

### 7.4 Reuse examples and notation coherently

Where appropriate, carry the same tokens, dimensions, symbols and numerical values across adjacent lessons. The shared predictive distribution should remain recognizable when the course moves between generation, scoring and learning.

Do not force one toy example into a concept it cannot represent faithfully. If assumptions change, state the change and explain why.

## 8. Caption, alternative text and surrounding explanation

These are three different communication layers.

### Caption: state the takeaway

A good caption tells the reader what the figure establishes and, where necessary, its key qualification. It does not merely repeat the title or say “the diagram below shows”.

A useful pattern is:

> **Main takeaway.** What the visual encodes, under which convention or assumption, and one important limitation or interpretation boundary.

For a multi-panel figure, explain the relation between panels. Define non-obvious symbols or abbreviations either in the figure or caption. Do not move an essential scientific caveat exclusively into alt text.

### Alternative text: provide an equivalent textual account

- For a simple figure, concise alt text may be sufficient.
- For a complex architecture, graph, matrix or plot, provide concise alt text plus nearby prose or a data table conveying the detailed structure.
- Describe relationships, direction, axes, trends and meaningful values, not decoration.
- Do not begin with “image of” or repeat the caption verbatim.
- Do not claim more precision than the figure contains.
- Make essential text in the figure available in the page itself.

### Prose introduction: teach the reader how to inspect it

The nearby prose should answer:
- What should I look at first?
- Which relationship or transformation matters?
- What conclusion should I draw?
- What should I not infer?

A figure is not self-explanatory merely because its labels are technically correct.

## 9. Bilingual and responsive design

### French and English

For every core visual, verify that both language variants exist or document why they do not; labels, notation and examples agree with the page language; the variants communicate equivalent scientific content and caveats; captions and alt text are translated; and links/anchors resolve in both languages.

Parity means equivalent teaching value, not identical line breaks or text lengths.

### Desktop and mobile

A desktop SVG scaled down is not automatically usable on mobile. Choose deliberately between one responsive SVG, a simplified mobile variant, vertically stacked panels, or an accessible textual/table equivalent.

Inspect the rendered result at wide and narrow widths. Check clipping, label collisions, overflow, illegible type, excessive height and reading order. Mobile variants must preserve the same scientific claims and must not silently omit essential information.

### Rendering and accessibility

Inspect the rendered HTML, not just source markup:
- correct figure and language variant load;
- SVG viewBox, dimensions and responsive CSS behave as intended;
- captions and alt text have the expected semantic structure;
- no broken paths, missing fonts, clipped labels or horizontal page overflow;
- surrounding interactive controls do not degrade keyboard or screen-reader use;
- adjacent equations render correctly and use consistent notation.

## 10. Validation protocol

### Before merge

- [ ] Learner question and visual takeaway are explicit.
- [ ] Design brief identifies the gap and intended level.
- [ ] Existing figures/assets were checked for reuse.
- [ ] Source ideas and factual claims have traceable provenance.
- [ ] Equations, dimensions, values, axes and operation order were checked.
- [ ] Reading order and arrow/colour semantics are unambiguous.
- [ ] Figure is introduced at the point of need.
- [ ] Caption explains takeaway and caveats.
- [ ] Alt text conveys essential relationships; complex figures have a textual equivalent.
- [ ] FR/EN variants are substantively equivalent.
- [ ] Desktop/mobile rendering has been inspected.
- [ ] Links, anchors, equations and surrounding prose have been checked.
- [ ] Visual asset register records asset, source, provenance and licence status.
- [ ] PR explains why the visual improves the lesson and what alternatives were rejected.

### Name the evidence level honestly

| Evidence | What it establishes | What it does not establish |
|---|---|---|
| Source review | Authored markup, labels, references and placement | Actual rendered appearance |
| SVG/XML inspection | Dimensions, structure, embedded content and metadata | Visual legibility or legal authorship |
| Quarto render/build | Site generation and asset resolution | Good browser layout or comprehension |
| Browser inspection | Actual rendering, responsive behavior, interactions and accessibility checks performed | Improved learning outcomes |
| Learner task/observation | Whether representative learners can perform the intended task | Universal effectiveness |

Never describe source inspection as a browser visual review. Never claim improved learning outcomes without learner-facing evidence.

## 11. Review at three levels

Every figure must be reviewed at three levels:

1. **Local:** does it explain the intended section accurately?
2. **Page:** does it complement prose, equations, examples and other figures without repetition?
3. **Route:** does it use concepts already introduced, prepare the next page and remain consistent with figures elsewhere?

For route-wide work, use the canonical route in data/guided-route.yml and the Understand Path Audit procedure. Do not infer curriculum order from filenames or image order.

Keep distinct:
- knowledge/concept relationships;
- computational/data-flow relationships;
- architecture/component containment;
- curriculum and reading order;
- implementation dependencies.

## 12. Asset lifecycle

Whenever a visual is added, substantially revised, moved, replaced or removed:

- update docs/visual-assets-register.md;
- record sources that informed it and whether artwork is original, adapted or reused;
- record creator/contributor provenance and exact licence/permission evidence, or explicitly mark uncertainty;
- preserve source links and attribution even when the source image is not reused;
- update EN/FR counterparts and references;
- check for duplicate or orphaned assets;
- record pedagogical rationale and validation evidence in the PR.

Unknown licensing is a finding, not an automatic reason to remove an existing asset. Follow the preservation rule in the visual asset register. Do not copy third-party figures into project SVGs without permission; create an independently authored explanatory representation and cite the underlying source where appropriate.

## 13. Baseline: Understand route visual audit (2026-11-26)

A source-level inspection covered the 20 canonical Understand pages in French and English. It found a substantial existing visual foundation in the overview, embeddings, positional information, contextualized representations, Transformer, Q/K/V, attention, causal masking, logits, entropy, generation, ICL, cross-entropy and training loop.

The following are candidate gaps or improvement areas, not automatic instructions to create figures:

| Page/topic | Source-level finding | Next action to assess |
|---|---|---|
| Context engineering | The explanation covers context assembly, selection, retrieval, prioritization, compression, security and evaluation; no dedicated explanatory diagram was identified in the inspected section. | Design a context-assembly candidate distinguishing application/system information, selected input sequence and per-position accessible context. |
| Likelihood/scoring | The numerical example does not yet have a clear visual trace of observed tokens and conditional probabilities in the inspected section. | Show observed sequence, conditional probabilities, product and log-sum; distinguish scoring from generation. |
| Loss | Stepwise explanation and numerical material exist, but no token-level aggregation visual was identified in the inspected section. | Show per-token losses, valid/ignored targets, mask semantics and aggregation denominator. |
| Gradients | The inspected section relies substantially on equations and stepwise explanation. | Show loss → logit gradients → parameter gradients, then separately optimizer update. |
| Text and data | Existing stepper/table material is useful but may not make text → token pieces → IDs immediately inspectable. | Consider an annotated tokenization trace only if it improves on the current worked example. |
| Positional encoding | A comparison visual exists in optional/collapsed material. | Assess whether the core absolute-position/RoPE distinction belongs in the main lesson. |
| Cross-entropy | Existing target-probability comparison is useful. | Consider a plot of negative log target probability only if it adds insight beyond the numerical comparison. |
| Attention/FlashAttention | Core attention explanation and optional optimization figures coexist. | Preserve the distinction between mathematical dense attention and IO-aware implementation. |
| Training loop | Main training visual and optimizer comparison exist. | Check whether the optimizer comparison is proportionate and clearly optional if it distracts from the core loop. |

This is a prioritization baseline, not final approval of every asset. The audit used source inspection; it did not establish browser rendering, visual quality of every SVG, mobile behavior or learner outcomes. Reopen pages and inspect rendered figures before final decisions.

### Suggested implementation order

1. **Shared prediction, scoring and learning:** likelihood, loss and gradients, coordinated with #575 and the existing running example.
2. **Context construction:** context engineering, distinguishing system context, transmitted sequence and causal accessibility.
3. **Representation and prediction refinements:** text/token/ID trace, positional encoding placement, logits/probability/cross-entropy consistency.
4. **Route-wide visual QA:** inspect every core figure, caption, alt text, bilingual counterpart and desktop/mobile rendering; document any decision to retain, revise or not add a visual.

Do not automatically implement every proposal. Reassess each candidate using section 5.

## 14. Reusable design record

Use this compact record in a PR description or audit note for each substantive new or revised figure:

- **Page / section:**
- **Figure ID / asset paths (FR, EN, mobile):**
- **Learner question:**
- **Learning objective:**
- **Gap in current explanation:**
- **Main visual takeaway:**
- **Chosen form and rationale:**
- **Alternatives considered / rejected:**
- **Entities, operations, arrows, axes and conventions:**
- **Scientific source / equations / experiment:**
- **Scope, assumptions and limitations:**
- **Placement rationale:**
- **Caption:**
- **Alt text / textual equivalent:**
- **FR/EN parity:**
- **Desktop/mobile inspection:**
- **Asset provenance and licence status:**
- **Validation and evidence level:**
- **Decision:** add / reuse / revise / prose-math-table / defer.

Shorten the record for trivial adjustments. It should make the pedagogical decision inspectable, not create bureaucracy.

## 15. Completion criteria for a route-wide visual audit

A route-wide audit is complete only when:

- every canonical page and FR/EN counterpart has been inventoried;
- every existing core figure has been reviewed for purpose, scientific fidelity, placement, caption and alt text;
- each candidate gap has an explicit add/reuse/revise/no-visual/defer decision;
- redundant, misleading, inaccessible or misplaced figures have actionable findings;
- every accepted new visual has a design brief and validated placement;
- figures have rendered desktop/mobile evidence, or an explicit unresolved status;
- shared examples, notation and visual semantics are coherent across the route;
- asset provenance/licence records are current;
- source, build, browser and learner evidence are distinguished;
- residual work is recorded with priorities and canonical owners.

The route does not pass merely because every page contains an image. It passes when each visual earns its place and the visual language helps the learner build one coherent, scientifically correct mental model.
