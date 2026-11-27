# Q/K/V — four-source comparison and canonical-page audit

> **Scope clarification (2026-11-27):** this is a deliberately bounded comparison of four tutorial resources, not the complete bibliography, construction corpus or claim-evidence inventory for the current Q/K/V page. Jose Parreño Garcia is a later page-cited blog with its own source review; Vaswani et al. is the primary research anchor with a separate focused review. Their roles are reconciled in [the Q/K/V source collection, §12](../source-reviews/qkv-source-collection.md#12-page-level-diversity-and-coverage-audit--2026-11-27). Do not infer page usage or claim support from membership in this four-tutorial comparison.

**Review date:** 2026-11-05  
**Sources:** Nishanthan K (DEV), Neha KK (Medium), Codefinity, Michael Brenndoerfer  
**Canonical pages:** [Q/K/V (EN)](../../site/en/queries-keys-values.qmd) · [Q/K/V (FR)](../../site/fr/queries-keys-values.qmd) · [Scaled dot-product attention (EN)](../../site/en/scaled-dot-product-attention.qmd) · [Scaled dot-product attention (FR)](../../site/fr/scaled-dot-product-attention.qmd)

## 1. Executive conclusion

Brenndoerfer does not introduce a new Q/K/V mechanism. Its incremental value is a stronger intermediate-level treatment of the standard mechanism: an assumption-explicit variance derivation for scaling, an end-to-end toy computation, explicit discussion of dimensions and limitations, and useful interpretations of value aggregation.

The four tutorials have distinct pedagogical strengths:

- **Nishanthan:** compact functional/visual walkthrough and misconception checks.
- **Neha KK:** motivation for separating matching and payload into distinct learned projections.
- **Codefinity:** bridge from Q/K roles to vector geometry, lexical polysemy and formative-question design.
- **Brenndoerfer:** mathematical exposition, numerical tracing and geometric interpretation of weighted aggregation.

The project should not reproduce four tutorials. It should retain one coherent canonical explanation and use the sources as complementary inputs to pedagogy. The current pages already integrate several Brenndoerfer contributions. The source catalogue, coverage matrix and older Brenndoerfer review need reconciliation so that their records match the current pages.

## 2. Four-source comparison

| Dimension | Nishanthan (DEV) | Neha KK (Medium) | Codefinity | Brenndoerfer |
|---|---|---|---|---|
| Primary lens | Functional walkthrough / search analogy | Architectural rationale / coreference | Vector geometry / polysemy / quiz | Mathematical derivation / numerical trace / geometry |
| Main learner question | What do Q, K and V do in the attention flow? | Why separate matching from payload? | How can Q/K compatibility be understood geometrically? | Why scale by sqrt(d_k), and what does weighted aggregation produce? |
| Best teaching device | Role-to-pipeline narrative; bank and pronoun examples | “Why three projections?” framing; pronoun with candidate antecedents | Q/K alignment; bank/river contrast; role-confusion distractors | Variance derivation; tensor shapes; hand-designed “The cat sat” trace; visualizations |
| Distinct incremental value | Misconception warnings against hard retrieval and semantic-similarity readings | Explicit architectural rationale for decoupling matching and payload | Optional geometric bridge and assessment-design patterns | Visible assumptions, intermediate numerical trace, routing/payload and convex-combination interpretations |
| Main limitation | Search analogy may imply discrete retrieval; original figure not inspected | Compact computation is less complete than project treatment; linguistic example is illustrative | Geometry can be mistaken for cosine-only similarity; full course not scanned | Some claims need qualification; random projections are not learned behavior; media/quiz/code execution not fully inspected |
| Best disposition | Integrate by reference; retain misconception prompts | Integrate rationale in existing Q/K/V explanation | Integrate bounded geometry/contrast; retain quiz patterns as design references | Integrate bounded explanatory notes; retain scaling derivation and worked example by reference; no duplicate workbench |

Agreement on the standard score → scale → softmax → weighted-sum pipeline is pedagogical convergence, not independent experimental validation. Primary formulations and independently checkable mathematics remain the technical anchors.

## 3. Brenndoerfer: incremental contribution

| Contribution | Versus earlier tutorials | Versus current LLM Lab | Decision |
|---|---|---|---|
| Database/library lookup analogy | Similar to DEV and Medium search/database framing | Existing index-card analogy already teaches functional roles | Already covered; no second analogy |
| Explicit variance derivation | More developed than earlier brief scaling explanations | Dedicated attention-score-scaling lesson owns derivation and simulation | Integrate by reference; do not duplicate |
| Tensor shapes, including d_k and d_v | More explicit exposition than short tutorials | Q/K/V, attention lessons and NumPy implementation cover shapes and unequal widths | Already covered; alternative reference |
| “The cat sat” trace | More complete than compact examples in earlier sources | Project already has a hand-worked attention calculation and NumPy projection/shape exercise | Integrate by reference; no second workbench |
| Routing versus payload | Makes the functional distinction unusually explicit | The core Q/K/V pages state the distinction in their main prose; the advanced page develops its mathematical interpretation | Present in the core lesson; no separate source-attributed collapsible note or empirical claim about specialized heads |
| Message-passing interpretation | Not comparably explicit in the earlier three records | The current scaled-attention pages contain weighted aggregation but no message-passing framing | Absent in FR and EN; defer unless a learner need justifies this additional analogy |
| Convex-hull property | Distinct mathematical consequence, not developed by earlier three tutorials | The current scaled-attention pages do not state the convex-hull consequence | Absent in FR and EN; defer pending a demonstrated learner need; do not treat the extraction's earlier disposition as proof of integration |
| Random-init attention visual | No equivalent qualified visualization in earlier scanned material | Project cautions against reading examples as empirical evidence; visual inventory records the heatmap's limits | Retain as source-quality and learner-misconception case |
| Symmetry, linguistic-head and linearity claims | Richer technical stress-test material | Source review records necessary qualifications | Retain as technical regression cases |

### 3.1 Variance derivation

Under the simplifying assumptions of zero-mean, unit-variance query/key components, independence between query and key components, and independence of the products across dimensions,
\[
q^\top k = \sum_{m=1}^{d_k}q_m k_m
\]
has variance \(d_k\), hence standard deviation \(\sqrt{d_k}\). Dividing by \(\sqrt{d_k}\) controls score scale under this model.

This is not a universal empirical law for trained activations. Scaling does not guarantee diffuse softmax rows or healthy gradients under every distribution, mask, learned parameterization or temperature. Keep the full derivation in the dedicated scaling deep dive; do not duplicate it on the Q/K/V page.

### 3.2 Convex-hull property

For one query row with at least one accessible key, let \(\alpha_j\geq0\) and \(\sum_{j\in A}\alpha_j=1\), where \(A\) is the set of accessible positions. Then
\[
o=\sum_{j\in A}\alpha_jv_j
\]
is a convex combination of the accessible value vectors, so it belongs to their convex hull.

This applies to the weighted sum **before** output projection, residual addition, normalization or MLP transformation. It does not apply to a fully masked row, whose weights are not a probability distribution, and does not imply that the final Transformer-block representation remains in the same convex hull.

The fact is mathematically valid and useful as a possible geometric interpretation of aggregation, but it is not currently present in the bilingual scaled-attention pages (checked 2026-11-27). Keep it as a source-level candidate; do not claim integration or add it to the core lesson without learner evidence. It does not require a new page or canonical concept node.

### 3.3 Routing versus payload

Q/K scores determine the weights assigned to accessible positions. V supplies the vectors to which those weights are applied. Holding Q and K fixed while changing V leaves attention weights unchanged, although the weighted output may change.

This distinction is the most useful bridge between the role explanation and the attention computation. Any linguistic illustration (e.g. grammatical information influencing routing while another feature is transmitted) must remain explicitly hypothetical: the source does not provide trained-head measurements establishing such specialization.

## 4. Audit of the canonical pages

### Q/K/V core lesson and advanced deep dive (EN and FR)

The current bilingual core Understand pages cover:
- learned Q/K/V projections of the representation entering the attention sublayer;
- the functional roles and shared-input projection equations;
- current hidden representations versus first-layer token embeddings;
- positional-information variants, including RoPE-style injection;
- self-attention versus cross-attention;
- matching/routing (Q/K) versus payload/content (V), stated in the main explanatory prose;
- a pronoun-coreference example, explicitly labelled as illustrative rather than evidence of a trained head's behavior.

The advanced Q/K/V deep dives additionally cover:
- dot-product geometry and the distinction from cosine similarity;
- the bank/river lexical-ambiguity example;
- interpretation limits for contextual representations and attention weights.

The geometric lens and lexical-ambiguity example are therefore present in the advanced destination, not as optional collapsible notes on the core Q/K/V pages. The Codefinity contribution is integrated at the deeper level; it should not be described as content on the core lesson.

### Scaled-attention pages (EN and FR)

The current bilingual pages cover:
- \(S=QK^\top\), scaling, optional additive masking, row-wise softmax and \(O=AV\);
- tensor shapes and a worked one-query/two-key numerical example;
- scores, weights and outputs as distinct objects;
- why attention weights are not causal explanations;
- the distinction between attention weights over positions and the later vocabulary softmax.

The current source files do not contain the message-passing analogy or the convex-hull consequence. The weighted-sum formula alone does not establish that either interpretation has been taught explicitly.

**Assessment:** message passing and convex-hull geometry remain candidate explanatory additions, not current page content. The present core pipeline is coherent without them; defer both until a learner task demonstrates a concrete need.

### Bilingual parity

The FR and EN pages have matching core computation and interpretive safeguards. Neither currently contains the message-passing or convex-hull note, so there is no language-parity defect for those deferred contributions. This source-file check does not establish rendered visual parity; browser rendering, mobile behavior, keyboard navigation and screen-reader behavior remain separate validation gates.

## 5. Source-to-project coverage and genuine remaining gaps

| Learner question | Canonical owner | Brenndoerfer's incremental value | Decision / remaining action |
|---|---|---|---|
| What are Q, K and V? | Q/K/V page | Alternative analogy and projection exposition | No new content |
| Why separate matching from payload? | Q/K/V core lesson | Explicit routing/payload formulation | Present in the main prose; do not describe it as a separate source-attributed note |
| How are scores calculated and normalized? | Scaled-attention page | Detailed intermediate trace | Explicitly taught; source reference only |
| Why divide by sqrt(d_k)? | Attention-score-scaling deep dive | Assumption-led variance argument | Present as a derivation in the deep dive; source-specific attribution is not explicit |
| What are the tensor shapes? | Q/K/V, tensors, attention implementation | Alternative shape walkthrough | Already covered |
| What does the weighted sum mean geometrically? | Scaled-attention page | Convex-hull interpretation | Weighted sum is explicit; convex-hull consequence is absent and deferred |
| Can attention be viewed as message passing? | Scaled-attention page | Explicit message/payload analogy | Absent; defer pending learner need |
| Do random heatmaps show learned specialization? | Interpretation safeguards | Concrete cautionary example | Keep as pilot/review prompt; no semantic inference |
| Does a head perform coreference or syntax? | Q/K/V and contextualized-representations pages | Example exposes risk of overinterpretation | No empirical claim without model/head evidence |
| How does this extend to multi-head, cross-attention, GQA/MQA? | Architecture and Build pages | Source is narrower than project route | Keep existing page ownership |

The most important remaining gap is **learner evidence**, not another explanation. Test whether readers distinguish: (1) routing from payload, (2) weighted mixture from argmax retrieval, (3) convex-hull scope from claims about the whole block, and (4) random-init visualization from learned behavior. Reuse the existing pilot protocol; do not create a parallel quiz.

## 6. Technical qualifications to preserve

1. Variance: zero mean and unit variance alone are insufficient; independence assumptions are needed for the stated sum variance.
2. Softmax saturation: scaling addresses score magnitude under a model; it is not a universal guarantee against saturation or vanishing gradients.
3. Random projections: the toy example demonstrates tensor flow, not learned linguistic behavior.
4. Attention interpretation: weights alone are not causal explanations or universal semantic relevance scores.
5. Symmetry: permutation symmetry requires explicit conditions on positional information, masks and projection structure.
6. Linearity: Q/K/V projections are linear maps, but complete attention is nonlinear because of softmax; the Transformer block has further transformations.
7. Convex hull: restrict the property to the normalized weighted sum over accessible values, before later transformations.
8. Linguistic examples: proposed syntactic/semantic routing is hypothetical unless actual model/head measurements are supplied.

## 7. Workflow and record reconciliation

The repository uses four complementary record types: extraction (source claims and source-local graph), review (technical/pedagogical judgement and inspection limits), cross-source matrix (learner-question coverage), and canonical pages (selected learner-facing synthesis).

Required reconciliation:
- Earlier collection/matrix sections still use three-source wording. Extend the current comparison scope to four without rewriting historical source-specific reviews.
- The original Brenndoerfer review deferred convex hull. The current EN/FR attention pages now contain the bounded property; the disposition is therefore superseded by **integrate**.
- Extraction nodes for routing/payload, message passing and convex hull are source-local. They do not automatically require canonical graph nodes; the project integrates them as explanatory notes.
- Variance derivation remains **integrate by reference**; do not duplicate it.
- No new Q/K/V page, route edge, numerical workbench or generic quiz is warranted.
- Visual inventory is textual, not visual inspection. Original media bytes and reuse rights remain unresolved.

### Reusable decision rule

A new source should trigger a canonical change only when it adds a learner question, a materially different explanatory lens that improves transfer, an important qualification/counterexample, a useful experiment/assessment/implementation behavior, or evidence that the current explanation fails for learners. Topical overlap alone is insufficient. A source can be useful as a reference without being copied into the curriculum.

## 8. Final disposition

| Item | Disposition |
|---|---|
| Database analogy | Already covered |
| Variance derivation | Integrate by reference |
| Tensor-shape walkthrough | Already covered / reference |
| “The cat sat” trace | Integrate by reference |
| Routing versus payload | Present in the main prose of Q/K/V EN/FR; not a separate source-attributed callout |
| Message-passing interpretation | Absent in scaled-attention EN/FR; deferred |
| Convex-hull property | Absent in scaled-attention EN/FR; deferred pending learner evidence |
| Random-init heatmap | Retain as caution / pilot prompt |
| Symmetry, nonlinearity and learned-head claims | Technical regression cases |
| New canonical page, graph node or route | Not justified |
| New generic Q/K/V quiz | Not justified before learner evidence |
| Third-party figure reuse | Not approved; inspection and rights unresolved |

## 9. Page-production workflow pilot — 2026-11-26

This Q/K/V lesson pair is the first end-to-end application of the seven-stage page-production workflow. The pilot reuses the existing four-source comparison, complementary-perspectives synthesis, source reviews, extraction records, page pair, advanced deep dive, Practice companion and recent rendering evidence. It does not reopen source ingestion or create a new page/registry.

### 9.1 Page blueprint

| Blueprint dimension | Decision for the Q/K/V lesson |
|---|---|
| Learner problem | A learner can follow the Transformer overview but may still conflate the representations used to calculate attention weights with the representations whose content is aggregated. |
| Learner value | Understanding this separation makes the attention calculation, parameter interventions, cross-attention and implementation trace intelligible. |
| Observable outcomes | Explain the roles of Q, K and V; reconstruct the shared-input projections and their shapes; distinguish self-attention from cross-attention provenance; predict what can and cannot change under an isolated projection intervention. |
| Scope / owner | The core Understand page owns the functional roles, shared-input projection rationale, block-input provenance and basic dimensions for self-attention. The scaled-dot-product-attention page owns the score, scaling, mask, softmax and weighted-sum derivation. |
| Non-goals | Do not duplicate the full score/softmax derivation, advanced gradient geometry, multi-head variants, KV-cache behavior or implementation details owned by the advanced Q/K/V, attention and Transformer-block pages. |
| Prerequisites / route | Transformer overview is the previous Understand page; scaled dot-product attention is next. Contextualized representations and tensor conventions are useful references, not additional mandatory route steps. |
| Mathematical contract | For the shared block input $X\in\mathbb{R}^{T\times d_{model}}$, $Q=XW_Q$, $K=XW_K$, $V=XW_V$; $Q,K\in\mathbb{R}^{T\times d_k}$ and $V\in\mathbb{R}^{T\times d_v}$. Biases and post-projection positional transformations are stated as architecture-dependent qualifications. |
| Worked-example decision | Do not force one end-to-end numerical trace into this lesson. Its role is to explain projection provenance and functional separation. The existing Q/K/V Practice companion already carries projection calculations and parameter-intervention tasks; numerical score/softmax/aggregation work belongs to the next lesson and its Practice resources. Keep linguistic examples explicitly illustrative, not empirical evidence about a trained head. |
| Source synthesis | Retain the four-source comparison (Nishanthan, Neha KK, Codefinity, Brenndoerfer) and its complementary explanatory lenses. The Jose Parreño recommendation-system analogy remains a bounded optional intuition, not a new mechanism. Vaswani et al. remains the primary mechanism reference. |
| Misconceptions / limits | Q/K are not universal semantic-similarity measures; dot product is not cosine similarity; attention is soft weighting, not hard nearest-neighbour lookup; weights alone are not causal explanations; a linguistic example does not prove that one head performs coreference; self-attention and cross-attention have different input provenance. |
| Companions | Keep the dedicated Q/K/V Practice page for assessment and exercises; the advanced Q/K/V page for gradients and geometry; scaled attention for the numerical mechanism; Transformer-block walkthrough for implementation. No new flashcard set, concept node, route step or exercise page is justified. |
| Validation evidence | Use source-level exercise checks, bilingual source review, the 25 November Chromium/browser review and published-artifact inspection. Keep manual accessibility/deployment and learner-effectiveness gates separate. |

### 9.2 Seven-stage workflow evaluation

| Stage | Evidence in this pilot | Result / remaining work |
|---|---|---|
| 1. Ingest | Four tutorial sources are recorded in the Q/K/V source collection; the Jose Parreño article has its own review. Primary Vaswani reference is linked. | Reuse existing records. The four tutorial scans remain partial where noted; do not imply that uninspected media were reviewed. |
| 2. Model sources | Source records, extraction dossiers and source-local pedagogical models distinguish claims, teaching moves, evidence limits and asset status. | Sufficient for this page decision. Source-local nodes must not be promoted automatically into canonical concepts. |
| 3. Synthesize | Four-source comparison and complementary-perspectives synthesis distinguish convergence, unique teaching value, contradictions and boundaries. | Sufficient. No new technical mechanism or additional canonical source synthesis is required. |
| 4. Blueprint | The table above makes learner contract, scope, ownership, route, mathematical contract, example strategy and companions explicit. | Complete for this bounded revision. The blueprint belongs in this existing synthesis record; no standalone blueprint file is needed. |
| 5. Write | The bilingual pages already contain the functional distinction, projection equations, dimensions, architecture qualifications, analogy boundaries and contextual examples. | Two targeted corrections are applied in this pilot: align the hidden `purpose` with the actual lesson outcomes, and explicitly state that Q/K/V are recomputed inside each block from that block's input states. |
| 6. Derive companions | Dedicated Practice page, advanced Q/K/V deep dive, scaled-attention lesson and Transformer-block Build walkthrough already exist. | Preserve the current separation. The gradient exercise now exposes its focused deep-dive prerequisite; no new exercise is warranted. |
| 7. Validate | #1649 records source-level exercise and arithmetic checks; #1619 records EN/FR desktop/mobile Chromium review; #1620 records published-artifact inspection. | These are distinct evidence types. #483 still tracks live deployment/manual keyboard, touch and screen-reader checks; #447 learner pilot remains gated. No learner-effectiveness claim is made. |

### 9.3 Findings and decisions

1. **Metadata contract:** the previous `purpose` described only a W_V intervention, while the page teaches the full role/projection distinction. The FR/EN purpose fields now describe the actual lesson outcome and retain parameter-intervention prediction as a transfer capability.
2. **Computational placement:** the page already identified the block input and later contextualized states, but the repeated per-block computation was implicit. The new sentence makes explicit that Q/K/V are recomputed inside each attention sublayer from the current block input; they do not follow the final contextualized representations.
3. **Page ownership:** keep the current division: Q/K/V projections and roles here; score → scale → mask → softmax → value aggregation in scaled dot-product attention; gradient paths and advanced variants in the deep dive; code trace in Build.
4. **Evidence boundary:** recent browser and artifact reviews support rendering, localization, responsive layout and link structure for the inspected source tree. They do not establish manual assistive-technology coverage or learner mastery.
5. **No graph or route change:** no stable new concept, typed semantic relation, computational node or guided-route step is justified by this pilot.

### 9.4 Remaining work

- Complete #483's live-host verification where possible, full keyboard traversal, touch-device review and manual screen-reader check of the diagrams.
- Run the #447 learner pilot only after its accessibility/deployment gate is satisfied; measure the declared transfer outcomes rather than asking only for role recall.
- Revisit the page only if learner evidence identifies a specific misconception not already covered by the current Practice tasks.
- Keep the four-source scan limitations and third-party asset rights status visible; do not infer visual inspection or permission from a textual inventory.

This pilot demonstrates the workflow's hand-offs and non-duplication decisions. It does not validate the workflow's effectiveness across all page archetypes; a second pilot should use a materially different page type, preferably a mathematical or implementation-heavy lesson.

## 10. Related records

- [Q/K/V source collection](../source-reviews/qkv-source-collection.md)
- [Pedagogical coverage matrix](qkv-pedagogical-coverage-matrix-2026-11.md)
- [Complementary perspectives synthesis](qkv-complementary-perspectives-2026-11.md)
- [Brenndoerfer source review](../source-reviews/qkv-mbrenndoerfer-2026-11.md)
- [Brenndoerfer visual inventory](../source-reviews/qkv-brenndoerfer-visual-inventory-2026-11.md)
- [Q/K/V self-audit](../source-reviews/llm-lab-qkv-self-audit-2026-11.md)
- [Learning-impact baseline](qkv-learning-impact-baseline-2026-11.md)
- [Learner pilot protocol #447](https://github.com/JM-Brun/llm-lab/issues/447)
- [Visual/accessibility review #483](https://github.com/JM-Brun/llm-lab/issues/483)


## 11. Issue #1739 pilot — Q/K/V intellectual-contribution inventory

**Pilot unit:** the canonical bilingual Q/K/V lesson pair (French and English), treated as one lesson with two language realizations. This is an audit of the existing synthesis, not a request to rewrite a page that is already substantially developed.

### 11.1 Evidence set and inspection boundary

The pilot reuses the four tutorial sources in the [Q/K/V source collection](../source-reviews/qkv-source-collection.md), adds the separately reviewed Jose Parreño article already cited by the lesson, and uses Vaswani et al. as the primary technical cross-check.

| Source | Relevant contribution records | Inspection boundary |
|---|---|---|
| Nishanthan K, DEV | attention-score-not-semantic-similarity; weighted-aggregation-not-argmax; context-examples; projection-learning | Author text and a two-comment thread inspected. Image bytes, linked resources and reuse rights unresolved; the Medium mirror contains an unresolved image placeholder. |
| Neha KK, Medium | role-decoupling; pronoun-context-example; attention-map-interpretability | Visible author text reconciled against the live page-text view. Figure bytes, linked resources and rights unresolved. |
| Codefinity | geometric-alignment-framing; bank-polysemy-example; quiz-purpose and related checks | Lesson and parent outline inspected. Full interactive course, assignments and linked resources not inspected; SVG bytes and rights unresolved. |
| Michael Brenndoerfer | routing-versus-payload; message-passing; convex-hull; scaling-variance | Chapter text inspected and nine visual teaching moves inventoried. Original assets/rights unresolved; code was not executed and quiz interactions were not tested. |
| Jose Parreño Garcia, *Understanding Transformers (Part 4)* | qkv-role-analogy; learned-qkv-projections; contextual-relationships | Complete visible author-authored article body inspected. Embedded figures were not retrieved; comments, code and numerical examples were not audited. The article remains partially scanned. |
| Vaswani et al. (2017), *Attention Is All You Need* | Primary formulation cross-check | Reuse the existing [Vaswani attention-formulation review](../source-reviews/vaswani-attention-formulation-2026-11.md); do not create a duplicate source record or extraction. |

The five tutorial/article sources are not independent experimental confirmations of the mechanism. Their role is to expose explanatory choices, examples, caveats and teaching moves. Technical claims are checked against the primary formulation and the project's existing mathematical/implementation treatments. Uninspected media are not treated as absent or assessed.

### 11.2 Aggregated contribution inventory

The IDs below are **stable identifiers local to this synthesis dossier**. They aggregate one or more source-level extraction items into a learner-facing contribution. They are not concept IDs, computational nodes, page tags or a new global registry.

| Local ID | Contribution and learner question | Source evidence | Current canonical treatment | Decision |
|---|---|---|---|---|
| qkv-ic-01-routing-payload | **Separate matching from payload.** Why are Q/K used to determine the weighting while V supplies the content being aggregated? | Neha role-decoupling; Brenndoerfer routing-versus-payload; Jose qkv-role-analogy | Main lesson, “Three complementary roles” and “Why three projections from the same input?” The distinction is stated as a functional separation, not as literal retrieval. | **Keep in the core lesson.** This is a central design rationale, not a new concept or a second analogy. |
| qkv-ic-02-jointly-learned-projections | **Distinct but jointly learned projections.** Why can one shared input produce three different learned views without treating Q, K and V as independently trained modules? | Nishanthan projection-learning; Jose learned-qkv-projections; Neha role-decoupling; Vaswani primary formulation | Main lesson equations and explanation: distinct W_Q, W_K, W_V, learned jointly from the same block input. | **Keep in the core lesson.** Preserve the distinction between separate parameter matrices and joint optimization; do not claim that this parameterization is uniquely optimal. |
| qkv-ic-03-per-block-provenance | **Where are Q/K/V computed?** They are recomputed inside each attention sublayer from that block's current input states; they do not follow the final contextualized representations. | Project synthesis grounded in the adopted [canonical computational spine](../canonical-computational-spine.md) and issue [#575](https://github.com/JM-Brun/llm-lab/issues/575), rather than attributed to a tutorial | Main lesson, “Why three projections from the same input?”; the text distinguishes first-block input, later contextualized states, positional mechanisms and cross-attention provenance. | **Keep in the core lesson.** This is a project-level architectural clarification. Preserve its provenance as an architectural decision, not as a source quotation or a new graph node. |
| qkv-ic-04-context-example-boundary | **Use context without overclaiming interpretation.** A pronoun-reference example makes cross-position information flow concrete, while the explicit caveat prevents the example being read as evidence that one head solves coreference. | Neha pronoun-context-example; Nishanthan context-examples; Jose contextual-relationships | Main lesson, “The problem: using context”, in both languages. The example motivates the mechanism and explicitly does not report measured attention weights or head behaviour. | **Keep one concise example and its caveat.** Do not stack multiple near-identical linguistic examples on this page; fuller lexical ambiguity belongs to contextualized representations. |
| qkv-ic-05-isolated-projection-intervention | **Predict what changes under an intervention.** Changing W_V alone changes the content being aggregated but does not change the Q/K-derived attention weights. | Direct mathematical consequence of the projection and attention equations; reinforced by the existing Q/K/V exercise and attention intervention workbench | Main lesson takeaway plus the dedicated Practice companion; the page purpose explicitly includes predicting isolated-projection effects. | **Keep the consequence visible; rehearse it in Practice.** This is a transfer test, not a claim of novelty in the literature. |
| qkv-ic-06-recommendation-analogy | **A familiar retrieval analogy.** A recommendation/search scenario separates the request, comparison features and returned content. | Jose qkv-role-analogy | Existing optional recommendation-system callout in the main lesson, with an explicit boundary: learned continuous vectors and weighted aggregation are not a discrete catalogue lookup. | **Retain as an optional alternative lens.** Do not promote the analogy to a definition or add more analogies merely to increase source coverage. |
| qkv-ic-07-vector-geometry | **What does Q/K alignment mean geometrically?** Dot product depends on both norms and angle; it is not generally cosine similarity. | Codefinity geometric-alignment-framing; four-source synthesis; mathematical identity qᵀk = ||q|| ||k|| cos(theta) | Advanced Q/K/V page, “Géométrie des compatibilités Q–K”; the core lesson links to the advanced treatment. | **Keep in Deepen.** Do not expand the core page with a second geometric derivation. |
| qkv-ic-08-scaling-variance | **Why divide by sqrt(d_k)?** A probabilistic derivation connects dimension to score variance, with explicit independence and unit-variance assumptions. | Brenndoerfer scaling-variance; Vaswani primary formulation | Dedicated attention-score-scaling deep dive and its simulation. | **Integrate by reference.** Keep assumptions and limitations visible; do not duplicate the derivation in Q/K/V. |
| qkv-ic-09-message-passing | **View attention as content-dependent message passing.** Positions contribute value vectors according to query-key-derived weights. | Brenndoerfer message-passing | The earlier synthesis says this was integrated, but the 2026-11-27 recheck did not find it in the current FR/EN scaled-attention source files or the adjacent canonical pages inspected. | **Not currently verified as integrated.** Keep as a candidate for the scaled-attention lesson only if the value and scope are reconfirmed; do not imply a fixed graph or an exact equivalence with graph neural networks. |
| qkv-ic-10-convex-hull | **A geometric consequence of normalized aggregation.** A row-wise nonnegative weighted sum lies in the convex hull of the accessible value vectors. | Brenndoerfer convex-hull; direct consequence of normalized nonnegative weights | The earlier synthesis says this was integrated, but the 2026-11-27 recheck did not find it in the current FR/EN scaled-attention source files or the adjacent canonical pages inspected. | **Not currently verified as integrated.** Reassess as an optional mathematical note; scope it to the weighted sum before output projection, residual addition or later transformations. Never generalize it to the whole Transformer block. |
| qkv-ic-11-attention-interpretation-limits | **Weights are not causal explanations or universal semantic relevance scores.** | Nishanthan attention-score-not-semantic-similarity; Neha attention-map-interpretability; Jose technical review | Explicit misconception treatment in the scaled-attention lesson and advanced Q/K/V material. | **Preserve the caveat at the point of likely misinterpretation.** No duplicate warning block is needed on every adjacent page. |
| qkv-ic-12-soft-versus-hard-retrieval | **Attention is a weighted mixture, not an argmax lookup.** | Nishanthan weighted-aggregation-not-argmax; Neha retrieval framing; Jose weighted aggregation | Q/K/V role explanation and the scaled-attention derivation O = AV. | **Already covered.** Use the existing numerical example and Practice material; do not add a second workbench. |
| qkv-ic-13-assessment-patterns | **Check mechanism purpose, dynamic weighting versus fixed pooling, and contextual aggregation.** | Codefinity quiz-purpose and related question items | Existing self-check and dedicated Q/K/V Practice companion. | **Retain as assessment-design references.** Do not add a generic quiz without learner evidence of a specific gap. |

### 11.3 Page-level judgement

The core Q/K/V lesson already has more than the target two or three substantive contributions:

1. a functional design rationale (matching versus payload);
2. the architectural placement and provenance of the projections within each block;
3. a contextual example whose evidential limits are explicit;
4. a counterfactual that lets the learner predict the effect of changing one projection;
5. an optional alternative analogy with its limitations stated.

The geometric, probabilistic and convex-geometry contributions are valuable, but their correct destinations are Deepen or the scaled-attention lesson. They should not be pulled into the core lesson to increase its apparent richness.

The French and English page-map contracts have equivalent scope, purpose, route and revision-support semantics. The inspected lesson bodies also preserve the same explanatory structure and caveats ([FR lesson](../../site/fr/queries-keys-values.qmd), [EN lesson](../../site/en/queries-keys-values.qmd)). No new concept, computational edge, prerequisite, guided-route step, page, or generic exercise is justified by this corpus.

**Pilot result:** no content rewrite is required for the Q/K/V pair at this stage. The value of the pilot is to make its existing contributions explicit, connect them to their source evidence, and distinguish core contributions from material already routed elsewhere. The existing revision-support field remains a compact statement of revision coverage; it should not be overloaded into a contribution catalogue.

### 11.4 Meta-model fit and preservation decision

The existing model already represents most of the required information:

- Source extraction files store source-scoped atomic items, locators, evidence, confidence, assumptions and limitations.
- The pedagogical profile stores the learner question, explanatory lens, teaching form, abstraction level, distinctive value and limitations.
- The pedagogical assessment stores reasoned judgements for novelty, complementarity, pedagogical value, applicability, redundancy and evidence quality.
- Candidate destinations, disposition and disposition rationale record the proposed project destination and the item-level editorial decision.
- The existing topic synthesis dossier compares source items and the canonical lesson, and can hold an aggregate contribution ID and exact page-section destination.
- The concept registry remains the owner of scientific concepts; page-map metadata remains the owner of page scope, purpose, navigation and editorial classification.

**Do not add a new page-metadata field or a new contribution registry in this pilot.** The page schema is not intended to contain a second prose inventory, and source extraction records must remain source-specific. The dossier-local aggregate IDs above are a controlled cross-source synthesis aid, not canonical concept IDs.

A real limitation remains: the extraction contract validates candidate page IDs but does not provide a validated page-anchor relation for every contribution. This pilot records the exact section destinations in the synthesis dossier. Reconsider a minimal, typed anchor reference only if the same traceability gap recurs across a second materially different page type and cannot be maintained reliably in the existing synthesis record. Any such change must update the source schema, validator, fixtures, tests and documentation together.

**Preservation rule calibrated by this pilot:** do not delete an extracted pedagogical item because it is redundant in the current lesson. Keep its source record and disposition. If an integrated contribution is moved or rewritten, update its aggregate dossier entry and destination; preserve the source item, evidence boundary and bilingual counterpart. A change to the concept graph or curriculum is not implied by a change to an explanatory lens.

### 11.5 Reusable workflow for issue #1739

Apply this sequence per canonical lesson (French and English as one audit unit), reusing the source-integration workflow and existing validators:

1. **Resolve the lesson contract.** Read the page-map scope and purpose, locate the lesson in the canonical route, identify its concept/page owners and its adjacent pages. Record the actual learner question before looking for novel material.
2. **Close the existing corpus first.** Search the source catalogue, source collections, reviews and extraction files using the page topic and canonical concept IDs. Record source IDs, versions, scan status and component-level inspection limits. Do not treat a citation as a scan.
3. **Extract candidate ideas.** Reuse atomic extraction items and their pedagogical profiles. Add a new extraction only for a genuinely unrecorded source contribution with a precise locator. Separate author claims, community comments, project interpretation and primary technical evidence.
4. **Compare by learner function.** Group items by the learner question or cognitive obstacle they address, not by similar wording. Identify convergence, complementarity, contradiction, qualification, redundancy and missing coverage. Source frequency is not evidence strength.
5. **Inspect the canonical page pair.** Locate the exact existing paragraph, figure, equation, callout, exercise or omission in French and English. Distinguish absent, implicit, explicit, and already treated elsewhere. Verify adjacent canonical owners before proposing a new section.
6. **Make a placement decision.** Use the existing dispositions and select: core lesson, short note/callout, Deepen, Foundations, Build, Practice, integrate by reference, already covered, defer or reject. Record pedagogical value, epistemic status, provenance, page destination and overload risk.
7. **Aggregate and preserve.** Add or update the topic's existing synthesis dossier. Use a dossier-local aggregate ID only when multiple source items or project-level reasoning form one reusable learner contribution. Do not add a concept node for an explanatory lens.
8. **Validate proportionately.** Check source-catalogue validation when extraction data changes; check page metadata and concept/curriculum validators only when their owned data changes; render and inspect both languages when page content changes. Report source inspection, technical review, automated tests, browser review, accessibility review and learner evidence as separate evidence classes.

### 11.6 Issue-wide deliverables and task breakdown

| Work package | Concrete tasks | Durable deliverable / completion evidence |
|---|---|---|
| A. Meta-model audit | Inspect page metadata, source catalogue, extraction taxonomy, concept registry, page graph, curriculum and source workflows; map ownership and current fields. | A concise model-fit decision: reusable fields, missing relations, non-goals and any justified minimal extension. |
| B. Page/corpus inventory | Enumerate canonical lessons from the existing route; for each lesson resolve the source corpus and extraction coverage before searching externally. | Page-by-page coverage matrix with French/English IDs, learner purpose, source IDs, scan limits and inspection status. |
| C. Candidate contribution catalogue | Extract and group pedagogical ideas, perspectives, intuitions, caveats, counterexamples, questions and implications; preserve source locators and epistemic status. | Per-topic synthesis entries with stable local aggregate IDs, source-item references, page-section references (explicit anchors where available), learner value and placement decisions. |
| D. Targeted external research | Search only for evidenced gaps; prioritize primary sources for technical claims and complementary instructional sources for pedagogy. Record useful non-contributions and rejected overclaims too. | Search log and source-review/extraction records, with no source-count target. |
| E. Editorial integration | Integrate only high-value contributions; preserve lesson scope and adjacent page ownership; maintain French/English equivalence and existing practice/deep-dive separation. | Small page diffs with before/after mapping, no-loss checks and updated synthesis decisions. |
| F. Validation and maintenance | Run the owning validators, bilingual render checks, targeted browser/accessibility review and learner checks when gated. Add the audit step to normal page creation/refactor review. | Evidence report with distinct validation classes and a repeatable checklist in the existing contributor workflow. |

**Recommended rollout:** complete A using the existing architecture; use this Q/K/V pilot as the first calibrated case; run a second pilot on a materially different lesson (preferably a probabilistic/mathematical lesson such as logits, likelihood or cross-entropy); only then freeze any additional metadata contract. After that, audit the full canonical Understand route in coherent batches, not by introducing a new automation workflow per concept.

**Explicit non-goals:** no quota of three ideas, no new graph family, no generic contribution taxonomy before a query/use case, no automatic source-to-page promotion, no duplication of existing Deepen/Build/Practice content, and no claim of learner effectiveness without learner evidence.


### 11.7 Superseding source-page reconciliation — 2026-11-27

A fresh source-file check was performed because the earlier synthesis record described message passing and the convex-hull property as integrated. The following current French and English canonical lesson sources were inspected: scaled dot-product attention, advanced Q/K/V, attention-score scaling, contextualized-representations advanced, and the Transformer-block walkthrough.

**Observed result:** the scaled-attention pages currently explain the weighted sum \(O=AV\), distinguish scores/weights/outputs, and warn against reading attention weights as semantic or causal explanations. The two specific explanations below were not found in the inspected current page sources:

- **Message passing:** no explicit content-dependent message-passing interpretation was found.
- **Convex hull:** no statement of the convex-combination property or its bounded pre-projection scope was found.

This means the earlier statements in sections 8 and 9.3 that both additions were integrated are **not supported by the current canonical page sources inspected on 2026-11-27**. This subsection supersedes those statements for the current-state audit. It does not establish whether the material was intentionally removed, never merged, or recorded as integrated prematurely; that history remains to be checked.

**Required follow-up before changing the lesson:**

1. Inspect the relevant historical PR/commit or review evidence to determine why the earlier synthesis marked the two contributions as integrated.
2. Decide independently whether each contribution still improves the scaled-attention lesson:
   - message passing is an optional information-flow analogy and must remain explicitly distinct from a fixed graph or a graph neural network;
   - the convex-hull property is a concise mathematical consequence of nonnegative weights summing to one, but applies only to the weighted sum over the accessible value vectors before output projection and later block transformations.
3. Either restore a minimal bilingual treatment with exact source/page references and rendered validation, or correct the earlier synthesis disposition to deferred/not integrated. Do not leave the discrepancy unresolved or preserve an inaccurate “integrated” status.

This finding is a concrete preservation/traceability failure mode for issue #1739: a contribution's extraction and a prior integration decision do not prove that the corresponding content is still present in the current published lesson. The audit must verify the actual destination in both languages.


## 11. Current source-to-page destination verification — 2026-11-27

This matrix checks the current Quarto source files after the source-to-page traceability contract was added. It distinguishes the core Understand page from the advanced Q/K/V destination. “Explicit” describes the teaching content currently present; it does not by itself mean that the source is the technical evidence for the claim.

| Contribution and canonical source item | Learner claim / teaching point | FR destination | EN destination | Current presence | Source role and decision |
|---|---|---|---|---|---|
| Neha KK — [extraction](../../data/extractions/neha-kk-understanding-qkv-medium.yml), role-decoupling | Why learn separate matching (Q/K) and payload (V) projections? | [Core Q/K/V](../../site/fr/queries-keys-values.qmd#pourquoi-trois-projections-à-partir-de-la-même-entrée) | [Core Q/K/V](../../site/en/queries-keys-values.qmd#why-three-projections-from-the-same-input) | explicit | Construction resource; the page explains the design rationale. The source is not primary technical evidence. |
| Neha KK — same extraction, pronoun-context-example | Why can a position need information from another position? | [Core Q/K/V](../../site/fr/queries-keys-values.qmd#probleme-utiliser-contexte) | [Core Q/K/V](../../site/en/queries-keys-values.qmd#problem-using-context) | explicit | Construction resource and local example attribution; illustration, not evidence of a trained head's behavior. |
| Nishanthan K — [extraction](../../data/extractions/nishanthan-k-qkv-transformers-devto.yml), role-separation | Distinguish Q, K and V by their roles in the flow | [Core Q/K/V](../../site/fr/queries-keys-values.qmd#trois-roles-complementaires) | [Core Q/K/V](../../site/en/queries-keys-values.qmd#three-complementary-roles) | explicit | Construction resource; the source is also linked as supplementary reading, not primary evidence. |
| Codefinity — [extraction](../../data/extractions/codefinity-qkv-building-blocks.yml), geometric-alignment-framing | What does Q–K compatibility mean geometrically? | [Advanced Q/K/V](../../site/fr/queries-keys-values-advanced.qmd#geometrie-compatibilites-qk) | [Advanced Q/K/V](../../site/en/queries-keys-values-advanced.qmd#qk-compatibility-geometry) | explicit | Construction resource; deeper destination only. Dot product is not generally cosine similarity. |
| Codefinity — same extraction, bank-polysemy-example | Distinguish lexical ambiguity from pronoun coreference | [Advanced Q/K/V](../../site/fr/queries-keys-values-advanced.qmd#interpretation-representations-limites) | [Advanced Q/K/V](../../site/en/queries-keys-values-advanced.qmd#interpreting-representations-limits) | explicit | Construction resource; illustrative example, not empirical head-level evidence. |
| Brenndoerfer — [extraction](../../data/extractions/mbrenndoerfer-qkv-attention-mechanism.yml), routing-versus-payload | Separate the representation that controls compatibility from the content aggregated | [Core Q/K/V](../../site/fr/queries-keys-values.qmd#trois-roles-complementaires) | [Core Q/K/V](../../site/en/queries-keys-values.qmd#three-complementary-roles) | explicit | Construction resource; present in main prose, not as the previously claimed source-attributed collapsible note. |
| Brenndoerfer — same extraction, message-passing | Interpret attention as content-dependent message passing | [Scaled attention](../../site/fr/scaled-dot-product-attention.qmd#calcul-en-cinq-étapes) | [Scaled attention](../../site/en/scaled-dot-product-attention.qmd#five-computation-steps) | absent | The destination contains weighted aggregation, not the message-passing analogy. Defer; no page change justified without learner evidence. |
| Brenndoerfer — same extraction, convex-hull | Infer the convex-hull constraint from normalized nonnegative weights | [Scaled attention](../../site/fr/scaled-dot-product-attention.qmd#calcul-en-cinq-étapes) | [Scaled attention](../../site/en/scaled-dot-product-attention.qmd#five-computation-steps) | absent | The mathematical property is valid for a non-empty normalized row before later transformations, but is not stated on the current pages. Defer; do not imply integration. |
| Vaswani et al. — [extraction](../../data/extractions/vaswani-et-al-attention-is-all-you-need-2017.yml), learned-qkv-projections | Learned projections and their relation to the self-attention input | [Core Q/K/V](../../site/fr/queries-keys-values.qmd#pourquoi-trois-projections-à-partir-de-la-même-entrée) | [Core Q/K/V](../../site/en/queries-keys-values.qmd#why-three-projections-from-the-same-input) | explicit | Primary architectural support, with the page's compact single-head notation distinguished from the paper's per-head formulation. |

**Verification boundary:** this is a source-file inspection on 2026-11-27, not a fresh browser/rendered-page or accessibility audit. The FR/EN source destinations were checked separately. No global contribution registry or PAGE-MAP field is introduced.
