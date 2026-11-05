# Q/K/V — four-source comparison and canonical-page audit

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

## 9. Related records

- [Q/K/V source collection](../source-reviews/qkv-source-collection.md)
- [Pedagogical coverage matrix](qkv-pedagogical-coverage-matrix-2026-11.md)
- [Complementary perspectives synthesis](qkv-complementary-perspectives-2026-11.md)
- [Brenndoerfer source review](../source-reviews/qkv-mbrenndoerfer-2026-11.md)
- [Brenndoerfer visual inventory](../source-reviews/qkv-brenndoerfer-visual-inventory-2026-11.md)
- [Q/K/V self-audit](../source-reviews/llm-lab-qkv-self-audit-2026-11.md)
- [Learning-impact baseline](qkv-learning-impact-baseline-2026-11.md)
- [Learner pilot protocol #447](https://github.com/JM-Brun/llm-lab/issues/447)
- [Visual/accessibility review #483](https://github.com/JM-Brun/llm-lab/issues/483)
