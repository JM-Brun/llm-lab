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
| Routing versus payload | Makes the functional distinction unusually explicit | Dedicated optional note exists on Q/K/V EN/FR | Integrated |
| Message-passing interpretation | Not comparably explicit in the earlier three records | Attention page describes values as messages and Q/K weights as content-dependent routing | Integrated as an analogy, not a fixed-graph claim |
| Convex-hull property | Distinct mathematical consequence, not developed by earlier three tutorials | Attention page states the nonnegative/normalized-weight conditions and bounds the claim to the pre-projection weighted sum | Integrated with scope limitations |
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

The fact is useful as a precise geometric interpretation of aggregation, but does not require a new page or canonical concept node.

### 3.3 Routing versus payload

Q/K scores determine the weights assigned to accessible positions. V supplies the vectors to which those weights are applied. Holding Q and K fixed while changing V leaves attention weights unchanged, although the weighted output may change.

This distinction is the most useful bridge between the role explanation and the attention computation. Any linguistic illustration (e.g. grammatical information influencing routing while another feature is transmitted) must remain explicitly hypothetical: the source does not provide trained-head measurements establishing such specialization.

## 4. Audit of the canonical pages

### Q/K/V pages (EN and FR)

The current bilingual pages cover:
- learned Q/K/V projections of the representation entering the attention sublayer;
- the functional roles and shared-input projection equations;
- current hidden representations versus first-layer token embeddings;
- positional-information variants, including RoPE-style injection;
- self-attention versus cross-attention;
- matching/routing (Q/K) versus payload/content (V);
- coreference versus lexical polysemy as distinct contextual phenomena;
- the limitation that linguistic examples are not evidence that a particular head solves a task;
- dot product versus cosine similarity, hard retrieval and attention-weight interpretation caveats.

**Assessment:** Brenndoerfer's routing/payload distinction clarifies the explanation but does not create a new mechanism or justify a new page. It belongs as an optional note in the existing Q/K/V page.

### Scaled-attention pages (EN and FR)

The current bilingual pages cover:
- \(S=QK^\top\), scaling, optional additive masking, row-wise softmax and \(O=AV\);
- tensor shapes and a worked one-query/two-key numerical example;
- scores, weights and outputs as distinct objects;
- message passing as a content-dependent analogy;
- the convex-hull property under nonnegative normalized weights, bounded to the pre-projection weighted sum;
- why attention weights are not causal explanations;
- fully masked-row behavior and the contract of the current single-head, unbatched NumPy implementation.

**Assessment:** the message-passing and convex-hull additions are complementary notes, not a reason to expand the core pipeline.

### Bilingual parity

The EN and FR source files contain corresponding routing/payload and message-passing/convex-hull notes. This establishes source-content parity, not rendered visual parity. Browser rendering, mobile behavior, keyboard navigation, disclosure interaction and screen-reader behavior remain subject to the separate visual/accessibility review.

## 5. Source-to-project coverage and genuine remaining gaps

| Learner question | Canonical owner | Brenndoerfer's incremental value | Decision / remaining action |
|---|---|---|---|
| What are Q, K and V? | Q/K/V page | Alternative analogy and projection exposition | No new content |
| Why separate matching from payload? | Q/K/V page | Explicit routing/payload formulation | Integrated |
| How are scores calculated and normalized? | Scaled-attention page | Detailed intermediate trace | Reference only |
| Why divide by sqrt(d_k)? | Attention-score-scaling deep dive | Assumption-led variance argument | Check assumptions in deep dive; no duplication |
| What are the tensor shapes? | Q/K/V, tensors, attention implementation | Alternative shape walkthrough | Already covered |
| What does the weighted sum mean geometrically? | Scaled-attention page | Convex-hull interpretation | Integrated; pilot can test comprehension |
| Can attention be viewed as message passing? | Scaled-attention page | Explicit message/payload analogy | Integrated; retain analogy boundary |
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
| Routing versus payload | Integrated in Q/K/V EN/FR |
| Message-passing interpretation | Integrated in attention EN/FR |
| Convex-hull property | Integrated in attention EN/FR, scope qualified |
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
