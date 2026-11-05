# Page-group audit pilot — 2026-11-06

**Repository:** JM-Brun/llm-lab  
**Baseline:** main, inspected 2026-11-06  
**Method:** first application of the page-group-audit skill, followed by calibration recommendations.

> This is a pedagogical and information-architecture audit, not a full scientific peer review. Page bodies, page-map metadata, guided-route data, curriculum documentation and Quarto configuration were inspected. Rendered-browser and learner usability testing were not performed.

## 1. Executive synthesis

The pilot confirms that LLM Lab contains several different kinds of page relationships that must not be collapsed into one generic notion of a group:

- a core learning sequence;
- optional depth branches;
- a conceptual family whose members have different reader-facing destinations;
- a Build dependency branch related to, but distinct from, the conceptual inference sequence.

The strongest conclusion is not that all pages should look alike. It is that their roles and transitions must be legible while preserving the distinct purposes of Understand, Build, Deepen and Practice.

Three follow-ups emerged:

1. Decide whether the attention-score-scaling deep dive should be exposed among the optional resources of the computation stage.
2. Keep the conceptual text/tokenization route distinct from the G1b corpus-preparation Build branch, while making the hand-off discoverable.
3. Model group membership by role (core, optional, branch, context), not as a flat list that accidentally implies a linear sequence.

These are documented recommendations, not changes to canonical page content or route data.

## 2. Group A — Text input and tokenization family

### Scope and membership

**Group model:** concept family plus cross-destination companion.

**Core conceptual pages**
- site/fr/text-data.qmd — overview of the text-to-model-input pipeline.
- site/fr/tokenization-strategies.qmd — core comparison of segmentation strategies.

**Optional depth pages**
- site/fr/unicode-text.qmd — Unicode code points, UTF-8 bytes and normalization.
- site/fr/tokenizer-design-evaluation.qmd — tokenizer design, measurement, evaluation and multilingual effects.

**Build companion, not a core learning step**
- site/fr/corpus-preparation.qmd — provenance, filtering, deduplication, splits, tokenizer fitting/freezing and hand-off to training examples.

**Context/boundary pages:** site/fr/embedding-space.qmd and site/fr/training-examples.qmd.

EN counterparts exist under site/en/ for all five group pages. This establishes counterpart existence, not complete semantic translation parity.

### Intended reader journey

The Understand route is:

text-data → tokenization-strategies → embedding-space

Unicode is optional technical depth below the overview. Tokenizer design/evaluation is optional advanced depth alongside the strategy lesson. Corpus preparation belongs to Build: it uses shared text/tokenization foundations to prepare training data, but it is not the next conceptual step after tokenization.

Evidence:
- data/guided-route.yml, stage text-input: text-data and tokenization-strategies are core; unicode-text and tokenizer-design-evaluation are optional.
- docs/learning-path.md: Unicode/UTF-8 is optional technical depth; corpus preparation and training-example construction form a separate G1b → G2 branch.
- site/fr/text-data.qmd distinguishes prompt encoding from training-corpus preparation and delegates specialist details.
- site/fr/corpus-preparation.qmd is a guided-build page under build-path.

### Assessment

**Verdict: coherent, with a well-designed branch boundary.**

The five pages are not a five-step sequence. They comprise two core pages, two optional deep dives and one Build companion. A flat sequence would create a false prerequisite chain and imply that corpus engineering is required to understand inference.

### Findings

| ID | Priority | Scope | Evidence and impact | Recommendation |
|---|---|---|---|---|
| A-01 | P1 | Group/navigation | The curriculum separates the conceptual route and Build branch, but a flat five-page inventory can imply one sequence. | Mark every member core, optional, branch or context. State separately whether membership implies sequence. |
| A-02 | P2 | Transition | text-data distinguishes prompt encoding from corpus preparation; corpus-preparation is a Build page related to text/tokenization. The boundary is sound, but the hand-off should remain explicit. | Verify that the text-data boundary section links to corpus-preparation as a Build application and states that it is not required for conceptual inference learning. |
| A-03 | Observation | Bilingual | FR and EN counterparts exist. File existence does not prove equivalent scope, examples or navigation. | Compare metadata, route membership, headings, examples and key transitions in future bilingual audits. |

### What is working

- The guided route places Unicode and tokenizer evaluation in optional resources, not core pages.
- text-data delegates specialist content rather than teaching Unicode, algorithms, corpus governance and embeddings in full.
- Corpus preparation remains Build and connects to training examples.
- Page scopes support complementary explanations.

### Acceptance checks

- The text-input stage remains two core pages and two optional resources.
- Corpus preparation remains in Build and is not made a mandatory Understand prerequisite.
- The conceptual-to-Build hand-off states the different reader goal.
- FR/EN parity is checked semantically before claiming equivalence.

## 3. Group B — Core pedagogical computation route

### Scope and membership

**Group model:** guided-route stage with a transition to the next stage.

**Core pages**
1. site/fr/transformer.qmd
2. site/fr/queries-keys-values.qmd
3. site/fr/scaled-dot-product-attention.qmd
4. site/fr/causal-masking.qmd

**Optional advanced pages**
- site/fr/cross-attention.qmd
- site/fr/attention-score-scaling.qmd

**Downstream context:** site/fr/logits.qmd.

### Intended reader journey

Transformer overview → Q/K/V projections → scaled dot-product attention → causal masking → logits.

This is a conceptual sequence, not the order of implementation dependencies. It does not require the learner to study multi-head attention or every advanced architecture before understanding core computation.

### Transition analysis

| Transition | Established by previous page | Assumed by next page | Assessment |
|---|---|---|---|
| Transformer → Q/K/V | A GPT forward pass contains Transformer blocks and self-attention. | Learned projections inside self-attention. | Strong: Q/K/V explicitly refers back to the Transformer overview. |
| Q/K/V → scaled attention | Roles and shapes of Q, K and V. | Matrix products, softmax and weighted aggregation. | Strong: the next page owns the calculation deliberately excluded from Q/K/V. |
| Scaled attention → causal mask | Scores become normalized weights and aggregate values. | Where a mask constrains attention scores. | Strong: the attention page delegates the temporal constraint. |
| Causal mask → logits | Future positions are excluded in an autoregressive pass. | The network state is transformed into vocabulary scores. | Acceptable: the Transformer overview covers the full forward pass; a short bridge may help, but a new mandatory page is not justified. |

### Assessment

**Verdict: coherent core sequence with a small optional-depth coverage gap.**

The page-map contracts are aligned: each page names what it covers and delegates the next operation. The sequence connects attention computation to the autoregressive constraint and then to output scores.

### Findings

| ID | Priority | Scope | Evidence and impact | Recommendation |
|---|---|---|---|---|
| B-01 | P2 | Guided route/depth | site/fr/attention-score-scaling.qmd declares scaled-dot-product-attention as its parent and develops the 1/sqrt(d_k) factor. data/guided-route.yml currently lists cross-attention as the computation stage's optional page but omits attention-score-scaling. The deep dive is discoverable through page hierarchy, but not the stage's optional resources. | Decide explicitly whether the computation stage should expose this mathematical deep dive. If yes, add it to FR and EN optional_pages; otherwise document why it is intentionally outside the stage. |
| B-02 | P3 | Transition | The causal-mask page hands off to logits, while the computation stage ends at masking and prediction is a distinct next stage. The boundary is valid but may benefit from a concise bridge. | Check the rendered transition and add one sentence only if the relation is not already clear. Do not duplicate the logits explanation. |
| B-03 | Observation | Optional depth | Cross-attention belongs to a different architectural setting and should not be inserted into the core decoder-only GPT sequence. | Preserve its optional status and explain its encoder-decoder/multimodal context where linked. |

### What is working

- Core pages have explicit scopes and page-specific outcomes.
- suggested_route.previous/next agrees with the conceptual progression.
- Hierarchy edges describe conceptual containment rather than replacing sequence.
- Scaling and cross-attention have distinct purposes and are not redundant with the core route.

### Acceptance checks

- The four core pages remain the computation-stage core.
- Advanced scaling and cross-attention remain optional, not prerequisites.
- The scaling deep dive is either exposed in the guided route or its exclusion is documented.
- The causal-mask → logits hand-off does not duplicate either page.

## 4. Group C — Transformer architecture and practice family

### Scope and membership

**Group model:** architectural concept family spanning multiple reader-facing destinations.

- site/fr/transformer-architectures.qmd — Understand / optional architecture comparison.
- site/fr/transformer.qmd — Understand / system-level GPT computation overview.
- site/fr/transformer-explainer.qmd — Practice / experiment comparing BERT, GPT-2 and T5 and exploring a GPT-2 visualization.
- site/fr/transformer-block-walkthrough.qmd — Build / code walkthrough of the implemented pre-LN Transformer block.
- site/fr/cross-attention.qmd — Deepen / advanced cross-attention mechanism.

### Intended relationship

These pages share the Transformer subject but do not form one reading sequence:

- architecture comparison answers which broad Transformer configurations exist;
- the system overview answers how a GPT forward pass fits together;
- the experiment asks what can be observed and tested in running implementations or visualizations;
- the code walkthrough explains how this project's block is implemented;
- cross-attention explains how a decoder consults a separate encoder representation.

This is a cross-destination family, not a chapter sequence. Readers may enter from different points depending on whether they want conceptual understanding, implementation, experimentation or advanced depth.

### Assessment

**Verdict: conceptually coherent, intentionally heterogeneous, with a navigation-labeling risk.**

Different page types are an architectural strength when their destinations and purposes are visible. Making the pages uniform or forcing them into one sequence would damage the information architecture.

### Findings

| ID | Priority | Scope | Evidence and impact | Recommendation |
|---|---|---|---|---|
| C-01 | P1 | Group/navigation | The pages occupy Understand, Build, Practice and Deepen. A generic next-page chain would misrepresent the relationship and imply false prerequisites. | Present them as distinct ways to explore the Transformer, with destination labels and task-oriented descriptions. Do not merge them into one linear path. |
| C-02 | P2 | Cross-link | The block walkthrough links to concept pages for Q/K/V, scaled attention and causal masking. This is the correct concept-to-implementation bridge. | Preserve these links and make the direction explicit: concept page for mechanism; walkthrough for this project's executable realization. |
| C-03 | P2 | Scope/entry point | The architecture comparison is optional and distinct from the GPT computation overview. A learner studying decoder-only GPT need not complete BERT/T5 comparison first. | Keep the architecture comparison optional/background; do not make it a prerequisite of the core computation route. |
| C-04 | Observation | Experiment | Transformer Explainer distinguishes visual observation from computational proof and documents interface limitations. | Preserve this epistemic distinction; do not present visualization as a substitute for concept pages or implementation tests. |

### What is working

- The group has different and complementary learning modes.
- Architecture comparison, GPT overview and cross-attention do not compete for the same scope.
- The experiment makes limits of visual evidence explicit.
- The code walkthrough is grounded in a concrete source file and links back to concepts.

### Acceptance checks

- Navigation distinguishes Understand, Build, Practice and Deepen.
- No generic previous/next chain is introduced across this family.
- Concept-to-code links remain useful without duplicating large explanations.
- Experimental observations remain explicitly bounded.

## 5. Group D — Five-page local sequence around attention

### Scope and membership

**Group model:** five-page local reading window, including the downstream hand-off.

1. site/fr/transformer.qmd
2. site/fr/queries-keys-values.qmd
3. site/fr/scaled-dot-product-attention.qmd
4. site/fr/causal-masking.qmd
5. site/fr/logits.qmd

This is five pages total, not five previous and five next. The order is verified against page metadata and the narrative curriculum, not inferred from filenames.

### Assessment

**Verdict: coherent sequence with clear scope hand-offs.**

This is a useful regression case for sequential audits. Each page establishes the conceptual object needed by the next, and each page's scope excludes the main subject of the following page.

### Transition matrix

| From → To | Established | Assumed | Bridge quality | Action |
|---|---|---|---|---|
| Transformer → Q/K/V | Self-attention as a component of the GPT block. | Learned query, key and value projections. | Strong | Preserve the explicit introductory reference. |
| Q/K/V → scaled attention | Roles and shapes of Q, K and V. | Scores, scaling, softmax and aggregation. | Strong | Preserve the deliberate scope boundary. |
| Scaled attention → causal mask | Score/weight/value computation and mask insertion point. | Future positions must be excluded for autoregressive prediction. | Strong | Preserve separate treatment of calculation and causal constraint. |
| Causal mask → logits | Causal restriction on information flow. | The resulting network state is transformed into vocabulary scores. | Adequate | Verify rendered hand-off; add only a short bridge if needed. |

### Findings

| ID | Priority | Scope | Evidence and impact | Recommendation |
|---|---|---|---|---|
| D-01 | P2 | Transition | The sequence crosses from internal attention computation to output representation. The Transformer overview covers the full forward pass, but the local window's final hand-off may be abrupt without that overview. | Check whether the causal-mask conclusion points clearly to output/logits. If not, add a one-sentence bridge, not a repeated logits section. |
| D-02 | Observation | Group boundary | The window does not include probabilities, likelihood or generation. These belong to the next prediction/decoding portion of the route. | Retain the boundary and identify the next stage as context rather than expanding every local window indefinitely. |

### What is working

- The five-page sequence agrees with the computation stage plus the logits hand-off.
- Page metadata provides an explicit route rather than relying on filename sorting.
- Page scopes are complementary and avoid teaching the whole attention mechanism repeatedly.

## 6. Cross-group synthesis

| Recurring issue | Groups | Interpretation | Method consequence |
|---|---|---|---|
| Group membership has different roles | A, B, C | A flat list can falsely imply sequence or mandatory status. | Require a role-aware group map. |
| Several navigation systems coexist | A–D | Site hierarchy, guided stage, suggested route, concept hierarchy and destination answer different questions. | Inspect each relevant projection separately; never treat one as a proxy for another. |
| Relatedness does not imply core-path membership | A–C | A page can be related without being a prerequisite or sequential step. | Record membership role and relation type separately. |
| Bilingual file parity is not semantic parity | A–D | Matching paths do not establish equivalent scope, examples or route membership. | Compare EN/FR content and metadata explicitly, and report confidence. |
| Transition quality depends on page purpose | B–D | Concept-to-concept, concept-to-build and concept-to-experiment transitions need different bridges. | Classify transition types, not only adjacent page pairs. |

## 7. Prioritized action plan

| Priority | Action | Affected sources | Acceptance criterion |
|---|---|---|---|
| P1 | Preserve role-aware group membership in audits and navigation summaries. | Audit skill and future reports | Every member is marked core, optional, branch or context; sequence is stated separately. |
| P2 | Decide whether attention-score-scaling belongs in the computation stage's optional resources. | data/guided-route.yml and generated FR/EN contexts | Decision is documented; if included, both languages resolve the same page ID and generated contexts validate. |
| P2 | Verify text-data → corpus-preparation hand-off. | FR/EN text-data and Build pages | Link identifies corpus preparation as Build, not a prerequisite for conceptual inference learning. |
| P2 | Verify causal-mask → logits bridge in rendered pages. | FR/EN causal-masking and logits | Reader can identify the transition to vocabulary scores without duplicated exposition. |
| P2 | Add semantic bilingual parity to the audit procedure. | Audit skill | EN/FR comparison covers metadata, role, examples, scope, links and stage membership, not only file existence. |
| P3 | Reuse these four groups as regression examples for future skill changes. | This report and audit skill | A proposed skill change is checked against all four cases and preserves intentional differences. |

## 8. Iteration log — skill improvements

The initial skill is strong on audit dimensions but underspecifies practical mechanics for repeatable application. The next revision should add:

1. Role-aware membership: core, optional, branch, context, and excluded-but-relevant pages.
2. Scope semantics: distinguish N pages total from N neighbors on each side; do not treat context pages as core findings.
3. Multiple projections: inspect curriculum, guided-route YAML, Build route, Quarto navigation, page metadata route/hierarchy/related edges, and destination tags where relevant.
4. Transition types: concept→concept, concept→deep-dive, concept→build, concept→experiment, and stage→stage.
5. Bilingual parity protocol: compare counterpart existence first, then semantic equivalence; report the two separately.
6. Evidence ledger: every claim must trace to a path, metadata field, rendered element or observed link. Mark unverified rendered behavior unknown.
7. Regression calibration: test new skill versions against at least one sequential group, one route stage, one heterogeneous family, and one group with optional/Build branches.
8. Change control: audits are diagnostic unless implementation is requested; do not silently alter page content or canonical registries.

## 9. Limitations and confidence

- **High confidence:** group roles and route boundaries stated directly in canonical curriculum, guided-route YAML and page-map metadata.
- **Medium confidence:** transition usability inferred from source text and explicit links without a rendered browser walkthrough.
- **Not assessed:** learner comprehension, responsive rendering, keyboard/screen-reader experience, and full semantic parity of all EN/FR page bodies.
- Quarto rendering, metadata validation, link checks and CI were not run for this audit. No candidate action is claimed as implemented.
